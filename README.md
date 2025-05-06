# AI Notes App

AI Notes App is a full-stack note-taking application that provides JWT-based user authentication and sentiment analysis using natural language processing. It is built with FastAPI for the backend, React for the frontend, and Docker Compose for deployment.

## Features

- Secure login system using JWT tokens
- Create, list, and manage notes
- Sentiment analysis using TextBlob (positive, neutral, negative)
- SQLite database with persistent Docker volume
- Dockerized frontend and backend
- Clean REST API with Swagger documentation

## Technologies Used

- Python, FastAPI, SQLAlchemy
- React, Axios
- SQLite, TextBlob
- Docker, Docker Compose


## Project Structure

```
ai_notes_app/
├── app/                   # FastAPI backend
│   ├── main.py
│   ├── database.py
│   ├── auth_jwt.py
│   └── data/              # SQLite database location
├── frontend/              # React frontend
│   ├── src/
│   └── Dockerfile
├── requirements.txt       # Python dependencies
├── Dockerfile             # Backend Dockerfile
├── docker-compose.yml     # Orchestration file
```



## Prerequisites

- Docker and Docker Compose installed


## Getting Started with Docker Compose

1. Clone the repository:

```bash
git clone https://github.com/philipobiorah/ai-notes-app.git
cd ai-notes-app

```
2. Build and start the application
```bash
docker-compose up --build
```
3. Access the application
   - Frontend: http://localhost:3000
   - Backend API (Swagger): http://localhost:8000/docs

4. Default Credentials
    - Username: admin
    - Password: password
  
API Endpoints
All endpoints require a valid JWT in the Authorization header (Bearer <token>).

- POST /token – Login to get JWT token

- GET /notes – Get all notes

- POST /notes – Create a new note

- GET /notes/{id}/analyze – Analyze sentiment of a note

Development without Docker (optional)
```bash
cd app
python -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload
```
Frontend
```bash
cd frontend
npm install
npm start
```
Data Persistence
The SQLite database is stored in a volume mounted to the host
```bash
./dbdata:/app/app/data
```


