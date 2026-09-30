# AI Scam Message Detector

An engineering capstone project featuring a cybersecurity intelligence web application that detects, analyzes, and evaluates potential scam messages across WhatsApp, SMS, and Email. The application provides scam risk classification (Low, Medium, High), numerical risk scoring (0–100), pattern analysis, actionable safety recommendations, and screenshot OCR text extraction.

---

## Key Features

1. **Multi-Platform Support**: Paste messages originating from WhatsApp, SMS, or Email.
2. **Scam Risk Classification**: Classifies messages as **Low**, **Medium**, or **High** risk.
3. **Risk Score Meter**: Calculates a detailed threat score from **0 to 100**.
4. **Pattern & Keyword Analysis**: Highlights suspicious urgency, financial lures, impersonation, phishing links, and bank security threats.
5. **Actionable Recommendations**: Offers context-specific security guidance based on threat severity.
6. **Screenshot OCR Extraction**: Upload screenshots (`PNG`, `JPG`, `JPEG`, `WEBP`) to automatically extract text via Tesseract OCR and run threat analysis.
7. **Cybersecurity Dashboard**: Modern, dark-themed, responsive web UI with real-time indicators and dynamic risk meter visualization.
8. **Preset Demo Scenarios**: Quick-load example messages representing common scams and legitimate communications.
9. **AI API & Rule Engine**: Dual detection capability—uses external AI API integrations (OpenAI, Gemini, Groq) with intelligent fallback to a deterministic rule-based pattern matching engine.
10. **Safety Disclaimer & Validation**: Emphasizes that low risk scores do not guarantee absolute safety, maintaining high security standards.

---

## Project Directory Structure

```
.
├── app.py                  # Flask Web Application & REST API routes
├── config.py               # Application configuration and env var management
├── detector.py             # Core scam analysis engine (Rule engine + AI API fallback)
├── ocr.py                  # Tesseract OCR screenshot extraction module
├── requirements.txt        # Python package dependencies
├── .env.example            # Sample environment variables template
├── templates/
│   └── index.html          # Main HTML5 cybersecurity dashboard
├── static/
│   ├── css/
│   │   └── styles.css      # Custom dark cybersecurity UI styling
│   └── js/
│       └── main.js         # Frontend interactive AJAX & UI logic
└── tests/
    ├── test_app.py         # Integration tests for Flask endpoints
    ├── test_detector.py    # Unit tests for scam detector logic
    └── test_ocr.py         # Unit tests for OCR image extraction
```

---

## Requirements & Prerequisites

- **Python**: 3.10+ (Tested on Python 3.12)
- **Tesseract OCR**: Required for screenshot OCR functionality.
  - **Linux (Debian/Ubuntu)**: `sudo apt-get install -y tesseract-ocr`
  - **macOS**: `brew install tesseract`
  - **Windows**: Download Tesseract-OCR installer and add to system PATH or configure `TESSERACT_CMD` in `.env`.

---

## Installation & Setup

1. **Clone or Navigate to the Repository Directory**:
   ```bash
   cd /path/to/repository
   ```

2. **Create and Activate a Virtual Environment** (Optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variable Configuration**:
   Copy `.env.example` to `.env` (or set environment variables):
   ```bash
   cp .env.example .env
   ```
   Configure variables as needed:
   ```env
   SECRET_KEY=your-flask-secret-key
   AI_API_KEY=your-optional-ai-api-key
   AI_PROVIDER=openai  # Options: openai, gemini, groq
   TESSERACT_CMD=/usr/bin/tesseract  # Optional path override
   ```
   *Note: If no `AI_API_KEY` is provided, the application automatically uses the built-in deterministic rule engine.*

---

## Running the Application

Start the Flask development server:
```bash
python3 app.py
```
Open your web browser and navigate to:
`http://127.0.0.1:5000`

---

## Running Automated Tests

To execute the complete unit and integration test suite:
```bash
pytest
```
Or run python's built-in unittest framework:
```bash
python3 -m unittest discover -v -s tests
```

---

## Security & Ethics Considerations

- **API Keys**: API keys are securely read from server environment variables and **never** exposed to client-side frontend code.
- **Low Risk Disclaimer**: The application explicitly alerts users that a Low risk score does not guarantee 100% message safety. Users are always encouraged to maintain vigilance and verify senders independently.
