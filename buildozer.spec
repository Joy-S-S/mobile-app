[app]
title = Mamlkah Mobile
package.name = mamlkah
package.domain = org.mamlkah
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy==2.3.0,requests,urllib3,idna,certifi,charset-normalizer
orientation = portrait
osx.python_version = 3
osx.kivy_version = 1.9.1
fullscreen = 0
android.permissions = INTERNET,VIBRATE,WAKE_LOCK
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True
android.icon.filename = assets/icon.png
android.presplash_filename = assets/splash.png
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
