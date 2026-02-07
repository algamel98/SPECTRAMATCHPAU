# SpectraMatch Windows Installer Builder

This folder contains everything needed to build a professional Windows installer (.exe) for the SpectraMatch Desktop application.

## What the Installer Does

When a user runs the generated `.exe` installer, they get a professional wizard:

1. **Welcome Page** — With SpectraMatch logo and branding
2. **License Agreement** — User must accept before continuing
3. **Installation Path** — Default: `C:\Program Files\SpectraMatch\` (user can change)
4. **Shortcut Options** — Desktop shortcut + Start Menu entry (both checked by default)
5. **Install Progress** — Shows file extraction progress
6. **Finish Page** — Option to launch SpectraMatch immediately

After installation:
- A **desktop shortcut** with the SpectraMatch icon is created
- A **Start Menu group** with the app + uninstaller is created
- The user can **uninstall** cleanly via Windows Settings > Apps

---

## Prerequisites

You need two free tools installed on your **build machine** (not the end-user's machine):

### 1. PyInstaller
```bash
pip install pyinstaller
```

### 2. Inno Setup 6 (Free)
Download from: https://jrsoftware.org/isdl.php

Install with default options. The build script auto-detects the installation path.

---

## How to Build

### One-Click Build
Simply double-click:
```
installer\build_installer.bat
```

This script automatically:
1. Checks all prerequisites
2. Converts the PNG logo to `.ico` format
3. Generates branded wizard images (`.bmp`)
4. Bundles the entire app with PyInstaller (~3-10 minutes first time)
5. Compiles the Inno Setup installer

### Output
```
installer\output\SpectraMatch_Setup_2.2.1.exe
```

This single `.exe` file is your complete installer — ready to distribute.

---

## How to Distribute

### Option A: Serve from Your Web App (Default)
Place the built `.exe` in `installer/output/` and the Flask route `/download/desktop` will serve it directly. The "Download for Windows" button in the web app header already points to this route.

### Option B: External Hosting (Recommended for Production)
Upload the `.exe` to one of:
- **GitHub Releases** (free, reliable)
- **Any CDN or file hosting service**
- **Your JPaaS hosting** (if it supports large static files)

Then set the environment variable:
```bash
DESKTOP_INSTALLER_URL=https://github.com/yourname/spectramatch/releases/download/v2.2.1/SpectraMatch_Setup_2.2.1.exe
```

The Flask route will automatically redirect to this URL instead of serving the local file.

---

## Files in This Folder

| File | Purpose |
|------|---------|
| `build_installer.bat` | One-click build automation script |
| `spectramatch.spec` | PyInstaller spec file (what to bundle) |
| `spectramatch_setup.iss` | Inno Setup script (installer wizard config) |
| `LICENSE.txt` | License agreement shown during installation |
| `convert_icon.py` | Converts PNG logo → multi-size `.ico` |
| `create_wizard_images.py` | Generates branded `.bmp` wizard images |
| `README.md` | This file |

### Generated During Build (gitignored)
| File | Purpose |
|------|---------|
| `spectramatch.ico` | Application icon (multi-size) |
| `wizard_image.bmp` | Large wizard sidebar image (164×314) |
| `wizard_small.bmp` | Small wizard corner image (55×55) |
| `output/SpectraMatch_Setup_*.exe` | The final installer |

---

## Updating the Version

When releasing a new version, update these locations:
1. `spectramatch_setup.iss` — `#define MyAppVersion "X.Y.Z"`
2. `app.py` — The installer filename in `download_desktop_installer()`
3. `templates/index.html` — The version shown in the download button
4. `desktop/splash.html` — The version tag

---

## End-User Requirements

The installer handles everything. The end-user needs:
- **Windows 10 or later** (64-bit)
- **~500 MB disk space**
- No Python installation required
- No manual dependency installation required
