<p align="center">
  <img src="static/images/logo_square_with_name_1024x1024.png" alt="SpectraMatch Logo" width="200">
</p>

<h1 align="center">SpectraMatch</h1>

<p align="center">
  <strong>Textile Quality Control System — Professional Color &amp; Pattern Analysis</strong><br>
  <em>Pamukkale University · Department of Electrical and Electronic Engineering</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-2.2.3-blue" alt="Version">
  <img src="https://img.shields.io/badge/python-3.9%2B-green" alt="Python">
  <img src="https://img.shields.io/badge/framework-Flask-lightgrey" alt="Flask">
  <img src="https://img.shields.io/badge/license-Academic-orange" alt="License">
  <img src="https://img.shields.io/badge/language-EN%20%7C%20TR-informational" alt="i18n">
</p>

---

## Overview

SpectraMatch is a research-grade image quality control system designed for the textile industry. It provides quantitative color and pattern analysis by comparing a **reference** image against a **sample** image, producing detailed metrics, visual diagnostics, and downloadable PDF reports.

The system is developed as part of ongoing research at the **Department of Electrical and Electronic Engineering, Pamukkale University (PAU)**, Denizli, Turkey.

### Key Capabilities

- **Color Analysis** — Computes CIE ΔE2000 color difference across user-defined sampling points, with support for multiple illuminants (D65, D50, A, C, F2, TL84) and color spaces (CIELAB, sRGB, CMYK, XYZ).
- **Pattern Analysis** — Evaluates structural similarity (SSIM), GLCM texture features, Fourier-domain frequency analysis, and phase correlation between reference and sample images.
- **Single Image Analysis** — Standalone mode for analyzing a single image's color distribution, texture uniformity, and defect indicators without a reference.
- **Region Selection** — Interactive region-of-interest tools including circle, square, rectangle, and freehand polygon (pen) selection with real-time visual overlay.
- **Sampling Configuration** — Configurable N-point sampling with manual placement, random generation, or hybrid workflows. Points are validated against the selected region.
- **PDF Report Generation** — Produces professional, multi-page PDF reports with charts, statistical tables, recommendations, and a settings receipt. Reports are available in English and Turkish.
- **Bilingual Interface** — Full English and Turkish localization across all UI elements, tooltips, warnings, and generated reports.

---

## Architecture

SpectraMatch ships as a single codebase that serves two interfaces:

| Component | Technology | Description |
|-----------|-----------|-------------|
| **Web Application** | Flask + Vanilla JS | Browser-based UI accessible at `http://localhost:5000` |
| **Desktop Application** | Flask + pywebview | Native window wrapping the same Flask backend |

Both interfaces share the same backend (`app.py`) and analysis modules. The desktop version adds a native window shell via [pywebview](https://pywebview.flowrl.com/) with a custom splash screen.

### Project Structure

```
SPECTRAMATCH2026_feb/
├── app.py                      # Flask application (routes, API endpoints)
├── wsgi.py                     # WSGI entry point for production deployment
├── requirements.txt            # Python dependencies
├── Launch_Desktop_App.bat      # Windows launcher for desktop mode
│
├── modules/                    # Backend analysis engine
│   ├── ColorUnitBackend.py     # Color difference analysis (ΔE2000, CIELAB, illuminants)
│   ├── PatternUnitBackend.py   # Pattern analysis (SSIM, GLCM, FFT, phase correlation)
│   ├── SingleImageUnitBackend.py  # Single-image standalone analysis
│   ├── RecommendationsEngine.py   # Threshold-aware findings & recommendations
│   ├── ReportTranslations.py   # Bilingual translation dictionary for PDF reports
│   ├── ReportUtils.py          # Shared PDF styling, constants, and utilities
│   └── SettingsReceipt.py      # Settings receipt PDF generator
│
├── templates/
│   ├── index.html              # Web application UI
│   └── desktop.html            # Desktop application UI
│
├── desktop/
│   ├── app_desktop.py          # pywebview launcher and JS↔Python bridge
│   └── splash.html             # Desktop splash screen
│
└── static/
    ├── css/                    # Stylesheets (main.css, shape-dropdown.css, image-actions.css)
    ├── js/                     # Client-side JavaScript
    │   ├── app.js              # Main application logic and UI controller
    │   ├── region-selector.js  # Interactive region selection on images
    │   ├── region-validator.js # Point-in-region validation (circle, rect, polygon)
    │   ├── i18n.js             # Internationalization (EN/TR translations)
    │   └── development-modal.js
    ├── images/                 # Logos and flag icons
    ├── DataSheets/             # Technical datasheets (EN/TR PDFs)
    ├── READYTOTEST/            # Built-in sample images for quick testing
    └── Animation/              # Loading animation assets
```

---

## Analysis Pipeline

### Color Unit

1. User uploads a reference and sample image.
2. N sampling points are placed (manually, randomly, or hybrid) within the selected region.
3. At each point, a local patch is extracted from both images.
4. Pixel values are converted: **sRGB → XYZ → CIELAB** (with optional chromatic adaptation to the selected illuminant).
5. **CIEDE2000 (ΔE\*₀₀)** is computed per point.
6. Aggregate statistics are calculated: mean, standard deviation, min, max.
7. A **Composite Score Index (CSI)** is derived from the ΔE distribution.
8. Results are compared against user-defined pass/conditional/fail thresholds.

### Pattern Unit

1. Both images are converted to grayscale.
2. **SSIM** (Structural Similarity Index) is computed with a sliding window.
3. **GLCM** (Gray-Level Co-occurrence Matrix) texture features are extracted: contrast, dissimilarity, homogeneity, energy, correlation.
4. **FFT** (Fast Fourier Transform) spectral analysis compares frequency-domain characteristics.
5. **Phase correlation** measures translational alignment.
6. A weighted composite pattern score is produced.

### Single Image Unit

Performs color distribution analysis, texture uniformity assessment, and defect detection on a single image without requiring a reference.

---

## Getting Started

### Prerequisites

- **Python 3.9** or later
- **pip** package manager

### Installation

```bash
# Clone the repository
git clone https://github.com/algamel98/SPECTRAMATCHPAU.git
cd SPECTRAMATCHPAU

# Install dependencies
pip install -r requirements.txt
```

### Running the Web Application

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

### Running the Desktop Application (Windows)

Double-click `Launch_Desktop_App.bat`, or run manually:

```bash
pip install pywebview
python desktop/app_desktop.py
```

A native window will open with a splash screen, then load the application.

### Production Deployment

The application includes a `wsgi.py` entry point compatible with production WSGI servers:

```bash
# Example with Gunicorn
gunicorn wsgi:application --bind 0.0.0.0:5000
```

Heavy dependencies (OpenCV, NumPy, ReportLab) are lazy-imported to keep WSGI startup fast and avoid timeout issues behind reverse proxies.

---

## Features in Detail

### Region Selection Tools

| Tool | Description |
|------|-------------|
| **Circle** | Circular selection with adjustable diameter (20–500 px) |
| **Square** | Square selection with adjustable side length |
| **Rectangle** | Rectangular selection with independent width and height |
| **Pen (Freehand)** | Draw a custom closed polygon directly on the image |

All tools support click-to-place, drag-to-move, and scroll-to-resize (except Pen). The selected region is visually overlaid on both reference and sample images simultaneously.

### Sampling Modes

- **Manual** — Click directly on the image to place each sampling point.
- **Random** — Automatically generate N random points within the selected region.
- **Hybrid** — Place some points manually, then fill the remainder randomly.

Points placed outside the defined region are rejected with a visual warning.

### PDF Reports

Each analysis generates a downloadable PDF report containing:

- Header with logo, report ID, timestamp, operator name, and software version
- Image thumbnails of reference and sample
- Statistical summary tables with color-coded pass/fail indicators
- Diagnostic charts (histograms, scatter plots, FFT spectra)
- Threshold-aware recommendations generated by the Recommendations Engine
- Bilingual output (English or Turkish, selected by the user)
- A separate Settings Receipt PDF documenting all configuration parameters used

### Internationalization

The entire interface is available in **English** and **Turkish**:

- All UI labels, buttons, tooltips, and error messages
- PDF report content, table headers, and recommendations
- Real-time language switching without page reload (web) or with page retranslation (desktop)

---

## Configuration

Analysis parameters are configurable through the Advanced Settings modal:

| Parameter | Description | Default |
|-----------|-------------|---------|
| Selection Shape | Region shape for analysis | Circle |
| Sampling Count | Number of sampling points (N) | 10 |
| Color Unit | Color space for comparison | CIELAB |
| Illuminant | Reference illuminant | D65 |
| Pass Threshold | ΔE threshold for PASS | 1.0 |
| Conditional Threshold | ΔE threshold for CONDITIONAL | 2.0 |
| CSI Good / Warning | CSI score thresholds | 85 / 70 |
| Report Language | Language for PDF output | English |
| Operator | Operator name for reports | — |
| Timezone | UTC offset for timestamps | +3 |

---

## Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Python, Flask, OpenCV, NumPy, scikit-image, SciPy, Matplotlib |
| **PDF Generation** | ReportLab |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **Desktop Shell** | pywebview |
| **Deployment** | WSGI (Gunicorn, mod_wsgi compatible) |

---

## Built-in Test Images

The application includes six built-in test images in `static/READYTOTEST/` for quick evaluation. These can be loaded directly from the **Ready-to-Test** button in the toolbar (desktop) or header (web) without manual file upload.

- **Pair 1**: Test1 (reference) + Test2 (sample)
- **Pair 2**: Test3 (reference) + Test4 (sample)
- **Pair 3**: Test5 (reference) + Test6 (sample)

Each image can also be loaded individually for Single Image mode.

---

## Research Context

This software is developed as part of research at **Pamukkale University (PAU)**, Department of Electrical and Electronic Engineering, Denizli, Turkey. It is intended for academic and industrial evaluation of color consistency and pattern fidelity in textile production.

The system implements established colorimetric standards (CIE ΔE2000, CIELAB) and image analysis techniques (SSIM, GLCM, FFT) within a practical, user-facing application suitable for laboratory and production-floor use.

---

## Author

**Abdelbary Algamel**  
Department of Electrical and Electronic Engineering  
Pamukkale University, Denizli, Turkey  
[aalgamel23@posta.pau.edu.tr](mailto:aalgamel23@posta.pau.edu.tr)

**Supervisor:** Dr. Adem Ukte  
Pamukkale University, Denizli, Turkey

---

## License

This project is developed for academic research purposes at Pamukkale University. All rights reserved. Contact the author for licensing inquiries.
