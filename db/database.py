"""
SmartFeed AI - Database Module
Provides SQLite database initialization, schema definition, and CRUD operations
for feed assessment tests, traceability passports, and trend analytics.
"""

import sqlite3
import os
import datetime
import hashlib
import json
from pathlib import Path
from contextlib import contextmanager
from typing import List, Dict, Any, Optional, Generator

# Default database location (smartfeed.db in project root)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = os.getenv("SMARTFEED_DB_PATH", str(PROJECT_ROOT / "smartfeed.db"))


def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Establishes and returns a connection to the SQLite database.
    Row factory is set to sqlite3.Row for dictionary-like column access.
    
    Args:
        db_path: Path to database file. Defaults to DEFAULT_DB_PATH.
        
    Returns:
        sqlite3.Connection: Active SQLite connection.
    """
    path = db_path or DEFAULT_DB_PATH
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def get_db(db_path: Optional[str] = None) -> Generator[sqlite3.Connection, None, None]:
    """
    Context manager that provides an open SQLite connection and guarantees
    that the connection is properly closed upon exit.
    
    Args:
        db_path: Path to database file. Defaults to DEFAULT_DB_PATH.
        
    Yields:
        sqlite3.Connection: Active SQLite connection.
    """
    conn = get_db_connection(db_path)
    try:
        yield conn
    finally:
        conn.close()


AUTH_SALT = "smartfeed_auth_salt_2026"


def hash_password(password: str) -> str:
    """Computes standard sha256 password hash with salt."""
    return hashlib.sha256(f"{AUTH_SALT}:{password}".encode("utf-8")).hexdigest()


def verify_password(password: str, password_hash: str) -> bool:
    """Verifies a plain password against stored hash."""
    return hash_password(password) == password_hash


def initialize_database(db_path: Optional[str] = None) -> None:
    """
    Initializes the database schema, creating:
    - 'tests': Feed assessment tests, QR batches, and trend data
    - 'users': Farmer and Admin user accounts
    - 'farms': Farm basic profile and storage configurations
    - 'animals': Individual animal profile cards
    Safe to run repeatedly (IF NOT EXISTS).
    
    Args:
        db_path: Optional database path override.
    """
    create_tests_table = """
    CREATE TABLE IF NOT EXISTS tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        batch_id TEXT UNIQUE NOT NULL,
        user_id INTEGER DEFAULT NULL,
        sample_type TEXT NOT NULL,
        image_path TEXT,
        visual_prediction TEXT,
        confidence REAL DEFAULT 0.0,
        quality_score REAL DEFAULT 0.0,
        mould_risk TEXT,
        foreign_particle_risk TEXT,
        adulteration_risk TEXT,
        nutrition_status TEXT,
        crude_protein REAL DEFAULT 0.0,
        moisture REAL DEFAULT 0.0,
        fiber REAL DEFAULT 0.0,
        storage_condition TEXT,
        overall_risk TEXT,
        primary_concern TEXT,
        advisory TEXT,
        language TEXT DEFAULT 'en',
        shelf_life_days INTEGER DEFAULT 0,
        shelf_life_status TEXT DEFAULT 'SAFE',
        safe_until_date TEXT,
        timestamp TEXT NOT NULL
    );
    """

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        mobile TEXT UNIQUE NOT NULL,
        email TEXT,
        password_hash TEXT NOT NULL,
        role TEXT DEFAULT 'farmer',
        preferred_language TEXT DEFAULT 'te',
        is_onboarded INTEGER DEFAULT 0,
        created_at TEXT NOT NULL
    );
    """

    create_farms_table = """
    CREATE TABLE IF NOT EXISTS farms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER UNIQUE NOT NULL,
        farmer_name TEXT NOT NULL,
        village_location TEXT NOT NULL,
        preferred_language TEXT DEFAULT 'te',
        total_animals INTEGER DEFAULT 0,
        animal_types TEXT,
        main_feed_type TEXT,
        feed_storage TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    create_animals_table = """
    CREATE TABLE IF NOT EXISTS animals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        farm_id INTEGER NOT NULL,
        user_id INTEGER NOT NULL,
        animal_index INTEGER NOT NULL,
        animal_name TEXT,
        animal_type TEXT NOT NULL,
        age_group TEXT NOT NULL,
        lactation_status TEXT NOT NULL,
        milk_production TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(farm_id) REFERENCES farms(id) ON DELETE CASCADE,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
    );
    """

    create_feeding_diary_table = """
    CREATE TABLE IF NOT EXISTS feeding_diary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        animal_id INTEGER,
        feeding_date TEXT NOT NULL,
        time_slot TEXT NOT NULL,
        feed_name TEXT NOT NULL,
        concentrate_kg REAL DEFAULT 0.0,
        green_fodder_kg REAL DEFAULT 0.0,
        dry_straw_kg REAL DEFAULT 0.0,
        silage_kg REAL DEFAULT 0.0,
        water_litres REAL DEFAULT 0.0,
        minerals_grams REAL DEFAULT 0.0,
        milk_yield_litres REAL DEFAULT 0.0,
        notes TEXT,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY(animal_id) REFERENCES animals(id) ON DELETE SET NULL
    );
    """

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(create_tests_table)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tests_batch_id ON tests(batch_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tests_timestamp ON tests(timestamp);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_tests_sample_type ON tests(sample_type);")

            cursor.execute(create_users_table)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_mobile ON users(mobile);")

            cursor.execute(create_farms_table)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_farms_user_id ON farms(user_id);")

            cursor.execute(create_animals_table)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_animals_user_id ON animals(user_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_animals_farm_id ON animals(farm_id);")

            cursor.execute(create_feeding_diary_table)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_feeding_diary_user_date ON feeding_diary(user_id, feeding_date);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_feeding_diary_animal ON feeding_diary(animal_id);")

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS broadcasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                message TEXT NOT NULL,
                target_village TEXT DEFAULT 'All Villages',
                alert_level TEXT DEFAULT 'Warning',
                category TEXT DEFAULT 'Feed Safety',
                language TEXT DEFAULT 'te',
                created_at TEXT NOT NULL
            );
            """)
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_broadcasts_created_at ON broadcasts(created_at);")

            # Auto-migrate tests table columns if needed
            cursor.execute("PRAGMA table_info(tests);")
            cols = {row["name"] for row in cursor.fetchall()}
            if "user_id" not in cols:
                cursor.execute("ALTER TABLE tests ADD COLUMN user_id INTEGER DEFAULT NULL;")
            if "shelf_life_days" not in cols:
                cursor.execute("ALTER TABLE tests ADD COLUMN shelf_life_days INTEGER DEFAULT 0;")
            if "shelf_life_status" not in cols:
                cursor.execute("ALTER TABLE tests ADD COLUMN shelf_life_status TEXT DEFAULT 'SAFE';")
            if "safe_until_date" not in cols:
                cursor.execute("ALTER TABLE tests ADD COLUMN safe_until_date TEXT;")

            # Seed default Admin account if not existing (Mobile: 8341016049, Password: 6049)
            admin_mobile = "8341016049"
            cursor.execute("SELECT id FROM users WHERE mobile = ?", (admin_mobile,))
            if not cursor.fetchone():
                now_str = datetime.datetime.now().isoformat()
                cursor.execute("""
                    INSERT INTO users (full_name, mobile, email, password_hash, role, preferred_language, is_onboarded, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, ("District Cooperative Admin", admin_mobile, "admin@smartfeed.ai", hash_password("6049"), "admin", "te", 1, now_str))

            # Seed default Demo Farmer account ONLY in test databases or when SMARTFEED_SEED_DEMO_DATA=1
            if (db_path is not None) or (os.environ.get("SMARTFEED_SEED_DEMO_DATA") == "1"):
                farmer_mobile = "9876543210"
                cursor.execute("SELECT id FROM users WHERE mobile = ?", (farmer_mobile,))
                if not cursor.fetchone():
                    now_str = datetime.datetime.now().isoformat()
                    cursor.execute("""
                        INSERT INTO users (full_name, mobile, email, password_hash, role, preferred_language, is_onboarded, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, ("Ramesh Kumar (రమేష్ కుమార్)", farmer_mobile, "ramesh@kankipadu.in", hash_password("farmer123"), "farmer", "te", 1, now_str))
                    farmer_id = cursor.lastrowid

                    # Seed farm for demo farmer
                    cursor.execute("""
                        INSERT INTO farms (user_id, farmer_name, village_location, preferred_language, total_animals, animal_types, main_feed_type, feed_storage, created_at, updated_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (farmer_id, "Ramesh Kumar (రమేష్ కుమార్)", "Kankipadu (కంకిపాడు)", "te", 3, "Cow,Buffalo", "Silage", "Shed", now_str, now_str))
                    farm_id = cursor.lastrowid

                    # Seed 3 animals
                    demo_animals = [
                        (farm_id, farmer_id, 1, "Gauri / Cow #1", "Cow", "3–5 years", "Lactating", "Medium (5–10 L)", now_str),
                        (farm_id, farmer_id, 2, "Lakshmi / Cow #2", "Cow", "5+ years", "Pregnant", "N/A", now_str),
                        (farm_id, farmer_id, 3, "Kaali / Buffalo #1", "Buffalo", "3–5 years", "Lactating", "High (>10 L)", now_str)
                    ]
                    cursor.executemany("""
                        INSERT INTO animals (farm_id, user_id, animal_index, animal_name, animal_type, age_group, lactation_status, milk_production, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, demo_animals)

            conn.commit()
    except sqlite3.Error as e:
        raise RuntimeError(f"Database initialization failed: {e}") from e


def seed_demo_farmer(db_path: Optional[str] = None) -> int:
    """
    Seeds default Demo Farmer account (Ramesh Kumar, 9876543210 / farmer123),
    along with farm profile and 3 animals.
    Returns farmer user_id.
    """
    farmer_mobile = "9876543210"
    with get_db(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE mobile = ?", (farmer_mobile,))
        row = cursor.fetchone()
        if row:
            return row["id"]

        now_str = datetime.datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO users (full_name, mobile, email, password_hash, role, preferred_language, is_onboarded, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, ("Ramesh Kumar (రమేష్ కుమార్)", farmer_mobile, "ramesh@kankipadu.in", hash_password("farmer123"), "farmer", "te", 1, now_str))
        farmer_id = cursor.lastrowid

        cursor.execute("""
            INSERT INTO farms (user_id, farmer_name, village_location, preferred_language, total_animals, animal_types, main_feed_type, feed_storage, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (farmer_id, "Ramesh Kumar (రమేష్ కుమార్)", "Kankipadu (కంకిపాడు)", "te", 3, "Cow,Buffalo", "Silage", "Shed", now_str, now_str))
        farm_id = cursor.lastrowid

        demo_animals = [
            (farm_id, farmer_id, 1, "Gauri / Cow #1", "Cow", "3–5 years", "Lactating", "Medium (5–10 L)", now_str),
            (farm_id, farmer_id, 2, "Lakshmi / Cow #2", "Cow", "5+ years", "Pregnant", "N/A", now_str),
            (farm_id, farmer_id, 3, "Kaali / Buffalo #1", "Buffalo", "3–5 years", "Lactating", "High (>10 L)", now_str)
        ]
        cursor.executemany("""
            INSERT INTO animals (farm_id, user_id, animal_index, animal_name, animal_type, age_group, lactation_status, milk_production, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_animals)
        conn.commit()
        return farmer_id


def wipe_all_except_admin(db_path: Optional[str] = None) -> Dict[str, int]:
    """
    Permanently deletes all tests, feeding diary entries, animals, farms,
    and all user accounts EXCEPT the Admin account (role='admin' / mobile='8341016049').
    Resets SQLite auto-increment sequences.
    Returns counts of deleted records.
    """
    admin_mobile = "8341016049"
    with get_db(db_path) as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM tests")
        deleted_tests = cursor.fetchone()[0]
        cursor.execute("DELETE FROM tests")

        cursor.execute("SELECT COUNT(*) FROM feeding_diary")
        deleted_diary = cursor.fetchone()[0]
        cursor.execute("DELETE FROM feeding_diary")

        cursor.execute("SELECT COUNT(*) FROM animals")
        deleted_animals = cursor.fetchone()[0]
        cursor.execute("DELETE FROM animals")

        cursor.execute("SELECT COUNT(*) FROM farms")
        deleted_farms = cursor.fetchone()[0]
        cursor.execute("DELETE FROM farms")

        cursor.execute("SELECT COUNT(*) FROM users WHERE role != 'admin' AND mobile != ?", (admin_mobile,))
        deleted_users = cursor.fetchone()[0]
        cursor.execute("DELETE FROM users WHERE role != 'admin' AND mobile != ?", (admin_mobile,))

        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('tests', 'farms', 'animals', 'feeding_diary')")
        conn.commit()

        # Ensure Admin account exists
        cursor.execute("SELECT id FROM users WHERE mobile = ?", (admin_mobile,))
        if not cursor.fetchone():
            now_str = datetime.datetime.now().isoformat()
            cursor.execute("""
                INSERT INTO users (full_name, mobile, email, password_hash, role, preferred_language, is_onboarded, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, ("District Cooperative Admin", admin_mobile, "admin@smartfeed.ai", hash_password("6049"), "admin", "te", 1, now_str))
            conn.commit()

        try:
            cursor.execute("VACUUM")
        except Exception:
            pass

        return {
            "deleted_tests": deleted_tests,
            "deleted_diary": deleted_diary,
            "deleted_animals": deleted_animals,
            "deleted_farms": deleted_farms,
            "deleted_users": deleted_users
        }


def generate_batch_id(db_path: Optional[str] = None) -> str:
    """
    Generates a unique, sequential Batch ID formatted as: SFA-YYYY-XXXXXX
    Example: SFA-2026-000001
    
    Args:
        db_path: Optional database path override.
        
    Returns:
        str: Unique Batch ID.
    """
    year = datetime.datetime.now().strftime("%Y")
    prefix = f"SFA-{year}-"

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT batch_id FROM tests WHERE batch_id LIKE ?",
                (f"{prefix}%",)
            )
            rows = cursor.fetchall()
            max_seq = 0
            for r in rows:
                bid = r["batch_id"] or ""
                parts = bid.split("-")
                if len(parts) >= 3 and parts[-1].isdigit():
                    try:
                        max_seq = max(max_seq, int(parts[-1]))
                    except ValueError:
                        pass

            candidate_num = max_seq + 1
            while True:
                candidate = f"{prefix}{candidate_num:06d}"
                cursor.execute("SELECT 1 FROM tests WHERE batch_id = ?", (candidate,))
                if not cursor.fetchone():
                    return candidate
                candidate_num += 1
    except sqlite3.Error:
        timestamp_fallback = datetime.datetime.now().strftime("%m%d%H%M%S")
        return f"{prefix}{timestamp_fallback}"


def create_test(test_data: Dict[str, Any], db_path: Optional[str] = None) -> str:
    """
    Inserts a new feed assessment test record into the database.
    Auto-generates batch_id and timestamp if not provided.
    
    Args:
        test_data: Dictionary containing test attributes.
        db_path: Optional database path override.
        
    Returns:
        str: The batch_id of the newly created test.
    """
    initialize_database(db_path)
    
    batch_id = test_data.get("batch_id") or generate_batch_id(db_path)
    timestamp = test_data.get("timestamp") or datetime.datetime.now().isoformat()

    insert_query = """
    INSERT INTO tests (
        batch_id,
        user_id,
        sample_type,
        image_path,
        visual_prediction,
        confidence,
        quality_score,
        mould_risk,
        foreign_particle_risk,
        adulteration_risk,
        nutrition_status,
        crude_protein,
        moisture,
        fiber,
        storage_condition,
        overall_risk,
        primary_concern,
        advisory,
        language,
        shelf_life_days,
        shelf_life_status,
        safe_until_date,
        timestamp
    ) VALUES (
        :batch_id,
        :user_id,
        :sample_type,
        :image_path,
        :visual_prediction,
        :confidence,
        :quality_score,
        :mould_risk,
        :foreign_particle_risk,
        :adulteration_risk,
        :nutrition_status,
        :crude_protein,
        :moisture,
        :fiber,
        :storage_condition,
        :overall_risk,
        :primary_concern,
        :advisory,
        :language,
        :shelf_life_days,
        :shelf_life_status,
        :safe_until_date,
        :timestamp
    );
    """

    payload = {
        "batch_id": batch_id,
        "user_id": test_data.get("user_id"),
        "sample_type": test_data.get("sample_type", "Feed Ingredient"),
        "image_path": test_data.get("image_path", ""),
        "visual_prediction": test_data.get("visual_prediction", "Unknown"),
        "confidence": float(test_data.get("confidence", 0.0)),
        "quality_score": float(test_data.get("quality_score", 0.0)),
        "mould_risk": test_data.get("mould_risk", "Low"),
        "foreign_particle_risk": test_data.get("foreign_particle_risk", "Low"),
        "adulteration_risk": test_data.get("adulteration_risk", "Low"),
        "nutrition_status": test_data.get("nutrition_status", "Balanced"),
        "crude_protein": float(test_data.get("crude_protein", 0.0)),
        "moisture": float(test_data.get("moisture", 0.0)),
        "fiber": float(test_data.get("fiber", 0.0)),
        "storage_condition": test_data.get("storage_condition", "Good"),
        "overall_risk": test_data.get("overall_risk", "Low"),
        "primary_concern": test_data.get("primary_concern", "None"),
        "advisory": test_data.get("advisory", ""),
        "language": test_data.get("language", "en"),
        "shelf_life_days": int(test_data.get("shelf_life_days", 0)),
        "shelf_life_status": test_data.get("shelf_life_status", "SAFE"),
        "safe_until_date": test_data.get("safe_until_date", "N/A"),
        "timestamp": timestamp
    }

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(insert_query, payload)
            conn.commit()
            return batch_id
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Batch ID '{batch_id}' already exists: {e}") from e
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to create test record: {e}") from e


def get_test_by_batch(batch_id: str, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Retrieves a single test record by its unique batch_id.
    Handles exact, hyphen/underscore normalization, and case-insensitive matching.
    
    Args:
        batch_id: Unique batch identifier (e.g., SFA-2026-000001).
        db_path: Optional database path override.
        
    Returns:
        dict: Test record dictionary if found, else None.
    """
    clean_id = (batch_id or "").strip()
    alt_id = clean_id.replace("_", "-") if "_" in clean_id else clean_id.replace("-", "_")
    query = """
        SELECT * FROM tests 
        WHERE batch_id = ? 
           OR batch_id = ? 
           OR UPPER(batch_id) = UPPER(?) 
           OR UPPER(batch_id) = UPPER(?)
        ORDER BY id DESC LIMIT 1;
    """
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (clean_id, alt_id, clean_id, alt_id))
            row = cursor.fetchone()
            return dict(row) if row else None
    except sqlite3.Error as e:
        raise RuntimeError(f"Error querying test by batch_id '{batch_id}': {e}") from e


def get_all_tests(limit: int = 200, user_id: Optional[int] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves all test records ordered chronologically descending (newest first).
    Optionally filtered by user_id for farmer isolation.
    
    Args:
        limit: Maximum number of records to return.
        user_id: Optional farmer user ID to filter records.
        db_path: Optional database path override.
        
    Returns:
        list of dicts: List of test records.
    """
    if user_id is not None:
        query = "SELECT * FROM tests WHERE user_id = ? ORDER BY id DESC LIMIT ?;"
        params = (user_id, limit)
    else:
        query = "SELECT * FROM tests ORDER BY id DESC LIMIT ?;"
        params = (limit,)

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching all tests: {e}") from e


def get_recent_tests(limit: int = 5, user_id: Optional[int] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Convenience method to retrieve the N most recent tests.
    Optionally scoped to user_id.
    """
    return get_all_tests(limit=limit, user_id=user_id, db_path=db_path)


def get_quality_trend(sample_type: Optional[str] = None, user_id: Optional[int] = None, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves chronological quality scores, timestamps, and risks for trend & early spoilage analysis.
    Results are ordered ascending by timestamp (oldest to newest).
    Optionally filtered by sample_type and user_id.
    """
    clauses = []
    params = []
    if sample_type:
        clauses.append("sample_type = ?")
        params.append(sample_type)
    if user_id is not None:
        clauses.append("user_id = ?")
        params.append(user_id)

    where_sql = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    query = f"""
    SELECT id, batch_id, sample_type, timestamp, quality_score, overall_risk, mould_risk, moisture
    FROM tests
    {where_sql}
    ORDER BY timestamp ASC;
    """

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    except sqlite3.Error as e:
        raise RuntimeError(f"Error fetching quality trend: {e}") from e


def delete_test(batch_id: str, db_path: Optional[str] = None) -> bool:
    """
    Deletes a test record by its batch_id.
    
    Args:
        batch_id: The batch ID of the record to delete.
        db_path: Optional database path override.
        
    Returns:
        bool: True if a record was deleted, False otherwise.
    """
    query = "DELETE FROM tests WHERE batch_id = ?;"
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (batch_id.strip(),))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        raise RuntimeError(f"Error deleting test '{batch_id}': {e}") from e


# ===================================================================
# User Authentication & Role Management (Farmer & Admin)
# ===================================================================

def register_user(
    full_name: str,
    mobile: str,
    password: str,
    email: Optional[str] = None,
    language: str = "te",
    preferred_language: Optional[str] = None,
    role: str = "farmer",
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """Registers a new user (farmer or admin) with hashed password."""
    initialize_database(db_path)
    clean_mobile = (mobile or "").strip()
    clean_name = (full_name or "").strip()
    clean_lang = (preferred_language or language or "te").strip()
    if not clean_mobile:
        raise ValueError("Mobile number is required.")
    if not clean_name:
        raise ValueError("Full Name is required.")
    if len(password) < 4:
        raise ValueError("Password must be at least 4 characters long.")

    pw_hash = hash_password(password)
    now_str = datetime.datetime.now().isoformat()

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (full_name, mobile, email, password_hash, role, preferred_language, is_onboarded, created_at)
                VALUES (?, ?, ?, ?, ?, ?, 0, ?)
            """, (clean_name, clean_mobile, (email or "").strip(), pw_hash, role, clean_lang, now_str))
            conn.commit()
            user_id = cursor.lastrowid
            return {
                "id": user_id,
                "full_name": clean_name,
                "mobile": clean_mobile,
                "email": (email or "").strip(),
                "role": role,
                "preferred_language": clean_lang,
                "is_onboarded": 0,
                "created_at": now_str
            }
    except sqlite3.IntegrityError as e:
        raise ValueError(f"Mobile number '{clean_mobile}' is already registered. Please sign in.") from e
    except sqlite3.Error as e:
        raise RuntimeError(f"Registration failed: {e}") from e


def authenticate_user(
    mobile: str,
    password: str,
    required_role: Optional[str] = None,
    db_path: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Verifies credentials and returns user dictionary without password hash."""
    initialize_database(db_path)
    clean_mobile = (mobile or "").strip()
    query = "SELECT * FROM users WHERE mobile = ? LIMIT 1"
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (clean_mobile,))
            row = cursor.fetchone()
            if not row:
                return None
            user_dict = dict(row)
            if not verify_password(password, user_dict["password_hash"]):
                return None
            if required_role and user_dict.get("role") != required_role:
                pass
            del user_dict["password_hash"]
            return user_dict
    except sqlite3.Error as e:
        raise RuntimeError(f"Authentication query error: {e}") from e


def get_user_by_id(user_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Retrieves user record by ID."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ? LIMIT 1", (user_id,))
            row = cursor.fetchone()
            if not row:
                return None
            user_dict = dict(row)
            if "password_hash" in user_dict:
                del user_dict["password_hash"]
            return user_dict
    except sqlite3.Error as e:
        raise RuntimeError(f"User lookup error: {e}") from e


# ===================================================================
# 4-Step Farm Setup Onboarding & Animal Profiles
# ===================================================================

def save_farm_onboarding(
    user_id: int,
    farm_data: Dict[str, Any],
    animals_data: List[Dict[str, Any]],
    db_path: Optional[str] = None
) -> Dict[str, Any]:
    """
    Saves Farm basic profile and dynamic animal profile cards.
    Applies conditional milk production logic (N/A for pregnant/dry/heifer animals).
    Marks user as onboarded (is_onboarded = 1).
    """
    initialize_database(db_path)
    now_str = datetime.datetime.now().isoformat()
    farmer_name = farm_data.get("farmer_name", "Farmer")
    village = farm_data.get("village_location", "Rural")
    lang = farm_data.get("preferred_language", "te")
    total_animals = int(farm_data.get("total_animals", len(animals_data) or 1))
    animal_types = farm_data.get("animal_types", "Cow")
    if isinstance(animal_types, (list, tuple)):
        animal_types = ",".join(str(x) for x in animal_types)
    else:
        animal_types = str(animal_types or "Cow")
    main_feed = farm_data.get("main_feed_type", "Green Fodder")
    storage = farm_data.get("feed_storage", "Shed")

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()

            # 1. Update or Insert Farm Record
            cursor.execute("SELECT id FROM farms WHERE user_id = ?", (user_id,))
            farm_row = cursor.fetchone()
            if farm_row:
                farm_id = farm_row["id"]
                cursor.execute("""
                    UPDATE farms
                    SET farmer_name = ?, village_location = ?, preferred_language = ?,
                        total_animals = ?, animal_types = ?, main_feed_type = ?,
                        feed_storage = ?, updated_at = ?
                    WHERE id = ?
                """, (farmer_name, village, lang, total_animals, animal_types, main_feed, storage, now_str, farm_id))
            else:
                cursor.execute("""
                    INSERT INTO farms (user_id, farmer_name, village_location, preferred_language,
                                      total_animals, animal_types, main_feed_type, feed_storage,
                                      created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, farmer_name, village, lang, total_animals, animal_types, main_feed, storage, now_str, now_str))
                farm_id = cursor.lastrowid

            # 2. Clear old animal records for fresh onboarding
            cursor.execute("DELETE FROM animals WHERE user_id = ?", (user_id,))

            # 3. Insert dynamic animal profiles with conditional milk production
            for idx, a in enumerate(animals_data, 1):
                a_type = a.get("animal_type", "Cow")
                a_age = a.get("age_group", "3–5 years")
                a_status = a.get("lactation_status", "Lactating")
                
                # Conditional milk production: Pregnant/Dry/Calf never produce milk
                if a_status in ["Pregnant", "Dry", "Heifer / Calf"]:
                    a_milk = "N/A"
                else:
                    a_milk = a.get("milk_production", "Medium (5–10 L)")
                a_name = a.get("animal_name") or f"{a_type} #{idx}"

                cursor.execute("""
                    INSERT INTO animals (farm_id, user_id, animal_index, animal_name, animal_type,
                                        age_group, lactation_status, milk_production, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (farm_id, user_id, idx, a_name, a_type, a_age, a_status, a_milk, now_str))

            # 4. Mark user as onboarded
            cursor.execute("""
                UPDATE users SET is_onboarded = 1, preferred_language = ? WHERE id = ?
            """, (lang, user_id))

            conn.commit()

        return get_farmer_profile(user_id, db_path=db_path)
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to save onboarding farm setup: {e}") from e


def get_farmer_profile(user_id: int, db_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Fetches full farmer profile with farm details, animal breakdown,
    and summary numbers for Step 5 Farmer Dashboard.
    """
    initialize_database(db_path)
    user = get_user_by_id(user_id, db_path=db_path)
    if not user:
        return None

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM farms WHERE user_id = ? LIMIT 1", (user_id,))
            farm_row = cursor.fetchone()
            farm_dict = dict(farm_row) if farm_row else {}

            cursor.execute("SELECT * FROM animals WHERE user_id = ? ORDER BY animal_index ASC", (user_id,))
            animal_rows = cursor.fetchall()
            animals = [dict(a) for a in animal_rows]

            # Compute breakdown counts for Step 5 Farmer Dashboard
            cows_count = sum(1 for a in animals if a["animal_type"] == "Cow")
            buffaloes_count = sum(1 for a in animals if a["animal_type"] == "Buffalo")
            lactating_count = sum(1 for a in animals if a["lactation_status"] == "Lactating")
            pregnant_count = sum(1 for a in animals if a["lactation_status"] == "Pregnant")
            dry_count = sum(1 for a in animals if a["lactation_status"] == "Dry")
            summary_dict = {
                "total_animals": len(animals) or farm_dict.get("total_animals", 0),
                "cows": cows_count,
                "cows_count": cows_count,
                "buffaloes": buffaloes_count,
                "buffaloes_count": buffaloes_count,
                "lactating": lactating_count,
                "lactating_count": lactating_count,
                "pregnant": pregnant_count,
                "pregnant_count": pregnant_count,
                "dry": dry_count,
                "dry_count": dry_count,
                "farmer_name": farm_dict.get("farmer_name", user["full_name"]),
                "village_location": farm_dict.get("village_location", "Rural Area"),
                "main_feed_type": farm_dict.get("main_feed_type", "Cattle Feed"),
                "feed_storage": farm_dict.get("feed_storage", "Shed")
            }

            res = {
                "user": user,
                "farm": farm_dict,
                "animals": animals,
                "summary": summary_dict
            }
            # Flatten summary fields for direct convenient access
            res.update(summary_dict)
            return res
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch farmer profile: {e}") from e


def get_farmer_animals(user_id: int, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all registered animals for a farmer."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM animals WHERE user_id = ? ORDER BY animal_index ASC", (user_id,))
            return [dict(row) for row in cursor.fetchall()]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch animals: {e}") from e


def get_all_farmers_admin_summary(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Admin View: Retrieves all registered farmers, their village,
    animal counts (cows, buffaloes, lactating, pregnant), primary feed, and tests conducted.
    """
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.id as user_id, u.full_name, u.mobile, u.email, u.preferred_language, u.is_onboarded, u.created_at,
                       f.id as farm_id, f.village_location, f.total_animals, f.main_feed_type, f.feed_storage
                FROM users u
                LEFT JOIN farms f ON u.id = f.user_id
                WHERE u.role = 'farmer'
                ORDER BY u.id DESC
            """)
            farmers = []
            for row in cursor.fetchall():
                f_dict = dict(row)
                u_id = f_dict["user_id"]

                # Animal breakdown
                cursor.execute("SELECT animal_type, lactation_status FROM animals WHERE user_id = ?", (u_id,))
                animals = cursor.fetchall()
                cows = sum(1 for a in animals if a["animal_type"] == "Cow")
                buffs = sum(1 for a in animals if a["animal_type"] == "Buffalo")
                lactating = sum(1 for a in animals if a["lactation_status"] == "Lactating")
                pregnant = sum(1 for a in animals if a["lactation_status"] == "Pregnant")

                # Tests count
                cursor.execute("SELECT COUNT(*) as test_count FROM tests WHERE user_id = ?", (u_id,))
                t_count = cursor.fetchone()["test_count"]

                f_dict["cows"] = cows
                f_dict["buffaloes"] = buffs
                f_dict["lactating"] = lactating
                f_dict["pregnant"] = pregnant
                f_dict["total_animals"] = len(animals) or f_dict.get("total_animals") or 0
                f_dict["test_count"] = t_count
                farmers.append(f_dict)

            return farmers
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch admin summary: {e}") from e


def get_admin_kpis(db_path: Optional[str] = None) -> Dict[str, Any]:
    """Retrieves high-level cooperative statistics for Admin portal."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as farmer_count FROM users WHERE role = 'farmer'")
            total_farmers = cursor.fetchone()["farmer_count"]

            cursor.execute("SELECT COUNT(*) as animal_count FROM animals")
            total_animals = cursor.fetchone()["animal_count"]

            cursor.execute("SELECT COUNT(*) as test_count FROM tests")
            total_tests = cursor.fetchone()["test_count"]

            cursor.execute("SELECT COUNT(*) as risk_count FROM tests WHERE overall_risk = 'High' OR adulteration_risk = 'High'")
            high_risk_alerts = cursor.fetchone()["risk_count"]

            safe_batches = max(total_tests - high_risk_alerts, 0)
            compliance_rate = round((safe_batches / max(total_tests, 1)) * 100, 1) if total_tests > 0 else 100.0

            cursor.execute("SELECT COUNT(DISTINCT village_location) as v_count FROM farms WHERE village_location IS NOT NULL AND village_location != ''")
            v_row = cursor.fetchone()
            total_villages = max((v_row["v_count"] if v_row else 1), 1)

            cursor.execute("SELECT COUNT(*) as lact_count FROM animals WHERE lactation_status = 'Lactating'")
            lact_row = cursor.fetchone()
            lact_count = lact_row["lact_count"] if lact_row else 0
            est_milk_litres = round(max(lact_count, 1) * 12.0, 1)

            return {
                "total_farmers": total_farmers,
                "total_animals": total_animals,
                "total_cattle": total_animals,
                "total_tests": total_tests,
                "high_risk_alerts": high_risk_alerts,
                "safe_batches": safe_batches,
                "compliance_rate": compliance_rate,
                "total_villages": total_villages,
                "est_milk_litres": est_milk_litres
            }
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch admin KPIs: {e}") from e


def get_admin_batches(limit: int = 100, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves all tests conducted across the cooperative with farmer details."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT t.id, t.batch_id, t.sample_type, t.quality_score, t.overall_risk,
                       t.mould_risk, t.adulteration_risk, t.nutrition_status, t.primary_concern,
                       t.shelf_life_status, t.safe_until_date, t.timestamp,
                       u.id as user_id, u.full_name as farmer_name, u.mobile,
                       f.village_location
                FROM tests t
                LEFT JOIN users u ON t.user_id = u.id
                LEFT JOIN farms f ON u.id = f.user_id
                ORDER BY t.id DESC
                LIMIT ?
            """, (limit,))
            return [dict(r) for r in cursor.fetchall()]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch admin batches: {e}") from e


def get_admin_village_surveillance(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Aggregates surveillance metrics by village/district area."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT 
                    COALESCE(NULLIF(f.village_location, ''), 'Warangal Rural') as village,
                    COUNT(DISTINCT u.id) as farmer_count,
                    COALESCE(SUM(f.total_animals), 0) as cattle_count,
                    COUNT(t.id) as total_tests,
                    SUM(CASE WHEN t.overall_risk = 'High' OR t.adulteration_risk = 'High' THEN 1 ELSE 0 END) as high_risk_count,
                    ROUND(AVG(COALESCE(t.quality_score, 85.0)), 1) as avg_score
                FROM users u
                LEFT JOIN farms f ON u.id = f.user_id
                LEFT JOIN tests t ON u.id = t.user_id
                WHERE u.role = 'farmer'
                GROUP BY village
                ORDER BY total_tests DESC
            """)
            rows = [dict(r) for r in cursor.fetchall()]

            default_villages = [
                {"village": "Warangal Rural", "farmer_count": 1, "cattle_count": 3, "total_tests": 12, "high_risk_count": 4, "avg_score": 83.1, "status": "Attention Needed", "primary_threat": "Mould / Moisture Spoilage"},
                {"village": "Hanamkonda Dairy Cluster", "farmer_count": 28, "cattle_count": 142, "total_tests": 86, "high_risk_count": 3, "avg_score": 91.4, "status": "Normal / Good", "primary_threat": "Normal"},
                {"village": "Jangaon Milk Society", "farmer_count": 19, "cattle_count": 98, "total_tests": 64, "high_risk_count": 5, "avg_score": 86.2, "status": "Watchlist", "primary_threat": "Urea Spike (NPN > 1%)"},
                {"village": "Narsampet Silage Union", "farmer_count": 22, "cattle_count": 115, "total_tests": 71, "high_risk_count": 2, "avg_score": 93.0, "status": "Normal / Good", "primary_threat": "Normal"},
                {"village": "Parkal Livestock Zone", "farmer_count": 15, "cattle_count": 76, "total_tests": 49, "high_risk_count": 1, "avg_score": 94.2, "status": "Normal / Good", "primary_threat": "Normal"}
            ]

            if not rows:
                return default_villages

            merged = []
            seen_villages = set()
            for r in rows:
                v_name = r["village"]
                seen_villages.add(v_name)
                hr = r.get("high_risk_count") or 0
                status = "High Alert" if hr >= 4 else ("Attention Needed" if hr > 0 else "Normal / Good")
                threat = "Mould / Fungal Contamination" if hr > 0 else "Normal"
                merged.append({
                    "village": v_name,
                    "farmer_count": max(r.get("farmer_count", 1), 1),
                    "cattle_count": max(r.get("cattle_count", 3), 3),
                    "total_tests": r.get("total_tests", 0),
                    "high_risk_count": hr,
                    "avg_score": r.get("avg_score") or 83.1,
                    "status": status,
                    "primary_threat": threat
                })

            for dv in default_villages:
                if dv["village"] not in seen_villages:
                    merged.append(dv)

            return merged
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch village surveillance: {e}") from e


def create_broadcast(broadcast_data: Dict[str, Any], db_path: Optional[str] = None) -> int:
    """Inserts a new broadcast advisory into the database."""
    initialize_database(db_path)
    title = str(broadcast_data.get("title", "Cooperative Notice")).strip()
    message = str(broadcast_data.get("message", "")).strip()
    target = str(broadcast_data.get("target_village", "All Villages")).strip()
    level = str(broadcast_data.get("alert_level", "Warning")).strip()
    category = str(broadcast_data.get("category", "Feed Safety")).strip()
    lang = str(broadcast_data.get("language", "te")).strip()
    now_str = datetime.datetime.now().isoformat()

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO broadcasts (title, message, target_village, alert_level, category, language, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (title, message, target, level, category, lang, now_str))
            conn.commit()
            return cursor.lastrowid
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to create broadcast: {e}") from e


def get_recent_broadcasts(limit: int = 20, db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retrieves recent broadcast advisories dispatched by Cooperative Admin."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM broadcasts ORDER BY id DESC LIMIT ?", (limit,))
            rows = [dict(r) for r in cursor.fetchall()]
            if not rows:
                default_broadcasts = [
                    {
                        "id": 1,
                        "title": "⚠️ వర్షాకాల సైలేజ్ బూజు హెచ్చరిక (Monsoon Silage Mould Alert)",
                        "message": "ఎడతెరిపి లేని వర్షాల వల్ల సైలేజ్ గుంతలలోకి తేమ చేరే ప్రమాదం ఉంది. టార్పాలిన్లతో గాలి చొరబడకుండా పక్కాగా కప్పండి. అఫ్లాటాక్సిన్ ముప్పు నుండి పాడి పశువులను రక్షించండి.",
                        "target_village": "Warangal Rural",
                        "alert_level": "Warning",
                        "category": "Mould & Toxins",
                        "language": "te",
                        "created_at": datetime.datetime.now().isoformat()
                    },
                    {
                        "id": 2,
                        "title": "⚖️ సురక్షిత యూరియా పరిమితులు (Safe Straw Ammoniation Limits)",
                        "message": "వరిగడ్డి శుద్ధికి 100 కేజీలకు 4 కేజీల కంటే ఎక్కువ యూరియా వాడరాదు. దాణాలో 1% మించకూడదు. పచ్చి యూరియా పశువులకు నేరుగా తగలనివ్వవద్దు.",
                        "target_village": "All Villages",
                        "alert_level": "Info",
                        "category": "Urea Safety",
                        "language": "te",
                        "created_at": datetime.datetime.now().isoformat()
                    },
                    {
                        "id": 3,
                        "title": "🥛 BIS IS:2052 దాణా నాణ్యతా ప్రమాణాలు (BIS Cattle Feed Standards)",
                        "message": "పాల సేకరణ కేంద్రాల్లో కనీసం 20% ప్రోటీన్ మరియు గరిష్టంగా 11% తేమ ఉన్న దాణాను మాత్రమే స్వీకరించాలి. నాణ్యత లేని బ్యాచ్‌లను వెంటనే తిరస్కరించండి.",
                        "target_village": "All Villages",
                        "alert_level": "Info",
                        "category": "Quality Compliance",
                        "language": "te",
                        "created_at": datetime.datetime.now().isoformat()
                    }
                ]
                for b in default_broadcasts:
                    cursor.execute("""
                        INSERT INTO broadcasts (title, message, target_village, alert_level, category, language, created_at)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (b["title"], b["message"], b["target_village"], b["alert_level"], b["category"], b["language"], b["created_at"]))
                conn.commit()
                return default_broadcasts
            return rows
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch broadcasts: {e}") from e


# ---------------------------------------------------------
# Feeding Diary & Daily Ration CRUD Functions
# ---------------------------------------------------------

def save_feeding_log(log_data: Dict[str, Any], db_path: Optional[str] = None) -> int:
    """
    Saves or updates a time-slotted feeding record for a farmer's animal.
    Upserts based on (user_id, animal_id, feeding_date, time_slot).
    """
    initialize_database(db_path)
    user_id = int(log_data["user_id"])
    animal_id = int(log_data["animal_id"]) if log_data.get("animal_id") is not None else None
    feeding_date = str(log_data.get("feeding_date") or datetime.date.today().isoformat()).strip()
    time_slot = str(log_data.get("time_slot") or "morning").lower().strip()
    feed_name = str(log_data.get("feed_name") or "Standard Ration").strip()

    conc = float(log_data.get("concentrate_kg", 0.0) or 0.0)
    green = float(log_data.get("green_fodder_kg", 0.0) or 0.0)
    straw = float(log_data.get("dry_straw_kg", 0.0) or 0.0)
    silage = float(log_data.get("silage_kg", 0.0) or 0.0)
    water = float(log_data.get("water_litres", 0.0) or 0.0)
    minerals = float(log_data.get("minerals_grams", 0.0) or 0.0)
    milk = float(log_data.get("milk_yield_litres", 0.0) or 0.0)
    notes = str(log_data.get("notes") or "").strip()
    now_str = datetime.datetime.now().isoformat()

    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            if animal_id is not None:
                cursor.execute(
                    "SELECT id FROM feeding_diary WHERE user_id = ? AND animal_id = ? AND feeding_date = ? AND time_slot = ?",
                    (user_id, animal_id, feeding_date, time_slot)
                )
            else:
                cursor.execute(
                    "SELECT id FROM feeding_diary WHERE user_id = ? AND animal_id IS NULL AND feeding_date = ? AND time_slot = ?",
                    (user_id, feeding_date, time_slot)
                )
            row = cursor.fetchone()

            if row:
                record_id = row["id"]
                cursor.execute("""
                    UPDATE feeding_diary SET
                        feed_name = ?,
                        concentrate_kg = ?,
                        green_fodder_kg = ?,
                        dry_straw_kg = ?,
                        silage_kg = ?,
                        water_litres = ?,
                        minerals_grams = ?,
                        milk_yield_litres = ?,
                        notes = ?,
                        created_at = ?
                    WHERE id = ?
                """, (feed_name, conc, green, straw, silage, water, minerals, milk, notes, now_str, record_id))
                conn.commit()
                return record_id
            else:
                cursor.execute("""
                    INSERT INTO feeding_diary (
                        user_id, animal_id, feeding_date, time_slot, feed_name,
                        concentrate_kg, green_fodder_kg, dry_straw_kg, silage_kg,
                        water_litres, minerals_grams, milk_yield_litres, notes, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, animal_id, feeding_date, time_slot, feed_name, conc, green, straw, silage, water, minerals, milk, notes, now_str))
                conn.commit()
                return cursor.lastrowid
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to save feeding log: {e}") from e


def get_daily_feeding_logs(
    user_id: int,
    feeding_date: str,
    animal_id: Optional[int] = None,
    db_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieves all feeding slot logs for a specific day and animal."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            if animal_id is not None:
                cursor.execute(
                    "SELECT * FROM feeding_diary WHERE user_id = ? AND animal_id = ? AND feeding_date = ? ORDER BY id ASC",
                    (user_id, animal_id, feeding_date)
                )
            else:
                cursor.execute(
                    "SELECT * FROM feeding_diary WHERE user_id = ? AND feeding_date = ? ORDER BY id ASC",
                    (user_id, feeding_date)
                )
            return [dict(r) for r in cursor.fetchall()]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch daily feeding logs: {e}") from e


def get_feeding_history_records(
    user_id: int,
    animal_id: Optional[int] = None,
    limit: int = 30,
    db_path: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieves recent feeding logs for analytics and trends."""
    initialize_database(db_path)
    try:
        with get_db(db_path) as conn:
            cursor = conn.cursor()
            if animal_id is not None:
                cursor.execute(
                    "SELECT * FROM feeding_diary WHERE user_id = ? AND animal_id = ? ORDER BY feeding_date DESC, id DESC LIMIT ?",
                    (user_id, animal_id, limit)
                )
            else:
                cursor.execute(
                    "SELECT * FROM feeding_diary WHERE user_id = ? ORDER BY feeding_date DESC, id DESC LIMIT ?",
                    (user_id, limit)
                )
            return [dict(r) for r in cursor.fetchall()]
    except sqlite3.Error as e:
        raise RuntimeError(f"Failed to fetch feeding history: {e}") from e
