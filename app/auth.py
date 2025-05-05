from fastapi import Header, HTTPException

API_KEY = "mysecretkey"

def verify_api_key(x_api_key: str = Header(..., alias="x-api-key")):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
