# -*- coding: utf-8 -*-
import io, os, math, logging, tempfile
from pathlib import Path
import numpy as np
import cv2
from datetime import datetime, timedelta
from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from .ReportTranslations import get_translator, translate_status

# Scientific / Image Algo imports
from skimage.metrics import structural_similarity as ssim
from skimage.feature import graycomatrix, graycoprops

from scipy.fft import fft2, fftshift
# phaseCorrelate is in cv2

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

# Resolve static image paths robustly in JPaaS/mod_wsgi
BASE_DIR = Path(__file__).resolve().parents[1]
STATIC_IMAGES_DIR = BASE_DIR / "static" / "images"
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image as RLImage, Table, TableStyle, Spacer, PageBreak, Flowable, KeepTogether
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# =================================================================================================
# CONFIGURATION
# =================================================================================================

SOFTWARE_VERSION = "2.2.1"
COMPANY_NAME = "Textile Engineering Solutions"
COMPANY_SUBTITLE = "Professional Pattern Analysis Solutions"
REPORT_TITLE = "Pattern Analysis Report"
PAGE_SIZE = A4
MARGIN_L = 50
MARGIN_R = 50
MARGIN_T = 50
MARGIN_B = 50
DPI = 300
DEFAULT_TIMEZONE_OFFSET_HOURS = 3
FRAME_MARGIN = 9

BLUE1 = colors.HexColor("#2980B9")
BLUE2 = colors.HexColor("#3498DB")
GREEN = colors.HexColor("#27AE60")
RED = colors.HexColor("#E74C3C")
ORANGE = colors.HexColor("#F39C12")
NEUTRAL_DARK = colors.HexColor("#2C3E50")
NEUTRAL = colors.HexColor("#7F8C8D")
NEUTRAL_L = colors.HexColor("#BDC3C7")

STATUS_COLORS = {"PASS": GREEN, "FAIL": RED, "CONDITIONAL": ORANGE}

PRIMARY_LOGO = r"logo_square_with_name_1024x1024.png"
FALLBACK_LOGOS = [
    r"logo_square_with_name_1024x1024.png",
    r"logo_square_no_name_1024x1024.png"
]

DEFAULT_CONFIG = {
    'operator': 'Unknown',
    'timezone_offset': 3,
    'thresholds': {
        'Structural SSIM': {'pass': 85.0, 'conditional': 70.0},
        'Gradient Similarity': {'pass': 85.0, 'conditional': 70.0},
        'Phase Correlation': {'pass': 85.0, 'conditional': 70.0},
        'Structural Match': {'pass': 85.0, 'conditional': 70.0}
    },
    'global_threshold': 75.0,
    'sections': {
        'ssim': True,
        'gradient': True,
        'phase': True,
        'structural': True,
        'fourier': True,
        'glcm': True,
        'gradient_boundary': True,
        'phase_boundary': True,
        'summary': True,
        'conclusion': True,
        'recommendation': True
    }
}

# =================================================================================================
# HELPERS
# =================================================================================================

def setup_fonts():
    """Setup fonts with full Turkish character support (İ, Ö, Ü, Ş, Ç, Ğ, ı, ş, ğ)."""
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    
    # Try Arial - excellent Turkish character support on Windows
    try:
        if os.path.exists(r"C:\Windows\Fonts\arial.ttf"):
            pdfmetrics.registerFont(TTFont('Arial', r"C:\Windows\Fonts\arial.ttf"))
            pdfmetrics.registerFont(TTFont('Arial-Bold', r"C:\Windows\Fonts\arialbd.ttf"))
            return "Arial", "Arial-Bold"
    except:
        pass
    
    # Try Segoe UI - modern Windows font with full Turkish support
    try:
        if os.path.exists(r"C:\Windows\Fonts\segoeui.ttf"):
            pdfmetrics.registerFont(TTFont('SegoeUI', r"C:\Windows\Fonts\segoeui.ttf"))
            pdfmetrics.registerFont(TTFont('SegoeUI-Bold', r"C:\Windows\Fonts\segoeuib.ttf"))
            return "SegoeUI", "SegoeUI-Bold"
    except:
        pass
    
    # Try Tahoma - good Turkish support
    try:
        if os.path.exists(r"C:\Windows\Fonts\tahoma.ttf"):
            pdfmetrics.registerFont(TTFont('Tahoma', r"C:\Windows\Fonts\tahoma.ttf"))
            pdfmetrics.registerFont(TTFont('Tahoma-Bold', r"C:\Windows\Fonts\tahomabd.ttf"))
            return "Tahoma", "Tahoma-Bold"
    except:
        pass
    
    # Fallback to Helvetica (may not support all Turkish chars)
    return "Helvetica", "Helvetica-Bold"

PDF_FONT_REGULAR, PDF_FONT_BOLD = setup_fonts()

styles = getSampleStyleSheet()
StyleTitle = ParagraphStyle("Title", parent=styles["Heading1"], fontName=PDF_FONT_BOLD, fontSize=20, textColor=NEUTRAL_DARK, leading=24, alignment=TA_LEFT)
StyleH1 = ParagraphStyle("H1", parent=styles["Heading2"], fontName=PDF_FONT_BOLD, fontSize=15, textColor=BLUE1, leading=18, spaceAfter=8, keepWithNext=1)
StyleH2 = ParagraphStyle("H2", parent=styles["Heading3"], fontName=PDF_FONT_BOLD, fontSize=12.5, textColor=BLUE2, leading=16, spaceAfter=6, keepWithNext=1)
StyleBody = ParagraphStyle("Body", parent=styles["BodyText"], fontName=PDF_FONT_REGULAR, fontSize=10, leading=14)
StyleSmall = ParagraphStyle("Small", parent=styles["BodyText"], fontName=PDF_FONT_REGULAR, fontSize=9, leading=12, textColor=NEUTRAL)

def get_local_time(offset=None):
    o = DEFAULT_TIMEZONE_OFFSET_HOURS if offset is None else offset
    return datetime.utcnow() + timedelta(hours=o)

def pick_logo():
    if os.path.exists(PRIMARY_LOGO): return PRIMARY_LOGO
    for p in FALLBACK_LOGOS:
        if os.path.exists(p): return p
    # Check static/images
    static_logo = (STATIC_IMAGES_DIR / PRIMARY_LOGO)
    if static_logo.exists():
        return str(static_logo)
    return None

def numpy_to_rl(img_array, max_width=5*inch, max_height=4*inch):
    # Handle BGRA/RGBA - Composite over BLACK background
    if img_array.ndim == 3 and img_array.shape[2] == 4:
        b, g, r, a = cv2.split(img_array)
        # Create black background
        bg = np.zeros_like(b)
        
        # Composite: Source * Alpha + Dest * (1 - Alpha)
        # Since Dest is black (0), it simplifies to Source * Alpha
        alpha_f = a.astype(float) / 255.0
        b = (b * alpha_f).astype(np.uint8)
        g = (g * alpha_f).astype(np.uint8)
        r = (r * alpha_f).astype(np.uint8)
        
        rgb = cv2.merge([r, g, b])
        pil_img = Image.fromarray(rgb)
    elif len(img_array.shape) == 3:
        pil_img = Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))
    else:
        pil_img = Image.fromarray(img_array)
    
    img_width, img_height = pil_img.size
    scale = min(max_width / (img_width or 1), max_height / (img_height or 1))
    new_width = img_width * scale
    new_height = img_height * scale
    
    img_buffer = io.BytesIO()
    pil_img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return RLImage(img_buffer, width=new_width, height=new_height)

def badge(text, back_color=NEUTRAL):
    class _Badge(Flowable):
        def __init__(self, t, bg):
            super().__init__()
            self.t, self.bg = t, bg
            self.w = max(60, 8 * len(t))
            self.h = 16
        def draw(self):
            self.canv.setFillColor(self.bg)
            self.canv.roundRect(0, 0, self.w, self.h, 3, fill=1, stroke=0)
            self.canv.setFillColor(colors.white)
            self.canv.setFont(PDF_FONT_BOLD, 9)
            self.canv.drawCentredString(self.w/2, 3, self.t)
        def wrap(self, availW, availH):
            return (self.w, self.h)
    return _Badge(text, back_color)

def make_header_footer(report_timestamp=None, analysis_id="", report_lang='en'):
    # Turkish translations for header/footer
    if report_lang == 'tr':
        company_name = 'Tekstil Mühendislik Çözümleri'
        subtitle = 'Profesyonel Desen Analizi Çözümleri'
    else:
        company_name = COMPANY_NAME
        subtitle = COMPANY_SUBTITLE
    
    def hf(canvas_, doc):
        canvas_.saveState()
        w, h = PAGE_SIZE
        # Frame
        canvas_.setStrokeColor(colors.HexColor("#E0E0E0"))
        canvas_.setLineWidth(0.8)
        canvas_.rect(FRAME_MARGIN, FRAME_MARGIN, w - 2*FRAME_MARGIN, h - 2*FRAME_MARGIN, stroke=1, fill=0)

        # Header
        y = h - 40
        canvas_.setStrokeColor(NEUTRAL_L)
        canvas_.setLineWidth(0.6)
        canvas_.line(MARGIN_L, y, w - MARGIN_R, y)

        canvas_.setFillColor(BLUE1)
        canvas_.setFont(PDF_FONT_BOLD, 10.5)
        canvas_.drawString(MARGIN_L, y + 10, company_name)

        cw = canvas_.stringWidth(company_name, PDF_FONT_BOLD, 10.5)
        canvas_.setFillColor(colors.black)
        canvas_.drawString(MARGIN_L + cw + 5, y + 10, " | ")
        
        pw = canvas_.stringWidth(" | ", PDF_FONT_BOLD, 10.5)
        canvas_.setFillColor(NEUTRAL)
        canvas_.setFont(PDF_FONT_REGULAR, 8.5)
        canvas_.drawString(MARGIN_L + cw + pw + 5, y + 10, subtitle)
        
        # Footer
        fy = 25
        canvas_.setStrokeColor(NEUTRAL_L)
        canvas_.setLineWidth(0.6)
        canvas_.line(MARGIN_L, fy + 10, w - MARGIN_R, fy + 10)

        canvas_.setFillColor(NEUTRAL)
        canvas_.setFont(PDF_FONT_REGULAR, 8)
        page_text = f"Sayfa {doc.page}" if report_lang == 'tr' else f"Page {doc.page}"
        canvas_.drawCentredString(w/2, fy - 3, page_text)

        if report_timestamp:
            canvas_.drawString(MARGIN_L, fy - 3, report_timestamp.strftime("%Y-%m-%d %H:%M:%S"))

        # Small logo
        footer_logo_path = STATIC_IMAGES_DIR / "logo_vertical_512x256.png"
        if footer_logo_path.exists():
            try:
                canvas_.drawImage(str(footer_logo_path), w - MARGIN_R - 36, fy - 6, width=36, height=18, preserveAspectRatio=True, mask='auto')
            except: pass

        canvas_.restoreState()
    return hf

# =================================================================================================
# IMAGE LOGIC
# =================================================================================================

def composite_over_black(img):
    if img.ndim == 3 and img.shape[2] == 4:
        b, g, r, a = cv2.split(img)
        alpha_f = a.astype(float) / 255.0
        b = (b * alpha_f).astype(np.uint8)
        g = (g * alpha_f).astype(np.uint8)
        r = (r * alpha_f).astype(np.uint8)
        return cv2.merge([b, g, r])
    return img

def preprocess_to_structure(img):
    # Ensure transparency is black
    img_bgr = composite_over_black(img)
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    filtered = cv2.bilateralFilter(gray, 9, 75, 75)
    return filtered

def method1_structural_ssim(ref, sample):
    ref_gray = preprocess_to_structure(ref)
    sample_gray = preprocess_to_structure(sample)
    if ref_gray.shape != sample_gray.shape:
        sample_gray = cv2.resize(sample_gray, (ref_gray.shape[1], ref_gray.shape[0]))
    
    score, diff_img = ssim(ref_gray, sample_gray, full=True)
    diff_img = (diff_img * 255).astype(np.uint8)
    diff_img_colored = cv2.applyColorMap(255 - diff_img, cv2.COLORMAP_JET)
    return score * 100, diff_img_colored

def method3_gradient_similarity(ref, sample):
    ref_gray = preprocess_to_structure(ref)
    sample_gray = preprocess_to_structure(sample)
    if ref_gray.shape != sample_gray.shape:
        sample_gray = cv2.resize(sample_gray, (ref_gray.shape[1], ref_gray.shape[0]))
        
    ref_gx = cv2.Sobel(ref_gray, cv2.CV_64F, 1, 0, ksize=3)
    ref_gy = cv2.Sobel(ref_gray, cv2.CV_64F, 0, 1, ksize=3)
    ref_mag = np.sqrt(ref_gx**2 + ref_gy**2)
    
    sample_gx = cv2.Sobel(sample_gray, cv2.CV_64F, 1, 0, ksize=3)
    sample_gy = cv2.Sobel(sample_gray, cv2.CV_64F, 0, 1, ksize=3)
    sample_mag = np.sqrt(sample_gx**2 + sample_gy**2)
    
    ref_mag_norm = cv2.normalize(ref_mag, None, 0, 1, cv2.NORM_MINMAX)
    sample_mag_norm = cv2.normalize(sample_mag, None, 0, 1, cv2.NORM_MINMAX)
    
    # Visualization
    ref_mag_uint8 = cv2.normalize(ref_mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    sample_mag_uint8 = cv2.normalize(sample_mag, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    score, diff_img = ssim(ref_mag_uint8, sample_mag_uint8, full=True)
    diff_img = (diff_img * 255).astype(np.uint8)
    diff_img_colored = cv2.applyColorMap(255 - diff_img, cv2.COLORMAP_HOT)
    
    gradient_diff = np.abs(ref_mag_norm - sample_mag_norm)
    return score * 100, diff_img_colored, {'gradient_diff': gradient_diff}



def method6_phase_correlation(ref, sample):
    ref_gray = preprocess_to_structure(ref)
    sample_gray = preprocess_to_structure(sample)
    if ref_gray.shape != sample_gray.shape:
        sample_gray = cv2.resize(sample_gray, (ref_gray.shape[1], ref_gray.shape[0]))
        
    ref_float = np.float32(ref_gray)
    sample_float = np.float32(sample_gray)
    
    try:
        shift, response = cv2.phaseCorrelate(ref_float, sample_float)
        score = response * 100
    except:
        score = 0.0
        
    phase_diff = cv2.absdiff(ref_gray, sample_gray)
    diff_img = cv2.applyColorMap(phase_diff, cv2.COLORMAP_INFERNO)
    phase_diff_norm = phase_diff.astype(np.float32) / 255.0
    return score, diff_img, {'phase_diff': phase_diff_norm}

def create_gradient_red_boundaries(sample, gradient_data):
    gradient_diff = gradient_data['gradient_diff']
    threshold = np.percentile(gradient_diff, 70)
    diff_mask = (gradient_diff > threshold).astype(np.uint8) * 255
    kernel = np.ones((7, 7), np.uint8)
    diff_mask = cv2.morphologyEx(diff_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    diff_mask = cv2.morphologyEx(diff_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    diff_mask = cv2.dilate(diff_mask, np.ones((5, 5), np.uint8), iterations=2)
    
    contours, _ = cv2.findContours(diff_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sample_vis = composite_over_black(sample)
    sample_rgb = cv2.cvtColor(sample_vis, cv2.COLOR_BGR2RGB)
    if sample_rgb.shape[:2] != diff_mask.shape:
        sample_rgb = cv2.resize(sample_rgb, (diff_mask.shape[1], diff_mask.shape[0]))
    
    contoured = sample_rgb.copy()
    filled = sample_rgb.copy()
    
    sig_cnts = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
    cv2.drawContours(contoured, sig_cnts, -1, (255, 0, 0), thickness=4)
    for c in sig_cnts:
        m = np.zeros(diff_mask.shape, dtype=np.uint8)
        cv2.drawContours(m, [c], -1, 255, -1)
        filled[m == 255] = filled[m == 255] * 0.6 + np.array([255, 0, 0]) * 0.4
    cv2.drawContours(filled, sig_cnts, -1, (255, 0, 0), thickness=4)
    
    total = gradient_diff.size
    colored = np.count_nonzero(diff_mask)
    black = total - colored
    bin_coef = (100 - (colored/black)*100) if black > 0 else 0
    
    diff_norm = gradient_diff / (np.max(gradient_diff) + 1e-10)
    col_ints = diff_norm[diff_mask > 0]
    w_sum = np.sum(col_ints)
    wei_coef = (100 - (w_sum/black)*100) if black > 0 else 0
    
    return contoured, filled, bin_coef, wei_coef, len(sig_cnts)

def create_phase_red_boundaries(sample, phase_data):
    phase_diff = phase_data['phase_diff']
    # Same logic as gradient
    threshold = np.percentile(phase_diff, 70)
    diff_mask = (phase_diff > threshold).astype(np.uint8) * 255
    kernel = np.ones((7, 7), np.uint8)
    diff_mask = cv2.morphologyEx(diff_mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    diff_mask = cv2.morphologyEx(diff_mask, cv2.MORPH_OPEN, kernel, iterations=1)
    diff_mask = cv2.dilate(diff_mask, np.ones((5, 5), np.uint8), iterations=2)
    
    contours, _ = cv2.findContours(diff_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sample_vis = composite_over_black(sample)
    sample_rgb = cv2.cvtColor(sample_vis, cv2.COLOR_BGR2RGB)
    if sample_rgb.shape[:2] != diff_mask.shape:
        sample_rgb = cv2.resize(sample_rgb, (diff_mask.shape[1], diff_mask.shape[0]))
    
    contoured = sample_rgb.copy()
    filled = sample_rgb.copy()
    
    sig_cnts = [cnt for cnt in contours if cv2.contourArea(cnt) > 100]
    cv2.drawContours(contoured, sig_cnts, -1, (255, 0, 0), thickness=4)
    for c in sig_cnts:
        m = np.zeros(diff_mask.shape, dtype=np.uint8)
        cv2.drawContours(m, [c], -1, 255, -1)
        filled[m == 255] = filled[m == 255] * 0.6 + np.array([255, 0, 0]) * 0.4
    cv2.drawContours(filled, sig_cnts, -1, (255, 0, 0), thickness=4)
    
    total = phase_diff.size
    colored = np.count_nonzero(diff_mask)
    black = total - colored
    bin_coef = (100 - (colored/black)*100) if black > 0 else 0
    
    diff_norm = phase_diff / (np.max(phase_diff) + 1e-10)
    col_ints = diff_norm[diff_mask > 0]
    w_sum = np.sum(col_ints)
    wei_coef = (100 - (w_sum/black)*100) if black > 0 else 0
    
    return contoured, filled, bin_coef, wei_coef, len(sig_cnts)

def determine_status(value, pass_t, cond_t, lower_is_better=False):
    if lower_is_better:
        if value < pass_t: return "PASS"
        elif value <= cond_t: return "CONDITIONAL"
        else: return "FAIL"
    else:
        if value >= pass_t: return "PASS"
        elif value >= cond_t: return "CONDITIONAL"
        else: return "FAIL"

# =================================================================================================
# FOURIER DOMAIN ANALYSIS
# =================================================================================================

def fourier_domain_analysis(img_bgr):
    """
    Perform 2D FFT analysis on a single image.
    Returns dict with spectrum plot data, peaks table, and metrics.
    """
    gray = cv2.cvtColor(composite_over_black(img_bgr), cv2.COLOR_BGR2GRAY).astype(np.float64)
    h, w = gray.shape

    # 2D FFT
    f_transform = np.fft.fft2(gray)
    f_shift = np.fft.fftshift(f_transform)
    magnitude = np.abs(f_shift)
    log_mag = np.log1p(magnitude)

    cy, cx = h // 2, w // 2

    # Find top peaks (exclude DC component)
    mag_copy = magnitude.copy()
    mag_copy[cy-2:cy+3, cx-2:cx+3] = 0  # zero out DC neighborhood

    num_peaks = 5
    peaks = []
    for _ in range(num_peaks):
        idx = np.unravel_index(np.argmax(mag_copy), mag_copy.shape)
        py, px = idx
        peak_mag = mag_copy[py, px]
        if peak_mag < 1e-6:
            break
        radius = math.sqrt((px - cx)**2 + (py - cy)**2)
        angle = math.degrees(math.atan2(-(py - cy), px - cx))
        peaks.append({
            'radius': radius,
            'angle': angle,
            'magnitude': peak_mag,
            'px': int(px),
            'py': int(py)
        })
        # Suppress neighborhood to find next distinct peak
        r_suppress = max(3, int(radius * 0.15))
        y_lo = max(0, py - r_suppress)
        y_hi = min(h, py + r_suppress + 1)
        x_lo = max(0, px - r_suppress)
        x_hi = min(w, px + r_suppress + 1)
        mag_copy[y_lo:y_hi, x_lo:x_hi] = 0

    # Metrics
    if len(peaks) >= 1:
        dominant_peak = peaks[0]
        fundamental_period = (1.0 / (dominant_peak['radius'] / max(h, w))) if dominant_peak['radius'] > 0 else 0.0
        dominant_orientation = dominant_peak['angle']
    else:
        fundamental_period = 0.0
        dominant_orientation = 0.0

    # Anisotropy: ratio of max to min spread in frequency domain
    if len(peaks) >= 2:
        radii = [p['radius'] for p in peaks if p['radius'] > 0]
        if len(radii) >= 2:
            anisotropy = max(radii) / min(radii)
        else:
            anisotropy = 1.0
    else:
        anisotropy = 1.0

    return {
        'log_magnitude': log_mag,
        'peaks': peaks,
        'fundamental_period': fundamental_period,
        'dominant_orientation': dominant_orientation,
        'anisotropy': anisotropy,
        'center': (cx, cy),
        'shape': (h, w)
    }


def plot_fft_spectrum(fda_result, out_path, title='2D FFT Power Spectrum'):
    """Plot the 2D FFT power spectrum with peak markers."""
    log_mag = fda_result['log_magnitude']
    peaks = fda_result['peaks']
    cx, cy = fda_result['center']

    fig, ax = plt.subplots(figsize=(6.5, 5))
    im = ax.imshow(log_mag, cmap='hot', aspect='auto')
    cbar = fig.colorbar(im, ax=ax, shrink=0.85)
    cbar.set_label('Log Magnitude', fontsize=9)

    # Mark peaks
    for i, p in enumerate(peaks):
        ax.plot(p['px'], p['py'], 'g^', markersize=8, markeredgecolor='white', markeredgewidth=0.5)
        ax.annotate(f"P{i+1}", (p['px'], p['py']), textcoords="offset points",
                    xytext=(5, -8), fontsize=7, color='lime', fontweight='bold')

    ax.set_xlabel('Frequency X', fontsize=9)
    ax.set_ylabel('Frequency Y', fontsize=9)
    ax.set_title(title, fontsize=11, fontweight='bold')
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches='tight')
    plt.close(fig)


# =================================================================================================
# GLCM TEXTURE ANALYSIS
# =================================================================================================

def glcm_texture_analysis(img_bgr):
    """
    Compute GLCM texture properties for a single image.
    Returns dict with property values and the GLCM matrix.
    """
    gray = cv2.cvtColor(composite_over_black(img_bgr), cv2.COLOR_BGR2GRAY)
    # Quantize to fewer levels for meaningful GLCM
    gray_q = (gray // 4).astype(np.uint8)  # 64 levels
    
    # Compute GLCM at multiple angles, distance=1
    distances = [1]
    angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]
    glcm = graycomatrix(gray_q, distances=distances, angles=angles, levels=64, symmetric=True, normed=True)
    
    # Extract properties (mean across all angles)
    props = {}
    for prop_name in ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']:
        vals = graycoprops(glcm, prop_name)
        props[prop_name] = float(np.mean(vals))
    
    return {
        'properties': props,
        'glcm_matrix': glcm[:, :, 0, 0],  # First distance, first angle for visualization
    }


def plot_glcm_comparison(ref_props, sam_props, out_path, tr=None):
    """Plot grouped bar chart comparing GLCM properties between reference and sample."""
    if tr is None:
        tr = lambda k, d=None: (d if d else k.replace('_', ' ').title())
    
    prop_keys = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']
    prop_labels = [tr(f'glcm_{k.lower()}') for k in prop_keys]
    
    ref_vals = [ref_props['properties'][k] for k in prop_keys]
    sam_vals = [sam_props['properties'][k] for k in prop_keys]
    
    x = np.arange(len(prop_keys))
    w = 0.32
    
    fig, ax = plt.subplots(figsize=(8, 4))
    bars1 = ax.bar(x - w/2, ref_vals, w, label='Reference', color='#2980B9', edgecolor='white', linewidth=0.5)
    bars2 = ax.bar(x + w/2, sam_vals, w, label='Sample', color='#E74C3C', edgecolor='white', linewidth=0.5)
    
    ax.set_xticks(x)
    ax.set_xticklabels(prop_labels, fontsize=8, rotation=15, ha='right')
    ax.set_title('GLCM Property Comparison', fontsize=11, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.15, axis='y')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            ax.annotate(f'{h:.3f}', xy=(bar.get_x() + bar.get_width()/2, h),
                       xytext=(0, 3), textcoords='offset points', ha='center', fontsize=6.5)
    
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches='tight')
    plt.close(fig)


def plot_glcm_heatmaps(ref_glcm_matrix, sam_glcm_matrix, out_path):
    """Plot side-by-side GLCM matrix heatmaps for reference and sample."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
    
    im1 = ax1.imshow(ref_glcm_matrix, cmap='hot', aspect='auto')
    ax1.set_title('Reference GLCM', fontsize=10, fontweight='bold')
    ax1.set_xlabel('Gray Level j', fontsize=8)
    ax1.set_ylabel('Gray Level i', fontsize=8)
    fig.colorbar(im1, ax=ax1, shrink=0.8)
    
    im2 = ax2.imshow(sam_glcm_matrix, cmap='hot', aspect='auto')
    ax2.set_title('Sample GLCM', fontsize=10, fontweight='bold')
    ax2.set_xlabel('Gray Level j', fontsize=8)
    ax2.set_ylabel('Gray Level i', fontsize=8)
    fig.colorbar(im2, ax=ax2, shrink=0.8)
    
    fig.tight_layout()
    fig.savefig(out_path, dpi=180, bbox_inches='tight')
    plt.close(fig)


# =================================================================================================
# PDF GENERATION
# =================================================================================================

def structural_difference_analysis(ref, sample):
    # Prepare images (Grayscale -> Resize -> CLAHE)
    h_target = min(ref.shape[0], sample.shape[0])
    w_target = min(ref.shape[1], sample.shape[1])
    
    # Resize to match smaller dimension (or reference? safely use min)
    img1 = cv2.resize(ref, (w_target, h_target))
    img2 = cv2.resize(sample, (w_target, h_target))
    
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    normalized1 = clahe.apply(gray1)
    normalized2 = clahe.apply(gray2)
    
    # 1. Simple Difference
    diff_normalized = cv2.absdiff(normalized1, normalized2)
    _, thresh_normalized = cv2.threshold(diff_normalized, 30, 255, cv2.THRESH_BINARY)
    kernel = np.ones((3, 3), np.uint8)
    cleaned_normalized = cv2.morphologyEx(thresh_normalized, cv2.MORPH_OPEN, kernel)
    cleaned_normalized = cv2.morphologyEx(cleaned_normalized, cv2.MORPH_CLOSE, kernel)
    
    # 2. Edge-based
    edges1 = cv2.Canny(normalized1, 50, 150)
    edges2 = cv2.Canny(normalized2, 50, 150)
    edge_diff = cv2.absdiff(edges1, edges2)
    edge_diff_dilated = cv2.dilate(edge_diff, kernel, iterations=2)
    
    # 3. Gradient
    sobelx1 = cv2.Sobel(normalized1, cv2.CV_64F, 1, 0, ksize=3)
    sobely1 = cv2.Sobel(normalized1, cv2.CV_64F, 0, 1, ksize=3)
    gradient1 = np.sqrt(sobelx1**2 + sobely1**2)
    
    sobelx2 = cv2.Sobel(normalized2, cv2.CV_64F, 1, 0, ksize=3)
    sobely2 = cv2.Sobel(normalized2, cv2.CV_64F, 0, 1, ksize=3)
    gradient2 = np.sqrt(sobelx2**2 + sobely2**2)
    
    gradient1 = cv2.normalize(gradient1, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    gradient2 = cv2.normalize(gradient2, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    
    gradient_diff = cv2.absdiff(gradient1, gradient2)
    _, gradient_thresh = cv2.threshold(gradient_diff, 40, 255, cv2.THRESH_BINARY)
    gradient_cleaned = cv2.morphologyEx(gradient_thresh, cv2.MORPH_OPEN, kernel)
    gradient_cleaned = cv2.morphologyEx(gradient_cleaned, cv2.MORPH_CLOSE, kernel)
    
    # 4. Frequency
    f1 = np.fft.fft2(normalized1)
    f2 = np.fft.fft2(normalized2)
    magnitude1 = np.abs(f1)
    magnitude2 = np.abs(f2)
    freq_diff = np.abs(magnitude1 - magnitude2)
    freq_diff_spatial = np.abs(np.fft.ifft2(freq_diff))
    freq_diff_spatial = cv2.normalize(freq_diff_spatial, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
    _, freq_thresh = cv2.threshold(freq_diff_spatial, 30, 255, cv2.THRESH_BINARY)
    freq_cleaned = cv2.morphologyEx(freq_thresh, cv2.MORPH_OPEN, kernel)
    
    # 5. SSIM
    _, ssim_diff = ssim(normalized1, normalized2, full=True)
    ssim_diff = (ssim_diff * 255).astype(np.uint8)
    # ssim_diff is similarity map, we want difference
    ssim_diff_inv = 255 - ssim_diff
    _, ssim_thresh = cv2.threshold(ssim_diff_inv, 200, 255, cv2.THRESH_BINARY)
    ssim_cleaned = cv2.morphologyEx(ssim_thresh, cv2.MORPH_OPEN, kernel)
    ssim_cleaned = cv2.morphologyEx(ssim_cleaned, cv2.MORPH_CLOSE, kernel)
    
    # 6. Combined Fusion
    # All inputs should be uint8 0-255.
    combined = (
        cleaned_normalized.astype(float) * 0.25 +
        edge_diff_dilated.astype(float) * 0.20 +
        gradient_cleaned.astype(float) * 0.25 +
        freq_cleaned.astype(float) * 0.15 +
        ssim_cleaned.astype(float) * 0.15
    )
    combined = combined.astype(np.uint8)
    _, combined_thresh = cv2.threshold(combined, 100, 255, cv2.THRESH_BINARY)
    
    kernel_large = np.ones((5, 5), np.uint8)
    combined_final = cv2.morphologyEx(combined_thresh, cv2.MORPH_OPEN, kernel_large)
    combined_final = cv2.morphologyEx(combined_final, cv2.MORPH_CLOSE, kernel_large)
    
    # 7. Noise Filtered
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(combined_final, connectivity=8)
    min_size = 50
    combined_filtered = np.zeros_like(combined_final)
    for i in range(1, num_labels):
        if stats[i, cv2.CC_STAT_AREA] >= min_size:
            combined_filtered[labels == i] = 255
            
    # 8. Pure Differences only (Red overlay)
    img1_color = cv2.cvtColor(gray1, cv2.COLOR_GRAY2BGR)
    diff_only = np.zeros_like(img1_color)
    diff_only[combined_filtered > 0] = [0, 0, 255] # Red BGR
    # Optional: Composite over original? User said "Pure Differences only" and showed red on black in code
    # Code: diff_only = np.zeros_like... diff_only[...] = Red. So background is black.
    
    # 9. Visualization Compilations
    # Subplot: Gradient, Combined, Noise Filtered
    fig1, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    axes[0].imshow(gradient_cleaned, cmap='hot')
    axes[0].set_title('Gradient Magnitude Diff', fontsize=14, fontweight='bold')
    axes[0].axis('off')

    axes[1].imshow(combined_final, cmap='hot')
    axes[1].set_title('Combined (All Methods)', fontsize=14, fontweight='bold')
    axes[1].axis('off')

    axes[2].imshow(combined_filtered, cmap='hot')
    axes[2].set_title('Noise Filtered', fontsize=14, fontweight='bold')
    axes[2].axis('off')
    
    plt.tight_layout()
    
    # Save subplot to buffer
    buf_subplot = io.BytesIO()
    plt.savefig(buf_subplot, format='png', bbox_inches='tight', dpi=150)
    buf_subplot.seek(0)
    subplot_raw = buf_subplot.read()
    buf_subplot.seek(0)
    plt.close(fig1)
    
    # Prepare Pure Diff Image (using matplotlib or direct?)
    # User code used plt for "Pure Differences Only" to add title. We can do that or just layout in ReportLab.
    # Using PLT ensures consistency with user request "place large image... with title"
    fig2, ax = plt.subplots(1, 1, figsize=(10, 8))
    ax.imshow(cv2.cvtColor(diff_only, cv2.COLOR_BGR2RGB))
    # ax.set_title('Pure Differences Only', fontsize=16, fontweight='bold')
    ax.axis('off')
    plt.tight_layout()
    
    buf_diff = io.BytesIO()
    plt.savefig(buf_diff, format='png', bbox_inches='tight', dpi=150)
    buf_diff.seek(0)
    diff_raw = buf_diff.read()
    buf_diff.seek(0)
    plt.close(fig2)
    
    # Metrics
    total_pixels = gray1.shape[0] * gray1.shape[1]
    changed_pixels = np.sum(combined_filtered > 0)
    change_percentage = (changed_pixels / total_pixels) * 100
    
    # User Request: Score must be 100 - current value (Closer to 100 is better)
    similarity_score = max(0, 100 - change_percentage)
    
    if similarity_score >= 99.9:
        verdict = "IDENTICAL"
        v_color = GREEN
    elif similarity_score >= 99.0:
        verdict = "VERY SIMILAR"
        v_color = ORANGE
    elif similarity_score >= 95.0:
        verdict = "SIMILAR"
        v_color = ORANGE
    else:
        verdict = "DIFFERENT"
        v_color = RED
        
    return {
        'subplot_img': RLImage(buf_subplot, width=7.0*inch, height=2.3*inch), # Aspect ratio approx 18:6 = 3:1
        'diff_img': RLImage(buf_diff, width=5.0*inch, height=4.0*inch), # Slightly smaller (was 6.0x4.8)
        'subplot_raw': subplot_raw,
        'diff_raw': diff_raw,
        'total_pixels': total_pixels,
        'changed_pixels': changed_pixels,
        'change_percentage': change_percentage,
        'similarity_score': similarity_score,
        'verdict': verdict,
        'verdict_color': v_color
    }


def generate_pdf_headless(ref_img, sample_img, scores, diff_images, composite_score, 
                          gradient_results, phase_results, output_path, config=None, report_id=None, timestamp=None,
                          structural_results=None, fourier_results=None, glcm_results=None, is_combined=False):
    cfg = config or DEFAULT_CONFIG
    sections = cfg.get('sections', {})
    operator = cfg.get('operator', 'Unknown')
    tz_offset = cfg.get('timezone_offset', 3)
    primary_ill = cfg.get('primary_illuminant', 'D65')
    
    # Get report language and translator
    report_lang = cfg.get('report_lang', 'en')
    tr = get_translator(report_lang)
    
    ts = timestamp if timestamp else get_local_time(tz_offset)
    analysis_id = report_id if report_id else f"PAT_{ts.strftime('%y%m%d_%H%M%S')}"
    
    doc = SimpleDocTemplate(output_path, pagesize=A4, 
                            leftMargin=MARGIN_L, rightMargin=MARGIN_R, 
                            topMargin=MARGIN_T, bottomMargin=MARGIN_B)
    content = []
    
    global_thresh = float(cfg.get('global_threshold', 75.0))
    if composite_score >= global_thresh:
        final_status = "PASS"
    elif composite_score >= (global_thresh - 15): 
        final_status = "CONDITIONAL"
    else:
        final_status = "FAIL"
    
    # Cover
    content.append(Spacer(1, 0.5 * inch))
    logo_path = pick_logo()
    if logo_path:
        content.append(RLImage(logo_path, width=2.0*inch, height=2.0*inch))
        content.append(Spacer(1, 0.3*inch))
        
    content.append(Paragraph(tr('pattern_report_title'), StyleTitle))
    content.append(Spacer(1, 0.15*inch))
    content.append(Paragraph(tr('cover_company'), StyleH2))
    content.append(Spacer(1, 0.08*inch))
    
    subtitle_style = ParagraphStyle('ElegantSubtitle', parent=StyleSmall, fontSize=9, textColor=NEUTRAL, fontName=PDF_FONT_REGULAR, leading=12, alignment=TA_LEFT)
    content.append(Paragraph(f"<i>{tr('cover_subtitle')}</i>", subtitle_style))
    content.append(Spacer(1, 0.2*inch))
    content.append(badge(f"{tr('primary_illuminant')}: {primary_ill}", back_color=BLUE1))
    content.append(Spacer(1, 0.4*inch))
    
    meta_data = [
        [tr('details'), ""],
        [tr('generated_on'), ts.strftime("%Y-%m-%d %H:%M:%S")],
        [tr('operator'), operator],
        [tr('report_id'), analysis_id],
        [tr('software_version'), SOFTWARE_VERSION],
    ]
    meta_table = Table(meta_data, colWidths=[2*inch, 3*inch], hAlign="CENTER")
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NEUTRAL_L),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("FONTNAME", (0, 0), (-1, 0), PDF_FONT_BOLD),
        ("FONTNAME", (0, 1), (-1, -1), PDF_FONT_REGULAR),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.Color(0.8, 0.8, 0.8)),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 1), (-1, -1), 5),
        ("RIGHTPADDING", (0, 1), (-1, -1), 5),
        ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
        ("BACKGROUND", (0, 3), (-1, 3), colors.whitesmoke),
        ("BACKGROUND", (0, 5), (-1, 5), colors.whitesmoke),
    ]))
    content.append(meta_table)
    content.append(Spacer(1, 0.4*inch))
    
    # Exec Summary
    class ExecutiveSummaryHeader(Flowable):
        def __init__(self, status, width):
            super().__init__()
            self.status = status
            self.box_width = width
            self.box_height = 28
        def draw(self):
            if "CONDITIONAL" in self.status: color = ORANGE
            elif "FAIL" in self.status: color = RED
            else: color = GREEN
            self.canv.setFillColor(color)
            self.canv.rect(0, 0, self.box_width, self.box_height, fill=1, stroke=0)
            self.canv.setFillColor(colors.white)
            self.canv.setFont(PDF_FONT_BOLD, 12)
            exec_text = f"{tr('executive_summary')}: {translate_status(self.status, report_lang)}"
            self.canv.drawCentredString(self.box_width / 2, 9, exec_text)
        def wrap(self, availW, availH):
            return (self.box_width, self.box_height)
            
    page_width = A4[0] - MARGIN_L - MARGIN_R
    content.append(ExecutiveSummaryHeader(final_status, page_width))
    content.append(Spacer(1, 0.15*inch))
    
    weights = {'Structural SSIM': 25, 'Gradient Similarity': 25, 'Phase Correlation': 25, 'Structural Match': 25}
    metrics_data = [['Metric', tr('score') + ' (%)', 'Weight (%)', tr('status')]]
    for method, score in scores.items():
        thr_pass = float(cfg['thresholds'][method]['pass'])
        thr_cond = float(cfg['thresholds'][method]['conditional'])
        st = determine_status(score, thr_pass, thr_cond)
        metrics_data.append([method, f"{score:.1f}", str(weights.get(method, 0)), st])
    
    composite_label = 'Bileşik Skor' if report_lang == 'tr' else 'Composite Score'
    metrics_data.append([composite_label, f"{composite_score:.1f}", '100', translate_status(final_status, report_lang)])
    
    m_table = Table(metrics_data, colWidths=[2.2*inch, 1.0*inch, 1.0*inch, 1.0*inch], hAlign="LEFT")
    style_cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), BLUE2),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), PDF_FONT_BOLD),
        ("FONTSIZE", (0, 0), (-1, 0), 9),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("FONTNAME", (0, 1), (-1, -1), PDF_FONT_REGULAR),
        ("FONTSIZE", (0, 1), (-1, -1), 9),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.5, NEUTRAL_L),
        ("BACKGROUND", (0, -1), (-1, -1), colors.HexColor("#F0F0F0")),
        ("FONTNAME", (0, -1), (-1, -1), PDF_FONT_BOLD),
    ]
    for i, row in enumerate(metrics_data[1:], 1):
        if row[3] == "PASS": style_cmds.append(("TEXTCOLOR", (3, i), (3, i), GREEN))
        elif row[3] == "FAIL": style_cmds.append(("TEXTCOLOR", (3, i), (3, i), RED))
        else: style_cmds.append(("TEXTCOLOR", (3, i), (3, i), ORANGE))
        
    m_table.setStyle(TableStyle(style_cmds))
    content.append(m_table)
    content.append(PageBreak())

    # ── Large Pattern Section Title Banner (only in combined report) ──
    if is_combined:
        class PatternSectionBanner(Flowable):
            """Full-width prominent banner marking the start of the Pattern Analysis section."""
            def __init__(self, width, lang='en'):
                super().__init__()
                self.box_width = width
                self.box_height = 72
                self.lang = lang
            def draw(self):
                c = self.canv
                # Light background band
                c.setFillColor(colors.HexColor("#D6E4F0"))
                c.roundRect(0, 0, self.box_width, self.box_height, 6, fill=1, stroke=0)
                # Accent stripe at bottom
                c.setFillColor(BLUE1)
                c.rect(0, 0, self.box_width, 4, fill=1, stroke=0)
                # Main title
                title_text = "DESEN ANALİZİ BÖLÜMÜ" if self.lang == 'tr' else "PATTERN ANALYSIS SECTION"
                c.setFillColor(colors.HexColor("#2C3E50"))
                c.setFont(PDF_FONT_BOLD, 22)
                c.drawCentredString(self.box_width / 2, 38, title_text)
                # Subtitle
                sub_text = "Yapısal Benzerlik ve Doku Analizi" if self.lang == 'tr' else "Structural Similarity & Texture Analysis"
                c.setFillColor(colors.HexColor("#5A7A9B"))
                c.setFont(PDF_FONT_REGULAR, 11)
                c.drawCentredString(self.box_width / 2, 16, sub_text)
            def wrap(self, availW, availH):
                return (self.box_width, self.box_height)

        content.append(PatternSectionBanner(page_width, report_lang))
        content.append(Spacer(1, 0.35 * inch))

    # Images
    input_images_title = 'Girdi Görüntüleri' if report_lang == 'tr' else 'Input Images'
    img_data = [
        [numpy_to_rl(ref_img, 3.2*inch, 2.5*inch), numpy_to_rl(sample_img, 3.2*inch, 2.5*inch)],
        [Paragraph(f"<b>{tr('reference')}</b>", StyleSmall), Paragraph(f"<b>{tr('sample')}</b>", StyleSmall)]
    ]
    t_imgs = Table(img_data, colWidths=[3.5*inch, 3.5*inch])
    t_imgs.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    content.append(KeepTogether([
        Paragraph(input_images_title, StyleH1),
        Spacer(1, 0.2*inch),
        t_imgs,
        Spacer(1, 0.3*inch),
    ]))
    
    # Methods
    method_groups = [
        ['Structural SSIM'],
        ['Phase Correlation', 'Gradient Similarity']
    ]
    
    method_config_map = {'Structural SSIM': 'ssim', 'Gradient Similarity': 'gradient', 'Phase Correlation': 'phase', 'Structural Match': 'structural'}
    
    for group in method_groups:
        active = False
        for m in group:
            if m not in scores: continue
            if not sections.get(method_config_map[m], True): continue
            
            active = True
            score = scores[m]
            st = determine_status(score, float(cfg['thresholds'][m]['pass']), float(cfg['thresholds'][m]['conditional']))
            
            sim_score_label = 'Benzerlik Skoru' if report_lang == 'tr' else 'Similarity Score'
            diff_viz_title = 'Fark Görselleştirmesi' if report_lang == 'tr' else 'Difference Visualization'
            content.append(KeepTogether([
                Paragraph(m, StyleH1),
                Paragraph(f"<b>{sim_score_label}:</b> {score:.2f}%", StyleBody),
                badge(st, STATUS_COLORS.get(st, NEUTRAL)),
                Spacer(1, 0.1*inch),
                Paragraph(diff_viz_title, StyleH2),
                numpy_to_rl(diff_images[m], 4.5*inch, 2.5*inch),
                Spacer(1, 0.3*inch),
            ]))
            
        if active: content.append(PageBreak())

    # Boundaries
    bound_methods = []
    if sections.get('phase_boundary', True) and phase_results:
        bound_methods.append(('Phase Correlation', phase_results))
    if sections.get('gradient_boundary', True) and gradient_results:
        bound_methods.append(('Gradient Similarity', gradient_results))
        
    for idx, (name, res) in enumerate(bound_methods):
        cont, fill, b_coef, w_coef, _ = res
        bound_title = f"{name} - Sınır Algılama" if report_lang == 'tr' else f"{name} - Boundary Detection"
        
        img1 = numpy_to_rl(cont, 3.2*inch, 2.3*inch)
        img2 = numpy_to_rl(fill, 3.2*inch, 2.3*inch)
        
        contour_label = 'Kırmızı Kontur' if report_lang == 'tr' else 'Red Contour'
        filled_label = 'Doldurulmuş Bölge' if report_lang == 'tr' else 'Filled Region'
        it = Table([[Paragraph(contour_label, StyleSmall), Paragraph(filled_label, StyleSmall)], [img1, img2]], 
                   colWidths=[3.4*inch, 3.4*inch])
        it.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        
        det_metrics_title = 'Algılama Metrikleri' if report_lang == 'tr' else 'Detection Metrics'
        metric_label = 'Metrik' if report_lang == 'tr' else 'Metric'
        value_label = 'Değer' if report_lang == 'tr' else 'Value'
        bin_sim_label = 'İkili Benzerlik' if report_lang == 'tr' else 'Binary Similarity'
        weight_sim_label = 'Ağırlıklı Benzerlik' if report_lang == 'tr' else 'Weighted Similarity'
        met_t = Table([[metric_label, value_label], 
                       [bin_sim_label, f"{b_coef:.2f}%"], 
                       [weight_sim_label, f"{w_coef:.2f}%"]], 
                      colWidths=[2.5*inch, 2*inch], hAlign="CENTER")
        met_t.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), NEUTRAL_L),
            ("FONTNAME", (0,0), (-1,0), PDF_FONT_BOLD),
            ("FONTNAME", (0,1), (-1,-1), PDF_FONT_REGULAR),
            ("FONTSIZE", (0,0), (-1,-1), 9),
            ("GRID", (0,0), (-1,-1), 0.5, NEUTRAL_L)
        ]))
        content.append(KeepTogether([
            Paragraph(bound_title, StyleH1),
            it,
            Spacer(1, 0.2*inch),
            Paragraph(det_metrics_title, StyleH2),
            met_t,
        ]))
        content.append(Spacer(1, 0.3*inch))
        
    # Structural Difference Analysis
    if sections.get('structural', True) and structural_results:
        content.append(Spacer(1, 0.3 * inch))
        
        struct_diff_title = 'Yapısal Fark Analizi' if report_lang == 'tr' else 'Structural Difference Analysis'
        diff_viz_multi = 'Fark Görselleştirmesi (Çoklu Yöntem)' if report_lang == 'tr' else 'Difference Visualization (Multi-Method)'
        content.append(KeepTogether([
            Paragraph(struct_diff_title, StyleTitle),
            Spacer(1, 0.15 * inch),
            Paragraph(diff_viz_multi, StyleH1),
            structural_results['subplot_img'],
            Spacer(1, 0.15 * inch),
        ]))
        
        # Center the large image
        diff_tbl = Table([[structural_results['diff_img']]], colWidths=[6.2*inch])
        diff_tbl.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        content.append(diff_tbl)
        content.append(Spacer(1, 0.3 * inch))
        
        # Results Table
        verdict = structural_results['verdict']
        v_color = structural_results['verdict_color']
        
        # Add checkbox icon for verdict
        if verdict == "IDENTICAL": icon = "✓ "
        elif verdict == "DIFFERENT": icon = "✗ "
        else: icon = "≈ "
        
        res_data = [
            ['Metric', tr('value')],
            [tr('changed_pixels'), f"{structural_results['changed_pixels']:,}"],
            [tr('similarity_score'), f"{structural_results['similarity_score']:.2f}%"],
            [tr('result').upper(), f"{icon}{translate_status(verdict, report_lang)}"]
        ]
        
        res_table = Table(res_data, colWidths=[2.5*inch, 3.0*inch], hAlign="CENTER")
        res_style = [
            ("BACKGROUND", (0, 0), (-1, 0), BLUE2),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, -1), PDF_FONT_BOLD),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("GRID", (0, 0), (-1, -1), 0.5, NEUTRAL_L),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ("TEXTCOLOR", (1, 3), (1, 3), v_color), # Color the verdict
            ("FONTSIZE", (0, 0), (-1, -1), 10), # Reduced from 11
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ]
        res_table.setStyle(TableStyle(res_style))
        content.append(KeepTogether([
            Paragraph(tr('conclusion'), StyleH1),
            res_table,
        ]))
        
        
    # Fourier Domain Analysis (Sample Image)
    if sections.get('fourier', True) and fourier_results:
        content.append(Spacer(1, 0.3 * inch))

        # FFT Spectrum Image
        if fourier_results.get('spectrum_img_path') and os.path.exists(fourier_results['spectrum_img_path']):
            content.append(KeepTogether([
                Paragraph(tr('fourier_title'), StyleTitle),
                Spacer(1, 0.1 * inch),
                Paragraph(f"<i>{tr('fourier_subtitle')}</i>", StyleSmall),
                Spacer(1, 0.15 * inch),
                Paragraph(tr('fft_spectrum_title'), StyleH1),
                RLImage(fourier_results['spectrum_img_path'], 5.0*inch, 3.8*inch),
                Spacer(1, 0.15 * inch),
            ]))
        else:
            content.append(KeepTogether([
                Paragraph(tr('fourier_title'), StyleTitle),
                Spacer(1, 0.1 * inch),
                Paragraph(f"<i>{tr('fourier_subtitle')}</i>", StyleSmall),
                Spacer(1, 0.15 * inch),
            ]))

        # Peaks Table
        fda_peaks = fourier_results.get('peaks', [])
        if fda_peaks:
            peak_header = [tr('peak'), tr('radius'), tr('angle_deg'), tr('magnitude')]
            peak_data = [peak_header]
            for i, p in enumerate(fda_peaks):
                peak_data.append([f"P{i+1}", f"{p['radius']:.2f}", f"{p['angle']:.2f}", f"{p['magnitude']:.2f}"])
            t_peaks = Table(peak_data, colWidths=[1.0*inch, 1.5*inch, 1.5*inch, 1.5*inch], hAlign="LEFT")
            t_peaks.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), BLUE2),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), PDF_FONT_BOLD),
                ("FONTNAME", (0, 1), (-1, -1), PDF_FONT_REGULAR),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, NEUTRAL_L),
                ("ALIGN", (1, 0), (-1, -1), "CENTER"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
            ]))
            content.append(KeepTogether([
                Paragraph(tr('fourier_peaks_title'), StyleH1),
                t_peaks,
                Spacer(1, 0.2 * inch),
            ]))

        # Metrics Table (Reference vs Sample for dual, just Sample for single)
        fda_ref = fourier_results.get('ref', None)
        fda_sam = fourier_results.get('sample', fourier_results)
        if fda_ref:
            met_header = [tr('metric'), tr('reference'), tr('sample')]
            met_data = [met_header,
                [tr('fundamental_period'), f"{fda_ref['fundamental_period']:.2f}", f"{fda_sam['fundamental_period']:.2f}"],
                [tr('dominant_orientation'), f"{fda_ref['dominant_orientation']:.2f}", f"{fda_sam['dominant_orientation']:.2f}"],
                [tr('anisotropy_ratio'), f"{fda_ref['anisotropy']:.2f}", f"{fda_sam['anisotropy']:.2f}"],
            ]
            met_widths = [2.5*inch, 1.5*inch, 1.5*inch]
        else:
            met_header = [tr('metric'), tr('value')]
            met_data = [met_header,
                [tr('fundamental_period'), f"{fda_sam['fundamental_period']:.2f}"],
                [tr('dominant_orientation'), f"{fda_sam['dominant_orientation']:.2f}"],
                [tr('anisotropy_ratio'), f"{fda_sam['anisotropy']:.2f}"],
            ]
            met_widths = [2.5*inch, 2.0*inch]
        t_met = Table(met_data, colWidths=met_widths, hAlign="LEFT")
        t_met.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE2),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), PDF_FONT_BOLD),
            ("FONTNAME", (0, 1), (-1, -1), PDF_FONT_REGULAR),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, NEUTRAL_L),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ]))
        content.append(KeepTogether([
            Paragraph(tr('fourier_metrics_title'), StyleH1),
            t_met,
        ]))

    # GLCM Texture Analysis
    if sections.get('glcm', False) and glcm_results:
        content.append(Spacer(1, 0.3 * inch))

        # GLCM Property Comparison Table
        ref_glcm = glcm_results.get('ref', {})
        sam_glcm = glcm_results.get('sample', {})
        ref_props = ref_glcm.get('properties', {})
        sam_props = sam_glcm.get('properties', {})

        prop_keys = ['contrast', 'dissimilarity', 'homogeneity', 'energy', 'correlation', 'ASM']
        prop_header = [tr('glcm_property'), tr('reference'), tr('sample')]
        prop_data = [prop_header]
        for pk in prop_keys:
            prop_data.append([tr(f'glcm_{pk.lower()}'), f"{ref_props.get(pk, 0):.4f}", f"{sam_props.get(pk, 0):.4f}"])

        t_glcm = Table(prop_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch], hAlign="LEFT")
        t_glcm.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), BLUE2),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), PDF_FONT_BOLD),
            ("FONTNAME", (0, 1), (-1, -1), PDF_FONT_REGULAR),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("GRID", (0, 0), (-1, -1), 0.5, NEUTRAL_L),
            ("ALIGN", (1, 0), (-1, -1), "CENTER"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
        ]))
        content.append(KeepTogether([
            Paragraph(tr('glcm_title'), StyleTitle),
            Spacer(1, 0.1 * inch),
            Paragraph(f"<i>{tr('glcm_subtitle')}</i>", StyleSmall),
            Spacer(1, 0.15 * inch),
            Paragraph(tr('glcm_comparison_title'), StyleH1),
            t_glcm,
            Spacer(1, 0.15 * inch),
        ]))

        # GLCM Bar Chart
        if glcm_results.get('comparison_img_path') and os.path.exists(glcm_results['comparison_img_path']):
            content.append(RLImage(glcm_results['comparison_img_path'], 5.5*inch, 2.8*inch))
            content.append(Spacer(1, 0.2 * inch))

        # GLCM Heatmaps
        if glcm_results.get('heatmap_img_path') and os.path.exists(glcm_results['heatmap_img_path']):
            content.append(KeepTogether([
                Paragraph(tr('glcm_heatmap_title'), StyleH1),
                RLImage(glcm_results['heatmap_img_path'], 6.0*inch, 2.5*inch),
                Spacer(1, 0.15 * inch),
            ]))

        content.append(Paragraph(f"<i>{tr('glcm_interpretation')}</i>", StyleSmall))

    # Analysis Insights & Recommendations (via RecommendationsEngine)
    if sections.get('recommendations_pattern', True):
        from modules.RecommendationsEngine import generate_pattern_recommendations, render_findings_to_flowables

        content.append(Spacer(1, 0.3 * inch))

        global_thr = float(cfg.get('global_threshold', cfg.get('global_pattern_threshold', 75.0)))
        method_thresholds = cfg.get('thresholds', {})

        findings, conclusion_text, conclusion_status = generate_pattern_recommendations(
            composite_score=composite_score,
            scores=scores,
            structural_results=structural_results,
            global_threshold=global_thr,
            thresholds=method_thresholds,
            lang=report_lang
        )

        rec_title = 'Temel Bulgular ve Öneriler' if report_lang == 'tr' else 'Key Findings & Recommendations'
        rec_flowables = render_findings_to_flowables(
            findings, conclusion_text, conclusion_status, rec_title, lang=report_lang
        )
        content.extend(rec_flowables)

    doc.build(content, onFirstPage=make_header_footer(ts, analysis_id, report_lang), onLaterPages=make_header_footer(ts, analysis_id, report_lang))

# =================================================================================================
# MAIN PIPELINE
# =================================================================================================

def analyze_and_generate(ref_img, sample_img, config, output_path, report_id=None, timestamp=None, is_combined=False):
    cfg = config or DEFAULT_CONFIG
    sections = cfg.get('sections', {})
    
    scores = {}
    diff_images = {}
    active_count = 0
    grad_res = None
    phase_res = None
    
    # Dependency Logic:
    # Analysis must run if the section is enabled OR if dependent sections (Recommendations, Conclusion, Summary) need the data.
    any_deps_enabled = sections.get('recommendations_pattern', True) or sections.get('conclusion', True) or sections.get('summary', True)

    # 1. SSIM
    # Run if section is enabled OR if dependencies need scores
    if sections.get('ssim', True) or any_deps_enabled:
        sc, di = method1_structural_ssim(ref_img, sample_img)
        scores['Structural SSIM'] = sc
        diff_images['Structural SSIM'] = di
        if sections.get('enable_ssim', True) or True: # It always counts towards composite if calculated
            active_count += 1
        
    # 2. Gradient
    if sections.get('gradient', True) or sections.get('gradient_boundary', True) or any_deps_enabled:
        sc, di, data = method3_gradient_similarity(ref_img, sample_img)
        grad_res = create_gradient_red_boundaries(sample_img, data) # Always needed if ran? Used in PDF generation.
        # Store score if gradient specifically or dependants
        if sections.get('gradient', True) or any_deps_enabled:
            scores['Gradient Similarity'] = sc
            diff_images['Gradient Similarity'] = di
            active_count += 1
            
    # 3. Phase
    if sections.get('phase', True) or sections.get('phase_boundary', True) or any_deps_enabled:
        sc, di, data = method6_phase_correlation(ref_img, sample_img)
        phase_res = create_phase_red_boundaries(sample_img, data)
        if sections.get('phase', True) or any_deps_enabled:
            scores['Phase Correlation'] = sc
            diff_images['Phase Correlation'] = di
            active_count += 1
            
    # 4. Structural Difference (Configurable)
    structural_results = None
    if sections.get('structural', True) or sections.get('recommendations_pattern', True) or any_deps_enabled:
        try:
            structural_results = structural_difference_analysis(ref_img, sample_img)
            scores['Structural Match'] = structural_results['similarity_score']
            active_count += 1
        except Exception as e:
            print(f"Error in structural difference analysis: {e}")
            import traceback
            traceback.print_exc()

            
    # 5. Fourier Domain Analysis
    fourier_results = None
    if sections.get('fourier', True):
        try:
            import tempfile as _tmpmod
            _fda_tmp = _tmpmod.mkdtemp()
            fda_sam = fourier_domain_analysis(sample_img)
            fda_ref = fourier_domain_analysis(ref_img)
            spectrum_path = os.path.join(_fda_tmp, "fft_spectrum.png")
            plot_fft_spectrum(fda_sam, spectrum_path)
            fourier_results = {
                'spectrum_img_path': spectrum_path,
                'peaks': fda_sam['peaks'],
                'sample': fda_sam,
                'ref': fda_ref,
                'fundamental_period': fda_sam['fundamental_period'],
                'dominant_orientation': fda_sam['dominant_orientation'],
                'anisotropy': fda_sam['anisotropy'],
            }
        except Exception as e:
            print(f"Error in Fourier domain analysis: {e}")
            import traceback
            traceback.print_exc()

    # 6. GLCM Texture Analysis
    glcm_results = None
    if sections.get('glcm', False):
        try:
            import tempfile as _tmpmod
            _glcm_tmp = _tmpmod.mkdtemp()
            ref_glcm = glcm_texture_analysis(ref_img)
            sam_glcm = glcm_texture_analysis(sample_img)
            
            report_lang = cfg.get('report_lang', 'en')
            tr = get_translator(report_lang)
            
            comparison_path = os.path.join(_glcm_tmp, "glcm_comparison.png")
            plot_glcm_comparison(ref_glcm, sam_glcm, comparison_path, tr=tr)
            
            heatmap_path = os.path.join(_glcm_tmp, "glcm_heatmap.png")
            plot_glcm_heatmaps(ref_glcm['glcm_matrix'], sam_glcm['glcm_matrix'], heatmap_path)
            
            glcm_results = {
                'ref': ref_glcm,
                'sample': sam_glcm,
                'comparison_img_path': comparison_path,
                'heatmap_img_path': heatmap_path,
            }
        except Exception as e:
            print(f"Error in GLCM texture analysis: {e}")
            import traceback
            traceback.print_exc()

    # Composite
    weights = {'Structural SSIM': 0.25, 'Gradient Similarity': 0.25, 'Phase Correlation': 0.25, 'Structural Match': 0.25}
    composite = sum(scores.get(k, 0) * weights.get(k, 0.25) for k in scores) if active_count > 0 else 0
    
    generate_pdf_headless(ref_img, sample_img, scores, diff_images, composite, grad_res, phase_res, output_path, cfg, 
                          report_id=report_id, timestamp=timestamp, structural_results=structural_results,
                          fourier_results=fourier_results, glcm_results=glcm_results, is_combined=is_combined)
    
    results = {
        'scores': scores,
        'composite_score': composite,
        'final_status': 'PASS' if composite >= cfg.get('global_threshold', 75.0) else ('CONDITIONAL' if composite >= (cfg.get('global_threshold', 75.0) - 15) else 'FAIL'),
        'diff_images': diff_images,
        'grad_boundary': grad_res,
        'phase_boundary': phase_res,
        'structural_results': structural_results,
        'fourier_results': fourier_results,
        'glcm_results': glcm_results,
    }
    return output_path, results

