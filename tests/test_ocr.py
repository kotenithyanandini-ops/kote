import io
from PIL import Image, ImageDraw
from ocr import extract_text_from_image

def test_ocr_extraction_valid_image():
    img = Image.new('RGB', (350, 80), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 10), 'Alert: Verify bank login', fill=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    img_bytes = buf.getvalue()

    result = extract_text_from_image(img_bytes)
    assert result["success"] is True
    assert "Verify" in result["extracted_text"] or "bank" in result["extracted_text"]

def test_ocr_empty_bytes():
    result = extract_text_from_image(b"")
    assert result["success"] is False
    assert "No image data" in result["error"]
