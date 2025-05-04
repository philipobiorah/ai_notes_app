from fastapi import Header, HTTPException


# API key security logic
API_KEY = "MySecretAPIKey"

def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden: Invalid API Key")
    
