import io
import pytest
from app import app
from PIL import Image, ImageDraw

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'AI Scam Message Detector' in response.data

def test_get_examples_route(client):
    response = client.get('/api/examples')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert len(data['examples']) > 0

def test_analyze_endpoint_valid(client):
    payload = {
        "text": "ALERT: Your bank account is suspended. Click http://scam.xyz to restore immediately!",
        "platform": "sms"
    }
    response = client.post('/api/analyze', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'success'
    assert data['analysis']['score'] >= 60
    assert data['analysis']['level'] == 'High'

def test_analyze_endpoint_empty_text(client):
    response = client.post('/api/analyze', json={"text": ""})
    assert response.status_code == 400
    data = response.get_json()
    assert data['status'] == 'error'

def test_ocr_endpoint_valid_image(client):
    img = Image.new('RGB', (300, 60), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    d.text((10, 10), 'Urgent action required', fill=(0, 0, 0))

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)

    data = {
        'image': (buf, 'test_screenshot.png'),
        'platform': 'whatsapp'
    }
    response = client.post('/api/ocr', data=data, content_type='multipart/form-data')
    assert response.status_code == 200
    res_data = response.get_json()
    assert res_data['status'] == 'success'
    assert 'analysis' in res_data

def test_ocr_endpoint_no_file(client):
    response = client.post('/api/ocr', data={})
    assert response.status_code == 400
    res_data = response.get_json()
    assert res_data['status'] == 'error'
