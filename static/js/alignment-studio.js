// ═══════════════════════════════════════════════════════════════════
// Alignment Studio — SpectraMatch v3.0.0
// Interactive Image Alignment & Registration Testing Window
// ═══════════════════════════════════════════════════════════════════

var AlignmentStudio = (function () {
    'use strict';

    var state = {
        isOpen: false,
        activeTechnique: 'direct',
        appliedTechnique: null,
        savedTechnique: null,
        testedTechniques: {},
        refImageSrc: null,
        sampleImageSrc: null,
        refFile: null,
        sampleFile: null,
        regionData: null,
        currentMetrics: null,
        currentPreviews: null,
        isProcessing: false,
        isDesktop: false,
        autoTestPending: null,
    };

    var TECHNIQUES = [
        { id: 'direct', icon: 'grid', category: 'baseline', handles: [] },
        { id: 'orb_homography', icon: 'crosshair', category: 'registration', handles: ['rotation', 'scale', 'perspective', 'translation'] },
        { id: 'ecc_alignment', icon: 'layers', category: 'registration', handles: ['rotation', 'scale', 'translation', 'shear'] },
        { id: 'phase_correlation', icon: 'activity', category: 'registration', handles: ['rotation', 'translation'] },
        { id: 'ai_smart_match', icon: 'cpu', category: 'ai', handles: ['rotation', 'scale', 'translation', 'perspective', 'lighting'] },
        { id: 'cascading_ecc', icon: 'anchor', category: 'registration', handles: ['rotation', 'scale', 'translation', 'shear'] },
        { id: 'orb_affine', icon: 'target', category: 'registration', handles: ['rotation', 'scale', 'translation'] },
        { id: 'subpixel_translation', icon: 'maximize', category: 'registration', handles: ['translation'] },
        { id: 'pyramid_align', icon: 'triangle', category: 'registration', handles: ['rotation', 'scale', 'translation'] },
        { id: 'tile_refine', icon: 'layout', category: 'registration', handles: ['translation'] },
    ];

    var ICONS = {
        grid: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>',
        crosshair: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="22" y1="12" x2="18" y2="12"/><line x1="6" y1="12" x2="2" y2="12"/><line x1="12" y1="6" x2="12" y2="2"/><line x1="12" y1="22" x2="12" y2="18"/></svg>',
        layers: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>',
        activity: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>',
        cpu: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/></svg>',
        play: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="5 3 19 12 5 21 5 3"/></svg>',
        check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>',
        save: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg>',
        image: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>',
        sliders: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/><line x1="1" y1="14" x2="7" y2="14"/><line x1="9" y1="8" x2="15" y2="8"/><line x1="17" y1="16" x2="23" y2="16"/></svg>',
        info: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>',
        arrowRight: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
        move: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="5 9 2 12 5 15"/><polyline points="9 5 12 2 15 5"/><polyline points="15 19 12 22 9 19"/><polyline points="19 9 22 12 19 15"/><line x1="2" y1="12" x2="22" y2="12"/><line x1="12" y1="2" x2="12" y2="22"/></svg>',
        rotateCw: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23 4 23 10 17 10"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10"/></svg>',
        anchor: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="5" r="3"/><line x1="12" y1="22" x2="12" y2="8"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/></svg>',
        target: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>',
        maximize: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>',
        triangle: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/></svg>',
        layout: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>',
    };

    var PROCESSING_STEPS = [
        'Loading images...',
        'Analyzing features...',
        'Computing alignment transform...',
        'Applying geometric correction...',
        'Generating preview comparisons...',
        'Finalizing results...'
    ];

    function t(key, fallback) {
        if (typeof I18n !== 'undefined' && I18n.t) { return I18n.t(key) || fallback; }
        return fallback;
    }

    // ═══════════════════════════════════════════════════════════════
    // Build Modal DOM
    // ═══════════════════════════════════════════════════════════════

    function buildModal() {
        var existing = document.getElementById('alignmentStudioOverlay');
        if (existing) existing.remove();

        var overlay = document.createElement('div');
        overlay.id = 'alignmentStudioOverlay';
        overlay.className = 'alignment-studio-overlay';
        overlay.innerHTML = _buildHTML();
        document.body.appendChild(overlay);
        overlay.addEventListener('click', function (e) { if (e.target === overlay) close(); });
        _bindEvents();
    }

    function _buildHTML() {
        var techniquesHTML = TECHNIQUES.map(function (tech) {
            var badgesHTML = tech.handles.map(function (h) {
                return '<span class="as-badge ' + h + '">' + t('align.badge.' + h, h) + '</span>';
            }).join('');
            return '<div class="as-technique-card' + (tech.id === 'direct' ? ' active' : '') + '" data-technique="' + tech.id + '">' +
                '<div class="as-technique-card-header">' +
                    '<div class="as-technique-icon ' + tech.category + '">' + ICONS[tech.icon] + '</div>' +
                    '<div class="as-technique-info">' +
                        '<div class="as-technique-name" data-i18n="align.name.' + tech.id + '">' + t('align.name.' + tech.id, tech.id) + '</div>' +
                        '<div class="as-technique-status" id="asStatus_' + tech.id + '"></div>' +
                    '</div>' +
                '</div>' +
                '<div class="as-technique-desc" data-i18n="align.desc.' + tech.id + '">' + t('align.desc.' + tech.id, '') + '</div>' +
                (badgesHTML ? '<div class="as-technique-badges">' + badgesHTML + '</div>' : '') +
                '<div class="as-technique-actions">' +
                    '<button class="as-btn as-btn-test" data-action="test" data-technique="' + tech.id + '" title="Test this technique live">' +
                        ICONS.play + '<span>' + t('align.test', 'Test') + '</span>' +
                    '</button>' +
                    '<button class="as-btn as-btn-save" data-action="save" data-technique="' + tech.id + '" title="Save this technique for analysis">' +
                        ICONS.save + '<span>Save</span>' +
                    '</button>' +
                '</div>' +
            '</div>';
        }).join('');

        return '<div class="as-container">' +
            '<div class="as-header">' +
                '<div class="as-header-icon">' + ICONS.sliders + '</div>' +
                '<div class="as-header-text">' +
                    '<h2 data-i18n="align.studio.title">' + t('align.studio.title', 'Image Alignment Studio') + '</h2>' +
                    '<small data-i18n="align.studio.subtitle">' + t('align.studio.subtitle', 'Test and compare alignment techniques interactively') + '</small>' +
                '</div>' +
                '<div class="as-header-spacer"></div>' +
                '<div class="as-saved-indicator" id="asSavedIndicator"></div>' +
                '<button class="as-close-btn" id="asCloseBtn">&times;</button>' +
            '</div>' +
            '<div class="as-body">' +
                '<div class="as-techniques-panel">' +
                    '<div class="as-techniques-header">' +
                        '<h3 data-i18n="align.techniques">' + t('align.techniques', 'Alignment Techniques') + '</h3>' +
                    '</div>' +
                    '<div class="as-techniques-list">' + techniquesHTML + '</div>' +
                '</div>' +
                '<div class="as-preview-panel">' +
                    '<div class="as-preview-area" id="asPreviewArea">' +
                        '<div class="as-preview-empty" id="asPreviewEmpty">' +
                            ICONS.image +
                            '<p>' + t('align.preview.empty', 'Select a technique and click Test to preview') + '</p>' +
                            '<small>' + t('align.preview.empty.hint', 'Upload both images first, then test alignment methods here') + '</small>' +
                        '</div>' +
                        '<div class="as-processing-overlay" id="asProcessingOverlay">' +
                            '<div class="as-processing-spinner"></div>' +
                            '<div class="as-processing-text" id="asProcessingText">Processing...</div>' +
                            '<div class="as-processing-step" id="asProcessingStep"></div>' +
                            '<div class="as-processing-bar"><div class="as-processing-bar-fill" id="asProcessingBarFill"></div></div>' +
                        '</div>' +
                    '</div>' +
                    '<div class="as-metrics-bar" id="asMetricsBar">' +
                        '<div class="as-footer-info">' + ICONS.info +
                            '<span>' + t('align.metrics.hint', 'Metrics will appear here after testing') + '</span>' +
                        '</div>' +
                    '</div>' +
                '</div>' +
            '</div>' +
            '<div class="as-footer">' +
                '<div class="as-footer-info">' + ICONS.info +
                    '<span>' + t('align.footer.note', 'Testing does not save settings. Use Save to confirm your choice.') + '</span>' +
                '</div>' +
                '<div class="as-footer-spacer"></div>' +
                '<button class="as-btn-footer as-btn-cancel" id="asCancelBtn">' +
                    '<span>' + t('align.cancel', 'Cancel') + '</span>' +
                '</button>' +
                '<button class="as-btn-footer as-btn-confirm" id="asConfirmBtn">' +
                    ICONS.check + '<span>' + t('align.confirm', 'Confirm & Close') + '</span>' +
                '</button>' +
            '</div>' +
        '</div>';
    }

    // ═══════════════════════════════════════════════════════════════
    // Event Binding
    // ═══════════════════════════════════════════════════════════════

    function _bindEvents() {
        var overlay = document.getElementById('alignmentStudioOverlay');
        if (!overlay) return;

        document.getElementById('asCloseBtn').addEventListener('click', close);
        document.getElementById('asCancelBtn').addEventListener('click', close);
        document.getElementById('asConfirmBtn').addEventListener('click', _onConfirm);

        // Technique cards — click to SELECT AND AUTO-TEST
        overlay.querySelectorAll('.as-technique-card').forEach(function (card) {
            card.addEventListener('click', function (e) {
                if (e.target.closest('.as-btn')) return;
                var techId = card.dataset.technique;
                _selectAndAutoTest(techId);
            });
        });

        // Test / Save buttons
        overlay.querySelectorAll('.as-btn[data-action]').forEach(function (btn) {
            btn.addEventListener('click', function (e) {
                e.stopPropagation();
                var action = btn.dataset.action;
                var techId = btn.dataset.technique;
                if (action === 'test') _testTechnique(techId);
                else if (action === 'save') _saveTechnique(techId);
            });
        });

        document.addEventListener('keydown', function (e) {
            if (state.isOpen && e.key === 'Escape') close();
        });
    }

    // ═══════════════════════════════════════════════════════════════
    // Open / Close
    // ═══════════════════════════════════════════════════════════════

    function open(options) {
        options = options || {};
        buildModal();

        state.refImageSrc = options.refSrc || null;
        state.sampleImageSrc = options.sampleSrc || null;
        state.refFile = options.refFile || null;
        state.sampleFile = options.sampleFile || null;
        state.regionData = options.regionData || null;
        state.isDesktop = options.isDesktop || false;
        state.testedTechniques = {};
        state.currentPreviews = null;
        state.currentMetrics = null;

        var modeSelect = document.getElementById(state.isDesktop ? 'propAlignmentMode' : 'alignment_mode');
        if (modeSelect) {
            state.savedTechnique = modeSelect.value || 'direct';
            state.appliedTechnique = state.savedTechnique;
        }

        var overlay = document.getElementById('alignmentStudioOverlay');
        overlay.style.display = 'flex';
        requestAnimationFrame(function () { overlay.classList.add('visible', 'fade-in'); });
        state.isOpen = true;

        _updateSavedIndicator();
        _updateI18n();
        _showSourceImages();

        // Auto-highlight saved technique
        _highlightSaved();

        // If images are loaded, auto-test current saved technique
        if (_hasImages() && state.savedTechnique && state.savedTechnique !== 'direct') {
            setTimeout(function () { _selectAndAutoTest(state.savedTechnique); }, 400);
        }
    }

    function close() {
        var overlay = document.getElementById('alignmentStudioOverlay');
        if (!overlay) return;
        overlay.classList.remove('visible', 'fade-in');
        setTimeout(function () { overlay.style.display = 'none'; }, 300);
        state.isOpen = false;
    }

    // ═══════════════════════════════════════════════════════════════
    // Technique Selection & Actions
    // ═══════════════════════════════════════════════════════════════

    function _selectAndAutoTest(techId) {
        _selectTechnique(techId);
        // If cached, just show. Otherwise auto-test if images available.
        if (state.testedTechniques[techId]) {
            state.currentPreviews = state.testedTechniques[techId].previews;
            state.currentMetrics = state.testedTechniques[techId].metrics;
            _renderPreview();
            _renderMetrics();
        } else if (_hasImages() && techId !== 'direct') {
            _testTechnique(techId);
        } else if (techId === 'direct') {
            _showSourceImages();
            _renderDirectMetrics();
        }
    }

    function _selectTechnique(techId) {
        state.activeTechnique = techId;
        var overlay = document.getElementById('alignmentStudioOverlay');
        overlay.querySelectorAll('.as-technique-card').forEach(function (card) {
            card.classList.toggle('active', card.dataset.technique === techId);
        });
    }

    function _testTechnique(techId) {
        if (state.isProcessing) return;
        if (!_hasImages()) {
            _showToast(t('align.no.images', 'Please upload both images first'), 'warn');
            return;
        }

        _selectTechnique(techId);
        state.isProcessing = true;

        // Show processing overlay with animated steps
        var processingEl = document.getElementById('asProcessingOverlay');
        var processingText = document.getElementById('asProcessingText');
        var processingStep = document.getElementById('asProcessingStep');
        var processingBar = document.getElementById('asProcessingBarFill');
        processingEl.classList.add('visible');
        processingText.textContent = t('align.processing', 'Processing alignment...');

        // Animate processing steps
        var stepIdx = 0;
        var stepInterval = setInterval(function () {
            if (stepIdx < PROCESSING_STEPS.length) {
                processingStep.textContent = PROCESSING_STEPS[stepIdx];
                processingBar.style.width = ((stepIdx + 1) / PROCESSING_STEPS.length * 100) + '%';
                stepIdx++;
            }
        }, 400);

        var btn = document.querySelector('.as-btn-test[data-technique="' + techId + '"]');
        if (btn) btn.classList.add('processing');

        var formData = new FormData();
        formData.append('mode', techId);
        formData.append('region_data', JSON.stringify(state.regionData || {}));

        _getImageFiles(function (refBlob, sampleBlob) {
            formData.append('ref_image', refBlob, 'ref.png');
            formData.append('sample_image', sampleBlob, 'sample.png');

            fetch('/api/alignment/preview', { method: 'POST', body: formData })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                clearInterval(stepInterval);
                state.isProcessing = false;
                if (btn) btn.classList.remove('processing');

                if (data.success) {
                    // Animate completion
                    processingStep.textContent = 'Complete!';
                    processingBar.style.width = '100%';

                    state.testedTechniques[techId] = { previews: data.previews, metrics: data.metrics };
                    state.currentPreviews = data.previews;
                    state.currentMetrics = data.metrics;

                    // Brief pause to show completion before revealing results
                    setTimeout(function () {
                        processingEl.classList.remove('visible');
                        _renderPreviewAnimated();
                        _renderMetrics();
                        _markCardTested(techId, data.metrics);
                    }, 350);

                    _showToast(t('align.test.success', 'Technique tested successfully'), 'success');
                } else {
                    processingEl.classList.remove('visible');
                    _showToast(data.error || t('align.test.failed', 'Test failed'), 'error');
                }
            })
            .catch(function (err) {
                clearInterval(stepInterval);
                state.isProcessing = false;
                processingEl.classList.remove('visible');
                if (btn) btn.classList.remove('processing');
                _showToast(t('align.test.error', 'Error testing technique: ') + err.message, 'error');
            });
        });
    }

    function _saveTechnique(techId) {
        state.savedTechnique = techId;
        state.appliedTechnique = techId;

        var modeSelect = document.getElementById(state.isDesktop ? 'propAlignmentMode' : 'alignment_mode');
        if (modeSelect) modeSelect.value = techId;

        // Visual feedback
        _highlightSaved();
        _updateSavedIndicator();

        // Animate the save button
        var saveBtn = document.querySelector('.as-btn-save[data-technique="' + techId + '"]');
        if (saveBtn) {
            saveBtn.classList.add('saved-flash');
            saveBtn.innerHTML = ICONS.check + '<span>Saved!</span>';
            setTimeout(function () {
                saveBtn.classList.remove('saved-flash');
                saveBtn.innerHTML = ICONS.save + '<span>Save</span>';
            }, 1500);
        }

        _showToast(t('align.applied', 'Technique saved: ') + _getTechName(techId), 'success');
    }

    function _onConfirm() {
        if (state.activeTechnique && state.activeTechnique !== state.savedTechnique) {
            _saveTechnique(state.activeTechnique);
        }
        var btn = document.getElementById('asConfirmBtn');
        btn.classList.add('confirmed');
        btn.innerHTML = ICONS.check + '<span>' + t('align.confirmed', 'Saved!') + '</span>';
        setTimeout(function () {
            btn.classList.remove('confirmed');
            btn.innerHTML = ICONS.check + '<span>' + t('align.confirm', 'Confirm & Close') + '</span>';
            close();
        }, 800);
    }

    function _highlightSaved() {
        var overlay = document.getElementById('alignmentStudioOverlay');
        if (!overlay) return;
        overlay.querySelectorAll('.as-technique-card').forEach(function (card) {
            card.classList.toggle('saved', card.dataset.technique === state.savedTechnique);
        });
        overlay.querySelectorAll('.as-btn-save').forEach(function (btn) {
            btn.classList.toggle('is-saved', btn.dataset.technique === state.savedTechnique);
        });
    }

    function _updateSavedIndicator() {
        var el = document.getElementById('asSavedIndicator');
        if (!el) return;
        if (state.savedTechnique && state.savedTechnique !== 'direct') {
            el.innerHTML = ICONS.check + '<span>Saved: ' + _getTechName(state.savedTechnique) + '</span>';
            el.className = 'as-saved-indicator active';
        } else {
            el.innerHTML = '<span>No alignment saved</span>';
            el.className = 'as-saved-indicator';
        }
    }

    function _markCardTested(techId, metrics) {
        var card = document.querySelector('.as-technique-card[data-technique="' + techId + '"]');
        if (!card) return;
        card.classList.add('tested', 'success-pulse');
        setTimeout(function () { card.classList.remove('success-pulse'); }, 800);

        // Show mini-metrics on the card
        var statusEl = document.getElementById('asStatus_' + techId);
        if (statusEl && metrics) {
            var parts = [];
            if (metrics.applied) {
                if (metrics.rotation_deg && Math.abs(metrics.rotation_deg) > 0.01)
                    parts.push(ICONS.rotateCw + ' ' + metrics.rotation_deg + '°');
                if (metrics.translation_x !== undefined && (Math.abs(metrics.translation_x) > 0.1 || Math.abs(metrics.translation_y) > 0.1))
                    parts.push(ICONS.move + ' (' + metrics.translation_x + ', ' + metrics.translation_y + ')px');
                if (metrics.correlation_coefficient !== undefined)
                    parts.push('r=' + metrics.correlation_coefficient);
                if (metrics.alignment_quality !== undefined)
                    parts.push('q=' + metrics.alignment_quality);
                statusEl.innerHTML = '<span class="as-mini-metric success">' + (parts.length > 0 ? parts.join(' | ') : 'Aligned') + '</span>';
            } else {
                statusEl.innerHTML = '<span class="as-mini-metric neutral">' + (metrics.reason || 'No correction needed') + '</span>';
            }
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // Preview Rendering
    // ═══════════════════════════════════════════════════════════════

    function _switchPreviewTab(tabId) {
        state.previewTab = tabId;
        var overlay = document.getElementById('alignmentStudioOverlay');
        overlay.querySelectorAll('.as-preview-tab').forEach(function (tab) {
            tab.classList.toggle('active', tab.dataset.preview === tabId);
        });
        _renderPreview();
    }

    function _showSourceImages() {
        if (!state.refImageSrc || !state.sampleImageSrc) return;
        var area = document.getElementById('asPreviewArea');
        var empty = document.getElementById('asPreviewEmpty');
        if (empty) empty.style.display = 'none';
        area.innerHTML = _keepProcessingOverlay() +
            '<div class="as-preview-images as-fade-in">' +
                '<div class="as-preview-pane">' +
                    '<span class="as-preview-label ref">' + t('align.reference', 'Reference') + '</span>' +
                    '<div class="as-preview-img-wrap"><img src="' + state.refImageSrc + '" alt="Reference"></div>' +
                '</div>' +
                '<div class="as-preview-pane">' +
                    '<span class="as-preview-label sample">' + t('align.sample', 'Sample') + '</span>' +
                    '<div class="as-preview-img-wrap"><img src="' + state.sampleImageSrc + '" alt="Sample"></div>' +
                '</div>' +
            '</div>';
    }

    function _renderPreviewAnimated() {
        _renderPreview(true);
    }

    function _renderPreview(animate) {
        if (!state.currentPreviews) return;
        var area = document.getElementById('asPreviewArea');
        var p = state.currentPreviews;
        var m = state.currentMetrics || {};
        var cls = animate ? ' as-slide-in' : '';
        var html = _keepProcessingOverlay();

        // Build transform indicator overlay
        var indicatorHTML = _buildTransformIndicator(m);

        // Only show side-by-side comparison
        html += '<div class="as-preview-images' + cls + '">' +
            '<div class="as-preview-pane">' +
                '<span class="as-preview-label ref">' + t('align.reference', 'Reference') + '</span>' +
                '<div class="as-preview-img-wrap"><img src="' + (state.refImageSrc || '') + '" alt="Reference"></div>' +
            '</div>' +
            '<div class="as-preview-vs">' + ICONS.arrowRight + '</div>' +
            '<div class="as-preview-pane">' +
                '<span class="as-preview-label aligned">' + t('align.aligned', 'Aligned Sample') + '</span>' +
                '<div class="as-preview-img-wrap as-aligned-wrap">' +
                    indicatorHTML +
                    '<img class="as-aligned-img' + (animate ? ' as-img-reveal' : '') + '" src="data:image/png;base64,' + p.aligned + '" alt="Aligned">' +
                '</div>' +
            '</div>' +
        '</div>';
        
        area.innerHTML = html;
    }

    function _buildTransformIndicator(m) {
        if (!m || !m.applied) return '';
        var lines = [];
        if (m.rotation_deg && Math.abs(m.rotation_deg) > 0.01)
            lines.push('<div class="as-indicator-item">' + ICONS.rotateCw + '<span>' + m.rotation_deg + '°</span></div>');
        if (m.translation_x !== undefined && (Math.abs(m.translation_x) > 0.1 || Math.abs(m.translation_y) > 0.1))
            lines.push('<div class="as-indicator-item">' + ICONS.move + '<span>(' + m.translation_x + ', ' + m.translation_y + ')px</span></div>');
        if (m.scale_factor !== undefined && Math.abs(m.scale_factor - 1.0) > 0.001)
            lines.push('<div class="as-indicator-item"><span>' + m.scale_factor + 'x</span></div>');
        if (lines.length === 0) return '';
        return '<div class="as-transform-indicator">' + lines.join('') + '</div>';
    }

    function _renderDirectMetrics() {
        var bar = document.getElementById('asMetricsBar');
        if (!bar) return;
        bar.innerHTML = '<span class="as-metric-status not-applied">Direct — No alignment preprocessing</span>';
    }

    function _renderMetrics() {
        var bar = document.getElementById('asMetricsBar');
        if (!bar || !state.currentMetrics) return;
        var m = state.currentMetrics;
        var parts = [];
        var applied = m.applied;

        parts.push('<span class="as-metric-status ' + (applied ? 'applied' : 'not-applied') + '">' +
            (applied ? t('align.status.applied', 'Corrected') : t('align.status.not.applied', 'No correction needed')) + '</span>');

        if (m.rotation_deg !== undefined && m.rotation_deg !== 0) {
            parts.push('<div class="as-metric-sep"></div>');
            parts.push('<div class="as-metric"><span class="as-metric-label">' + t('align.rotation', 'Rotation') + '</span><span class="as-metric-value">' + m.rotation_deg + '°</span></div>');
        }
        if (m.scale_factor !== undefined && m.scale_factor !== 1) {
            parts.push('<div class="as-metric-sep"></div>');
            parts.push('<div class="as-metric"><span class="as-metric-label">' + t('align.scale', 'Scale') + '</span><span class="as-metric-value">' + m.scale_factor + 'x</span></div>');
        }
        if (m.translation_x !== undefined && (m.translation_x !== 0 || m.translation_y !== 0)) {
            parts.push('<div class="as-metric-sep"></div>');
            parts.push('<div class="as-metric"><span class="as-metric-label">' + t('align.shift', 'Shift') + '</span><span class="as-metric-value">(' + m.translation_x + ', ' + m.translation_y + ')px</span></div>');
        }
        if (m.correlation_coefficient !== undefined) {
            parts.push('<div class="as-metric-sep"></div>');
            var ccClass = m.correlation_coefficient > 0.9 ? 'good' : (m.correlation_coefficient > 0.7 ? 'warn' : 'bad');
            parts.push('<div class="as-metric"><span class="as-metric-label">' + t('align.correlation', 'Correlation') + '</span><span class="as-metric-value ' + ccClass + '">' + m.correlation_coefficient + '</span></div>');
        }
        if (m.alignment_quality !== undefined) {
            parts.push('<div class="as-metric-sep"></div>');
            var qClass = m.alignment_quality > 0.9 ? 'good' : (m.alignment_quality > 0.7 ? 'warn' : 'bad');
            parts.push('<div class="as-metric"><span class="as-metric-label">' + t('align.quality', 'Quality') + '</span><span class="as-metric-value ' + qClass + '">' + m.alignment_quality + '</span></div>');
        }
        if (m.lighting_delta !== undefined && m.lighting_delta !== 0) {
            parts.push('<div class="as-metric-sep"></div>');
            var ldClass = Math.abs(m.lighting_delta) < 5 ? 'good' : (Math.abs(m.lighting_delta) < 15 ? 'warn' : 'bad');
            parts.push('<div class="as-metric"><span class="as-metric-label">' + t('align.lighting', 'Lighting \u0394') + '</span><span class="as-metric-value ' + ldClass + '">' + m.lighting_delta + '%</span></div>');
        }
        if (m.good_matches !== undefined) {
            parts.push('<div class="as-metric-sep"></div>');
            parts.push('<div class="as-metric"><span class="as-metric-label">' + t('align.matches', 'Matches') + '</span><span class="as-metric-value">' + m.good_matches + '</span></div>');
        }
        if (m.reason && !applied) {
            parts.push('<div class="as-metrics-spacer"></div>');
            parts.push('<div class="as-metric"><span class="as-metric-label as-metric-reason">' + m.reason + '</span></div>');
        }
        bar.innerHTML = parts.join('');
    }

    function _keepProcessingOverlay() {
        return '<div class="as-processing-overlay" id="asProcessingOverlay">' +
            '<div class="as-processing-spinner"></div>' +
            '<div class="as-processing-text" id="asProcessingText">Processing...</div>' +
            '<div class="as-processing-step" id="asProcessingStep"></div>' +
            '<div class="as-processing-bar"><div class="as-processing-bar-fill" id="asProcessingBarFill"></div></div>' +
        '</div>';
    }

    // ═══════════════════════════════════════════════════════════════
    // Image Helpers
    // ═══════════════════════════════════════════════════════════════

    function _hasImages() {
        if (state.refFile && state.sampleFile) return true;
        if (state.refImageSrc && state.sampleImageSrc) return true;
        return false;
    }

    function _getImageFiles(callback) {
        if (state.refFile && state.sampleFile) { callback(state.refFile, state.sampleFile); return; }
        var pending = 2, refBlob, sampleBlob;
        function check() { pending--; if (pending === 0) callback(refBlob, sampleBlob); }
        _srcToBlob(state.refImageSrc, function (b) { refBlob = b; check(); });
        _srcToBlob(state.sampleImageSrc, function (b) { sampleBlob = b; check(); });
    }

    function _srcToBlob(src, callback) {
        if (!src) { callback(new Blob()); return; }
        if (src instanceof Blob || src instanceof File) { callback(src); return; }
        fetch(src).then(function (r) { return r.blob(); }).then(callback).catch(function () { callback(new Blob()); });
    }

    function _getTechName(techId) { return t('align.name.' + techId, techId); }

    function _showToast(msg, type) {
        if (typeof showToast === 'function') { showToast(msg, type); }
        else if (typeof Desktop !== 'undefined' && Desktop.log) { Desktop.log(msg, type === 'error' ? 'error' : 'info'); }
        else { console.log('[AlignmentStudio] ' + type + ': ' + msg); }
    }

    function _updateI18n() {
        if (typeof I18n === 'undefined') return;
        var overlay = document.getElementById('alignmentStudioOverlay');
        if (overlay) {
            overlay.querySelectorAll('[data-i18n]').forEach(function (el) {
                var key = el.getAttribute('data-i18n');
                var translated = t(key, el.textContent);
                if (translated) el.textContent = translated;
            });
        }
    }

    // ═══════════════════════════════════════════════════════════════
    // Public API
    // ═══════════════════════════════════════════════════════════════

    return {
        open: open,
        close: close,
        isOpen: function () { return state.isOpen; },
        getAppliedTechnique: function () { return state.savedTechnique || state.appliedTechnique || 'direct'; },
        setAppliedTechnique: function (techId) { state.savedTechnique = techId; state.appliedTechnique = techId; },
    };

})();
