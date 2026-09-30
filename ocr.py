import io
from PIL import Image, ImageEnhance, ImageFilter
import pytesseract
from config import Config

if Config.TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_CMD


def extract_text_from_image(image_bytes: bytes) -> dict:
    """
    Processes an image file byte buffer and extracts text using Tesseract OCR.
    Includes image preprocessing for better readability.
    """
    if not image_bytes:
        return {"success": False, "error": "No image data provided", "extracted_text": ""}

    try:
        # Load image with PIL
        image = Image.open(io.BytesIO(image_bytes))

        # Convert palette/RGBA images to RGB
        if image.mode in ("P", "RGBA"):
            image = image.convert("RGB")

        # Basic Preprocessing: Grayscale & Contrast Enhancement
        gray_image = image.convert("L")
        enhancer = ImageEnhance.Contrast(gray_image)
        enhanced_image = enhancer.enhance(1.8)

        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(enhanced_image)
        cleaned_text = extracted_text.strip()

        if not cleaned_text:
            # Fallback attempt on original image
            extracted_text = pytesseract.image_to_string(image)
            cleaned_text = extracted_text.strip()

        return {
            "success": True,
            "extracted_text": cleaned_text,
            "character_count": len(cleaned_text),
            "message": "Text extracted successfully" if cleaned_text else "No text detected in image"
        }

    except Exception as e:
        return {
            "success": False,
            "error": f"Failed to process image: {str(e)}",
            "extracted_text": ""
        }
