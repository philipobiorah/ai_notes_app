from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta

# Settings
SECRET_KEY = "your-secret-key"  # use a secure, long key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Token retrieval method (from header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Password hashing (optional for real user system)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dummy user for demo
fake_user = {
    "username": "admin",
    "hashed_password": pwd_context.hash("password")
}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(username: str, password: str):
    if username != fake_user["username"]:
        return False
    if not verify_password(password, fake_user["hashed_password"]):
        return False
    return {"username": username}

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_jwt_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=403,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
