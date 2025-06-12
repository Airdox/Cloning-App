[app]

title = Voice Cloning App
package.name = voicecloningapk
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,m4a,ogg,txt,md,pth

version = 0.1

requirements = python3==3.9.13,kivy==2.1.0,android

orientation = portrait

# Android specific
android.permissions = READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE
android.api = 27
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.arch = armeabi-v7a

# Icon and presplash images (optional, paths are relative to source.dir)
# icon.filename = %(source.dir)s/data/icon.png
# presplash.filename = %(source.dir)s/data/presplash.png

[buildozer]

# Log level (0 = error, 1 = info, 2 = debug)
log_level = 2

# Warn on deprecated features? (0 or 1)
warn_on_deprecated = 1
