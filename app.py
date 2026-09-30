from flask import Flask, render_template, request, jsonify
from config import Config
from detector import analyze_message, SAFETY_DISCLAIMER
from ocr import extract_text_from_image

app = Flask(__name__)
app.config.from_object(Config)

# Preset demonstration examples
EXAMPLE_MESSAGES = [
    {
        "id": "ex_whatsapp_scam",
        "title": "WhatsApp Job Scam",
        "platform": "whatsapp",
        "type": "Scam",
        "text": "Hello! I am HR manager from Amazon. We offer daily work from home job earning $200-$500/day. No experience needed! Contact us on Telegram: @amazon_job_hr immediately to claim your slot."
    },
    {
        "id": "ex_sms_scam",
        "title": "SMS Bank Phishing",
        "platform": "sms",
        "type": "Scam",
        "text": "ALERT: Your bank account has been locked due to unauthorized activity. Verify your PIN and account immediately at http://secure-bank-verify.xyz/login within 2 hours or account will be blocked!"
    },
    {
        "id": "ex_email_scam",
        "title": "Email Lottery / Inheritance",
        "platform": "email",
        "type": "Scam",
        "text": "Congratulations! You have won $1,000,000 USD in International Wealth Grant. To claim your cash reward, please reply with your full name, bank details, and OTP code."
    },
    {
        "id": "ex_safe_meeting",
        "title": "Legitimate Meeting Request",
        "platform": "whatsapp",
        "type": "Safe",
        "text": "Hi Alex, hope you are doing well. Are we still meeting tomorrow at 3 PM for the project presentation in Room 204?"
    },
    {
        "id": "ex_safe_shipping",
        "title": "Official Delivery Update",
        "platform": "sms",
        "type": "Safe",
        "text": "Your package #183924 has been shipped and is scheduled for delivery today by 5 PM. Track package on official app."
    }
]


def allowed_file(filename):
    """Check if uploaded file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Render main dashboard view."""
    return render_template('index.html')


@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Returns preset example messages for demo."""
    return jsonify({"status": "success", "examples": EXAMPLE_MESSAGES})


@app.route('/api/analyze', methods=['POST'])
def analyze():
    """Endpoint to analyze plain text message."""
    data = request.get_json(silent=True) or {}
    message_text = data.get('text', '').strip()
    platform = data.get('platform', 'general').strip()

    if not message_text:
        return jsonify({
            "status": "error",
            "message": "Message text cannot be empty."
        }), 400

    if len(message_text) > 10000:
        return jsonify({
            "status": "error",
            "message": "Message text exceeds maximum length limit of 10,000 characters."
        }), 400

    analysis = analyze_message(message_text, platform)

    return jsonify({
        "status": "success",
        "analysis": analysis
    })


@app.route('/api/ocr', methods=['POST'])
def process_ocr():
    """Endpoint to upload screenshot image, perform OCR, and optionally auto-analyze."""
    if 'image' not in request.files:
        return jsonify({"status": "error", "message": "No image file provided in request."}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No file selected."}), 400

    if not allowed_file(file.filename):
        return jsonify({
            "status": "error",
            "message": f"Unsupported file type. Allowed formats: {', '.join(Config.ALLOWED_EXTENSIONS)}"
        }), 400

    try:
        image_bytes = file.read()
        ocr_result = extract_text_from_image(image_bytes)

        if not ocr_result.get("success"):
            return jsonify({
                "status": "error",
                "message": ocr_result.get("error", "OCR processing failed.")
            }), 500

        extracted_text = ocr_result.get("extracted_text", "")
        platform = request.form.get("platform", "general")

        # Automatically run detection if text extracted
        analysis = None
        if extracted_text:
            analysis = analyze_message(extracted_text, platform)

        return jsonify({
            "status": "success",
            "extracted_text": extracted_text,
            "character_count": ocr_result.get("character_count", 0),
            "analysis": analysis
        })

    except Exception as e:
        return jsonify({"status": "error", "message": f"Server error processing image: {str(e)}"}), 500


@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"status": "error", "message": "File size exceeds 5MB limit."}), 413


@app.errorhandler(404)
def not_found(error):
    return jsonify({"status": "error", "message": "Resource not found."}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"status": "error", "message": "An internal server error occurred."}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
