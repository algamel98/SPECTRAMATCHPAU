# -*- coding: utf-8 -*-
"""
RecommendationsEngine — Centralized, threshold-aware recommendations for all report types.

Generates professional insights tables and conclusion text for:
  - Color Unit (two-image comparison)
  - Pattern Unit (two-image comparison)
  - Single Image Unit (standalone analysis)

All outputs are bilingual (English / Turkish) and adapt dynamically to
user-defined thresholds so that changing pass/fail criteria still produces
meaningful, contextual recommendations.
"""

# ═══════════════════════════════════════════════════════════════════════════════
# TRANSLATION DICTIONARY
# ═══════════════════════════════════════════════════════════════════════════════

_T = {
    # ── Table Headers ──────────────────────────────────────────────────────
    'header_metric':        {'en': 'Metric',          'tr': 'Metrik'},
    'header_value':         {'en': 'Value',            'tr': 'Değer'},
    'header_evaluation':    {'en': 'Evaluation',       'tr': 'Değerlendirme'},
    'header_recommendation':{'en': 'Recommendation',   'tr': 'Öneri'},
    'header_finding':       {'en': 'Finding',          'tr': 'Bulgu'},

    # ── Section Titles ─────────────────────────────────────────────────────
    'title_recommendations':    {'en': 'Key Findings & Recommendations',
                                 'tr': 'Temel Bulgular ve Öneriler'},
    'title_conclusion':         {'en': 'Conclusion & Decision',
                                 'tr': 'Sonuç ve Karar'},
    'title_single_rec':         {'en': 'Analysis Summary & Recommendations',
                                 'tr': 'Analiz Özeti ve Öneriler'},

    # ── Metric Labels ──────────────────────────────────────────────────────
    'mean_delta_e':         {'en': 'Mean ΔE2000',              'tr': 'Ortalama ΔE2000'},
    'consistency':          {'en': 'Consistency (Std Dev)',     'tr': 'Tutarlılık (Std Sapma)'},
    'csi_score':            {'en': 'CSI Score',                 'tr': 'RBE Skoru'},
    'composite_score':      {'en': 'Composite Score',           'tr': 'Bileşik Skor'},
    'structural_match':     {'en': 'Structural Match',          'tr': 'Yapısal Eşleşme'},
    'worst_metric':         {'en': 'Weakest Metric',            'tr': 'En Zayıf Metrik'},
    'luminance':            {'en': 'Luminance (L*)',            'tr': 'Parlaklık (L*)'},
    'chroma':               {'en': 'Chroma Spread',             'tr': 'Kroma Dağılımı'},
    'color_uniformity':     {'en': 'Color Uniformity',          'tr': 'Renk Homojenliği'},
    'dominant_channel':     {'en': 'Dominant Channel',          'tr': 'Baskın Kanal'},

    # ── Delta E Evaluations ────────────────────────────────────────────────
    'de_imperceptible':     {'en': 'Imperceptible difference — within instrument noise.',
                             'tr': 'Algılanamaz fark — cihaz gürültüsü sınırları içinde.'},
    'de_slight':            {'en': 'Slight difference — visible only under controlled lighting.',
                             'tr': 'Hafif fark — yalnızca kontrollü aydınlatmada görülebilir.'},
    'de_noticeable':        {'en': 'Noticeable difference — perceptible to trained observers.',
                             'tr': 'Fark edilir fark — eğitimli gözlemciler tarafından algılanabilir.'},
    'de_significant':       {'en': 'Significant mismatch — clearly visible to the naked eye.',
                             'tr': 'Önemli uyumsuzluk — çıplak gözle açıkça görülebilir.'},
    'de_severe':            {'en': 'Severe mismatch — unacceptable color deviation.',
                             'tr': 'Ciddi uyumsuzluk — kabul edilemez renk sapması.'},

    # ── Delta E Recommendations ────────────────────────────────────────────
    'de_rec_none':          {'en': 'No action required. Process is optimal.',
                             'tr': 'İşlem gerekmez. Süreç optimal düzeyde.'},
    'de_rec_acceptable':    {'en': 'Acceptable for most applications. Continue monitoring.',
                             'tr': 'Çoğu uygulama için kabul edilebilir. İzlemeye devam edin.'},
    'de_rec_check_dye':     {'en': 'Review dye concentration, temperature, and timing parameters.',
                             'tr': 'Boya konsantrasyonu, sıcaklık ve zamanlama parametrelerini gözden geçirin.'},
    'de_rec_investigate':   {'en': 'Investigate root cause. Check raw material batch and process variables.',
                             'tr': 'Kök nedeni araştırın. Hammadde partisi ve süreç değişkenlerini kontrol edin.'},
    'de_rec_reject':        {'en': 'Reject batch and initiate corrective action procedure.',
                             'tr': 'Partiyi reddedin ve düzeltici faaliyet prosedürünü başlatın.'},

    # ── Consistency Evaluations ────────────────────────────────────────────
    'std_excellent':        {'en': 'Excellent uniformity — highly consistent across all regions.',
                             'tr': 'Mükemmel homojenlik — tüm bölgelerde yüksek tutarlılık.'},
    'std_good':             {'en': 'Good uniformity — minor regional variations within tolerance.',
                             'tr': 'İyi homojenlik — tolerans dahilinde küçük bölgesel farklılıklar.'},
    'std_moderate':         {'en': 'Moderate variation — some regions deviate noticeably.',
                             'tr': 'Orta düzey varyasyon — bazı bölgeler belirgin şekilde sapıyor.'},
    'std_high':             {'en': 'High variation — significant inconsistency across sample.',
                             'tr': 'Yüksek varyasyon — numune genelinde önemli tutarsızlık.'},

    'std_rec_stable':       {'en': 'Process is stable. Maintain current parameters.',
                             'tr': 'Süreç kararlı. Mevcut parametreleri koruyun.'},
    'std_rec_monitor':      {'en': 'Monitor uniformity. Check application equipment calibration.',
                             'tr': 'Homojenliği izleyin. Uygulama ekipmanı kalibrasyonunu kontrol edin.'},
    'std_rec_check':        {'en': 'Check application evenness, roller pressure, and dye bath circulation.',
                             'tr': 'Uygulama düzgünlüğünü, silindir basıncını ve boya banyosu sirkülasyonunu kontrol edin.'},
    'std_rec_halt':         {'en': 'Halt production. Perform full equipment inspection and recalibration.',
                             'tr': 'Üretimi durdurun. Tam ekipman muayenesi ve yeniden kalibrasyon yapın.'},

    # ── CSI Evaluations ────────────────────────────────────────────────────
    'csi_excellent':        {'en': 'Excellent color match — meets or exceeds quality standard.',
                             'tr': 'Mükemmel renk eşleşmesi — kalite standardını karşılıyor veya aşıyor.'},
    'csi_good':             {'en': 'Good match — within acceptable production tolerance.',
                             'tr': 'İyi eşleşme — kabul edilebilir üretim toleransı dahilinde.'},
    'csi_marginal':         {'en': 'Marginal match — at the boundary of acceptable limits.',
                             'tr': 'Sınırda eşleşme — kabul edilebilir sınırların kenarında.'},
    'csi_poor':             {'en': 'Poor match — below minimum quality threshold.',
                             'tr': 'Zayıf eşleşme — minimum kalite eşiğinin altında.'},

    'csi_rec_approved':     {'en': 'Approved. Proceed with production.',
                             'tr': 'Onaylandı. Üretime devam edin.'},
    'csi_rec_conditional':  {'en': 'Conditional approval. Increase inspection frequency.',
                             'tr': 'Koşullu onay. Muayene sıklığını artırın.'},
    'csi_rec_review':       {'en': 'Requires supervisory review before proceeding.',
                             'tr': 'Devam etmeden önce amirlik incelemesi gerektirir.'},
    'csi_rec_reject':       {'en': 'Reject. Do not proceed without corrective measures.',
                             'tr': 'Reddedin. Düzeltici önlemler alınmadan devam etmeyin.'},

    # ── Pattern Composite Evaluations ──────────────────────────────────────
    'comp_excellent':       {'en': 'Excellent structural alignment — pattern integrity preserved.',
                             'tr': 'Mükemmel yapısal hizalama — desen bütünlüğü korunmuş.'},
    'comp_good':            {'en': 'Good alignment — minor deviations within production tolerance.',
                             'tr': 'İyi hizalama — üretim toleransı dahilinde küçük sapmalar.'},
    'comp_marginal':        {'en': 'Marginal alignment — approaching quality limits.',
                             'tr': 'Sınırda hizalama — kalite sınırlarına yaklaşıyor.'},
    'comp_poor':            {'en': 'Poor alignment — significant pattern deviation detected.',
                             'tr': 'Zayıf hizalama — önemli desen sapması tespit edildi.'},

    'comp_rec_optimal':     {'en': 'Process is optimal. No corrective action needed.',
                             'tr': 'Süreç optimal. Düzeltici işlem gerekmez.'},
    'comp_rec_monitor':     {'en': 'Monitor production line. Schedule preventive maintenance.',
                             'tr': 'Üretim hattını izleyin. Önleyici bakım planlayın.'},
    'comp_rec_calibrate':   {'en': 'Calibrate alignment sensors and verify fabric feed tension.',
                             'tr': 'Hizalama sensörlerini kalibre edin ve kumaş besleme gerginliğini doğrulayın.'},
    'comp_rec_stop':        {'en': 'Stop production. Perform full machine calibration and inspection.',
                             'tr': 'Üretimi durdurun. Tam makine kalibrasyonu ve muayene yapın.'},

    # ── Structural Match Evaluations ───────────────────────────────────────
    'struct_identical':     {'en': 'Structurally identical — no geometric distortion detected.',
                             'tr': 'Yapısal olarak aynı — geometrik bozulma tespit edilmedi.'},
    'struct_minor':         {'en': 'Minor structural deviation — within acceptable range.',
                             'tr': 'Küçük yapısal sapma — kabul edilebilir aralıkta.'},
    'struct_moderate':      {'en': 'Moderate distortion — visible pattern shift or stretch.',
                             'tr': 'Orta düzey bozulma — görünür desen kayması veya gerilme.'},
    'struct_severe':        {'en': 'Severe distortion — significant layout deformation.',
                             'tr': 'Ciddi bozulma — önemli düzen deformasyonu.'},

    'struct_rec_none':      {'en': 'No layout issues. Fabric handling is consistent.',
                             'tr': 'Düzen sorunu yok. Kumaş işleme tutarlı.'},
    'struct_rec_tension':   {'en': 'Check fabric tension and roller alignment.',
                             'tr': 'Kumaş gerginliğini ve silindir hizalamasını kontrol edin.'},
    'struct_rec_inspect':   {'en': 'Inspect weaving/knitting parameters and fabric feed mechanism.',
                             'tr': 'Dokuma/örme parametrelerini ve kumaş besleme mekanizmasını inceleyin.'},
    'struct_rec_overhaul':  {'en': 'Full mechanical overhaul required. Check loom/knitting machine setup.',
                             'tr': 'Tam mekanik revizyon gerekli. Tezgah/örme makinesi kurulumunu kontrol edin.'},

    # ── Worst Metric ───────────────────────────────────────────────────────
    'worst_below_pass':     {'en': 'Below pass threshold — this metric is the primary quality limiter.',
                             'tr': 'Geçiş eşiğinin altında — bu metrik birincil kalite sınırlayıcısıdır.'},
    'worst_rec':            {'en': 'Focus improvement efforts on this metric first.',
                             'tr': 'İyileştirme çalışmalarını önce bu metriğe odaklayın.'},

    # ── Single Image Evaluations ───────────────────────────────────────────
    'lum_bright':           {'en': 'High luminance — sample appears bright/light.',
                             'tr': 'Yüksek parlaklık — numune parlak/açık görünüyor.'},
    'lum_medium':           {'en': 'Medium luminance — standard mid-tone range.',
                             'tr': 'Orta parlaklık — standart orta ton aralığı.'},
    'lum_dark':             {'en': 'Low luminance — sample appears dark/deep.',
                             'tr': 'Düşük parlaklık — numune koyu/derin görünüyor.'},

    'lum_rec_bright':       {'en': 'Verify lightness is intentional. Check for over-bleaching or under-dyeing.',
                             'tr': 'Açıklığın kasıtlı olduğunu doğrulayın. Aşırı ağartma veya yetersiz boyamayı kontrol edin.'},
    'lum_rec_medium':       {'en': 'Luminance within expected range. No action needed.',
                             'tr': 'Parlaklık beklenen aralıkta. İşlem gerekmez.'},
    'lum_rec_dark':         {'en': 'Verify darkness is intentional. Check for over-dyeing or insufficient rinsing.',
                             'tr': 'Koyuluğun kasıtlı olduğunu doğrulayın. Aşırı boyama veya yetersiz durulamayı kontrol edin.'},

    'chroma_narrow':        {'en': 'Narrow chroma spread — color is highly uniform.',
                             'tr': 'Dar kroma dağılımı — renk oldukça homojen.'},
    'chroma_moderate':      {'en': 'Moderate chroma spread — acceptable color variation.',
                             'tr': 'Orta kroma dağılımı — kabul edilebilir renk varyasyonu.'},
    'chroma_wide':          {'en': 'Wide chroma spread — significant color variation across sample.',
                             'tr': 'Geniş kroma dağılımı — numune genelinde önemli renk varyasyonu.'},

    'chroma_rec_uniform':   {'en': 'Color distribution is consistent. Process is well-controlled.',
                             'tr': 'Renk dağılımı tutarlı. Süreç iyi kontrol altında.'},
    'chroma_rec_monitor':   {'en': 'Monitor dye distribution. Check for uneven application.',
                             'tr': 'Boya dağılımını izleyin. Düzensiz uygulama olup olmadığını kontrol edin.'},
    'chroma_rec_investigate':{'en': 'Investigate dye bath uniformity and fabric preparation consistency.',
                              'tr': 'Boya banyosu homojenliğini ve kumaş hazırlama tutarlılığını araştırın.'},

    'uniformity_excellent': {'en': 'Excellent color uniformity across all sampling points.',
                             'tr': 'Tüm örnekleme noktalarında mükemmel renk homojenliği.'},
    'uniformity_good':      {'en': 'Good uniformity — minor point-to-point variation.',
                             'tr': 'İyi homojenlik — noktalar arası küçük varyasyon.'},
    'uniformity_poor':      {'en': 'Poor uniformity — significant variation between sampling points.',
                             'tr': 'Zayıf homojenlik — örnekleme noktaları arasında önemli varyasyon.'},

    'uniformity_rec_ok':    {'en': 'Dyeing process is consistent. Maintain current parameters.',
                             'tr': 'Boyama süreci tutarlı. Mevcut parametreleri koruyun.'},
    'uniformity_rec_check': {'en': 'Check dye penetration and fabric absorbency uniformity.',
                             'tr': 'Boya penetrasyonunu ve kumaş emicilik homojenliğini kontrol edin.'},
    'uniformity_rec_fix':   {'en': 'Significant non-uniformity. Review entire dyeing process chain.',
                             'tr': 'Önemli homojenlik sorunu. Tüm boyama süreç zincirini gözden geçirin.'},

    # ── Conclusion Texts ───────────────────────────────────────────────────
    'conclusion_pass':      {'en': 'Sample meets all quality standards within the defined tolerances. Approved for production.',
                             'tr': 'Numune, belirlenen toleranslar dahilinde tüm kalite standartlarını karşılamaktadır. Üretime onaylanmıştır.'},
    'conclusion_conditional':{'en': 'Sample is near quality limits. Conditional approval granted — increased monitoring and secondary verification recommended.',
                              'tr': 'Numune kalite sınırlarına yakındır. Koşullu onay verilmiştir — artırılmış izleme ve ikincil doğrulama önerilir.'},
    'conclusion_fail':      {'en': 'Sample does not meet the required quality standards. Reject and initiate root cause analysis before re-processing.',
                             'tr': 'Numune gerekli kalite standartlarını karşılamamaktadır. Reddedin ve yeniden işlemeden önce kök neden analizi başlatın.'},

    'conclusion_single_good':{'en': 'Sample color properties are within normal ranges. Suitable for further processing or comparison.',
                               'tr': 'Numune renk özellikleri normal aralıklarda. İleri işleme veya karşılaştırma için uygundur.'},
    'conclusion_single_warn':{'en': 'Some color properties show notable variation. Manual review recommended before proceeding.',
                               'tr': 'Bazı renk özellikleri belirgin varyasyon göstermektedir. Devam etmeden önce manuel inceleme önerilir.'},
    'conclusion_single_poor':{'en': 'Significant color non-uniformity detected. Investigate dyeing process before using this batch.',
                               'tr': 'Önemli renk homojenlik sorunu tespit edildi. Bu partiyi kullanmadan önce boyama sürecini araştırın.'},
}


def _t(key, lang):
    """Get translated string."""
    entry = _T.get(key, {})
    return entry.get(lang, entry.get('en', key))


# ═══════════════════════════════════════════════════════════════════════════════
# HELPER: Threshold-relative position
# ═══════════════════════════════════════════════════════════════════════════════

def _relative_position(value, pass_thr, cond_thr=None, higher_is_better=True):
    """
    Determine where a value sits relative to user-defined thresholds.
    Returns one of: 'excellent', 'good', 'marginal', 'poor'
    """
    if cond_thr is None:
        cond_thr = pass_thr * 0.7 if higher_is_better else pass_thr * 2.5

    if higher_is_better:
        if value >= pass_thr:
            return 'excellent'
        mid = (pass_thr + cond_thr) / 2.0
        if value >= mid:
            return 'good'
        if value >= cond_thr:
            return 'marginal'
        return 'poor'
    else:
        if value <= pass_thr * 0.5:
            return 'excellent'
        if value <= pass_thr:
            return 'good'
        if value <= cond_thr:
            return 'marginal'
        return 'poor'


def _level_to_color(level):
    """Map level string to a hex color for the accent bar."""
    return {
        'excellent': '#27AE60',
        'good':      '#2ECC71',
        'marginal':  '#F39C12',
        'poor':      '#E74C3C',
        'warn':      '#F39C12',
    }.get(level, '#7F8C8D')


# ═══════════════════════════════════════════════════════════════════════════════
# PDF RENDERING — Modern card-based layout (no data tables)
# ═══════════════════════════════════════════════════════════════════════════════

def render_findings_to_flowables(findings, conclusion_text, conclusion_status, section_title, lang='en'):
    """
    Render findings and conclusion as modern, professional ReportLab flowables.

    Each finding is rendered as a card block:
      ┌─────────────────────────────────────────────────┐
      │  METRIC NAME                          value     │  ← dark header bar
      │  Evaluation text describing the result.         │  ← light body
      │  ▸ Recommendation text with guidance.           │  ← recommendation line
      └─────────────────────────────────────────────────┘

    Parameters:
        findings: list of dicts, each with keys:
            'metric', 'value', 'evaluation', 'recommendation', 'level'
        conclusion_text: str
        conclusion_status: str — 'pass'|'conditional'|'fail'|'good'|'warn'|'poor'
        section_title: str
        lang: str

    Returns:
        list of ReportLab flowables
    """
    from reportlab.lib import colors as rl_colors
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.units import inch
    from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, KeepTogether

    from modules.ReportUtils import (
        PDF_FONT_BOLD, PDF_FONT_REGULAR,
        GREEN, RED, ORANGE, NEUTRAL_DARK, NEUTRAL,
        StyleH1, StyleH2, StyleBody,
    )

    flowables = []

    # Section title
    flowables.append(Paragraph(section_title, StyleH1))
    flowables.append(Spacer(1, 6))

    # Styles for card content
    card_metric_style = ParagraphStyle(
        'CardMetric', fontName=PDF_FONT_BOLD, fontSize=9.5,
        textColor=rl_colors.white, leading=13, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=0,
    )
    card_value_style = ParagraphStyle(
        'CardValue', fontName=PDF_FONT_BOLD, fontSize=9.5,
        textColor=rl_colors.white, leading=13, alignment=TA_LEFT,
        spaceBefore=0, spaceAfter=0,
    )
    card_eval_style = ParagraphStyle(
        'CardEval', fontName=PDF_FONT_REGULAR, fontSize=8.5,
        textColor=rl_colors.HexColor('#2C3E50'), leading=12, alignment=TA_LEFT,
        spaceBefore=2, spaceAfter=2,
    )
    card_rec_style = ParagraphStyle(
        'CardRec', fontName=PDF_FONT_REGULAR, fontSize=8.5,
        textColor=rl_colors.HexColor('#555555'), leading=12, alignment=TA_LEFT,
        spaceBefore=2, spaceAfter=2,
    )

    page_width = 495  # A4 minus margins (approx)

    for f in findings:
        accent_color = rl_colors.HexColor(_level_to_color(f.get('level', 'good')))

        # Row 1: Header bar with metric name and value
        header_cell = Paragraph(f['metric'], card_metric_style)
        value_cell = Paragraph(f['value'], card_value_style)

        header_table = Table(
            [[header_cell, value_cell]],
            colWidths=[page_width * 0.72, page_width * 0.28],
            rowHeights=[22],
        )
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), accent_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (0, 0), 10),
            ('RIGHTPADDING', (-1, -1), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ]))

        # Row 2: Evaluation text
        eval_para = Paragraph(f['evaluation'], card_eval_style)

        # Row 3: Recommendation with arrow prefix
        rec_para = Paragraph(f'<b>&gt;</b> {f["recommendation"]}', card_rec_style)

        body_table = Table(
            [[eval_para], [rec_para]],
            colWidths=[page_width],
        )
        body_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), rl_colors.HexColor('#F8F9FA')),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (0, 0), 6),
            ('BOTTOMPADDING', (-1, -1), (-1, -1), 6),
            ('LINEBELOW', (0, 0), (-1, 0), 0.3, rl_colors.HexColor('#E0E0E0')),
        ]))

        # Wrap header + body into one outer container
        card_table = Table(
            [[header_table], [body_table]],
            colWidths=[page_width],
        )
        card_table.setStyle(TableStyle([
            ('TOPPADDING', (0, 0), (-1, -1), 0),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ('BOX', (0, 0), (-1, -1), 0.5, rl_colors.HexColor('#D5D8DC')),
        ]))

        flowables.append(KeepTogether([card_table, Spacer(1, 8)]))

    # ── Conclusion Block ──────────────────────────────────────────────────
    conc_title = _t('title_conclusion', lang)

    # Conclusion status color and label
    status_map = {
        'pass':        (GREEN, 'PASS'),
        'conditional': (ORANGE, 'CONDITIONAL'),
        'fail':        (RED, 'FAIL'),
        'good':        (GREEN, 'GOOD'),
        'warn':        (ORANGE, 'WARNING'),
        'poor':        (RED, 'POOR'),
    }
    badge_color, badge_label = status_map.get(conclusion_status, (NEUTRAL, conclusion_status.upper()))

    badge_style = ParagraphStyle(
        'ConcBadge', fontName=PDF_FONT_BOLD, fontSize=10,
        textColor=rl_colors.white, leading=14, alignment=TA_LEFT,
    )
    body_conc_style = ParagraphStyle(
        'ConcBody', fontName=PDF_FONT_REGULAR, fontSize=9,
        textColor=rl_colors.HexColor('#2C3E50'), leading=13, alignment=TA_LEFT,
    )

    badge_para = Paragraph(badge_label, badge_style)
    conc_para = Paragraph(conclusion_text, body_conc_style)

    conc_table = Table(
        [[badge_para, conc_para]],
        colWidths=[80, page_width - 80],
    )
    conc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), badge_color),
        ('BACKGROUND', (1, 0), (1, 0), rl_colors.HexColor('#F8F9FA')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 0.5, rl_colors.HexColor('#D5D8DC')),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
    ]))
    flowables.append(KeepTogether([
        Spacer(1, 4),
        Paragraph(conc_title, StyleH2),
        Spacer(1, 4),
        conc_table,
    ]))

    return flowables


# ═══════════════════════════════════════════════════════════════════════════════
# COLOR UNIT RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_color_recommendations(mean_de00, reg_stats, csi_value,
                                    pass_thr, cond_thr, csi_good_thr, csi_warn_thr,
                                    lang='en'):
    """
    Generate findings for the Color Unit report.

    Returns:
        findings: list of dicts with 'metric', 'value', 'evaluation', 'recommendation', 'level'
        conclusion_text: str
        conclusion_status: str — 'pass' | 'conditional' | 'fail'
    """
    findings = []

    # ── 1. Mean Delta E ────────────────────────────────────────────────────
    pos = _relative_position(mean_de00, pass_thr, cond_thr, higher_is_better=False)
    de_eval_map = {
        'excellent': 'de_imperceptible',
        'good':      'de_slight',
        'marginal':  'de_noticeable',
        'poor':      'de_significant' if mean_de00 <= cond_thr * 2 else 'de_severe',
    }
    de_rec_map = {
        'excellent': 'de_rec_none',
        'good':      'de_rec_acceptable',
        'marginal':  'de_rec_check_dye',
        'poor':      'de_rec_investigate' if mean_de00 <= cond_thr * 2 else 'de_rec_reject',
    }
    findings.append({
        'metric': _t('mean_delta_e', lang),
        'value': f"{mean_de00:.2f}",
        'evaluation': _t(de_eval_map.get(pos, 'de_significant'), lang),
        'recommendation': _t(de_rec_map.get(pos, 'de_rec_reject'), lang),
        'level': pos,
    })

    # ── 2. Consistency (Std Dev of ΔE) ─────────────────────────────────────
    if reg_stats and len(reg_stats) > 1:
        import numpy as np
        all_de = [x['de00'] for x in reg_stats]
        std_dev = float(np.std(all_de))

        std_excellent = pass_thr * 0.25
        std_good = pass_thr * 0.5
        std_moderate = pass_thr * 1.0

        if std_dev <= std_excellent:
            s_eval, s_rec, s_lvl = 'std_excellent', 'std_rec_stable', 'excellent'
        elif std_dev <= std_good:
            s_eval, s_rec, s_lvl = 'std_good', 'std_rec_stable', 'good'
        elif std_dev <= std_moderate:
            s_eval, s_rec, s_lvl = 'std_moderate', 'std_rec_monitor', 'marginal'
        else:
            s_eval, s_rec, s_lvl = 'std_high', 'std_rec_check', 'poor'

        findings.append({
            'metric': _t('consistency', lang),
            'value': f"{std_dev:.2f}",
            'evaluation': _t(s_eval, lang),
            'recommendation': _t(s_rec, lang),
            'level': s_lvl,
        })

    # ── 3. CSI Score ───────────────────────────────────────────────────────
    csi_pos = _relative_position(csi_value, csi_good_thr, csi_warn_thr, higher_is_better=True)
    csi_eval_map = {'excellent': 'csi_excellent', 'good': 'csi_good',
                    'marginal': 'csi_marginal', 'poor': 'csi_poor'}
    csi_rec_map = {'excellent': 'csi_rec_approved', 'good': 'csi_rec_conditional',
                   'marginal': 'csi_rec_review', 'poor': 'csi_rec_reject'}
    findings.append({
        'metric': _t('csi_score', lang),
        'value': f"{csi_value:.2f}",
        'evaluation': _t(csi_eval_map[csi_pos], lang),
        'recommendation': _t(csi_rec_map[csi_pos], lang),
        'level': csi_pos,
    })

    # ── Conclusion ─────────────────────────────────────────────────────────
    if csi_pos == 'excellent' and pos in ('excellent', 'good'):
        conclusion_status = 'pass'
    elif csi_pos == 'poor' or pos == 'poor':
        conclusion_status = 'fail'
    else:
        conclusion_status = 'conditional'

    conclusion_text = _t(f'conclusion_{conclusion_status}', lang)
    return findings, conclusion_text, conclusion_status


# ═══════════════════════════════════════════════════════════════════════════════
# PATTERN UNIT RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_pattern_recommendations(composite_score, scores, structural_results,
                                      global_threshold, thresholds,
                                      lang='en'):
    """
    Generate findings for the Pattern Unit report.

    Returns:
        findings, conclusion_text, conclusion_status
    """
    findings = []

    # ── 1. Composite Score ─────────────────────────────────────────────────
    cond_thr = global_threshold * 0.85
    comp_pos = _relative_position(composite_score, global_threshold, cond_thr, higher_is_better=True)
    comp_eval_map = {'excellent': 'comp_excellent', 'good': 'comp_good',
                     'marginal': 'comp_marginal', 'poor': 'comp_poor'}
    comp_rec_map = {'excellent': 'comp_rec_optimal', 'good': 'comp_rec_monitor',
                    'marginal': 'comp_rec_calibrate', 'poor': 'comp_rec_stop'}
    findings.append({
        'metric': _t('composite_score', lang),
        'value': f"{composite_score:.1f}%",
        'evaluation': _t(comp_eval_map[comp_pos], lang),
        'recommendation': _t(comp_rec_map[comp_pos], lang),
        'level': comp_pos,
    })

    # ── 2. Structural Match ────────────────────────────────────────────────
    if structural_results and 'similarity_score' in structural_results:
        ss = structural_results['similarity_score']
        if ss >= 99.5:
            s_eval, s_rec, s_lvl = 'struct_identical', 'struct_rec_none', 'excellent'
        elif ss >= 97.0:
            s_eval, s_rec, s_lvl = 'struct_minor', 'struct_rec_tension', 'good'
        elif ss >= 90.0:
            s_eval, s_rec, s_lvl = 'struct_moderate', 'struct_rec_inspect', 'marginal'
        else:
            s_eval, s_rec, s_lvl = 'struct_severe', 'struct_rec_overhaul', 'poor'

        findings.append({
            'metric': _t('structural_match', lang),
            'value': f"{ss:.2f}%",
            'evaluation': _t(s_eval, lang),
            'recommendation': _t(s_rec, lang),
            'level': s_lvl,
        })

    # ── 3. Per-method weakest metric ───────────────────────────────────────
    if scores:
        worst_method = min(scores, key=scores.get)
        worst_score = scores[worst_method]
        method_thr = thresholds.get(worst_method, {})
        method_pass = float(method_thr.get('pass', global_threshold))

        if worst_score < method_pass:
            findings.append({
                'metric': _t('worst_metric', lang) + f": {worst_method}",
                'value': f"{worst_score:.1f}%",
                'evaluation': _t('worst_below_pass', lang),
                'recommendation': _t('worst_rec', lang),
                'level': 'poor',
            })

    # ── Conclusion ─────────────────────────────────────────────────────────
    if comp_pos == 'excellent':
        conclusion_status = 'pass'
    elif comp_pos == 'poor':
        conclusion_status = 'fail'
    else:
        conclusion_status = 'conditional'

    conclusion_text = _t(f'conclusion_{conclusion_status}', lang)
    return findings, conclusion_text, conclusion_status


# ═══════════════════════════════════════════════════════════════════════════════
# SINGLE IMAGE RECOMMENDATIONS
# ═══════════════════════════════════════════════════════════════════════════════

def generate_single_image_recommendations(measurements, lang='en'):
    """
    Generate findings for the Single Image report.

    Returns:
        findings, conclusion_text, conclusion_status
    """
    import numpy as np

    findings = []

    if not measurements or len(measurements) < 2:
        return findings, _t('conclusion_single_good', lang), 'good'

    labs = [m['lab'] for m in measurements]
    L_vals = [lab[0] for lab in labs]
    a_vals = [lab[1] for lab in labs]
    b_vals = [lab[2] for lab in labs]

    mean_L = float(np.mean(L_vals))
    std_L = float(np.std(L_vals))
    chroma_vals = [float(np.sqrt(a**2 + b**2)) for a, b in zip(a_vals, b_vals)]
    std_chroma = float(np.std(chroma_vals))

    rgbs = [m['rgb'] for m in measurements]
    mean_rgb = np.mean(rgbs, axis=0)

    # ── 1. Luminance Assessment ────────────────────────────────────────────
    if mean_L > 75:
        l_eval, l_rec, l_lvl = 'lum_bright', 'lum_rec_bright', 'marginal'
    elif mean_L > 35:
        l_eval, l_rec, l_lvl = 'lum_medium', 'lum_rec_medium', 'good'
    else:
        l_eval, l_rec, l_lvl = 'lum_dark', 'lum_rec_dark', 'marginal'

    findings.append({
        'metric': _t('luminance', lang),
        'value': f"{mean_L:.1f}",
        'evaluation': _t(l_eval, lang),
        'recommendation': _t(l_rec, lang),
        'level': l_lvl,
    })

    # ── 2. Chroma Spread ──────────────────────────────────────────────────
    if std_chroma < 2.0:
        c_eval, c_rec, c_lvl = 'chroma_narrow', 'chroma_rec_uniform', 'excellent'
    elif std_chroma < 5.0:
        c_eval, c_rec, c_lvl = 'chroma_moderate', 'chroma_rec_monitor', 'marginal'
    else:
        c_eval, c_rec, c_lvl = 'chroma_wide', 'chroma_rec_investigate', 'poor'

    findings.append({
        'metric': _t('chroma', lang),
        'value': f"{std_chroma:.2f}",
        'evaluation': _t(c_eval, lang),
        'recommendation': _t(c_rec, lang),
        'level': c_lvl,
    })

    # ── 3. Color Uniformity (L* std dev) ──────────────────────────────────
    if std_L < 2.0:
        u_eval, u_rec, u_lvl = 'uniformity_excellent', 'uniformity_rec_ok', 'excellent'
    elif std_L < 5.0:
        u_eval, u_rec, u_lvl = 'uniformity_good', 'uniformity_rec_check', 'marginal'
    else:
        u_eval, u_rec, u_lvl = 'uniformity_poor', 'uniformity_rec_fix', 'poor'

    findings.append({
        'metric': _t('color_uniformity', lang),
        'value': f"{std_L:.2f}",
        'evaluation': _t(u_eval, lang),
        'recommendation': _t(u_rec, lang),
        'level': u_lvl,
    })

    # ── 4. Dominant Channel ───────────────────────────────────────────────
    channel_names = ['R', 'G', 'B']
    dominant_idx = int(np.argmax(mean_rgb))
    dominant_name = channel_names[dominant_idx]
    dominant_val = float(mean_rgb[dominant_idx])

    dom_finding = {
        'en': f"Dominant channel is {dominant_name} ({dominant_val:.0f}/255). "
              f"RGB balance: R={mean_rgb[0]:.0f}, G={mean_rgb[1]:.0f}, B={mean_rgb[2]:.0f}.",
        'tr': f"Baskın kanal {dominant_name} ({dominant_val:.0f}/255). "
              f"RGB dengesi: R={mean_rgb[0]:.0f}, G={mean_rgb[1]:.0f}, B={mean_rgb[2]:.0f}."
    }
    dom_rec = {
        'en': 'Verify color balance matches target specification.',
        'tr': 'Renk dengesinin hedef spesifikasyonla eşleştiğini doğrulayın.'
    }

    findings.append({
        'metric': _t('dominant_channel', lang),
        'value': f"{dominant_name} ({dominant_val:.0f})",
        'evaluation': dom_finding.get(lang, dom_finding['en']),
        'recommendation': dom_rec.get(lang, dom_rec['en']),
        'level': 'good',
    })

    # ── Conclusion ─────────────────────────────────────────────────────────
    issues = 0
    if std_L >= 5.0:
        issues += 2
    elif std_L >= 2.0:
        issues += 1
    if std_chroma >= 5.0:
        issues += 2
    elif std_chroma >= 2.0:
        issues += 1

    if issues == 0:
        conclusion_status = 'good'
        conclusion_text = _t('conclusion_single_good', lang)
    elif issues <= 2:
        conclusion_status = 'warn'
        conclusion_text = _t('conclusion_single_warn', lang)
    else:
        conclusion_status = 'poor'
        conclusion_text = _t('conclusion_single_poor', lang)

    return findings, conclusion_text, conclusion_status
