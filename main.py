import os
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

app = FastAPI(title="Local JWT Auth API", version="1.0")
security = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
fake_users_db = {}

class UserCredentials(BaseModel):
    email: str
    password: str

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(credentials: UserCredentials):
    if credentials.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pwd = hash_password(credentials.password)
    fake_users_db[credentials.email] = {"email": credentials.email, "password": hashed_pwd}
    return {"message": "User registered successfully", "email": credentials.email}

@app.post("/auth/login")
def login(credentials: UserCredentials):
    user = fake_users_db.get(credentials.email)
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid login credentials")
    access_token = create_access_token(data={"sub": credentials.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/public/info")
def public_info():
    return {"message": "Welcome! This endpoint is open to everyone."}

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        return email
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

@app.get("/protected/profile")
def protected_profile(current_user: str = Depends(verify_token)):
    return {"message": "Access granted to protected route", "user_email": current_user}

@app.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    return None
