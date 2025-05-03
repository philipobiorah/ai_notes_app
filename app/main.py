from fastapi import FastAPI

app = FastAPI()


#basic route
@app.get("/")
def root():
    return {"message": "Welcome to the AI Notes App!"}


