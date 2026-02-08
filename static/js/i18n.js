/**
 * Internationalization (i18n) System for Textile QC System
 * Supports English and Turkish
 */

var I18n = {
    currentLang: 'en',

    translations: {
        en: {
            // Header
            'app.title': 'Textile QC System',
            'app.subtitle': 'Professional Color & Pattern Analysis',
            'source.code': 'Source Code',
            'download.source': 'Download Source',
            'download.desktop': 'Download for Windows',
            'datasheet': 'Datasheet',
            'download.datasheet': 'Download Datasheet',
            'english.datasheet': 'English Datasheet',
            'turkish.datasheet': 'Turkish Datasheet',
            'datasheet.modal.title': 'Technical Documentation',
            'datasheet.modal.description': 'The complete technical documentation is available in PDF format. Download the datasheet to access detailed information about system architecture, analysis methodology, mathematical foundations, and report interpretation guidelines.',
            'datasheet.modal.available': 'Available in English and Turkish',
            'download.pdf': 'Download PDF',

            // Sample Tests
            'samples': 'Samples',
            'sample.tests': 'Sample Tests',

            // Feedback
            'send.feedback': 'Send Feedback',
            'feedback.note': 'All fields are optional. You can submit feedback anonymously.',
            'send.anonymously': 'Send anonymously',
            'first.name': 'First Name',
            'last.name': 'Last Name',
            'page': 'Page',
            'email.address': 'Email Address',
            'phone.number': 'Phone Number',
            'feedback.type': 'Feedback Type',
            'feedback.type.note': 'Note',
            'feedback.type.complaint': 'Complaint',
            'feedback.type.report': 'Report',
            'feedback.type.suggestion': 'Suggestion',
            'feedback.type.question': 'Question',
            'feedback.type.other': 'Other',
            'message': 'Message',
            'attachment.note': 'If you would like to send attachments, it is preferable to send them via email to',
            'send': 'Send',
            'sending': 'Sending',
            'message.required': 'Message cannot be empty',
            'message.sent.successfully': 'Message sent successfully',
            'feedback.thank.you': 'Thank you for your cooperation. Your message will be taken into consideration and reviewed as soon as possible.',
            'send.new.feedback': 'Send New Feedback',
            'feedback.error': 'Failed to submit feedback',
            'loading.samples': 'Loading samples...',
            'preconfigured.tests': 'Pre-configured tests with generated reports',
            'run': 'Run',
            'ready': 'Ready',
            'ref.label': 'Ref',
            'sample.label': 'Sample',
            'samples.language.note.en': 'If you want the samples in Turkish, change the site language.',
            'samples.language.note.tr': 'If you want the samples in English, change the site language.',

            // Main Content
            'page.title': 'Image Quality Control Analysis',
            'page.subtitle': 'Upload reference and sample images to begin quality control analysis',
            'reference.image': 'Reference Image',
            'sample.image': 'Sample Image',
            'no.image': 'No image',
            'click.to.upload': 'Click to upload',

            // Shape Controls
            'circle': 'Circle',
            'square': 'Square',
            'rectangle': 'Rectangle',
            'pen': 'Pen (Freehand)',
            'pen.draw.hint': 'Click and drag on the image to draw a freehand region',
            'pen.close.warning': 'The freehand selection must be closed. Please draw a complete loop that connects back to the starting point.',
            'pen.not.closed': 'Selection Not Closed',
            'pen.drawing': 'Drawing...',
            'pen.complete': 'Freehand region set',
            'pen.clear': 'Clear Drawing',
            'pen.no.dimensions': 'Freehand mode — draw directly on the image',
            'rtt.btn': 'Test',
            'rtt.title': 'Ready-to-Test Images',
            'rtt.caption': 'Load built-in sample images for quick testing',
            'rtt.dual': 'Dual Mode (Reference + Sample)',
            'rtt.single': 'Single Image Mode',
            'rtt.pair': 'Pair',
            'rtt.loading': 'Loading image...',
            'rtt.loaded': 'Ready-to-test image loaded',
            'rtt.loaded.pair': 'Ready-to-test pair loaded',
            'process.entire.image': 'Process Entire Image',
            'single.image.mode': 'Single Image Analysis',
            'analyze.single.image': 'Analyze Single Image',
            'analyze.single.image.hint': 'Analyze only the sample image without comparison',
            'image.to.analyze': 'Image to be Analyzed',
            'size.px': 'Size (px):',
            'width.px': 'Width (px):',
            'height.px': 'Height (px):',
            'px': 'px',
            'region.hint': 'Click on image to place selection • Drag to move • Scroll to resize',
            'region.hint.html': '<ul class="hint-list"><li class="hint-item"><span class="hint-bullet"></span>Click on image to place selection</li><li class="hint-item"><span class="hint-bullet"></span>Drag to move</li><li class="hint-item"><span class="hint-bullet"></span>Scroll to resize</li></ul>',

            // Region Selection Settings
            'region.selection': 'Region Selection',
            'region.selection.desc': 'Configure the shape and dimensions of the analysis region cursor.',
            'region.shape': 'Selection Shape',
            'region.shape.hint': 'Choose the shape for region selection',
            'circle.diameter': 'Circle Diameter',
            'circle.diameter.hint': 'Diameter of the circular selection (20-500 px)',
            'square.size': 'Square Size',
            'square.size.hint': 'Size of the square selection (20-500 px)',
            'rectangle.width': 'Rectangle Width',
            'rectangle.width.hint': 'Width of the rectangle (20-500 px)',
            'rectangle.height': 'Rectangle Height',
            'rectangle.height.hint': 'Height of the rectangle (20-500 px)',
            'cursor.preview': 'Cursor Preview',

            // Buttons
            'advanced.settings': 'Advanced Settings',
            'start.processing': 'Start Processing',
            'delete.images': 'Delete Images',

            // Results
            'analysis.results': 'Analysis Results',
            'color.score': 'Color Score',
            'pattern.score': 'Pattern Score',
            'overall.score': 'Overall Score',
            'decision.accept': 'ACCEPT',
            'decision.reject': 'REJECT',
            'decision.conditional': 'CONDITIONAL ACCEPT',
            'download.report': 'Download Report (PDF)',
            'download.settings': 'Download Settings',

            // Loading
            'processing': 'Processing...',
            'please.wait': 'Please wait',
            'uploading.images': 'Uploading images...',
            'analyzing.colors': 'Analyzing colors...',
            'analyzing.patterns': 'Analyzing patterns...',
            'analyzing.repetition': 'Analyzing repetition...',
            'calculating.scores': 'Calculating scores...',
            'generating.report': 'Generating report...',
            'processing.complete': 'Processing complete!',
            'complete': 'Complete!',
            'preparing': 'Preparing...',
            'load.images': 'Load Images',
            'load.report': 'Load Report',
            'loading.sample.test': 'Loading Sample Test...',

            // Modal - Tabs
            'thresholds': 'Thresholds',
            'color.analysis': 'Color Analysis',
            'pattern.analysis': 'Pattern Analysis',
            'report.sections': 'Report Sections',
            'advanced.settings.title': 'Advanced Settings',
            'configure.parameters': 'Configure analysis parameters',

            // Modal - Thresholds
            'color.thresholds': 'Color Thresholds',
            'de.pass.threshold': 'ΔE Pass Threshold',
            'de.conditional.threshold': 'ΔE Conditional Threshold',
            'pattern.thresholds': 'Pattern Thresholds',
            'ssim.pass.threshold': 'SSIM Pass Threshold',
            'ssim.conditional.threshold': 'SSIM Conditional Threshold',
            'score.thresholds': 'Score Thresholds',
            'color.score.threshold': 'Color Score Threshold',
            'pattern.score.threshold': 'Pattern Score Threshold',
            'overall.score.threshold': 'Overall Score Threshold',

            // Modal - Color Analysis
            'color.difference.methods': 'Color Difference Methods',
            'use.cmc': 'Use CMC Color Difference',
            'cmc.ratio': 'CMC l:c Ratio',
            'acceptability': 'Acceptability',
            'perceptibility': 'Perceptibility',
            'spectrophotometer.settings': 'Spectrophotometer Settings',
            'observer.angle': 'Observer Angle',
            'standard.observer': 'Standard Observer',
            'geometry.mode': 'Geometry Mode',

            // Modal - Pattern Analysis
            'texture.parameters': 'Texture Parameters',

            'wavelet.type': 'Wavelet Type',
            'wavelet.levels': 'Wavelet Levels',
            'pattern.repetition': 'Pattern Repetition',
            'pattern.min.area': 'Pattern Min Area (px)',
            'pattern.max.area': 'Pattern Max Area (px)',
            'keypoint.detector': 'Keypoint Detector',
            'fast': 'Fast',
            'accurate': 'Accurate',

            // Modal - Report Sections
            'color.unit': 'Color Unit',
            'pattern.unit': 'Pattern Unit',
            'pattern.repetition.unit': 'Pattern Repetition',
            'spectrophotometer': 'Spectrophotometer',
            'analysis.settings.page': 'Analysis Settings Page',
            'operator.info': 'Operator Info',
            'operator.name': 'Operator Name',
            'operator': 'Operator',

            // Report Language
            'report.language': 'Report Language',
            'report.language.desc': 'Select the language for the generated PDF report. Technical terms will be kept in English inside parentheses.',
            'report.lang.en.desc': 'Report in English',
            'report.lang.tr.desc': 'Report in Turkish',

            // New Settings - General
            'general': 'General',
            'settings.intro': 'Configure general analysis settings and operator information.',
            'operator.info.desc': 'Information that appears in the generated report.',
            'operator.name.hint': 'Name shown on report header',
            'timezone': 'Time Zone',
            'timezone.hint': 'Time zone for report timestamps',
            'sampling.settings': 'Sampling Settings',
            'sampling.settings.desc': 'Control how sample points are distributed on the image for color analysis.',
            'num.sample.points': 'Sample Points',
            'num.sample.points.hint': 'Number of measurement points (3-20)',
            'sampling.mode': 'Sampling Mode',
            'sampling.mode.hint': 'Random generates new points each run, Manual lets you choose',
            'sampling.random': 'Random',
            'sampling.manual': 'Manual',
            'select.points.on.image': 'Select points on the image',
            'no.points.selected': 'No points selected',
            'points.selected': 'points selected',
            'select.sample.points': 'Select Sample Points',
            'select.points': 'Select Points',
            'complete.rest.randomly': 'Complete the rest randomly',
            'click.to.select.points': 'Click on the images to select measurement points for color analysis',
            'selected': 'Selected',
            'click.anywhere.hint': 'Click anywhere on either image to place a sample point. Points are mirrored on both images.',
            'point.outside.roi': 'Point must be within the selected region',
            'all.points.selected': 'All points selected! Click Confirm to save.',
            'all.points.already.selected': 'All points are already selected.',
            'upload.sample.first': 'Please upload a sample image before generating points.',
            'upload.both.images': 'Please upload both reference and sample images before generating points.',
            'point.outside.region': 'Point must be inside the selected analysis region. Please click within the highlighted area.',
            'invalid.point': 'Invalid Point',
            'undo.last': 'Undo Last',
            'clear.all': 'Clear All',
            'confirm.selection': 'Confirm Selection',
            'color.analysis.disabled.hint': 'Color Analysis must be enabled to select sample points.',
            'scoring.multipliers': 'Scoring Multipliers',
            'scoring.multipliers.desc': 'Adjust how scores are calculated from measurements.',
            'color.score.multiplier': 'Color Score Multiplier',
            'color.score.multiplier.hint': 'Higher = more sensitive to ΔE',
            'uniformity.multiplier': 'Uniformity Multiplier',
            'uniformity.multiplier.hint': 'Higher = stricter uniformity check',

            // New Settings - Thresholds
            'thresholds.intro': 'Set pass/fail thresholds for quality decisions. Values below Pass = ACCEPT, between Pass and Conditional = CONDITIONAL, above Conditional = REJECT.',
            'color.thresholds.desc': 'Industry standard: ΔE < 1.0 = imperceptible, 1-2 = close inspection, 2-3.5 = noticeable.',
            'de.pass.hint': 'Below this = PASS',
            'de.conditional.hint': 'Above this = FAIL',
            'pattern.thresholds.desc': 'SSIM ranges 0-1. Higher = more similar. Industry typical: 0.90-0.98.',
            'ssim.pass.hint': 'Above this = PASS',
            'ssim.conditional.hint': 'Below this = FAIL',
            'score.thresholds.desc': 'Minimum scores (0-100) required for passing quality control.',
            'color.score.threshold.hint': 'Minimum acceptable color score',
            'pattern.score.threshold.hint': 'Minimum acceptable pattern score',
            'overall.score.threshold.hint': 'Final pass/fail decision threshold',
            'lab.thresholds': 'Lab* Thresholds',
            'lab.thresholds.desc': 'Define component-level thresholds for Lab* quality assessment.',
            'lab.l.threshold': 'L* Threshold (Lightness)',
            'lab.l.hint': 'Max acceptable lightness difference',
            'lab.ab.threshold': 'a*/b* Threshold (Chroma)',
            'lab.ab.hint': 'Max acceptable chroma difference',
            'lab.thresh.dl': 'ΔL* Threshold',
            'lab.thresh.dl.desc': 'Lightness tolerance',
            'lab.thresh.da': 'Δa* Threshold',
            'lab.thresh.da.desc': 'Red-green axis tolerance',
            'lab.thresh.db': 'Δb* Threshold',
            'lab.thresh.db.desc': 'Yellow-blue axis tolerance',
            'lab.thresh.mag': 'Magnitude Threshold',
            'lab.thresh.mag.desc': 'Combined ΔLab vector magnitude',

            // New Settings - Color Analysis
            'color.intro': 'Configure color measurement methods and spectrophotometer simulation settings.',
            'color.methods.desc': 'ΔE2000 is always calculated. CMC is optional for textile industry compliance.',
            'use.cmc.hint': 'CMC(l:c) formula for textile industry',
            'cmc.ratio.hint': '2:1 for acceptability, 1:1 for perceptibility',
            'spectro.sim.desc': 'Simulates professional spectrophotometer measurement conditions.',
            'observer.angle.hint': 'CIE standard observer',
            'geometry.mode.hint': 'Measurement geometry configuration',
            'whiteness.settings': 'Whiteness & Yellowness',
            'whiteness.desc': 'Thresholds for white fabric evaluation (ISO brightness standards).',
            'whiteness.min': 'Minimum Whiteness Index',
            'whiteness.min.hint': 'CIE Whiteness Index threshold',
            'yellowness.max': 'Maximum Yellowness Index',
            'yellowness.max.hint': 'ASTM E313 Yellowness threshold',

            // New Settings - Pattern Analysis
            'pattern.intro': 'Configure texture analysis algorithms and pattern detection parameters.',

            'wavelet.settings': 'Wavelet Transform',
            'wavelet.desc': 'Multi-resolution frequency analysis of patterns.',
            'wavelet.type.hint': 'Wavelet basis function',
            'wavelet.levels.hint': 'Number of decomposition levels (1-5)',
            'pattern.detection.desc': 'Settings for finding and matching repeating patterns.',
            'keypoint.hint': 'Feature detection algorithm',
            'pattern.min.hint': 'Minimum detected pattern size',
            'pattern.max.hint': 'Maximum detected pattern size',
            'pattern.similarity': 'Similarity Threshold',
            'pattern.similarity.hint': 'Min similarity for pattern matching',
            'defect.detection': 'Defect Detection',
            'defect.desc': 'Settings for detecting anomalies and defects.',
            'defect.min.area': 'Min Defect Area (px)',
            'defect.min.hint': 'Minimum size to flag as defect',
            'saliency.strength': 'Saliency Strength',
            'saliency.hint': 'Anomaly detection sensitivity',

            // New Settings - Report Sections
            'report.intro': 'Choose which sections to include in the generated PDF report.',
            'main.sections': 'Main Report Sections',
            'main.sections.desc': 'Primary analysis sections in the report.',
            'color.unit.hint': 'ΔE, Lab*, color measurements',
            'pattern.unit.hint': 'SSIM, texture, symmetry analysis',
            'pattern.rep.hint': 'Repeat detection, spatial analysis',
            'spectro.hint': 'Simulated instrument readings',
            'settings.page.hint': 'Include all settings used in analysis',
            'color.subsections': 'Color Unit Sub-sections',
            'color.subsections.desc': 'Fine-tune color analysis report content.',
            'color.measurements': 'Color Measurements',
            'color.difference': 'Color Difference',
            'color.statistical': 'Statistical Analysis',
            'color.visual.diff': 'Visual Difference Map',
            'color.lab.detailed': 'Detailed Lab* Analysis',
            'color.recommendations': 'Recommendations',
            'pattern.subsections': 'Pattern Unit Sub-sections',
            'pattern.subsections.desc': 'Fine-tune pattern analysis report content.',
            'pattern.ssim': 'SSIM Analysis',
            'pattern.symmetry': 'Symmetry Analysis',
            'pattern.edge': 'Edge Detection',
            'pattern.advanced': 'Advanced Analysis',

            // Modal - Buttons
            'reset.to.defaults': 'Reset to Defaults',
            'cancel': 'Cancel',
            'apply.settings': 'Apply Settings',

            // Help Dialog
            'format.information': 'Format Information',
            'python.script': 'Python Script (.py)',
            'jupyter.notebook': 'Jupyter Notebook (.ipynb)',
            'download.this.format': 'Download this format',
            'learn.more': 'Learn more',

            // GitHub
            'github.browse.project': 'Browse the project on GitHub',
            'github.view.repository': 'View repository and documentation',
            'github.description': 'Access the complete source code, documentation, and project files on GitHub. The repository contains all the code, README files, and resources needed to understand and use the Textile QC System.',
            'github.read.readme': 'Please read the README file on the GitHub repository for detailed information about the project, installation instructions, and usage guidelines.',
            'github.under.construction': 'This project is under construction and actively being developed. New features and improvements are added regularly.',
            'github.inquiries.title': 'For Inquiries or Suggestions',
            'github.feedback.panel': 'Pull the feedback panel from the left side of the screen and fill out the survey',
            'github.visit.repository': 'Visit GitHub Repository',

            // Errors & Messages
            'error.reading.file': 'Error reading file',
            'please.upload.both': 'Please upload both reference and sample images',
            'please.upload.image': 'Please upload an image to analyze',
            'delete.confirm': 'Are you sure you want to delete all uploaded images?',
            'delete.image': 'Delete Image',
            'delete.image.confirm': 'Are you sure you want to delete the {image}?',
            'failed.to.load.samples': 'Failed to load samples',

            // Development Modal
            'development.title': 'Website Under Development',
            'development.message': 'This website is currently under development.',
            'development.view.samples': 'You can view the results through the ready-made samples from the Samples section on the left side of the screen.',
            'development.test.new': 'Or, to test new samples, download the source code (Python) and test it directly in the Google Colab environment.',
            'development.logos.note': 'To obtain full results, these logos must be added to Google Colab with the same filenames.',
            'development.download.logo': 'Download logo',
            'development.go.colab': 'Go to Google Colab',
            'development.download.code': 'Download the code available on the homepage',
            'development.source.code': 'Source Code',
            'development.close': 'Close',
            'development.copy.code': 'Copy Code',
            'development.copied': 'Copied!',
            'development.copy.instruction': 'Copy the code and paste it into the Google Colab environment.',

            // Footer
            'copyright': '© 2026 Textile Engineering Solutions | ',
            'contact.title': 'Contact',

            // Progress Steps
            'upload.images': 'Upload Images',
            'color.analysis.step': 'Color Analysis',
            'pattern.analysis.step': 'Pattern Analysis',
            'pattern.repetition.step': 'Pattern Repetition',
            'calculate.scores': 'Calculate Scores',
            'generate.report': 'Generate Report',
            'step.failed': 'Step failed',
            'analysis.failed': 'Analysis failed',

            // Source Code Help
            'what.is.python': 'What is a Python (.py) file?',
            'what.is.notebook': 'What is a Jupyter Notebook (.ipynb)?',
            'best.for': 'Best for:',
            'local.development': 'Local development, integration into existing projects, or running on servers.',
            'google.colab': 'Google Colab, quick experiments, learning, or when you don\'t want to set up a local environment.',
            'python.script.desc': 'A <strong>.py file</strong> is a standard Python script that can be executed in any Python environment.',
            'python.works.with': 'Works with Python 3.7 or higher',
            'python.run.directly': 'Run directly from command line or any IDE',
            'python.ideal.for': 'Ideal for local development and integration',
            'python.can.import': 'Can be imported as a module in your projects',
            'python.best.for': 'Local development, integration into existing projects, or running on servers.',
            'notebook.desc': 'A <strong>.ipynb file</strong> is an interactive notebook format perfect for step-by-step analysis and visualization.',
            'notebook.runs.colab': 'Runs directly in <strong>Google Colab</strong> — no setup needed!',
            'notebook.interactive': 'Interactive cells with explanations',
            'notebook.easy.modify': 'Easy to modify and experiment with',
            'notebook.visualizations': 'Visualizations are displayed inline',
            'notebook.best.for': 'Google Colab, quick experiments, learning, or when you don\'t want to set up a local environment.',

            // Language
            'language': 'Language',
            'english': 'English',
            'turkish': 'Turkish',

            // Analysis Configuration Modal
            'analysis.configuration': 'Analysis Configuration',
            'fine.tune.parameters': 'Fine-tune quality control parameters',
            'operator.information': 'Operator Information',
            'details.shown.report': 'Details shown on the generated report.',
            'operator.name.label': 'Operator Name',
            'operator.name.desc': 'Name of the person conducting analysis',
            'timezone.offset': 'Timezone Offset (UTC)',
            'timezone.offset.desc': 'Hours to adjust report timestamp',
            'selection.region': 'Selection Region',
            'selection.region.desc': 'Define the shape and dimensions of the analysis region.',
            'region.shape.label': 'Region Shape',
            'region.shape.desc': 'Select the shape for region selection',
            'dimensions': 'Dimensions',
            'dimensions.desc': 'Specify region size in pixels',
            'diameter.px': 'Diameter (px)',
            'side.length.px': 'Side Length (px)',
            'width.px': 'Width (px)',
            'height.px': 'Height (px)',
            'single.image.config': 'Single Image Configuration',
            'single.image.config.desc': 'Configure analysis implementation for Single Image Mode.',
            'sampling.configuration': 'Sampling Configuration',
            'sampling.count': 'Sampling Count',
            'points.to.measure': 'Points to measure',
            'select.points': 'Select Points',
            'complete.randomly': 'Complete the rest randomly',
            'selected.count': 'Selected',
            'illuminant.settings': 'Illuminant Settings',
            'single.image.unit': 'Single Image Unit',
            'report.language': 'Report Language',
            'report.language.desc': 'Language used in generated PDF reports',

            // Color Unit Tab
            'color.scoring.method': 'Color Scoring Method',
            'color.scoring.method.desc': 'Select which metric determines the Color Score, Pass/Conditional/Fail decision, and report cover display.',
            'scoring.basis': 'Scoring Basis',
            'scoring.basis.desc': 'Determines the primary color score',
            'thresholds.delta.e': 'Thresholds (Delta E 2000)',
            'define.pass.fail': 'Define pass/fail criteria for color difference.',
            'pass.threshold': 'Pass Threshold',
            'values.below.accepted': 'Values below this are accepted',
            'conditional.threshold': 'Conditional Threshold',
            'values.below.warning': 'Values below this are warning (if above pass)',
            'global.acceptance': 'Global Acceptance',
            'overall.color.score': 'Overall image color score threshold',
            'csi.thresholds': 'CSI Thresholds',
            'csi.thresholds.desc': 'Define color thresholds for the Color Similarity Index.',
            'csi.good.threshold': 'CSI Good Threshold',
            'above.this.green': 'Above this = Green',
            'csi.warning.threshold': 'CSI Warning Threshold',
            'above.this.orange': 'Above this = Orange',
            'sampling.config.desc': 'Configure how analysis points are selected for Color Analysis.',
            'target.points.max': 'Target number of points (max 100)',
            'incomplete': 'Incomplete',
            'complete': 'Complete',
            'partial': 'Partial',
            'manual': 'Manual',
            'random': 'Random',
            'selected.label': 'Selected',
            'single.report.sections.desc': 'Select sections to include in the Single Image report.',

            // Pattern Unit Tab
            'pattern.scoring.method': 'Pattern Scoring Method',
            'pattern.scoring.method.desc': 'Select which metric determines the Pattern Score on the report cover and UI.',
            'pattern.scoring.basis.desc': 'Determines the primary pattern score',
            'method.thresholds': 'Method Thresholds (Pass / Conditional)',
            'define.similarity.scores': 'Define similarity scores (0-100%) for pattern analysis.',
            'structural.ssim': 'Structural SSIM',
            'structural.match': 'Structural Match',
            'pass.conditional': 'Pass / Conditional',
            'gradient.similarity': 'Gradient Similarity',
            'phase.correlation': 'Phase Correlation',
            'global.pattern.score': 'Global Pattern Score',
            'overall.pass.threshold': 'Overall pass threshold',

            // Illuminant Settings Tab
            'global.report.illuminant': 'Global Report Illuminant',
            'select.primary.illuminant': 'Select the primary illuminant used for the entire report.',
            'primary.illuminant': 'Primary Illuminant',
            'used.standard.calc': 'Used for standard calculations',
            'illuminant.test.selection': 'Illuminant Test Selection',
            'enable.illuminants.desc': 'Enable illuminants for comparative color testing (displayed in Color Unit only).',
            'comparative.illuminants': 'Comparative Illuminants',

            // Report Sections Tab
            'color.unit.report.sections': 'Color Unit Report Sections',
            'select.components.color': 'Select components for the Color Unit section.',
            'color.spaces': 'Color Spaces',
            'rgb.values': 'RGB Values',
            'lab.values': 'Lab* Values',
            'xyz.values': 'XYZ Values',
            'cmyk.values': 'CMYK Values',
            'diff.metrics': 'Diff Metrics',
            'statistics': 'Statistics',
            'detailed.lab': 'Detailed Lab',
            'visualizations': 'Visualizations',
            'spectral.proxy': 'Spectral Proxy',
            'rgb.histograms': 'RGB Histograms',
            'visual.diff': 'Visual Diff',
            'illuminant.analysis': 'Illuminant Analysis',
            'recommendations': 'Recommendations',
            'pattern.unit.methods': 'Pattern Unit: Enabled Methods',
            'select.pattern.algorithms': 'Select which pattern algorithms to run and include.',
            'structural.difference': 'Structural Difference',
            'fourier.domain.analysis': 'Fourier Domain Analysis',
            'glcm.texture.analysis': 'GLCM Texture Analysis',
            'pattern.unit.boundary': 'Pattern Unit: Boundary & Report',
            'gradient.boundary': 'Gradient Boundary',
            'phase.boundary': 'Phase Boundary',
            'summary': 'Summary',
            'conclusion': 'Conclusion',

            // Detailed Results Panel
            'rpt.report.summary': 'Report Summary',
            'rpt.color.scoring': 'Color Scoring',
            'rpt.pattern.scoring': 'Pattern Scoring',
            'rpt.csi.color.similarity': 'CSI (Color Similarity)',
            'rpt.mean.de2000': 'Mean ΔE 2000',
            'rpt.report.size': 'Report Size',
            'rpt.structural.change': 'Structural Change',
            'rpt.color.analysis.details': 'Color Analysis Details',
            'rpt.pattern.analysis.details': 'Pattern Analysis Details',
            'rpt.texture.frequency': 'Texture & Frequency Analysis',
            'rpt.single.image.analysis': 'Single Image Analysis',
            'rpt.mean.de00': 'Mean ΔE00',
            'rpt.method': 'Method',
            'rpt.status': 'Status',
            'rpt.composite': 'Composite',
            'rpt.structural': 'Structural',
            'rpt.regional.color.metrics': 'Regional Color Metrics',
            'rpt.individual.method.scores': 'Individual Method Scores',
            'rpt.structural.difference': 'Structural Difference',
            'rpt.similarity.score': 'Similarity Score',
            'rpt.change.percentage': 'Change Percentage',
            'rpt.verdict': 'Verdict',
            'rpt.difference.maps': 'Difference Maps',
            'rpt.boundary.detection': 'Boundary Detection',
            'rpt.structural.analysis': 'Structural Analysis',
            'rpt.position': 'Position',
            'rpt.ref.lab': 'Ref L*a*b*',
            'rpt.sam.lab': 'Sam L*a*b*',
            'rpt.mode': 'Mode',
            'rpt.single.image.mode': 'Single Image Analysis',
            'rpt.de.heatmap': 'ΔE Heatmap',
            'rpt.de.heatmap.caption': 'Pixel-level color difference heatmap between reference and sample.',
            'rpt.spectral': 'Spectral Distribution (Proxy)',
            'rpt.spectral.caption': 'Approximated spectral reflectance curves from mean RGB values.',
            'rpt.histograms': 'RGB Histograms',
            'rpt.histograms.caption': 'Side-by-side RGB channel distribution for Reference and Sample.',
            'rpt.lab.scatter': 'a* vs b* Chromaticity Scatter',
            'rpt.lab.scatter.caption': 'Reference vs Sample chromaticity coordinates in the a*b* plane.',
            'rpt.lab.bars': 'Lab Components – Mean',
            'rpt.lab.bars.caption': 'Mean L*, a*, b* comparison between Reference and Sample.',
            'rpt.ssim.map': 'SSIM Difference Map',
            'rpt.ssim.map.caption': 'Structural SSIM difference — hot regions indicate structural dissimilarity.',
            'rpt.gradient.map': 'Gradient Similarity Map',
            'rpt.gradient.map.caption': 'Gradient magnitude difference — highlights edge/texture mismatches.',
            'rpt.phase.map': 'Phase Correlation Map',
            'rpt.phase.map.caption': 'Phase-based difference — detects spatial shifts and misalignment.',
            'rpt.gradient.boundary': 'Gradient Boundary',
            'rpt.gradient.boundary.caption': 'Significant gradient difference regions outlined on the sample.',
            'rpt.gradient.filled': 'Gradient Filled',
            'rpt.gradient.filled.caption': 'Gradient difference regions with filled red overlay.',
            'rpt.phase.boundary': 'Phase Boundary',
            'rpt.phase.boundary.caption': 'Significant phase difference regions outlined on the sample.',
            'rpt.phase.filled': 'Phase Filled',
            'rpt.phase.filled.caption': 'Phase difference regions with filled red overlay.',
            'rpt.multi.method': 'Multi-Method Comparison',
            'rpt.multi.method.caption': 'Gradient magnitude, combined methods, and noise-filtered difference maps.',
            'rpt.pure.diff': 'Pure Differences',
            'rpt.pure.diff.caption': 'Isolated pure difference regions (red on black).',
            'rpt.fourier': 'Fourier Spectrum (FFT)',
            'rpt.fourier.caption': '2D FFT magnitude spectrum showing frequency-domain characteristics.',
            'rpt.glcm': 'GLCM Texture Heatmap',
            'rpt.glcm.caption': 'Gray-Level Co-occurrence Matrix texture feature comparison heatmaps.',
            'rpt.histogram.single': 'RGB Histogram',
            'rpt.histogram.single.caption': 'RGB channel distribution of the sample image.',
            'rpt.spectral.single': 'Spectral Distribution (Proxy)',
            'rpt.spectral.single.caption': 'Approximated spectral reflectance curve from mean RGB values.',
            'rpt.fourier.single': 'Fourier Spectrum',
            'rpt.fourier.single.caption': '2D FFT magnitude spectrum showing frequency-domain characteristics.',
            'rpt.illuminant.analysis': 'Illuminant Analysis',
            'rpt.illuminant': 'Illuminant',
            'rpt.color.comparison': 'Color Comparison',
            'rpt.color.recommendations': 'Color — Key Findings & Recommendations',
            'rpt.pattern.recommendations': 'Pattern — Key Findings & Recommendations',
            'rpt.reference': 'Reference',
            'rpt.sample': 'Sample',
            'rpt.de.summary.stats': '\u0394E Summary Statistics',
            'rpt.metric': 'Metric',
            'rpt.average': 'Average',
            'rpt.std.dev': 'Std Dev',
            'rpt.min': 'Min',
            'rpt.max': 'Max'
        },

        tr: {
            // Header
            'app.title': 'Tekstil Kalite Kontrol Sistemi',
            'app.subtitle': 'Profesyonel Renk ve Desen Analizi',
            'source.code': 'Kaynak Kodu',
            'download.source': 'Kaynak İndir',
            'download.desktop': 'Windows için İndir',
            'datasheet': 'Veri Sayfası',
            'download.datasheet': 'Veri Sayfasını İndir',
            'english.datasheet': 'İngilizce Veri Sayfası',
            'turkish.datasheet': 'Türkçe Veri Sayfası',
            'datasheet.modal.title': 'Teknik Dokümantasyon',
            'datasheet.modal.description': 'Eksiksiz teknik dokümantasyon PDF formatında mevcuttur. Sistem mimarisi, analiz metodolojisi, matematiksel temeller ve rapor yorumlama kılavuzları hakkında ayrıntılı bilgilere erişmek için veri sayfasını indirin.',
            'datasheet.modal.available': 'İngilizce ve Türkçe olarak mevcuttur',
            'download.pdf': 'PDF İndir',

            // Sample Tests
            'samples': 'Örnekler',
            'sample.tests': 'Örnek Testler',

            // Feedback
            'send.feedback': 'Geri Bildirim Gönder',
            'feedback.note': 'Tüm alanlar isteğe bağlıdır. Anonim olarak geri bildirim gönderebilirsiniz.',
            'send.anonymously': 'Anonim gönder',
            'first.name': 'Ad',
            'last.name': 'Soyad',
            'page': 'Sayfa',
            'email.address': 'E-posta Adresi',
            'phone.number': 'Telefon Numarası',
            'feedback.type': 'Geri Bildirim Türü',
            'feedback.type.note': 'Not',
            'feedback.type.complaint': 'Şikayet',
            'feedback.type.report': 'Rapor',
            'feedback.type.suggestion': 'Öneri',
            'feedback.type.question': 'Soru',
            'feedback.type.other': 'Diğer',
            'message': 'Mesaj',
            'attachment.note': 'Ek göndermek isterseniz, e-posta ile göndermeniz tercih edilir:',
            'send': 'Gönder',
            'sending': 'Gönderiliyor',
            'message.required': 'Mesaj boş olamaz',
            'message.sent.successfully': 'Mesaj başarıyla gönderildi',
            'feedback.thank.you': 'İş birliğiniz için teşekkür ederiz. Mesajınız dikkate alınacak ve en kısa sürede incelenecektir.',
            'send.new.feedback': 'Yeni Geri Bildirim Gönder',
            'feedback.error': 'Geri bildirim gönderilemedi',
            'loading.samples': 'Örnekler yükleniyor...',
            'preconfigured.tests': 'Oluşturulmuş raporlarla önceden yapılandırılmış testler',
            'run': 'Çalıştır',
            'ready': 'Hazır',
            'ref.label': 'Referans',
            'sample.label': 'Örnek',
            'samples.language.note.en': 'Örnekleri Türkçe istiyorsanız, site dilini değiştirin.',
            'samples.language.note.tr': 'Örnekleri İngilizce istiyorsanız, site dilini değiştirin.',

            // Main Content
            'page.title': 'Görüntü Kalite Kontrol Analizi',
            'page.subtitle': 'Kalite kontrol analizine başlamak için referans ve örnek görüntüleri yükleyin',
            'reference.image': 'Referans Görüntü',
            'sample.image': 'Örnek Görüntü',
            'no.image': 'Görüntü yok',
            'click.to.upload': 'Yüklemek için tıklayın',

            // Shape Controls
            'circle': 'Daire',
            'square': 'Kare',
            'rectangle': 'Dikdörtgen',
            'pen': 'Kalem (Serbest)',
            'pen.draw.hint': 'Serbest bölge çizmek için görüntü üzerinde tıklayıp sürükleyin',
            'pen.close.warning': 'Serbest seçim kapatılmalıdır. Lütfen başlangıç noktasına geri bağlanan tam bir döngü çizin.',
            'pen.not.closed': 'Seçim Kapatılmadı',
            'pen.drawing': 'Çiziliyor...',
            'pen.complete': 'Serbest bölge ayarlandı',
            'pen.clear': 'Çizimi Temizle',
            'pen.no.dimensions': 'Serbest mod \u2014 do\u011frudan g\u00f6r\u00fcnt\u00fc \u00fczerinde \u00e7izin',
            'rtt.btn': 'Test',
            'rtt.title': 'Teste Haz\u0131r G\u00f6r\u00fcnt\u00fcler',
            'rtt.caption': 'H\u0131zl\u0131 test i\u00e7in yerle\u015fik \u00f6rnek g\u00f6r\u00fcnt\u00fcleri y\u00fckleyin',
            'rtt.dual': '\u00c7ift Mod (Referans + \u00d6rnek)',
            'rtt.single': 'Tek G\u00f6r\u00fcnt\u00fc Modu',
            'rtt.pair': '\u00c7ift',
            'rtt.loading': 'G\u00f6r\u00fcnt\u00fc y\u00fckleniyor...',
            'rtt.loaded': 'Teste haz\u0131r g\u00f6r\u00fcnt\u00fc y\u00fcklendi',
            'rtt.loaded.pair': 'Teste haz\u0131r \u00e7ift y\u00fcklendi',
            'process.entire.image': 'Tüm Görüntüyü İşle',
            'single.image.mode': 'Tek Görüntü Analizi',
            'analyze.single.image': 'Tek Görüntü Analiz Et',
            'analyze.single.image.hint': 'Karşılaştırma olmadan yalnızca örnek görüntüyü analiz et',
            'image.to.analyze': 'Analiz Edilecek Görüntü',
            'size.px': 'Boyut (px):',
            'width.px': 'Genişlik (px):',
            'height.px': 'Yükseklik (px):',
            'px': 'px',
            'region.hint': 'Seçim yerleştirmek için görüntüye tıklayın • Taşımak için sürükleyin • Boyutlandırmak için kaydırın',
            'region.hint.html': '<ul class="hint-list"><li class="hint-item"><span class="hint-bullet"></span>Seçim yerleştirmek için görüntüye tıklayın</li><li class="hint-item"><span class="hint-bullet"></span>Taşımak için sürükleyin</li><li class="hint-item"><span class="hint-bullet"></span>Boyutlandırmak için kaydırın</li></ul>',

            // Region Selection Settings
            'region.selection': 'Bölge Seçimi',
            'region.selection.desc': 'Analiz bölgesi imlecinin şeklini ve boyutlarını yapılandırın.',
            'region.shape': 'Seçim Şekli',
            'region.shape.hint': 'Bölge seçimi için şekli seçin',
            'circle.diameter': 'Daire Çapı',
            'circle.diameter.hint': 'Dairesel seçimin çapı (20-500 px)',
            'square.size': 'Kare Boyutu',
            'square.size.hint': 'Kare seçimin boyutu (20-500 px)',
            'rectangle.width': 'Dikdörtgen Genişliği',
            'rectangle.width.hint': 'Dikdörtgenin genişliği (20-500 px)',
            'rectangle.height': 'Dikdörtgen Yüksekliği',
            'rectangle.height.hint': 'Dikdörtgenin yüksekliği (20-500 px)',
            'cursor.preview': 'İmleç Önizleme',

            // Buttons
            'advanced.settings': 'Gelişmiş Ayarlar',
            'start.processing': 'İşlemeyi Başlat',
            'delete.images': 'Görüntüleri Sil',

            // Results
            'analysis.results': 'Analiz Sonuçları',
            'color.score': 'Renk Skoru',
            'pattern.score': 'Desen Skoru',
            'overall.score': 'Genel Skor',
            'decision.accept': 'KABUL',
            'decision.reject': 'RED',
            'decision.conditional': 'KOŞULLU KABUL',
            'download.report': 'Raporu İndir (PDF)',
            'download.settings': 'Ayarları İndir',

            // Loading
            'processing': 'İşleniyor...',
            'please.wait': 'Lütfen bekleyin',
            'uploading.images': 'Görüntüler yükleniyor...',
            'analyzing.colors': 'Renkler analiz ediliyor...',
            'analyzing.patterns': 'Desenler analiz ediliyor...',
            'analyzing.repetition': 'Tekrar analiz ediliyor...',
            'calculating.scores': 'Skorlar hesaplanıyor...',
            'generating.report': 'Rapor oluşturuluyor...',
            'processing.complete': 'İşlem tamamlandı!',
            'complete': 'Tamamlandı!',
            'preparing': 'Hazırlanıyor...',
            'load.images': 'Görüntüleri Yükle',
            'load.report': 'Raporu Yükle',
            'loading.sample.test': 'Örnek Test Yükleniyor...',

            // Modal - Tabs
            'thresholds': 'Eşikler',
            'color.analysis': 'Renk Analizi',
            'pattern.analysis': 'Desen Analizi',
            'report.sections': 'Rapor Bölümleri',
            'advanced.settings.title': 'Gelişmiş Ayarlar',
            'configure.parameters': 'Analiz parametrelerini yapılandır',

            // Modal - Thresholds
            'color.thresholds': 'Renk Eşikleri',
            'de.pass.threshold': 'ΔE Geçiş Eşiği',
            'de.conditional.threshold': 'ΔE Koşullu Eşiği',
            'pattern.thresholds': 'Desen Eşikleri',
            'ssim.pass.threshold': 'SSIM Geçiş Eşiği',
            'ssim.conditional.threshold': 'SSIM Koşullu Eşiği',
            'score.thresholds': 'Skor Eşikleri',
            'color.score.threshold': 'Renk Skoru Eşiği',
            'pattern.score.threshold': 'Desen Skoru Eşiği',
            'overall.score.threshold': 'Genel Skor Eşiği',

            // Modal - Color Analysis
            'color.difference.methods': 'Renk Farkı Yöntemleri',
            'use.cmc': 'CMC Renk Farkını Kullan',
            'cmc.ratio': 'CMC l:c Oranı',
            'acceptability': 'Kabul Edilebilirlik',
            'perceptibility': 'Algılanabilirlik',
            'spectrophotometer.settings': 'Spektrofotometre Ayarları',
            'observer.angle': 'Gözlemci Açısı',
            'standard.observer': 'Standart Gözlemci',
            'geometry.mode': 'Geometri Modu',

            // Modal - Pattern Analysis
            'texture.parameters': 'Doku Parametreleri',
            'wavelet.type': 'Dalgacık Türü',
            'wavelet.levels': 'Dalgacık Seviyeleri',
            'pattern.repetition': 'Desen Tekrarı',
            'pattern.min.area': 'Desen Min Alan (px)',
            'pattern.max.area': 'Desen Maks Alan (px)',
            'keypoint.detector': 'Anahtar Nokta Dedektörü',
            'fast': 'Hızlı',
            'accurate': 'Doğru',

            // Modal - Report Sections
            'color.unit': 'Renk Birimi',
            'pattern.unit': 'Desen Birimi',
            'pattern.repetition.unit': 'Desen Tekrarı',
            'spectrophotometer': 'Spektrofotometre',
            'analysis.settings.page': 'Analiz Ayarları Sayfası',
            'operator.info': 'Operatör Bilgisi',
            'operator.name': 'Operatör Adı',
            'operator': 'Operatör',

            // Report Language
            'report.language': 'Rapor Dili',
            'report.language.desc': 'Oluşturulan PDF raporu için dili seçin. Teknik terimler parantez içinde İngilizce olarak tutulacaktır.',
            'report.lang.en.desc': 'İngilizce Rapor',
            'report.lang.tr.desc': 'Türkçe Rapor',

            // New Settings - General
            'general': 'Genel',
            'settings.intro': 'Genel analiz ayarlarını ve operatör bilgilerini yapılandırın.',
            'operator.info.desc': 'Oluşturulan raporda görünen bilgiler.',
            'operator.name.hint': 'Rapor başlığında gösterilen ad',
            'timezone': 'Saat Dilimi',
            'timezone.hint': 'Rapor zaman damgaları için saat dilimi',
            'sampling.settings': 'Örnekleme Ayarları',
            'sampling.settings.desc': 'Renk analizi için görüntü üzerinde örnek noktaların nasıl dağıtılacağını kontrol edin.',
            'num.sample.points': 'Örnek Noktaları',
            'num.sample.points.hint': 'Ölçüm noktalarının sayısı (3-20)',
            'sampling.mode': 'Örnekleme Modu',
            'sampling.mode.hint': 'Rastgele her çalıştırmada yeni noktalar oluşturur, Manuel seçmenize izin verir',
            'sampling.random': 'Rastgele',
            'sampling.manual': 'Manuel',
            'select.points.on.image': 'Görüntü üzerinde noktaları seçin',
            'no.points.selected': 'Nokta seçilmedi',
            'points.selected': 'nokta seçildi',
            'select.sample.points': 'Örnek Noktaları Seç',
            'select.points': 'Noktaları Seç',
            'complete.rest.randomly': 'Kalanları rastgele tamamla',
            'click.to.select.points': 'Renk analizi için ölçüm noktaları seçmek üzere görüntülere tıklayın',
            'selected': 'Seçildi',
            'click.anywhere.hint': 'Örnek nokta yerleştirmek için herhangi bir görüntüye tıklayın. Noktalar her iki görüntüde de yansıtılır.',
            'point.outside.roi': 'Nokta seçili bölge içinde olmalıdır',
            'all.points.selected': 'Tüm noktalar seçildi! Kaydetmek için Onayla\'ya tıklayın.',
            'all.points.already.selected': 'Tüm noktalar zaten seçildi.',
            'upload.sample.first': 'Nokta oluşturmadan önce lütfen bir örnek görüntü yükleyin.',
            'upload.both.images': 'Nokta oluşturmadan önce lütfen hem referans hem de örnek görüntüleri yükleyin.',
            'point.outside.region': 'Nokta seçilen analiz bölgesi içinde olmalıdır. Lütfen vurgulanan alan içine tıklayın.',
            'invalid.point': 'Geçersiz Nokta',
            'undo.last': 'Son İşlemi Geri Al',
            'clear.all': 'Tümünü Temizle',
            'confirm.selection': 'Seçimi Onayla',
            'color.analysis.disabled.hint': 'Örnek noktaları seçmek için Renk Analizi etkinleştirilmelidir.',
            'scoring.multipliers': 'Puanlama Çarpanları',
            'scoring.multipliers.desc': 'Puanların ölçümlerden nasıl hesaplanacağını ayarlayın.',
            'color.score.multiplier': 'Renk Skoru Çarpanı',
            'color.score.multiplier.hint': 'Daha yüksek = ΔE\'ye daha duyarlı',
            'uniformity.multiplier': 'Homojenlik Çarpanı',
            'uniformity.multiplier.hint': 'Daha yüksek = daha katı homojenlik kontrolü',

            // New Settings - Thresholds
            'thresholds.intro': 'Kalite kararları için geçiş/başarısızlık eşiklerini ayarlayın. Geçiş\'in altındaki değerler = KABUL, Geçiş ile Koşullu arasındaki = KOŞULLU, Koşullu\'nun üstündeki = RED.',
            'color.thresholds.desc': 'Endüstri standardı: ΔE < 1.0 = algılanamaz, 1-2 = yakın inceleme, 2-3.5 = fark edilebilir.',
            'de.pass.hint': 'Bunun altında = GEÇİŞ',
            'de.conditional.hint': 'Bunun üstünde = BAŞARISIZ',
            'pattern.thresholds.desc': 'SSIM 0-1 arasında değişir. Daha yüksek = daha benzer. Endüstri tipik: 0.90-0.98.',
            'ssim.pass.hint': 'Bunun üstünde = GEÇİŞ',
            'ssim.conditional.hint': 'Bunun altında = BAŞARISIZ',
            'score.thresholds.desc': 'Kalite kontrolünü geçmek için gereken minimum puanlar (0-100).',
            'color.score.threshold.hint': 'Kabul edilebilir minimum renk skoru',
            'pattern.score.threshold.hint': 'Kabul edilebilir minimum desen skoru',
            'overall.score.threshold.hint': 'Son geçiş/başarısızlık karar eşiği',
            'lab.thresholds': 'Lab* Eşik Değerleri',
            'lab.thresholds.desc': 'Lab* kalite değerlendirmesi için bileşen düzeyinde eşik değerleri tanımlayın.',
            'lab.l.threshold': 'L* Eşiği (Parlaklık)',
            'lab.l.hint': 'Kabul edilebilir maksimum parlaklık farkı',
            'lab.ab.threshold': 'a*/b* Eşiği (Kroma)',
            'lab.ab.hint': 'Kabul edilebilir maksimum kroma farkı',
            'lab.thresh.dl': 'ΔL* Eşik Değeri',
            'lab.thresh.dl.desc': 'Parlaklık toleransı',
            'lab.thresh.da': 'Δa* Eşik Değeri',
            'lab.thresh.da.desc': 'Kırmızı-yeşil eksen toleransı',
            'lab.thresh.db': 'Δb* Eşik Değeri',
            'lab.thresh.db.desc': 'Sarı-mavi eksen toleransı',
            'lab.thresh.mag': 'Büyüklük Eşik Değeri',
            'lab.thresh.mag.desc': 'Birleşik ΔLab vektör büyüklüğü',

            // New Settings - Color Analysis
            'color.intro': 'Renk ölçüm yöntemlerini ve spektrofotometre simülasyonu ayarlarını yapılandırın.',
            'color.methods.desc': 'ΔE2000 her zaman hesaplanır. CMC tekstil endüstrisi uyumluluğu için isteğe bağlıdır.',
            'use.cmc.hint': 'Tekstil endüstrisi için CMC(l:c) formülü',
            'cmc.ratio.hint': 'Kabul edilebilirlik için 2:1, algılanabilirlik için 1:1',
            'spectro.sim.desc': 'Profesyonel spektrofotometre ölçüm koşullarını simüle eder.',
            'observer.angle.hint': 'CIE standart gözlemci',
            'geometry.mode.hint': 'Ölçüm geometrisi yapılandırması',
            'whiteness.settings': 'Beyazlık ve Sarılık',
            'whiteness.desc': 'Beyaz kumaş değerlendirmesi için eşikler (ISO parlaklık standartları).',
            'whiteness.min': 'Minimum Beyazlık İndeksi',
            'whiteness.min.hint': 'CIE Beyazlık İndeksi eşiği',
            'yellowness.max': 'Maksimum Sarılık İndeksi',
            'yellowness.max.hint': 'ASTM E313 Sarılık eşiği',

            // New Settings - Pattern Analysis
            'pattern.intro': 'Doku analizi algoritmalarını ve desen algılama parametrelerini yapılandırın.',
            'wavelet.settings': 'Dalgacık Dönüşümü',
            'wavelet.desc': 'Desenlerin çoklu çözünürlüklü frekans analizi.',
            'wavelet.type.hint': 'Dalgacık temel fonksiyonu',
            'wavelet.levels.hint': 'Ayrıştırma seviyesi sayısı (1-5)',
            'pattern.detection.desc': 'Tekrar eden desenleri bulma ve eşleştirme ayarları.',
            'keypoint.hint': 'Özellik algılama algoritması',
            'pattern.min.hint': 'Algılanan minimum desen boyutu',
            'pattern.max.hint': 'Algılanan maksimum desen boyutu',
            'pattern.similarity': 'Benzerlik Eşiği',
            'pattern.similarity.hint': 'Desen eşleştirmesi için minimum benzerlik',
            'defect.detection': 'Kusur Algılama',
            'defect.desc': 'Anormallik ve kusurları algılama ayarları.',
            'defect.min.area': 'Min Kusur Alanı (px)',
            'defect.min.hint': 'Kusur olarak işaretlenecek minimum boyut',
            'saliency.strength': 'Belirginlik Gücü',
            'saliency.hint': 'Anormallik algılama hassasiyeti',

            // New Settings - Report Sections
            'report.intro': 'Oluşturulan PDF raporuna dahil edilecek bölümleri seçin.',
            'main.sections': 'Ana Rapor Bölümleri',
            'main.sections.desc': 'Rapordaki birincil analiz bölümleri.',
            'color.unit.hint': 'ΔE, Lab*, renk ölçümleri',
            'pattern.unit.hint': 'SSIM, doku, simetri analizi',
            'pattern.rep.hint': 'Tekrar algılama, mekansal analiz',
            'spectro.hint': 'Simüle edilmiş cihaz okumaları',
            'settings.page.hint': 'Analizde kullanılan tüm ayarları dahil et',
            'color.subsections': 'Renk Birimi Alt Bölümleri',
            'color.subsections.desc': 'Renk analizi rapor içeriğini hassaslaştırın.',
            'color.measurements': 'Renk Ölçümleri',
            'color.difference': 'Renk Farkı',
            'color.statistical': 'İstatistiksel Analiz',
            'color.visual.diff': 'Görsel Fark Haritası',
            'color.lab.detailed': 'Detaylı Lab* Analizi',
            'color.recommendations': 'Öneriler',
            'pattern.subsections': 'Desen Birimi Alt Bölümleri',
            'pattern.subsections.desc': 'Desen analizi rapor içeriğini hassaslaştırın.',
            'pattern.ssim': 'SSIM Analizi',
            'pattern.symmetry': 'Simetri Analizi',
            'pattern.edge': 'Kenar Algılama',
            'pattern.advanced': 'Gelişmiş Analiz',

            // Modal - Buttons
            'reset.to.defaults': 'Varsayılanlara Sıfırla',
            'cancel': 'İptal',
            'apply.settings': 'Ayarları Uygula',

            // Help Dialog
            'format.information': 'Format Bilgisi',
            'python.script': 'Python Script (.py)',
            'jupyter.notebook': 'Jupyter Notebook (.ipynb)',
            'download.this.format': 'Bu formatı indir',
            'learn.more': 'Daha fazla bilgi',

            // GitHub
            'github.browse.project': 'Projeye GitHub\'da göz atın',
            'github.view.repository': 'Depoyu ve dokümantasyonu görüntüle',
            'github.description': 'GitHub\'da tam kaynak koduna, dokümantasyona ve proje dosyalarına erişin. Depo, Tekstil Kalite Kontrol Sistemini anlamak ve kullanmak için gereken tüm kodu, README dosyalarını ve kaynakları içerir.',
            'github.read.readme': 'Proje hakkında ayrıntılı bilgi, kurulum talimatları ve kullanım kılavuzları için lütfen GitHub deposundaki README dosyasını okuyun.',
            'github.under.construction': 'Bu proje yapım aşamasındadır ve aktif olarak geliştirilmektedir. Yeni özellikler ve iyileştirmeler düzenli olarak eklenmektedir.',
            'github.inquiries.title': 'Sorular veya Öneriler İçin',
            'github.feedback.panel': 'Ekranın sol tarafındaki geri bildirim panelini çekin ve anketi doldurun',
            'github.visit.repository': 'GitHub Deposunu Ziyaret Et',

            // Errors & Messages
            'error.reading.file': 'Dosya okuma hatası',
            'please.upload.both': 'Lütfen hem referans hem de örnek görüntüleri yükleyin',
            'please.upload.image': 'Lütfen analiz için bir görüntü yükleyin',
            'delete.confirm': 'Yüklenen tüm görüntüleri silmek istediğinizden emin misiniz?',
            'delete.image': 'Görüntüyü Sil',
            'delete.image.confirm': '{image} görüntüsünü silmek istediğinizden emin misiniz?',
            'failed.to.load.samples': 'Örnekler yüklenemedi',

            // Development Modal
            'development.title': 'Web Sitesi Geliştirme Aşamasında',
            'development.message': 'Bu web sitesi şu anda geliştirme aşamasındadır.',
            'development.view.samples': 'Sonuçları ekranın sol tarafındaki Örnekler bölümünden hazır örnekler aracılığıyla görüntüleyebilirsiniz.',
            'development.test.new': 'Veya yeni örnekleri test etmek için kaynak kodunu (Python) indirin ve doğrudan Google Colab ortamında test edin.',
            'development.logos.note': 'Tam sonuçlar elde etmek için bu logoların aynı dosya adlarıyla Google Colab\'a eklenmesi gerekir.',
            'development.download.logo': 'Logo indir',
            'development.go.colab': 'Google Colab\'a Git',
            'development.download.code': 'Ana sayfadaki mevcut kodu indirin',
            'development.source.code': 'Kaynak Kodu',
            'development.close': 'Kapat',
            'development.copy.code': 'Kodu Kopyala',
            'development.copied': 'Kopyalandı!',
            'development.copy.instruction': 'Kodu kopyalayın ve Google Colab ortamına yapıştırın.',

            // Footer
            'copyright': '© 2026 Tekstil Mühendisliği Çözümleri | ',
            'contact.title': 'İletişim',

            // Progress Steps
            'upload.images': 'Görüntüleri Yükle',
            'color.analysis.step': 'Renk Analizi',
            'pattern.analysis.step': 'Desen Analizi',
            'pattern.repetition.step': 'Desen Tekrarı',
            'calculate.scores': 'Skorları Hesapla',
            'generate.report': 'Rapor Oluştur',
            'step.failed': 'Adım başarısız',
            'analysis.failed': 'Analiz başarısız',

            // Source Code Help
            'what.is.python': 'Python (.py) dosyası nedir?',
            'what.is.notebook': 'Jupyter Notebook (.ipynb) nedir?',
            'best.for': 'En uygun:',
            'local.development': 'Yerel geliştirme, mevcut projelere entegrasyon veya sunucularda çalıştırma.',
            'google.colab': 'Google Colab, hızlı deneyler, öğrenme veya yerel ortam kurmak istemediğinizde.',
            'python.script.desc': '<strong>.py dosyası</strong>, herhangi bir Python ortamında çalıştırılabilen standart bir Python scriptidir.',
            'python.works.with': 'Python 3.7 veya üstü ile çalışır',
            'python.run.directly': 'Komut satırından veya herhangi bir IDE\'den doğrudan çalıştırın',
            'python.ideal.for': 'Yerel geliştirme ve entegrasyon için idealdir',
            'python.can.import': 'Projelerinizde modül olarak içe aktarılabilir',
            'python.best.for': 'Yerel geliştirme, mevcut projelere entegrasyon veya sunucularda çalıştırma.',
            'notebook.desc': '<strong>.ipynb dosyası</strong>, adım adım analiz ve görselleştirme için mükemmel bir etkileşimli notebook formatıdır.',
            'notebook.runs.colab': 'Doğrudan <strong>Google Colab</strong>\'da çalışır — kurulum gerekmez!',
            'notebook.interactive': 'Açıklamalarla etkileşimli hücreler',
            'notebook.easy.modify': 'Değiştirmesi ve denemesi kolay',
            'notebook.visualizations': 'Görselleştirmeler satır içinde görüntülenir',
            'notebook.best.for': 'Google Colab, hızlı deneyler, öğrenme veya yerel ortam kurmak istemediğinizde.',

            // Language
            'language': 'Dil',
            'english': 'İngilizce',
            'turkish': 'Türkçe',

            // Analysis Configuration Modal
            'analysis.configuration': 'Analiz Yapılandırması',
            'fine.tune.parameters': 'Kalite kontrol parametrelerini ayarlayın',
            'operator.information': 'Operatör Bilgileri',
            'details.shown.report': 'Oluşturulan raporda gösterilen bilgiler.',
            'operator.name.label': 'Operatör Adı',
            'operator.name.desc': 'Analizi yapan kişinin adı',
            'timezone.offset': 'Saat Dilimi Farkı (UTC)',
            'timezone.offset.desc': 'Rapor zaman damgasını ayarlamak için saat',
            'selection.region': 'Seçim Bölgesi',
            'selection.region.desc': 'Analiz bölgesinin şeklini ve boyutlarını tanımlayın.',
            'region.shape.label': 'Bölge Şekli',
            'region.shape.desc': 'Bölge seçimi için şekli seçin',
            'dimensions': 'Boyutlar',
            'dimensions.desc': 'Bölge boyutunu piksel olarak belirtin',
            'diameter.px': 'Çap (px)',
            'side.length.px': 'Kenar Uzunluğu (px)',
            'width.px': 'Genişlik (px)',
            'height.px': 'Yükseklik (px)',
            'single.image.config': 'Tek Görüntü Yapılandırması',
            'single.image.config.desc': 'Tek Görüntü Modu için analiz uygulamasını yapılandırın.',
            'sampling.configuration': 'Örnekleme Yapılandırması',
            'sampling.count': 'Örnekleme Sayısı',
            'points.to.measure': 'Ölçülecek noktalar',
            'select.points': 'Noktaları Seç',
            'complete.randomly': 'Geri kalanı rastgele tamamla',
            'selected.count': 'Seçilen',
            'illuminant.settings': 'Aydınlatma Ayarları',
            'single.image.unit': 'Tek Görüntü Birimi',
            'report.language': 'Rapor Dili',
            'report.language.desc': 'Oluşturulan PDF raporlarında kullanılan dil',

            // Color Unit Tab
            'color.scoring.method': 'Renk Puanlama Yöntemi',
            'color.scoring.method.desc': 'Renk Skoru, Geçiş/Koşullu/Başarısız kararını ve rapor kapak görünümünü belirleyen metriği seçin.',
            'scoring.basis': 'Puanlama Temeli',
            'scoring.basis.desc': 'Birincil renk skorunu belirler',
            'thresholds.delta.e': 'Eşikler (Delta E 2000)',
            'define.pass.fail': 'Renk farkı için geçti/kaldı kriterlerini tanımlayın.',
            'pass.threshold': 'Geçiş Eşiği',
            'values.below.accepted': 'Bu değerin altındakiler kabul edilir',
            'conditional.threshold': 'Koşullu Eşik',
            'values.below.warning': 'Bu değerin altındakiler uyarıdır (geçişin üzerindeyse)',
            'global.acceptance': 'Genel Kabul',
            'overall.color.score': 'Genel görüntü renk skoru eşiği',
            'csi.thresholds': 'RSE Eşikleri',
            'csi.thresholds.desc': 'Renk Benzerlik Endeksi için renk eşiklerini tanımlayın.',
            'csi.good.threshold': 'RSE İyi Eşiği',
            'above.this.green': 'Bunun üzeri = Yeşil',
            'csi.warning.threshold': 'RSE Uyarı Eşiği',
            'above.this.orange': 'Bunun üzeri = Turuncu',
            'sampling.config.desc': 'Renk Analizi için analiz noktalarının nasıl seçileceğini yapılandırın.',
            'target.points.max': 'Hedef nokta sayısı (maksimum 100)',
            'incomplete': 'Tamamlanmadı',
            'complete': 'Tamamlandı',
            'partial': 'Kısmi',
            'manual': 'Manuel',
            'random': 'Rastgele',
            'selected.label': 'Seçilen',
            'single.report.sections.desc': 'Tek Görüntü raporuna dahil edilecek bölümleri seçin.',

            // Pattern Unit Tab
            'pattern.scoring.method': 'Desen Puanlama Yöntemi',
            'pattern.scoring.method.desc': 'Rapor kapağı ve arayüzde gösterilecek Desen Skorunu belirleyen metriği seçin.',
            'pattern.scoring.basis.desc': 'Birincil desen skorunu belirler',
            'method.thresholds': 'Yöntem Eşikleri (Geçiş / Koşullu)',
            'define.similarity.scores': 'Desen analizi için benzerlik skorlarını (0-100%) tanımlayın.',
            'structural.ssim': 'Yapısal SSIM',
            'structural.match': 'Yapısal Eşleşme',
            'pass.conditional': 'Geçiş / Koşullu',
            'gradient.similarity': 'Gradyan Benzerliği',
            'phase.correlation': 'Faz Korelasyonu',
            'global.pattern.score': 'Genel Desen Skoru',
            'overall.pass.threshold': 'Genel geçiş eşiği',

            // Illuminant Settings Tab
            'global.report.illuminant': 'Genel Rapor Aydınlatması',
            'select.primary.illuminant': 'Tüm rapor için kullanılacak birincil aydınlatmayı seçin.',
            'primary.illuminant': 'Birincil Aydınlatma',
            'used.standard.calc': 'Standart hesaplamalar için kullanılır',
            'illuminant.test.selection': 'Aydınlatma Test Seçimi',
            'enable.illuminants.desc': 'Karşılaştırmalı renk testi için aydınlatmaları etkinleştirin (yalnızca Renk Biriminde görüntülenir).',
            'comparative.illuminants': 'Karşılaştırmalı Aydınlatmalar',

            // Report Sections Tab
            'color.unit.report.sections': 'Renk Birimi Rapor Bölümleri',
            'select.components.color': 'Renk Birimi bölümü için bileşenleri seçin.',
            'color.spaces': 'Renk Uzayları',
            'rgb.values': 'RGB Değerleri',
            'lab.values': 'Lab* Değerleri',
            'xyz.values': 'XYZ Değerleri',
            'cmyk.values': 'CMYK Değerleri',
            'diff.metrics': 'Fark Metrikleri',
            'statistics': 'İstatistikler',
            'detailed.lab': 'Detaylı Lab',
            'visualizations': 'Görselleştirmeler',
            'spectral.proxy': 'Spektral Vekil',
            'rgb.histograms': 'RGB Histogramları',
            'visual.diff': 'Görsel Fark',
            'illuminant.analysis': 'Aydınlatma Analizi',
            'recommendations': 'Öneriler',
            'pattern.unit.methods': 'Desen Birimi: Etkin Yöntemler',
            'select.pattern.algorithms': 'Çalıştırılacak ve dahil edilecek desen algoritmalarını seçin.',
            'structural.difference': 'Yapısal Fark',
            'fourier.domain.analysis': 'Fourier Alan Analizi',
            'glcm.texture.analysis': 'GLCM Doku Analizi',
            'pattern.unit.boundary': 'Desen Birimi: Sınır ve Rapor',
            'gradient.boundary': 'Gradyan Sınırı',
            'phase.boundary': 'Faz Sınırı',
            'summary': 'Özet',
            'conclusion': 'Sonuç',

            // Detailed Results Panel
            'rpt.report.summary': 'Rapor Özeti',
            'rpt.color.scoring': 'Renk Puanlama',
            'rpt.pattern.scoring': 'Desen Puanlama',
            'rpt.csi.color.similarity': 'CSI (Renk Benzerliği)',
            'rpt.mean.de2000': 'Ortalama ΔE 2000',
            'rpt.report.size': 'Rapor Boyutu',
            'rpt.structural.change': 'Yapısal Değişim',
            'rpt.color.analysis.details': 'Renk Analizi Detayları',
            'rpt.pattern.analysis.details': 'Desen Analizi Detayları',
            'rpt.texture.frequency': 'Doku ve Frekans Analizi',
            'rpt.single.image.analysis': 'Tek Görüntü Analizi',
            'rpt.mean.de00': 'Ortalama ΔE00',
            'rpt.method': 'Yöntem',
            'rpt.status': 'Durum',
            'rpt.composite': 'Bileşik',
            'rpt.structural': 'Yapısal',
            'rpt.regional.color.metrics': 'Bölgesel Renk Metrikleri',
            'rpt.individual.method.scores': 'Bireysel Yöntem Puanları',
            'rpt.structural.difference': 'Yapısal Fark',
            'rpt.similarity.score': 'Benzerlik Puanı',
            'rpt.change.percentage': 'Değişim Yüzdesi',
            'rpt.verdict': 'Karar',
            'rpt.difference.maps': 'Fark Haritaları',
            'rpt.boundary.detection': 'Sınır Tespiti',
            'rpt.structural.analysis': 'Yapısal Analiz',
            'rpt.position': 'Konum',
            'rpt.ref.lab': 'Ref L*a*b*',
            'rpt.sam.lab': 'Örn L*a*b*',
            'rpt.mode': 'Mod',
            'rpt.single.image.mode': 'Tek Görüntü Analizi',
            'rpt.de.heatmap': 'ΔE Isı Haritası',
            'rpt.de.heatmap.caption': 'Referans ve numune arasındaki piksel düzeyinde renk farkı ısı haritası.',
            'rpt.spectral': 'Spektral Dağılım (Vekil)',
            'rpt.spectral.caption': 'Ortalama RGB değerlerinden yaklaşık spektral yansıtma eğrileri.',
            'rpt.histograms': 'RGB Histogramları',
            'rpt.histograms.caption': 'Referans ve Numune için yan yana RGB kanal dağılımı.',
            'rpt.lab.scatter': 'a* - b* Kromatiklik Dağılımı',
            'rpt.lab.scatter.caption': 'a*b* düzleminde Referans ve Numune kromatiklik koordinatları.',
            'rpt.lab.bars': 'Lab Bileşenleri – Ortalama',
            'rpt.lab.bars.caption': 'Referans ve Numune arasında ortalama L*, a*, b* karşılaştırması.',
            'rpt.ssim.map': 'SSIM Fark Haritası',
            'rpt.ssim.map.caption': 'Yapısal SSIM farkı — sıcak bölgeler yapısal farklılığı gösterir.',
            'rpt.gradient.map': 'Gradyan Benzerlik Haritası',
            'rpt.gradient.map.caption': 'Gradyan büyüklük farkı — kenar/doku uyumsuzluklarını vurgular.',
            'rpt.phase.map': 'Faz Korelasyon Haritası',
            'rpt.phase.map.caption': 'Faz tabanlı fark — uzamsal kaymaları ve hizalama bozukluklarını tespit eder.',
            'rpt.gradient.boundary': 'Gradyan Sınırı',
            'rpt.gradient.boundary.caption': 'Numune üzerinde önemli gradyan fark bölgeleri.',
            'rpt.gradient.filled': 'Gradyan Dolgulu',
            'rpt.gradient.filled.caption': 'Kırmızı dolgulu gradyan fark bölgeleri.',
            'rpt.phase.boundary': 'Faz Sınırı',
            'rpt.phase.boundary.caption': 'Numune üzerinde önemli faz fark bölgeleri.',
            'rpt.phase.filled': 'Faz Dolgulu',
            'rpt.phase.filled.caption': 'Kırmızı dolgulu faz fark bölgeleri.',
            'rpt.multi.method': 'Çoklu Yöntem Karşılaştırması',
            'rpt.multi.method.caption': 'Gradyan büyüklüğü, birleşik yöntemler ve gürültü filtrelenmiş fark haritaları.',
            'rpt.pure.diff': 'Saf Farklar',
            'rpt.pure.diff.caption': 'İzole edilmiş saf fark bölgeleri (siyah üzerine kırmızı).',
            'rpt.fourier': 'Fourier Spektrumu (FFT)',
            'rpt.fourier.caption': 'Frekans alanı özelliklerini gösteren 2D FFT büyüklük spektrumu.',
            'rpt.glcm': 'GLCM Doku Isı Haritası',
            'rpt.glcm.caption': 'Gri Seviye Eş-oluşum Matrisi doku özelliği karşılaştırma ısı haritaları.',
            'rpt.histogram.single': 'RGB Histogramı',
            'rpt.histogram.single.caption': 'Numune görüntüsünün RGB kanal dağılımı.',
            'rpt.spectral.single': 'Spektral Dağılım (Vekil)',
            'rpt.spectral.single.caption': 'Ortalama RGB değerlerinden yaklaşık spektral yansıtma eğrisi.',
            'rpt.fourier.single': 'Fourier Spektrumu',
            'rpt.fourier.single.caption': 'Frekans alanı özelliklerini gösteren 2D FFT büyüklük spektrumu.',
            'rpt.illuminant.analysis': 'Aydınlatıcı Analizi',
            'rpt.illuminant': 'Aydınlatıcı',
            'rpt.color.comparison': 'Renk Karşılaştırması',
            'rpt.color.recommendations': 'Renk — Temel Bulgular ve Öneriler',
            'rpt.pattern.recommendations': 'Desen — Temel Bulgular ve Öneriler',
            'rpt.reference': 'Referans',
            'rpt.sample': 'Numune',
            'rpt.de.summary.stats': '\u0394E \u00d6zet \u0130statistikleri',
            'rpt.metric': 'Metrik',
            'rpt.average': 'Ortalama',
            'rpt.std.dev': 'Std Sapma',
            'rpt.min': 'Min',
            'rpt.max': 'Maks'
        }
    },

    /**
     * Initialize i18n system
     */
    init: function () {
        // Load saved language or default to English
        var savedLang = localStorage.getItem('textile_qc_lang');
        if (savedLang && this.translations[savedLang]) {
            this.currentLang = savedLang;
        } else {
            this.currentLang = 'en';
        }

        // Set HTML lang attribute
        document.documentElement.lang = this.currentLang;

        // Apply translations
        this.translatePage();
        
        // Update language dropdown if exists
        this.updateLanguageDropdown();
    },
    
    /**
     * Update language dropdown display
     */
    updateLanguageDropdown: function() {
        var currentFlag = document.getElementById('currentLangFlag');
        var currentText = document.getElementById('currentLangText');
        
        if (currentFlag && currentText) {
            if (this.currentLang === 'tr') {
                currentFlag.src = '/static/images/tr.svg';
                currentText.textContent = 'TR';
            } else {
                currentFlag.src = '/static/images/uk.svg';
                currentText.textContent = 'EN';
            }
        }
        
        // Update active state in dropdown
        var items = document.querySelectorAll('.lang-dropdown-item');
        items.forEach(function(item) {
            var lang = item.getAttribute('data-lang');
            if (lang === I18n.currentLang) {
                item.classList.add('active');
            } else {
                item.classList.remove('active');
            }
        });
    },

    /**
     * Translate a key
     */
    t: function (key) {
        var translation = this.translations[this.currentLang];
        if (!translation) {
            translation = this.translations['en'];
        }
        return translation[key] || key;
    },

    /**
     * Translate entire page
     */
    translatePage: function () {
        // Translate elements with data-i18n or data-i18n-html attribute
        document.querySelectorAll('[data-i18n], [data-i18n-html]').forEach(function (el) {
            var key = el.getAttribute('data-i18n') || el.getAttribute('data-i18n-html');
            var translation = I18n.t(key);

            // Handle different element types
            if (el.tagName === 'INPUT' && el.type === 'text' || el.tagName === 'INPUT' && el.type === 'number') {
                if (el.placeholder) {
                    el.placeholder = translation;
                } else {
                    el.value = translation;
                }
            } else if (el.tagName === 'INPUT' && el.type === 'button' || el.tagName === 'BUTTON') {
                // Don't translate button text if it contains dynamic content
                if (!el.hasAttribute('data-no-translate')) {
                    el.textContent = translation;
                }
            } else if (el.hasAttribute('data-i18n-html')) {
                el.innerHTML = translation;
            } else {
                el.textContent = translation;
            }
        });

        // Translate title
        var titleEl = document.querySelector('title');
        if (titleEl) {
            titleEl.textContent = I18n.t('app.title') + ' - ' + I18n.t('app.subtitle');
        }

        // Update language toggle switch
        if (typeof updateLanguageToggle === 'function') {
            updateLanguageToggle();
        }
    },

    /**
     * Change language
     */
    setLanguage: function (lang) {
        if (!this.translations[lang]) {
            console.warn('Language not supported:', lang);
            return;
        }

        this.currentLang = lang;
        localStorage.setItem('textile_qc_lang', lang);
        document.documentElement.lang = lang;
        this.translatePage();

        // Trigger custom event for other scripts
        document.dispatchEvent(new CustomEvent('languageChanged', { detail: { lang: lang } }));
    },

    /**
     * Get current language
     */
    getLanguage: function () {
        return this.currentLang;
    }
};

/**
 * Update language toggle switch appearance
 * (Kept for backward compatibility, but updateLanguageToggle in app.js is used)
 */
function updateLanguageSwitcher() {
    if (typeof updateLanguageToggle === 'function') {
        updateLanguageToggle();
    }
}

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () {
        I18n.init();
    });
} else {
    I18n.init();
}

