import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))) # Add the parent directory to the path (fix for macOS)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

API_KEY = {"x-api-key": "mysecretkey"} 


def test_root():
    response = client.get("/", headers=API_KEY)
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the AI Notes App!"}

def test_create_note():
    note = {
        "title": "Test Note",
        "content": "This is a valid test note content"
    }
    response = client.post("/notes", json=note, headers=API_KEY)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == note["title"]
    assert data["content"] == note["content"]


def test_analyze_note_sentiment():
    # First, create a positive note
    note = {
        "title": "Happy Note",
        "content": "I am feeling fantastic and everything is amazing!"
    }
    post_response = client.post("/notes", json=note, headers=API_KEY)
    assert post_response.status_code == 200
    note_id = post_response.json()["id"]

    # Now, analyze the sentiment
    analyze_response = client.get(f"/notes/{note_id}/analyze", headers=API_KEY)
    assert analyze_response.status_code == 200
    data = analyze_response.json()

    # Check that sentiment is recognized correctly
    assert data["sentiment"] == "positive"
    assert data["id"] == note_id
    assert data["title"] == note["title"]


# negative sentiment test
def test_analyze_negative_sentiment():
    # Create a clearly negative note
    note = {
        "title": "Angry Note",
        "content": "This is horrible. Everything is bad and upsetting."
    }
    post_response = client.post("/notes", json=note, headers=API_KEY)
    assert post_response.status_code == 200
    note_id = post_response.json()["id"]

    # Analyze sentiment
    analyze_response = client.get(f"/notes/{note_id}/analyze", headers=API_KEY)
    assert analyze_response.status_code == 200
    data = analyze_response.json()

    # Check the result
    assert data["sentiment"] == "negative"
    assert data["id"] == note_id
    assert data["title"] == note["title"]

