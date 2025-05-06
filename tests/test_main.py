import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # Fix for macOS module import

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Get JWT token
def get_auth_headers():
    login_data = {
        "username": "admin",
        "password": "password"
    }
    response = client.post("/token", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_root():
    headers = get_auth_headers()
    response = client.get("/", headers=headers)
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Notes App!"}


def test_create_note():
    headers = get_auth_headers()
    note = {
        "title": "Test Note",
        "content": "This is a valid test note content"
    }
    response = client.post("/notes", json=note, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == note["title"]
    assert data["content"] == note["content"]


def test_analyze_note_sentiment():
    headers = get_auth_headers()
    note = {
        "title": "Happy Note",
        "content": "I am feeling fantastic and everything is amazing!"
    }
    post_response = client.post("/notes", json=note, headers=headers)
    assert post_response.status_code == 200
    note_id = post_response.json()["id"]

    analyze_response = client.get(f"/notes/{note_id}/analyze", headers=headers)
    assert analyze_response.status_code == 200
    data = analyze_response.json()
    assert data["sentiment"] == "positive"
    assert data["id"] == note_id
    assert data["title"] == note["title"]


def test_analyze_negative_sentiment():
    headers = get_auth_headers()
    note = {
        "title": "Angry Note",
        "content": "This is horrible. Everything is bad and upsetting."
    }
    post_response = client.post("/notes", json=note, headers=headers)
    assert post_response.status_code == 200
    note_id = post_response.json()["id"]

    analyze_response = client.get(f"/notes/{note_id}/analyze", headers=headers)
    assert analyze_response.status_code == 200
    data = analyze_response.json()
    assert data["sentiment"] == "negative"
    assert data["id"] == note_id
    assert data["title"] == note["title"]
