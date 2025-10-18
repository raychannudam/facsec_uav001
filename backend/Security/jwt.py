import os
from dotenv import load_dotenv
from fastapi import HTTPException, APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from Models import UserModel, get_db, StreamingClientModel, MqttClientModel, StreamingUrlModel
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
import jwt
from pydantic import BaseModel
from Schemas.StreamingClient import StreamingLoginSchema
from fastapi import Form, Request
from enum import Enum

load_dotenv()

router = APIRouter()

class AUTH_SOURCE(str, Enum):
    SYSTEM = "system"
    MEDIAMTX = "mediamtx"
    MOSQUITTO = "mosquitto"

# Security and password hashing
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/token",
    scopes={"admin": "Admin privileges", "user": "User privileges"}
)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Environment variables
SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 15))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.environ.get("REFRESH_TOKEN_EXPIRE_MINUTES", 60))

# Pydantic models
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []

# Password verification
def verify_password(plain_password, hashed_password):
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

# Database user retrieval
def get_user(username: str, db: Session, source: AUTH_SOURCE):
    if source == AUTH_SOURCE.SYSTEM:
        return db.query(UserModel).filter(UserModel.username == username).first()
    if source == AUTH_SOURCE.MEDIAMTX:
        return db.query(StreamingClientModel).filter(StreamingClientModel.username == username, StreamingClientModel.status == True).first()
    if source == AUTH_SOURCE.MOSQUITTO:
        return db.query(MqttClientModel).filter(MqttClientModel.username == username, MqttClientModel.status == True).first()
    return None

# Authenticate user
def authenticate_user(username: str, password: str, db: Session, source: AUTH_SOURCE = AUTH_SOURCE.SYSTEM):
    user = get_user(username, db, source)
    if user is None or not verify_password(password, user.password):
        return False
    return user

# Token creation
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Dependency: get current user
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        scopes = payload.get("scopes", [])
        if username is None or token_type != "access":
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(username=username, db=db, source=AUTH_SOURCE.SYSTEM)
    if user is None:
        raise credentials_exception
    return user

# Role-based access
def require_roles(*roles):
    async def role_checker(current_user: UserModel = Depends(get_current_user)):
        user_roles = [role.name for role in current_user.roles]
        if not any(role in user_roles for role in roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Requires one of roles: {roles}"
            )
        return current_user
    return role_checker

# Login endpoint (returns access + refresh tokens)
@router.post("/token", response_model=Token)
async def get_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": user.username, "scopes": [role.name for role in user.roles]},
        expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username},
        expires_delta=refresh_token_expires
    )

    return Token(access_token=access_token, refresh_token=refresh_token)

# Refresh token endpoint
@router.post("/token/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str, db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        token_type = payload.get("type")
        if username is None or token_type != "refresh":
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    user = get_user(username=username, db=db)
    if user is None:
        raise credentials_exception

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token(
        data={"sub": user.username, "scopes": [role.name for role in user.roles]},
        expires_delta=access_token_expires
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=new_access_token, refresh_token=new_refresh_token)

@router.post("/streaming-login")
def mediamtx_login(login_req: StreamingLoginSchema, db: Session = Depends(get_db)):
    streaming_client = authenticate_user(login_req.user, login_req.password, db, source=AUTH_SOURCE.MEDIAMTX)
    action = login_req.action if login_req.action else ""
    path = login_req.path if login_req.path else ""
    action = login_req.action if login_req.action else ""
    protocol = login_req.protocol if login_req.protocol else ""
    print(login_req)
    if path == "" or action == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Path and action are required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not streaming_client:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if the user has access to the requested path
    streaming_url = db.query(StreamingUrlModel).filter(StreamingUrlModel.streaming_client_id == streaming_client.id, StreamingUrlModel.status == True).first()
    if not streaming_url:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No active streaming URLs found for this client",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if path != streaming_url.name:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Access to the {path} path is forbidden",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if protocol not in streaming_url.config["protocols"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Protocol '{protocol}' is not allowed for this path",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if action not in streaming_client.config["actions"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Action '{action}' is not permitted",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"status": "success"}

