[app]

title = Voice Cloning App
package.name = voicecloningapk
package.domain = com.secure.voicecloning
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,m4a,ogg,txt,md

version = 0.2.0

requirements = python3==3.11,kivy==2.2.0,android

orientation = portrait

# Android specific - using more recent and secure API levels
android.permissions = READ_EXTERNAL_STORAGE
android.api = 34
android.minapi = 26
android.sdk = 34
android.ndk = 25b
android.arch = arm64-v8a,armeabi-v7a

# Security enhancements
android.gradle_dependencies = androidx.security:security-crypto:1.1.0-alpha06
android.add_compile_options = compileOptions { sourceCompatibility JavaVersion.VERSION_1_8; targetCompatibility JavaVersion.VERSION_1_8 }

# Icon and presplash images (optional, paths are relative to source.dir)
# icon.filename = %(source.dir)s/data/icon.png
# presplash.filename = %(source.dir)s/data/presplash.png

[buildozer]

# Log level (0 = error, 1 = info, 2 = debug) - reduced for production
log_level = 1

# Warn on deprecated features? (0 or 1)
warn_on_deprecated = 1
