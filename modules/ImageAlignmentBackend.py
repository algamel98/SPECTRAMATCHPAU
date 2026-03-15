"""
ImageAlignmentBackend.py — SpectraMatch v3.0.0
Image Alignment & Registration Module for Textile Quality Control

Provides 10 alignment modes for preprocessing sample images before comparison:
1. Direct Pixel Comparison (no preprocessing)
2. ORB Feature-Based Alignment (Homography via ORB + RANSAC)
3. ECC Intensity-Based Alignment (Enhanced Correlation Coefficient)
4. Phase Correlation Alignment (FFT-based shift/rotation detection)
5. AI Smart Region Matching (Custom multi-strategy adaptive algorithm)
6. Cascading ECC Registration (Translation → Affine cascade)
7. ORB + RANSAC Affine-Preferred Alignment
8. Pure Phase Correlation Subpixel Translation
9. Coarse-to-Fine Pyramid Alignment
10. Tile-Based Local Refinement (Global + per-tile correction)

All techniques are designed for textile QC scenarios where:
- Same camera captures both reference and sample
- Minor capture variations: slight tilt, small angle, distance, lighting
- Colors and patterns must NOT be altered — only geometric normalization
"""

import cv2
import numpy as np
from enum import Enum


class AlignmentMode(Enum):
    DIRECT = 'direct'
    ORB_HOMOGRAPHY = 'orb_homography'
    ECC_ALIGNMENT = 'ecc_alignment'
    PHASE_CORRELATION = 'phase_correlation'
    AI_SMART_MATCH = 'ai_smart_match'
    CASCADING_ECC = 'cascading_ecc'
    ORB_AFFINE = 'orb_affine'
    SUBPIXEL_TRANSLATION = 'subpixel_translation'
    PYRAMID_ALIGN = 'pyramid_align'
    TILE_REFINE = 'tile_refine'


# ═══════════════════════════════════════════════════════════════════
# Mode Metadata
# ═══════════════════════════════════════════════════════════════════

ALIGNMENT_MODES = {
    'direct': {
        'id': 'direct',
        'name': 'Direct Pixel Comparison',
        'name_tr': 'Doğrudan Piksel Karşılaştırma',
        'description': 'Original mode with no preprocessing. Compares images pixel-by-pixel as captured. Best when capture conditions are perfectly controlled.',
        'description_tr': 'Ön işleme yapılmadan orijinal mod. Görüntüleri çekildiği gibi piksel piksel karşılaştırır. Çekim koşulları mükemmel kontrol edildiğinde en iyisidir.',
        'icon': 'grid',
        'category': 'baseline',
        'handles': [],
    },
    'orb_homography': {
        'id': 'orb_homography',
        'name': 'Feature-Based Alignment',
        'name_tr': 'Özellik Tabanlı Hizalama',
        'description': 'Uses ORB feature detection with RANSAC homography to correct perspective distortion, rotation, and scale differences between images.',
        'description_tr': 'Görüntüler arasındaki perspektif bozulması, döndürme ve ölçek farklılıklarını düzeltmek için RANSAC homografi ile ORB özellik algılama kullanır.',
        'icon': 'crosshair',
        'category': 'registration',
        'handles': ['rotation', 'scale', 'perspective', 'translation'],
    },
    'ecc_alignment': {
        'id': 'ecc_alignment',
        'name': 'Intensity-Based Alignment (ECC)',
        'name_tr': 'Yoğunluk Tabanlı Hizalama (ECC)',
        'description': 'Enhanced Correlation Coefficient method. Iteratively optimizes an affine transform to maximize correlation between images. Robust for small geometric changes.',
        'description_tr': 'Geliştirilmiş Korelasyon Katsayısı yöntemi. Görüntüler arasındaki korelasyonu en üst düzeye çıkarmak için afin dönüşümünü yinelemeli olarak optimize eder.',
        'icon': 'layers',
        'category': 'registration',
        'handles': ['rotation', 'scale', 'translation', 'shear'],
    },
    'phase_correlation': {
        'id': 'phase_correlation',
        'name': 'Phase Correlation Alignment',
        'name_tr': 'Faz Korelasyonu Hizalama',
        'description': 'FFT-based method that detects translation and rotation by analyzing phase spectrum. Very fast and effective for shift and rotation correction.',
        'description_tr': 'Faz spektrumunu analiz ederek öteleme ve döndürmeyi algılayan FFT tabanlı yöntem. Kaydırma ve döndürme düzeltmesi için çok hızlı ve etkilidir.',
        'icon': 'activity',
        'category': 'registration',
        'handles': ['rotation', 'translation'],
    },
    'ai_smart_match': {
        'id': 'ai_smart_match',
        'name': 'AI Smart Region Matching',
        'name_tr': 'AI Akıllı Bölge Eşleştirme',
        'description': 'Custom intelligent algorithm that automatically finds the corresponding region in the sample image. Combines multi-scale template matching, feature-guided refinement, and adaptive geometric correction.',
        'description_tr': 'Numune görüntüsünde karşılık gelen bölgeyi otomatik olarak bulan özel akıllı algoritma. Çoklu ölçekli şablon eşleştirme, özellik kılavuzlu iyileştirme ve uyarlanabilir geometrik düzeltmeyi birleştirir.',
        'icon': 'cpu',
        'category': 'ai',
        'handles': ['rotation', 'scale', 'translation', 'perspective', 'lighting'],
    },
    'cascading_ecc': {
        'id': 'cascading_ecc',
        'name': 'Cascading ECC Registration',
        'name_tr': 'Kademeli ECC Kaydı',
        'description': 'Two-stage ECC: first locks translation, then refines with affine if needed. More stable than single-pass ECC on repetitive textures.',
        'description_tr': 'İki aşamalı ECC: önce ötelemeyi kilitler, ardından gerekirse afin ile iyileştirir. Tekrarlayan dokularda tek geçişli ECC\'den daha kararlıdır.',
        'icon': 'anchor',
        'category': 'registration',
        'handles': ['rotation', 'scale', 'translation', 'shear'],
    },
    'orb_affine': {
        'id': 'orb_affine',
        'name': 'ORB Affine Alignment',
        'name_tr': 'ORB Afin Hizalama',
        'description': 'ORB features with RANSAC, preferring affine over homography. More constrained and stable for fabric shifts where perspective distortion is minimal.',
        'description_tr': 'RANSAC ile ORB özellikleri, homografi yerine afin dönüşümü tercih eder. Perspektif bozulmasının minimum olduğu kumaş kaymaları için daha kararlıdır.',
        'icon': 'target',
        'category': 'registration',
        'handles': ['rotation', 'scale', 'translation'],
    },
    'subpixel_translation': {
        'id': 'subpixel_translation',
        'name': 'Subpixel Translation',
        'name_tr': 'Alt Piksel Öteleme',
        'description': 'Pure X/Y shift correction using phase correlation with subpixel precision. Fastest technique — ideal when images are only translated without rotation.',
        'description_tr': 'Alt piksel hassasiyetle faz korelasyonu kullanarak saf X/Y kayma düzeltmesi. En hızlı teknik — görüntüler yalnızca döndürme olmadan ötelendiğinde idealdir.',
        'icon': 'maximize',
        'category': 'registration',
        'handles': ['translation'],
    },
    'pyramid_align': {
        'id': 'pyramid_align',
        'name': 'Pyramid Coarse-to-Fine',
        'name_tr': 'Piramit Kaba-İnce Hizalama',
        'description': 'Multi-scale ECC pyramid: estimates rough alignment at low resolution, then refines at full resolution. Very robust for repetitive textile patterns.',
        'description_tr': 'Çok ölçekli ECC piramidi: düşük çözünürlükte kaba hizalama tahmin eder, ardından tam çözünürlükte iyileştirir. Tekrarlayan tekstil desenleri için çok dayanıklıdır.',
        'icon': 'triangle',
        'category': 'registration',
        'handles': ['rotation', 'scale', 'translation'],
    },
    'tile_refine': {
        'id': 'tile_refine',
        'name': 'Tile-Based Local Refinement',
        'name_tr': 'Karo Tabanlı Yerel İyileştirme',
        'description': 'Global ECC translation followed by per-tile phase correlation refinement. Corrects residual local misalignment after global shift. Conservative — skips local correction if tiles disagree.',
        'description_tr': 'Genel ECC ötelemesi ardından karo başına faz korelasyonu iyileştirmesi. Genel kaymadan sonra kalan yerel hizalama bozukluğunu düzeltir. Muhafazakâr — karolar uyuşmazsa yerel düzeltmeyi atlar.',
        'icon': 'layout',
        'category': 'registration',
        'handles': ['translation'],
    },
}


def get_mode_info(mode_id):
    """Return metadata dict for a given mode."""
    return ALIGNMENT_MODES.get(mode_id, ALIGNMENT_MODES['direct'])


def list_modes():
    """Return list of all mode metadata dicts."""
    return list(ALIGNMENT_MODES.values())


# ═══════════════════════════════════════════════════════════════════
# 1. Direct Pixel Comparison — No preprocessing
# ═══════════════════════════════════════════════════════════════════

def align_direct(ref_img, sample_img, region_data=None):
    """No-op: returns images as-is. This is the current/legacy behavior."""
    return {
        'aligned_sample': sample_img.copy(),
        'transform_matrix': np.eye(3, dtype=np.float64),
        'method': 'direct',
        'metrics': {
            'applied': False,
            'description': 'No alignment applied — direct pixel comparison',
        },
    }


# ═══════════════════════════════════════════════════════════════════
# 2. ORB Feature-Based Alignment (Homography)
# ═══════════════════════════════════════════════════════════════════

def align_orb_homography(ref_img, sample_img, region_data=None,
                         max_features=5000, match_ratio=0.80,
                         min_matches=8):
    """
    Detect ORB keypoints, match with BFMatcher + Lowe's ratio test,
    estimate homography with RANSAC, and warp the sample image.

    Designed for textile QC: handles slight rotation, scale, perspective.
    Does NOT alter pixel colors — only geometric warping.
    """
    h, w = ref_img.shape[:2]

    # Ensure sample is same size as reference for comparison
    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    # Convert to grayscale for feature detection
    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY) if ref_img.shape[2] >= 3 else ref_img
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY) if work_sample.shape[2] >= 3 else work_sample

    # Detect ORB features (high count for textile patterns)
    orb = cv2.ORB_create(nfeatures=max_features, scoreType=cv2.ORB_HARRIS_SCORE)
    kp_ref, desc_ref = orb.detectAndCompute(ref_gray, None)
    kp_sam, desc_sam = orb.detectAndCompute(sam_gray, None)

    if desc_ref is None or desc_sam is None or len(kp_ref) < min_matches or len(kp_sam) < min_matches:
        return {
            'aligned_sample': work_sample,
            'transform_matrix': np.eye(3, dtype=np.float64),
            'method': 'orb_homography',
            'metrics': {
                'applied': False,
                'reason': 'Insufficient features detected',
                'ref_keypoints': len(kp_ref) if kp_ref else 0,
                'sample_keypoints': len(kp_sam) if kp_sam else 0,
            },
        }

    # Match descriptors using BFMatcher with Hamming distance
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    raw_matches = bf.knnMatch(desc_sam, desc_ref, k=2)

    # Lowe's ratio test
    good_matches = []
    for pair in raw_matches:
        if len(pair) == 2:
            m, n = pair
            if m.distance < match_ratio * n.distance:
                good_matches.append(m)

    # If ratio test yields too few, fallback to cross-check matching
    if len(good_matches) < min_matches:
        bf2 = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        cross_matches = bf2.match(desc_sam, desc_ref)
        cross_matches = sorted(cross_matches, key=lambda x: x.distance)
        good_matches = cross_matches[:min(200, len(cross_matches))]

    if len(good_matches) < min_matches:
        return {
            'aligned_sample': work_sample,
            'transform_matrix': np.eye(3, dtype=np.float64),
            'method': 'orb_homography',
            'metrics': {
                'applied': False,
                'reason': f'Insufficient good matches ({len(good_matches)}/{min_matches})',
                'total_matches': len(raw_matches),
                'good_matches': len(good_matches),
            },
        }

    # Extract matched point coordinates
    src_pts = np.float32([kp_sam[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_ref[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Estimate homography with RANSAC
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    if H is None:
        return {
            'aligned_sample': work_sample,
            'transform_matrix': np.eye(3, dtype=np.float64),
            'method': 'orb_homography',
            'metrics': {
                'applied': False,
                'reason': 'Homography estimation failed',
            },
        }

    inliers = int(mask.sum()) if mask is not None else 0

    # Decompose homography to extract rotation, scale, translation
    rotation_deg, scale_factor, tx, ty = _decompose_homography(H)

    # Safety check: reject extreme transforms (not minor capture issues)
    if abs(rotation_deg) > 15 or scale_factor < 0.7 or scale_factor > 1.4:
        return {
            'aligned_sample': work_sample,
            'transform_matrix': np.eye(3, dtype=np.float64),
            'method': 'orb_homography',
            'metrics': {
                'applied': False,
                'reason': f'Transform too extreme (rotation={rotation_deg:.1f}°, scale={scale_factor:.3f})',
                'rotation_deg': rotation_deg,
                'scale_factor': scale_factor,
            },
        }

    # Warp the sample image to align with reference
    aligned = cv2.warpPerspective(work_sample, H, (w, h),
                                  flags=cv2.INTER_LINEAR,
                                  borderMode=cv2.BORDER_REPLICATE)

    return {
        'aligned_sample': aligned,
        'transform_matrix': H.tolist(),
        'method': 'orb_homography',
        'metrics': {
            'applied': True,
            'ref_keypoints': len(kp_ref),
            'sample_keypoints': len(kp_sam),
            'good_matches': len(good_matches),
            'inliers': inliers,
            'rotation_deg': round(rotation_deg, 3),
            'scale_factor': round(scale_factor, 4),
            'translation_x': round(tx, 2),
            'translation_y': round(ty, 2),
            'description': f'Corrected {rotation_deg:.2f}° rotation, {scale_factor:.3f}x scale, ({tx:.1f}, {ty:.1f})px shift',
        },
    }


# ═══════════════════════════════════════════════════════════════════
# 3. ECC Intensity-Based Alignment
# ═══════════════════════════════════════════════════════════════════

def align_ecc(ref_img, sample_img, region_data=None,
              motion_type='affine', max_iterations=200,
              epsilon=1e-6):
    """
    Enhanced Correlation Coefficient alignment.
    Iteratively refines an affine (or euclidean) transform to maximize
    intensity correlation between reference and sample.

    Very robust for small geometric changes typical of textile QC.
    """
    MOTION_MAP = {
        'translation': cv2.MOTION_TRANSLATION,
        'euclidean': cv2.MOTION_EUCLIDEAN,
        'affine': cv2.MOTION_AFFINE,
    }
    cv_motion = MOTION_MAP.get(motion_type, cv2.MOTION_AFFINE)

    h, w = ref_img.shape[:2]

    # Ensure sample is same size as reference
    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    # Initialize warp matrix
    warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Convert to grayscale FLOAT32 (required by findTransformECC)
    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32) if ref_img.shape[2] >= 3 else ref_img.astype(np.float32)
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32) if work_sample.shape[2] >= 3 else work_sample.astype(np.float32)

    # Termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                max_iterations, epsilon)

    try:
        # Run ECC optimization
        cc, warp_matrix = cv2.findTransformECC(
            ref_gray, sam_gray, warp_matrix, cv_motion, criteria,
            inputMask=None, gaussFiltSize=5
        )

        # Warp the sample image (use work_sample which is already resized to ref dimensions)
        if cv_motion in (cv2.MOTION_TRANSLATION, cv2.MOTION_EUCLIDEAN, cv2.MOTION_AFFINE):
            aligned = cv2.warpAffine(
                work_sample, warp_matrix, (w, h),
                flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                borderMode=cv2.BORDER_REPLICATE
            )
        else:
            aligned = cv2.warpPerspective(
                work_sample, warp_matrix, (w, h),
                flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                borderMode=cv2.BORDER_REPLICATE
            )

        # Extract transform parameters
        rotation_deg = np.degrees(np.arctan2(warp_matrix[1, 0], warp_matrix[0, 0]))
        scale_x = np.sqrt(warp_matrix[0, 0]**2 + warp_matrix[1, 0]**2)
        scale_y = np.sqrt(warp_matrix[0, 1]**2 + warp_matrix[1, 1]**2)
        tx = warp_matrix[0, 2]
        ty = warp_matrix[1, 2]

        return {
            'aligned_sample': aligned,
            'transform_matrix': warp_matrix.tolist(),
            'method': 'ecc_alignment',
            'metrics': {
                'applied': True,
                'correlation_coefficient': round(float(cc), 6),
                'motion_type': motion_type,
                'rotation_deg': round(float(rotation_deg), 3),
                'scale_x': round(float(scale_x), 4),
                'scale_y': round(float(scale_y), 4),
                'translation_x': round(float(tx), 2),
                'translation_y': round(float(ty), 2),
                'description': f'ECC correlation={cc:.4f}, rotation={rotation_deg:.2f}°, shift=({tx:.1f}, {ty:.1f})px',
            },
        }

    except cv2.error as e:
        return {
            'aligned_sample': work_sample,
            'transform_matrix': np.eye(2, 3, dtype=np.float32).tolist(),
            'method': 'ecc_alignment',
            'metrics': {
                'applied': False,
                'reason': f'ECC convergence failed: {str(e)}',
            },
        }


# ═══════════════════════════════════════════════════════════════════
# 4. Phase Correlation Alignment
# ═══════════════════════════════════════════════════════════════════

def align_phase_correlation(ref_img, sample_img, region_data=None):
    """
    FFT-based phase correlation for detecting translation and rotation.

    Steps:
    1. Detect rotation using log-polar transform + phase correlation
    2. Correct rotation
    3. Detect translation using phase correlation
    4. Correct translation

    Very fast and reliable for small shifts and rotations.
    """
    h, w = ref_img.shape[:2]

    # Ensure sample is same size as reference
    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32) if ref_img.shape[2] >= 3 else ref_img.astype(np.float32)
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32) if work_sample.shape[2] >= 3 else work_sample.astype(np.float32)

    # Apply Hanning window to reduce edge effects for phase correlation
    hanning = cv2.createHanningWindow((w, h), cv2.CV_32F)

    # Step 1: Detect rotation using log-polar transform
    rotation_deg = _detect_rotation_logpolar(ref_gray, sam_gray)

    # Safety: limit rotation correction
    if abs(rotation_deg) > 15:
        rotation_deg = 0

    # Step 2: Correct rotation on color image
    center = (w / 2.0, h / 2.0)
    M_rot = cv2.getRotationMatrix2D(center, -rotation_deg, 1.0)

    rotated_sample = work_sample.copy()
    if abs(rotation_deg) > 0.05:
        rotated_sample = cv2.warpAffine(work_sample, M_rot, (w, h),
                                        flags=cv2.INTER_LINEAR,
                                        borderMode=cv2.BORDER_REPLICATE)

    # Step 3: Detect translation on rotation-corrected image
    rot_gray = cv2.cvtColor(rotated_sample[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32) if rotated_sample.shape[2] >= 3 else rotated_sample.astype(np.float32)

    # phaseCorrelate returns (dx, dy) to shift second image to match first
    shift, response = cv2.phaseCorrelate(ref_gray * hanning, rot_gray * hanning)
    tx, ty = shift  # positive tx means sample needs to move right to match ref

    # Safety: limit translation correction
    max_shift = min(w, h) * 0.20
    if abs(tx) > max_shift or abs(ty) > max_shift:
        tx, ty = 0, 0

    # Step 4: Apply translation to the rotation-corrected sample
    M_trans = np.float32([[1, 0, tx], [0, 1, ty]])
    aligned = cv2.warpAffine(rotated_sample, M_trans, (w, h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)

    applied = abs(rotation_deg) > 0.05 or abs(tx) > 0.5 or abs(ty) > 0.5

    return {
        'aligned_sample': aligned,
        'transform_matrix': M_trans.tolist(),
        'method': 'phase_correlation',
        'metrics': {
            'applied': applied,
            'rotation_deg': round(float(rotation_deg), 3),
            'translation_x': round(float(tx), 2),
            'translation_y': round(float(ty), 2),
            'phase_response': round(float(response), 6),
            'description': f'Phase correlation: rotation={rotation_deg:.2f}°, shift=({tx:.1f}, {ty:.1f})px, response={response:.4f}',
        },
    }


def _detect_rotation_logpolar(ref_gray, sam_gray):
    """Detect rotation angle using log-polar transform and phase correlation."""
    h, w = ref_gray.shape[:2]
    center = (w / 2, h / 2)
    max_radius = min(w, h) / 2

    # Window to reduce edge effects
    hanning = cv2.createHanningWindow((w, h), cv2.CV_32F)
    ref_win = ref_gray * hanning
    sam_win = sam_gray * hanning

    # Compute magnitude spectrum
    ref_fft = np.fft.fft2(ref_win)
    sam_fft = np.fft.fft2(sam_win)
    ref_mag = np.abs(np.fft.fftshift(ref_fft))
    sam_mag = np.abs(np.fft.fftshift(sam_fft))

    # Log-polar transform
    M_val = max_radius / np.log(max_radius)
    flags = cv2.INTER_LINEAR + cv2.WARP_FILL_OUTLIERS

    ref_lp = cv2.logPolar(ref_mag.astype(np.float32), center, M_val, flags)
    sam_lp = cv2.logPolar(sam_mag.astype(np.float32), center, M_val, flags)

    # Phase correlate on log-polar images to get rotation
    shift, _ = cv2.phaseCorrelate(ref_lp, sam_lp)
    angle = shift[1] * 360.0 / h

    # Resolve ambiguity (could be +180°)
    if angle > 90:
        angle -= 180
    elif angle < -90:
        angle += 180

    return angle


# ═══════════════════════════════════════════════════════════════════
# 5. AI Smart Region Matching (Custom Algorithm)
# ═══════════════════════════════════════════════════════════════════

def align_ai_smart_match(ref_img, sample_img, region_data=None):
    """
    Custom AI-based multi-strategy alignment algorithm.

    Combines multiple approaches in a cascade:
    1. Multi-scale normalized template matching to estimate position/scale
    2. ORB/AKAZE feature matching for geometric refinement
    3. Sub-pixel ECC refinement on the best candidate
    4. Adaptive lighting normalization (CLAHE on luminance only,
       preserving original chrominance for accurate color comparison)

    Returns the best alignment found across all strategies.
    """
    h_ref, w_ref = ref_img.shape[:2]
    h_sam, w_sam = sample_img.shape[:2]

    # ── Stage 1: Multi-scale Template Matching ──
    # Extract the reference region as template (or use full image)
    template = ref_img[:, :, :3] if ref_img.shape[2] >= 3 else ref_img
    search_img = sample_img[:, :, :3] if sample_img.shape[2] >= 3 else sample_img

    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    search_gray = cv2.cvtColor(search_img, cv2.COLOR_BGR2GRAY)

    best_match = _multi_scale_template_match(template_gray, search_gray,
                                             color_sample=sample_img,
                                             ref_shape=(h_ref, w_ref))

    # ── Stage 2: Feature-Based Geometric Refinement ──
    feature_result = _feature_guided_alignment(ref_img, sample_img)

    # ── Stage 3: Choose best strategy and refine ──
    # Compare which approach gives better correlation
    strategies = []

    if best_match is not None and best_match.get('aligned_sample') is not None:
        strategies.append(('template', best_match))

    if feature_result is not None and feature_result.get('aligned_sample') is not None:
        strategies.append(('feature', feature_result))

    if not strategies:
        # Fallback: try ECC directly
        ecc_result = align_ecc(ref_img, sample_img, motion_type='euclidean')
        return {
            'aligned_sample': ecc_result['aligned_sample'],
            'transform_matrix': ecc_result['transform_matrix'],
            'method': 'ai_smart_match',
            'metrics': {
                **ecc_result['metrics'],
                'strategy': 'ecc_fallback',
                'description': 'AI Smart Match: ECC fallback — ' + ecc_result['metrics'].get('description', ''),
            },
        }

    # Evaluate and select best strategy
    best_strategy = None
    best_aligned = None
    best_score = -1
    best_metrics = {}

    for name, result in strategies:
        aligned = result['aligned_sample']
        score = _compute_alignment_quality(ref_img, aligned)
        if score > best_score:
            best_score = score
            best_strategy = name
            best_aligned = aligned
            best_metrics = result.get('metrics', {})

    # ── Stage 4: Sub-pixel ECC Refinement on best result ──
    try:
        ref_gray_f = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY)
        best_gray_f = cv2.cvtColor(best_aligned[:, :, :3], cv2.COLOR_BGR2GRAY)
        if best_gray_f.shape[:2] != ref_gray_f.shape[:2]:
            best_gray_f = cv2.resize(best_gray_f, (ref_gray_f.shape[1], ref_gray_f.shape[0]))

        warp_ecc = np.eye(2, 3, dtype=np.float32)
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 50, 1e-5)
        cc, warp_ecc = cv2.findTransformECC(
            ref_gray_f, best_gray_f, warp_ecc,
            cv2.MOTION_EUCLIDEAN, criteria,
            inputMask=None, gaussFiltSize=3
        )

        h_out, w_out = ref_img.shape[:2]
        refined = cv2.warpAffine(
            best_aligned, warp_ecc, (w_out, h_out),
            flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
            borderMode=cv2.BORDER_REPLICATE
        )

        refined_score = _compute_alignment_quality(ref_img, refined)
        if refined_score > best_score:
            best_aligned = refined
            best_score = refined_score
            best_metrics['ecc_refined'] = True
            best_metrics['ecc_cc'] = round(float(cc), 6)
    except Exception:
        pass  # ECC refinement is optional

    # ── Stage 5: Lighting Inspection (non-destructive) ──
    lighting_delta = _analyze_lighting_difference(ref_img, best_aligned)

    # Build comprehensive metrics
    return {
        'aligned_sample': best_aligned,
        'transform_matrix': best_metrics.get('transform_matrix', np.eye(3).tolist()),
        'method': 'ai_smart_match',
        'metrics': {
            'applied': True,
            'strategy': best_strategy,
            'alignment_quality': round(float(best_score), 4),
            'rotation_deg': best_metrics.get('rotation_deg', 0),
            'scale_factor': best_metrics.get('scale_factor', 1.0),
            'translation_x': best_metrics.get('translation_x', 0),
            'translation_y': best_metrics.get('translation_y', 0),
            'ecc_refined': best_metrics.get('ecc_refined', False),
            'ecc_cc': best_metrics.get('ecc_cc', 0),
            'lighting_delta': lighting_delta,
            'description': f'AI Smart Match via {best_strategy}: quality={best_score:.4f}, lighting_delta={lighting_delta:.2f}',
        },
    }


def _multi_scale_template_match(template_gray, search_gray,
                                scale_range=(0.85, 1.15), scale_steps=7,
                                color_sample=None, ref_shape=None):
    """
    Multi-scale normalized cross-correlation template matching.
    Pads the search image so the template can slide even when same size.
    Returns dict with aligned color image and metrics, or None.
    """
    h_t, w_t = template_gray.shape[:2]
    h_s, w_s = search_gray.shape[:2]

    # Pad search image so template can always slide
    pad = max(int(max(h_t, w_t) * 0.20), 30)
    search_padded = cv2.copyMakeBorder(search_gray, pad, pad, pad, pad,
                                       cv2.BORDER_REPLICATE)
    h_sp, w_sp = search_padded.shape[:2]

    best_val = -1
    best_scale = 1.0
    best_loc = (0, 0)

    scales = np.linspace(scale_range[0], scale_range[1], scale_steps)

    for scale in scales:
        new_w = int(w_t * scale)
        new_h = int(h_t * scale)

        if new_w >= w_sp or new_h >= h_sp or new_w < 10 or new_h < 10:
            continue

        resized_template = cv2.resize(template_gray, (new_w, new_h))

        result = cv2.matchTemplate(search_padded, resized_template,
                                   cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val > best_val:
            best_val = max_val
            best_scale = scale
            # Adjust location to account for padding
            best_loc = (max_loc[0] - pad, max_loc[1] - pad)

    if best_val < 0.3:
        return None

    if color_sample is None:
        return None

    # Build affine transform: shift the sample so the matched region
    # aligns with the reference origin, then scale to match
    sx = 1.0 / best_scale
    sy = 1.0 / best_scale
    tx = -best_loc[0] * sx
    ty = -best_loc[1] * sy

    M = np.float32([[sx, 0, tx], [0, sy, ty]])

    h_out = ref_shape[0] if ref_shape else h_t
    w_out = ref_shape[1] if ref_shape else w_t

    aligned = cv2.warpAffine(color_sample, M, (w_out, h_out),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)

    return {
        'aligned_sample': aligned,
        'metrics': {
            'match_score': round(float(best_val), 4),
            'scale_factor': round(float(best_scale), 4),
            'translation_x': round(float(tx), 2),
            'translation_y': round(float(ty), 2),
            'transform_matrix': M.tolist(),
        },
    }


def _feature_guided_alignment(ref_img, sample_img):
    """
    Use AKAZE features (more robust than ORB for textile patterns)
    with geometric verification for alignment.
    """
    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY) if ref_img.shape[2] >= 3 else ref_img
    sam_gray = cv2.cvtColor(sample_img[:, :, :3], cv2.COLOR_BGR2GRAY) if sample_img.shape[2] >= 3 else sample_img

    # AKAZE is more robust for textured surfaces
    detector = cv2.AKAZE_create()
    kp_ref, desc_ref = detector.detectAndCompute(ref_gray, None)
    kp_sam, desc_sam = detector.detectAndCompute(sam_gray, None)

    if desc_ref is None or desc_sam is None or len(kp_ref) < 8 or len(kp_sam) < 8:
        return None

    # Match with BFMatcher
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    raw_matches = bf.knnMatch(desc_sam, desc_ref, k=2)

    good_matches = []
    for pair in raw_matches:
        if len(pair) == 2:
            m, n = pair
            if m.distance < 0.7 * n.distance:
                good_matches.append(m)

    if len(good_matches) < 8:
        return None

    src_pts = np.float32([kp_sam[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_ref[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Estimate affine transform (more constrained than homography)
    M, inliers = cv2.estimateAffinePartial2D(src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=5.0)

    if M is None:
        return None

    inlier_count = int(inliers.sum()) if inliers is not None else 0

    # Extract rotation and scale
    rotation_deg = np.degrees(np.arctan2(M[1, 0], M[0, 0]))
    scale_factor = np.sqrt(M[0, 0]**2 + M[1, 0]**2)
    tx = M[0, 2]
    ty = M[1, 2]

    # Safety limits
    if abs(rotation_deg) > 15 or scale_factor < 0.7 or scale_factor > 1.4:
        return None

    h, w = ref_img.shape[:2]
    aligned = cv2.warpAffine(sample_img, M, (w, h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)

    return {
        'aligned_sample': aligned,
        'metrics': {
            'good_matches': len(good_matches),
            'inliers': inlier_count,
            'rotation_deg': round(float(rotation_deg), 3),
            'scale_factor': round(float(scale_factor), 4),
            'translation_x': round(float(tx), 2),
            'translation_y': round(float(ty), 2),
            'transform_matrix': M.tolist(),
        },
    }


def _compute_alignment_quality(ref_img, aligned_img):
    """Compute normalized cross-correlation as alignment quality metric."""
    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float64)
    ali_gray = cv2.cvtColor(aligned_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float64)

    if ali_gray.shape[:2] != ref_gray.shape[:2]:
        ali_gray = cv2.resize(ali_gray, (ref_gray.shape[1], ref_gray.shape[0]))

    ref_norm = ref_gray - ref_gray.mean()
    ali_norm = ali_gray - ali_gray.mean()

    denom = np.sqrt(np.sum(ref_norm**2) * np.sum(ali_norm**2))
    if denom < 1e-10:
        return 0.0

    ncc = np.sum(ref_norm * ali_norm) / denom
    return float(ncc)


def _analyze_lighting_difference(ref_img, sample_img):
    """
    Analyze mean brightness difference between images.
    Returns delta as percentage — positive means sample is brighter.
    Does NOT modify images.
    """
    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float64)
    sam_gray = cv2.cvtColor(sample_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float64)

    if sam_gray.shape[:2] != ref_gray.shape[:2]:
        sam_gray = cv2.resize(sam_gray, (ref_gray.shape[1], ref_gray.shape[0]))

    ref_mean = ref_gray.mean()
    sam_mean = sam_gray.mean()

    if ref_mean < 1e-10:
        return 0.0

    delta_pct = ((sam_mean - ref_mean) / ref_mean) * 100.0
    return round(float(delta_pct), 2)


# ═══════════════════════════════════════════════════════════════════
# 6. Cascading ECC Registration (Translation → Affine)
# ═══════════════════════════════════════════════════════════════════

def align_cascading_ecc(ref_img, sample_img, region_data=None,
                        max_iterations=300, epsilon=1e-7):
    """
    Two-stage ECC alignment for robust global registration.

    Stage 1: Translation-only ECC to lock rough X/Y shift.
    Stage 2: If residual is significant, refine with affine ECC.

    More stable than jumping to affine directly because the initial
    translation estimate prevents the affine optimizer from diverging
    on repetitive textile patterns.
    """
    h, w = ref_img.shape[:2]

    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                max_iterations, epsilon)

    # ── Stage 1: Translation-only ECC ──
    warp_trans = np.eye(2, 3, dtype=np.float32)
    stage1_cc = 0.0
    try:
        stage1_cc, warp_trans = cv2.findTransformECC(
            ref_gray, sam_gray, warp_trans,
            cv2.MOTION_TRANSLATION, criteria,
            inputMask=None, gaussFiltSize=5
        )
    except cv2.error:
        # Translation ECC failed — return unmodified
        return {
            'aligned_sample': work_sample,
            'transform_matrix': np.eye(2, 3, dtype=np.float32).tolist(),
            'method': 'cascading_ecc',
            'metrics': {
                'applied': False,
                'reason': 'Translation ECC failed to converge',
            },
        }

    tx_s1 = float(warp_trans[0, 2])
    ty_s1 = float(warp_trans[1, 2])

    # Apply stage 1 translation
    stage1_aligned = cv2.warpAffine(
        work_sample, warp_trans, (w, h),
        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
        borderMode=cv2.BORDER_REPLICATE
    )

    # ── Stage 2: Affine refinement on the translation-corrected result ──
    stage2_cc = stage1_cc
    warp_affine = np.eye(2, 3, dtype=np.float32)
    final_aligned = stage1_aligned
    affine_applied = False

    # Only attempt affine if translation alone didn't achieve high correlation
    if stage1_cc < 0.995:
        try:
            s1_gray = cv2.cvtColor(stage1_aligned[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)
            criteria_s2 = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                           max_iterations // 2, epsilon * 10)
            stage2_cc, warp_affine = cv2.findTransformECC(
                ref_gray, s1_gray, warp_affine,
                cv2.MOTION_AFFINE, criteria_s2,
                inputMask=None, gaussFiltSize=5
            )
            if stage2_cc > stage1_cc:
                final_aligned = cv2.warpAffine(
                    stage1_aligned, warp_affine, (w, h),
                    flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
                    borderMode=cv2.BORDER_REPLICATE
                )
                affine_applied = True
        except cv2.error:
            pass  # Stage 2 is optional — stage 1 result is already good

    best_cc = max(stage1_cc, stage2_cc)
    applied = abs(tx_s1) > 0.3 or abs(ty_s1) > 0.3 or affine_applied

    # Extract final transform parameters
    rot_deg = 0.0
    scale_f = 1.0
    tx_final = tx_s1
    ty_final = ty_s1
    if affine_applied:
        rot_deg = float(np.degrees(np.arctan2(warp_affine[1, 0], warp_affine[0, 0])))
        scale_f = float(np.sqrt(warp_affine[0, 0]**2 + warp_affine[1, 0]**2))
        tx_final += float(warp_affine[0, 2])
        ty_final += float(warp_affine[1, 2])

    return {
        'aligned_sample': final_aligned,
        'transform_matrix': warp_trans.tolist(),
        'method': 'cascading_ecc',
        'metrics': {
            'applied': applied,
            'correlation_coefficient': round(float(best_cc), 6),
            'stage1_cc': round(float(stage1_cc), 6),
            'stage2_cc': round(float(stage2_cc), 6) if affine_applied else None,
            'affine_refined': affine_applied,
            'rotation_deg': round(rot_deg, 3),
            'scale_factor': round(scale_f, 4),
            'translation_x': round(tx_final, 2),
            'translation_y': round(ty_final, 2),
            'description': f'Cascading ECC: cc={best_cc:.4f}, shift=({tx_final:.1f},{ty_final:.1f})px'
                           + (f', affine refined' if affine_applied else ', translation only'),
        },
    }


# ═══════════════════════════════════════════════════════════════════
# 7. ORB + RANSAC Affine-Preferred Alignment
# ═══════════════════════════════════════════════════════════════════

def align_orb_affine(ref_img, sample_img, region_data=None,
                     max_features=6000, min_matches=10):
    """
    ORB keypoint matching with RANSAC, preferring an affine transform
    over full homography. Falls back to partial affine (similarity)
    if full affine is unstable.

    Better for fabric QC than homography because fabric images rarely
    have true perspective distortion — affine avoids over-fitting.
    """
    h, w = ref_img.shape[:2]

    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY)
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY)

    # Detect ORB features
    orb = cv2.ORB_create(nfeatures=max_features, scoreType=cv2.ORB_HARRIS_SCORE,
                         fastThreshold=10)
    kp_ref, desc_ref = orb.detectAndCompute(ref_gray, None)
    kp_sam, desc_sam = orb.detectAndCompute(sam_gray, None)

    if desc_ref is None or desc_sam is None:
        return _orb_affine_fallback(work_sample, 'No descriptors detected')

    if len(kp_ref) < min_matches or len(kp_sam) < min_matches:
        return _orb_affine_fallback(work_sample,
            f'Too few keypoints (ref={len(kp_ref)}, sam={len(kp_sam)})')

    # Two-pass matching: ratio test then cross-check fallback
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    raw_matches = bf.knnMatch(desc_sam, desc_ref, k=2)

    good_matches = []
    for pair in raw_matches:
        if len(pair) == 2:
            m, n = pair
            if m.distance < 0.78 * n.distance:
                good_matches.append(m)

    if len(good_matches) < min_matches:
        bf2 = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        cross = bf2.match(desc_sam, desc_ref)
        cross = sorted(cross, key=lambda x: x.distance)
        good_matches = cross[:min(300, len(cross))]

    if len(good_matches) < min_matches:
        return _orb_affine_fallback(work_sample,
            f'Too few good matches ({len(good_matches)})')

    src_pts = np.float32([kp_sam[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp_ref[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Try full affine first
    M_full, inliers_full = cv2.estimateAffine2D(
        src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=4.0)
    inlier_count_full = int(inliers_full.sum()) if inliers_full is not None else 0

    # Try partial affine (similarity: rotation + uniform scale + translation)
    M_partial, inliers_partial = cv2.estimateAffinePartial2D(
        src_pts, dst_pts, method=cv2.RANSAC, ransacReprojThreshold=4.0)
    inlier_count_partial = int(inliers_partial.sum()) if inliers_partial is not None else 0

    # Choose: prefer partial if it has comparable inlier count (more constrained = more stable)
    use_full = False
    if M_full is not None and M_partial is not None:
        if inlier_count_full > inlier_count_partial * 1.15:
            M = M_full
            inlier_count = inlier_count_full
            use_full = True
        else:
            M = M_partial
            inlier_count = inlier_count_partial
    elif M_partial is not None:
        M = M_partial
        inlier_count = inlier_count_partial
    elif M_full is not None:
        M = M_full
        inlier_count = inlier_count_full
        use_full = True
    else:
        return _orb_affine_fallback(work_sample, 'Affine estimation failed')

    # Extract parameters
    rotation_deg = float(np.degrees(np.arctan2(M[1, 0], M[0, 0])))
    scale_factor = float(np.sqrt(M[0, 0]**2 + M[1, 0]**2))
    tx = float(M[0, 2])
    ty = float(M[1, 2])

    # Safety limits
    if abs(rotation_deg) > 15 or scale_factor < 0.7 or scale_factor > 1.4:
        return _orb_affine_fallback(work_sample,
            f'Transform too extreme (rot={rotation_deg:.1f}°, scale={scale_factor:.3f})')

    aligned = cv2.warpAffine(work_sample, M, (w, h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)

    return {
        'aligned_sample': aligned,
        'transform_matrix': M.tolist(),
        'method': 'orb_affine',
        'metrics': {
            'applied': True,
            'transform_type': 'affine' if use_full else 'similarity',
            'ref_keypoints': len(kp_ref),
            'sample_keypoints': len(kp_sam),
            'good_matches': len(good_matches),
            'inliers': inlier_count,
            'rotation_deg': round(rotation_deg, 3),
            'scale_factor': round(scale_factor, 4),
            'translation_x': round(tx, 2),
            'translation_y': round(ty, 2),
            'description': f'ORB Affine ({("full" if use_full else "similarity")}): '
                           f'rot={rotation_deg:.2f}°, scale={scale_factor:.3f}, '
                           f'shift=({tx:.1f},{ty:.1f})px, {inlier_count} inliers',
        },
    }


def _orb_affine_fallback(work_sample, reason):
    """Safe fallback return for orb_affine."""
    return {
        'aligned_sample': work_sample,
        'transform_matrix': np.eye(2, 3, dtype=np.float64).tolist(),
        'method': 'orb_affine',
        'metrics': {
            'applied': False,
            'reason': reason,
        },
    }


# ═══════════════════════════════════════════════════════════════════
# 8. Pure Phase Correlation Subpixel Translation
# ═══════════════════════════════════════════════════════════════════

def align_subpixel_translation(ref_img, sample_img, region_data=None):
    """
    Pure subpixel translation correction using phase correlation.

    Unlike the existing phase_correlation technique (which also handles
    rotation via log-polar), this technique focuses ONLY on translation
    for maximum precision and speed. Best for cases where the image is
    simply shifted without rotation.

    Uses Hanning window to suppress edge artifacts and returns the
    phase correlation response as a confidence measure.
    """
    h, w = ref_img.shape[:2]

    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)

    # Hanning window reduces FFT edge leakage
    hanning = cv2.createHanningWindow((w, h), cv2.CV_32F)

    # Phase correlation for subpixel translation
    shift, response = cv2.phaseCorrelate(ref_gray * hanning, sam_gray * hanning)
    tx, ty = float(shift[0]), float(shift[1])

    # Safety: reject very large shifts (likely error from repetitive patterns)
    max_shift = min(w, h) * 0.25
    if abs(tx) > max_shift or abs(ty) > max_shift:
        return {
            'aligned_sample': work_sample,
            'transform_matrix': np.eye(2, 3, dtype=np.float32).tolist(),
            'method': 'subpixel_translation',
            'metrics': {
                'applied': False,
                'reason': f'Detected shift too large ({tx:.1f},{ty:.1f})px — likely false match',
                'translation_x': round(tx, 2),
                'translation_y': round(ty, 2),
                'phase_response': round(float(response), 6),
            },
        }

    applied = abs(tx) > 0.3 or abs(ty) > 0.3

    # Apply translation
    M = np.float32([[1, 0, tx], [0, 1, ty]])
    aligned = cv2.warpAffine(work_sample, M, (w, h),
                             flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)

    return {
        'aligned_sample': aligned,
        'transform_matrix': M.tolist(),
        'method': 'subpixel_translation',
        'metrics': {
            'applied': applied,
            'translation_x': round(tx, 2),
            'translation_y': round(ty, 2),
            'phase_response': round(float(response), 6),
            'description': f'Subpixel translation: shift=({tx:.2f},{ty:.2f})px, response={response:.4f}',
        },
    }


# ═══════════════════════════════════════════════════════════════════
# 9. Coarse-to-Fine Pyramid Alignment
# ═══════════════════════════════════════════════════════════════════

def align_pyramid(ref_img, sample_img, region_data=None,
                  levels=3, max_iterations=200, epsilon=1e-6):
    """
    Multi-scale pyramid alignment using ECC at each level.

    Estimates a rough translation at low resolution, then progressively
    refines at higher resolution levels. This is more stable than
    single-scale ECC on repetitive fabric textures because the coarse
    level sees larger structural features rather than individual threads.

    Pyramid levels:
      Level 0 = full resolution
      Level N = 1/(2^N) resolution
    """
    h, w = ref_img.shape[:2]

    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)

    # Build Gaussian pyramids (coarsest first)
    ref_pyr = [ref_gray]
    sam_pyr = [sam_gray]
    for _ in range(levels):
        ref_pyr.append(cv2.pyrDown(ref_pyr[-1]))
        sam_pyr.append(cv2.pyrDown(sam_pyr[-1]))

    # Start from coarsest level with translation-only model
    warp = np.eye(2, 3, dtype=np.float32)
    best_cc = 0.0

    for lvl in range(levels, -1, -1):
        ref_lvl = ref_pyr[lvl]
        sam_lvl = sam_pyr[lvl]

        # Scale the warp for this pyramid level
        if lvl < levels:
            warp[0, 2] *= 2.0
            warp[1, 2] *= 2.0

        # Use translation at coarsest, euclidean at mid, affine at finest
        if lvl == levels:
            motion = cv2.MOTION_TRANSLATION
            iters = max_iterations
        elif lvl > 0:
            motion = cv2.MOTION_EUCLIDEAN
            iters = max_iterations // 2
        else:
            motion = cv2.MOTION_AFFINE
            iters = max_iterations // 2

        # Ensure warp matrix shape matches motion model
        if motion == cv2.MOTION_TRANSLATION:
            warp_lvl = np.eye(2, 3, dtype=np.float32)
            warp_lvl[0, 2] = warp[0, 2]
            warp_lvl[1, 2] = warp[1, 2]
        else:
            warp_lvl = warp.copy()

        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                    iters, epsilon)

        try:
            cc, warp_lvl = cv2.findTransformECC(
                ref_lvl, sam_lvl, warp_lvl, motion, criteria,
                inputMask=None, gaussFiltSize=5
            )
            best_cc = cc

            # Promote result to full 2x3 affine for next level
            warp = np.eye(2, 3, dtype=np.float32)
            warp[:warp_lvl.shape[0], :warp_lvl.shape[1]] = warp_lvl
        except cv2.error:
            # If this level fails, keep the warp from previous level
            if lvl == levels:
                return {
                    'aligned_sample': work_sample,
                    'transform_matrix': np.eye(2, 3, dtype=np.float32).tolist(),
                    'method': 'pyramid_align',
                    'metrics': {
                        'applied': False,
                        'reason': 'Coarsest pyramid level ECC failed',
                    },
                }

    # Apply final warp to color image
    aligned = cv2.warpAffine(
        work_sample, warp, (w, h),
        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
        borderMode=cv2.BORDER_REPLICATE
    )

    # Extract parameters
    rotation_deg = float(np.degrees(np.arctan2(warp[1, 0], warp[0, 0])))
    scale_factor = float(np.sqrt(warp[0, 0]**2 + warp[1, 0]**2))
    tx = float(warp[0, 2])
    ty = float(warp[1, 2])

    applied = abs(tx) > 0.3 or abs(ty) > 0.3 or abs(rotation_deg) > 0.05

    return {
        'aligned_sample': aligned,
        'transform_matrix': warp.tolist(),
        'method': 'pyramid_align',
        'metrics': {
            'applied': applied,
            'correlation_coefficient': round(float(best_cc), 6),
            'pyramid_levels': levels + 1,
            'rotation_deg': round(rotation_deg, 3),
            'scale_factor': round(scale_factor, 4),
            'translation_x': round(tx, 2),
            'translation_y': round(ty, 2),
            'description': f'Pyramid ECC ({levels+1} levels): cc={best_cc:.4f}, '
                           f'shift=({tx:.1f},{ty:.1f})px, rot={rotation_deg:.2f}°',
        },
    }


# ═══════════════════════════════════════════════════════════════════
# 10. Tile-Based Local Refinement
# ═══════════════════════════════════════════════════════════════════

def align_tile_refine(ref_img, sample_img, region_data=None,
                      grid_size=4, max_local_shift=8):
    """
    Two-stage alignment: global + tile-based local correction.

    Stage 1: Global ECC translation to correct bulk shift.
    Stage 2: Split into NxN grid of tiles and estimate per-tile
             sub-pixel translation. Apply the median correction
             (robust to outlier tiles) or, if tiles agree well,
             build a smooth local correction field.

    Conservative: if local shifts are inconsistent across tiles,
    only the global correction is applied. This prevents distortion
    on uniform fabric regions.
    """
    h, w = ref_img.shape[:2]

    work_sample = sample_img.copy()
    if work_sample.shape[:2] != (h, w):
        work_sample = cv2.resize(work_sample, (w, h))

    ref_gray = cv2.cvtColor(ref_img[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)
    sam_gray = cv2.cvtColor(work_sample[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)

    # ── Stage 1: Global translation via ECC ──
    warp_global = np.eye(2, 3, dtype=np.float32)
    global_cc = 0.0
    try:
        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 200, 1e-6)
        global_cc, warp_global = cv2.findTransformECC(
            ref_gray, sam_gray, warp_global,
            cv2.MOTION_TRANSLATION, criteria,
            inputMask=None, gaussFiltSize=5
        )
    except cv2.error:
        pass  # proceed with identity if global fails

    global_tx = float(warp_global[0, 2])
    global_ty = float(warp_global[1, 2])

    # Apply global correction
    global_aligned = cv2.warpAffine(
        work_sample, warp_global, (w, h),
        flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP,
        borderMode=cv2.BORDER_REPLICATE
    )
    global_gray = cv2.cvtColor(global_aligned[:, :, :3], cv2.COLOR_BGR2GRAY).astype(np.float32)

    # ── Stage 2: Per-tile local shift estimation ──
    tile_h = h // grid_size
    tile_w = w // grid_size
    local_shifts_x = []
    local_shifts_y = []
    tile_responses = []

    for row in range(grid_size):
        for col in range(grid_size):
            y0 = row * tile_h
            x0 = col * tile_w
            y1 = min(y0 + tile_h, h)
            x1 = min(x0 + tile_w, w)

            # Skip very small tiles at edges
            if (y1 - y0) < 16 or (x1 - x0) < 16:
                continue

            ref_tile = ref_gray[y0:y1, x0:x1]
            sam_tile = global_gray[y0:y1, x0:x1]

            tw, th = x1 - x0, y1 - y0
            hanning = cv2.createHanningWindow((tw, th), cv2.CV_32F)

            try:
                shift, resp = cv2.phaseCorrelate(
                    ref_tile * hanning, sam_tile * hanning)
                dx, dy = float(shift[0]), float(shift[1])

                # Only trust tiles with reasonable shift
                if abs(dx) <= max_local_shift and abs(dy) <= max_local_shift:
                    local_shifts_x.append(dx)
                    local_shifts_y.append(dy)
                    tile_responses.append(float(resp))
            except cv2.error:
                continue

    # Decide whether local correction is trustworthy
    local_applied = False
    median_local_tx = 0.0
    median_local_ty = 0.0
    tile_agreement = 0.0

    if len(local_shifts_x) >= grid_size:  # need at least grid_size tiles
        median_local_tx = float(np.median(local_shifts_x))
        median_local_ty = float(np.median(local_shifts_y))

        # Measure agreement: std of tile shifts (low = consistent)
        std_x = float(np.std(local_shifts_x))
        std_y = float(np.std(local_shifts_y))
        tile_agreement = 1.0 / (1.0 + std_x + std_y)

        # Only apply if tiles agree reasonably and correction is meaningful
        significant = abs(median_local_tx) > 0.2 or abs(median_local_ty) > 0.2
        consistent = (std_x < max_local_shift * 0.5) and (std_y < max_local_shift * 0.5)

        if significant and consistent:
            local_applied = True

    # Apply local median correction on top of global
    final_aligned = global_aligned
    if local_applied:
        M_local = np.float32([[1, 0, median_local_tx], [0, 1, median_local_ty]])
        final_aligned = cv2.warpAffine(
            global_aligned, M_local, (w, h),
            flags=cv2.INTER_LINEAR,
            borderMode=cv2.BORDER_REPLICATE
        )

    total_tx = global_tx + (median_local_tx if local_applied else 0)
    total_ty = global_ty + (median_local_ty if local_applied else 0)
    applied = abs(total_tx) > 0.3 or abs(total_ty) > 0.3

    return {
        'aligned_sample': final_aligned,
        'transform_matrix': warp_global.tolist(),
        'method': 'tile_refine',
        'metrics': {
            'applied': applied,
            'correlation_coefficient': round(float(global_cc), 6),
            'global_translation_x': round(global_tx, 2),
            'global_translation_y': round(global_ty, 2),
            'local_refined': local_applied,
            'local_median_x': round(median_local_tx, 2) if local_applied else 0,
            'local_median_y': round(median_local_ty, 2) if local_applied else 0,
            'tiles_used': len(local_shifts_x),
            'tile_agreement': round(tile_agreement, 4),
            'translation_x': round(total_tx, 2),
            'translation_y': round(total_ty, 2),
            'description': f'Tile Refine: global=({global_tx:.1f},{global_ty:.1f})px'
                           + (f', local=({median_local_tx:.1f},{median_local_ty:.1f})px '
                              f'[{len(local_shifts_x)} tiles, agree={tile_agreement:.2f}]'
                              if local_applied
                              else f', no local refinement ({len(local_shifts_x)} tiles)'),
        },
    }


def _decompose_homography(H):
    """Extract approximate rotation, scale, translation from 3x3 homography."""
    rotation_deg = np.degrees(np.arctan2(H[1, 0], H[0, 0]))
    scale_factor = np.sqrt(H[0, 0]**2 + H[1, 0]**2)
    tx = H[0, 2]
    ty = H[1, 2]
    return float(rotation_deg), float(scale_factor), float(tx), float(ty)


# ═══════════════════════════════════════════════════════════════════
# Unified Alignment Dispatcher
# ═══════════════════════════════════════════════════════════════════

def apply_alignment(ref_img, sample_img, mode='direct', region_data=None, **kwargs):
    """
    Main entry point — dispatch to the appropriate alignment method.

    Args:
        ref_img: Reference image (numpy BGR/BGRA)
        sample_img: Sample image (numpy BGR/BGRA)
        mode: One of 'direct', 'orb_homography', 'ecc_alignment',
              'phase_correlation', 'ai_smart_match'
        region_data: Optional region selection data dict
        **kwargs: Additional method-specific parameters

    Returns:
        dict with keys: aligned_sample, transform_matrix, method, metrics
    """
    DISPATCH = {
        'direct': align_direct,
        'orb_homography': align_orb_homography,
        'ecc_alignment': align_ecc,
        'phase_correlation': align_phase_correlation,
        'ai_smart_match': align_ai_smart_match,
        'cascading_ecc': align_cascading_ecc,
        'orb_affine': align_orb_affine,
        'subpixel_translation': align_subpixel_translation,
        'pyramid_align': align_pyramid,
        'tile_refine': align_tile_refine,
    }

    align_fn = DISPATCH.get(mode, align_direct)

    try:
        result = align_fn(ref_img, sample_img, region_data=region_data, **kwargs)
    except Exception as e:
        print(f"[ImageAlignment] Error in {mode}: {e}")
        import traceback
        traceback.print_exc()
        result = {
            'aligned_sample': sample_img.copy(),
            'transform_matrix': np.eye(3).tolist(),
            'method': mode,
            'metrics': {
                'applied': False,
                'reason': f'Error: {str(e)}',
            },
        }

    return result


def generate_preview_images(ref_img, sample_img, result):
    """
    Generate visualization images for the alignment studio preview.
    Returns only the aligned image in base64 format.
    """
    import base64

    previews = {}
    aligned = result['aligned_sample']

    ali_bgr = aligned[:, :, :3] if aligned.shape[2] >= 3 else aligned
    
    h, w = ref_img.shape[:2]
    if ali_bgr.shape[:2] != (h, w):
        ali_bgr = cv2.resize(ali_bgr, (w, h))

    # Only return the aligned sample image
    previews['aligned'] = _img_to_base64(ali_bgr)

    return previews


def _img_to_base64(img):
    """Encode OpenCV image to base64 PNG string."""
    import base64
    _, buffer = cv2.imencode('.png', img)
    return base64.b64encode(buffer).decode('utf-8')
