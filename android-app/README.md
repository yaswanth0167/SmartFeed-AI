# 📱 SmartFeed AI - Native Android Application Project

This directory contains the complete, turnkey **Android Studio Gradle Project** for **SmartFeed AI**.

It wraps the cloud-deployed SmartFeed AI intelligence platform into a native Android application with hardware camera acceleration, offline resilience, and file upload choosers.

---

## 🌟 Key Features

1. **📷 Hardware Camera & Photo Chooser**:
   - Integrates with Android's native `MediaStore.ACTION_IMAGE_CAPTURE` and `FileProvider`.
   - When a farmer taps **"Upload Feed Photo"** or **"Take Picture"**, Android prompts them to either snap a live picture using the device camera or select a high-resolution photo from the gallery.
2. **🔄 Swipe-to-Refresh**:
   - Native `SwipeRefreshLayout` in SmartFeed Emerald (`#047857`) allowing instant cache refresh.
3. **📶 Offline Resilience Screen**:
   - Displays a clean Telugu/English offline notice with a 1-tap **Retry** button if network drops.
4. **🔙 Hardware Back Navigation**:
   - Intercepts phone back button to seamlessly navigate between tabs and scan history without accidentally closing the app. Double-tap back within 2 seconds exits cleanly.
5. **🎨 Native Styling & Launch Icons**:
   - Preconfigured with Emerald Green themes, Android Material 3 styles, and adaptive mipmap launcher icons (`mdpi`, `hdpi`, `xhdpi`, `xxhdpi`, `xxxhdpi`).

---

## 🛠️ How to Build the APK in Android Studio

### Prerequisites:
- [Android Studio Iguana / Hedgehog or newer](https://developer.android.com/studio)
- JDK 17 or JDK 21 (bundled with Android Studio)
- Android SDK 34 (Android 14)

### Step 1: Open the Project
1. Launch **Android Studio**.
2. Click **Open** (or `File -> Open`).
3. Select the `android-app` folder located inside the repository:
   ```
   y:\smartfeed-ai\android-app
   ```
4. Allow Gradle to sync dependencies (it will automatically download AndroidX, Material, and SwipeRefreshLayout).

### Step 2: Build the APK
- **Debug APK (For Direct Sharing & Testing on Phones)**:
  - In Android Studio menu: Click **Build -> Build Bundle(s) / APK(s) -> Build APK(s)**.
  - Or via terminal:
    ```bash
    ./gradlew assembleDebug
    ```
  - The generated APK will be at:
    ```
    app/build/outputs/apk/debug/app-debug.apk
    ```
- **Release APK (For Production / Google Play Store)**:
  - In Android Studio menu: Click **Build -> Generate Signed Bundle / APK**.
  - Choose **Android App Bundle (.aab)** for Google Play or **APK** for direct distribution.
  - Sign with your keystore and build.

---

## 📲 How to Install the APK on Any Android Phone

1. Copy `app-debug.apk` to your phone via USB, Google Drive, or send it directly via **WhatsApp / Telegram**.
2. Tap the file on the phone to install.
3. If prompted with *"Install from unknown sources"*, tap **Settings** and toggle **Allow from this source**.
4. The **SmartFeed AI** app will install with its official logo on your app drawer and home screen.
5. Open the app and grant Camera / Media permissions when prompted.

---

## 🌐 Connected Backend
- The app points to:
  ```
  https://smartfeed-ai-ckph.onrender.com
  ```
- Any backend diagnostic improvements, model updates, or translation refinements deployed to Render reflect in the Android app immediately without requiring users to reinstall the APK!