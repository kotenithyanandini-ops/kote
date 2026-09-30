document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const messageInput = document.getElementById('message-input');
    const platformSelect = document.getElementById('platform-select');
    const charCounter = document.getElementById('char-counter');
    const scanBtn = document.getElementById('scan-btn');
    const examplesContainer = document.getElementById('examples-container');

    // OCR Elements
    const dropzone = document.getElementById('dropzone');
    const screenshotInput = document.getElementById('screenshot-input');
    const selectedFileName = document.getElementById('selected-file-name');
    const ocrBtn = document.getElementById('ocr-btn');

    // UI Result State Containers
    const idleState = document.getElementById('idle-state');
    const loadingState = document.getElementById('loading-state');
    const resultContent = document.getElementById('result-content');
    const analysisSource = document.getElementById('analysis-source');

    // Result UI Elements
    const riskScoreDisplay = document.getElementById('risk-score-display');
    const riskLevelBadge = document.getElementById('risk-level-badge');
    const patternsList = document.getElementById('patterns-list');
    const wordsList = document.getElementById('words-list');
    const recommendationsList = document.getElementById('recommendations-list');
    const disclaimerText = document.getElementById('disclaimer-text');

    let selectedFile = null;

    // Load Demo Examples
    fetchExamples();

    // Event Listeners
    messageInput.addEventListener('input', () => {
        charCounter.textContent = messageInput.value.length;
    });

    scanBtn.addEventListener('click', () => {
        const text = messageInput.value.trim();
        if (!text) {
            alert('Please enter or paste a message to analyze.');
            return;
        }
        analyzeTextMessage(text, platformSelect.value);
    });

    // Dropzone / File Selection Logic
    dropzone.addEventListener('click', () => screenshotInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('dragover');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('dragover');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('dragover');
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    screenshotInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFileSelection(e.target.files[0]);
        }
    });

    ocrBtn.addEventListener('click', () => {
        if (!selectedFile) return;
        uploadAndAnalyzeScreenshot(selectedFile, platformSelect.value);
    });

    function handleFileSelection(file) {
        if (!['image/png', 'image/jpeg', 'image/jpg', 'image/webp'].includes(file.type)) {
            alert('Please select a valid image file (PNG, JPG, JPEG, WEBP).');
            return;
        }
        if (file.size > 5 * 1024 * 1024) {
            alert('Image size exceeds 5MB limit.');
            return;
        }
        selectedFile = file;
        selectedFileName.textContent = `📷 Selected file: ${file.name} (${(file.size / 1024).toFixed(1)} KB)`;
        selectedFileName.classList.remove('hidden');
        ocrBtn.disabled = false;
    }

    async function fetchExamples() {
        try {
            const resp = await fetch('/api/examples');
            const data = await resp.json();
            if (data.status === 'success' && data.examples) {
                renderExamples(data.examples);
            }
        } catch (err) {
            examplesContainer.innerHTML = '<p class="file-hint">Could not load examples.</p>';
        }
    }

    function renderExamples(examples) {
        examplesContainer.innerHTML = '';
        examples.forEach(ex => {
            const card = document.createElement('div');
            card.className = 'example-card';
            card.innerHTML = `
                <div class="ex-header">
                    <span class="ex-title">${escapeHtml(ex.title)}</span>
                    <span class="ex-tag ${ex.type === 'Scam' ? 'tag-scam' : 'tag-safe'}">${ex.type}</span>
                </div>
                <div class="ex-preview">${escapeHtml(ex.text)}</div>
            `;
            card.addEventListener('click', () => {
                messageInput.value = ex.text;
                platformSelect.value = ex.platform;
                charCounter.textContent = ex.text.length;
                analyzeTextMessage(ex.text, ex.platform);
            });
            examplesContainer.appendChild(card);
        });
    }

    async function analyzeTextMessage(text, platform) {
        showLoadingState();
        try {
            const resp = await fetch('/api/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text, platform })
            });

            const data = await resp.json();
            if (data.status === 'success' && data.analysis) {
                renderAnalysisResults(data.analysis);
            } else {
                alert(data.message || 'Analysis failed.');
                showIdleState();
            }
        } catch (err) {
            alert('Network error communicating with analysis backend.');
            showIdleState();
        }
    }

    async function uploadAndAnalyzeScreenshot(file, platform) {
        showLoadingState();
        const formData = new FormData();
        formData.append('image', file);
        formData.append('platform', platform);

        try {
            const resp = await fetch('/api/ocr', {
                method: 'POST',
                body: formData
            });

            const data = await resp.json();
            if (data.status === 'success') {
                if (data.extracted_text) {
                    messageInput.value = data.extracted_text;
                    charCounter.textContent = data.extracted_text.length;
                }
                if (data.analysis) {
                    renderAnalysisResults(data.analysis);
                } else {
                    alert('Text extracted successfully, but no risk analysis returned.');
                    showIdleState();
                }
            } else {
                alert(data.message || 'OCR processing failed.');
                showIdleState();
            }
        } catch (err) {
            alert('Network error uploading screenshot.');
            showIdleState();
        }
    }

    function renderAnalysisResults(analysis) {
        hideAllStates();

        // Source Tag
        if (analysis.source) {
            analysisSource.textContent = analysis.source;
            analysisSource.classList.remove('hidden');
        }

        // Score & Gauge Meter
        const score = analysis.score || 0;
        riskScoreDisplay.textContent = score;

        // Badge & Color Styling
        const level = (analysis.level || 'Low').toUpperCase();
        riskLevelBadge.textContent = level;
        riskLevelBadge.className = 'risk-badge';

        const riskMeter = document.querySelector('.risk-meter');

        if (level === 'HIGH') {
            riskLevelBadge.classList.add('badge-high');
            riskMeter.style.borderColor = 'var(--risk-high)';
            riskMeter.style.boxShadow = '0 0 20px rgba(239, 68, 68, 0.4)';
        } else if (level === 'MEDIUM') {
            riskLevelBadge.classList.add('badge-medium');
            riskMeter.style.borderColor = 'var(--risk-med)';
            riskMeter.style.boxShadow = '0 0 20px rgba(245, 158, 11, 0.4)';
        } else {
            riskLevelBadge.classList.add('badge-low');
            riskMeter.style.borderColor = 'var(--risk-low)';
            riskMeter.style.boxShadow = '0 0 20px rgba(16, 185, 129, 0.4)';
        }

        // Render Patterns
        patternsList.innerHTML = '';
        if (analysis.suspicious_patterns && analysis.suspicious_patterns.length > 0) {
            analysis.suspicious_patterns.forEach(item => {
                const patDiv = document.createElement('div');
                patDiv.className = 'pattern-item';
                patDiv.innerHTML = `
                    <div class="pattern-category">${escapeHtml(item.category)}</div>
                    <div class="pattern-desc">${escapeHtml(item.description)}</div>
                `;
                patternsList.appendChild(patDiv);
            });
        } else {
            patternsList.innerHTML = '<p class="pattern-desc">No known suspicious pattern indicators detected.</p>';
        }

        // Render Words / Keywords
        wordsList.innerHTML = '';
        if (analysis.found_words && analysis.found_words.length > 0) {
            analysis.found_words.forEach(word => {
                const chip = document.createElement('span');
                chip.className = 'word-chip';
                chip.textContent = word;
                wordsList.appendChild(chip);
            });
        } else {
            wordsList.innerHTML = '<p class="pattern-desc">No specific flag terms found.</p>';
        }

        // Render Recommendations
        recommendationsList.innerHTML = '';
        if (analysis.recommendations && analysis.recommendations.length > 0) {
            analysis.recommendations.forEach(rec => {
                const li = document.createElement('li');
                li.textContent = rec;
                recommendationsList.appendChild(li);
            });
        }

        // Render Disclaimer
        disclaimerText.textContent = analysis.disclaimer || 'Always verify senders carefully.';

        resultContent.classList.remove('hidden');
    }

    function showLoadingState() {
        hideAllStates();
        loadingState.classList.remove('hidden');
    }

    function showIdleState() {
        hideAllStates();
        idleState.classList.remove('hidden');
    }

    function hideAllStates() {
        idleState.classList.add('hidden');
        loadingState.classList.add('hidden');
        resultContent.classList.add('hidden');
        analysisSource.classList.add('hidden');
    }

    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/&/g, "&amp;")
                  .replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;")
                  .replace(/"/g, "&quot;")
                  .replace(/'/g, "&#039;");
    }
});
