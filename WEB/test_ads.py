import pytest
from flask import json
from flask import create_app  # Nahraďte `your_application` názvem vašeho hlavního modulu aplikace, kde je inicializován Flask app

@pytest.fixture
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_client()

def test_create_ad(client):
    """Testuje vytvoření nové reklamy."""
    response = client.post('/ads', json={
        'title': 'Test Ad',
        'image_url': 'http://example.com/image.jpg',
        'target_url': 'http://example.com',
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'active': True
    })
    assert response.status_code == 201
    assert 'ad_id' in json.loads(response.data)

def test_get_ads(client):
    """Testuje získání všech aktivních reklam."""
    response = client.get('/ads')
    assert response.status_code == 200
    assert isinstance(json.loads(response.data), list)  # Předpokládá, že databáze má již nějaké reklamy

def test_update_ad(client):
    """Testuje aktualizaci existující reklamy."""
    response = client.put('/ads/1', json={  # Předpokládá, že reklama s ID 1 existuje
        'title': 'Updated Title',
        'image_url': 'http://example.com/updated_image.jpg',
        'target_url': 'http://example.com/updated',
        'start_date': '2024-01-01',
        'end_date': '2024-12-31',
        'active': True
    })
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Ad updated'

def test_delete_ad(client):
    """Testuje smazání existující reklamy."""
    response = client.delete('/ads/1')  # Předpokládá, že reklama s ID 1 existuje
    assert response.status_code in [200, 404]  # Výsledek závisí na tom, jestli existuje
    data = json.loads(response.data)
    assert data['message'] in ["Ad deleted", "No ad found"]
