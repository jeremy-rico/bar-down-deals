from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.core.config import settings
from src.core.database import get_session
from src.users.models import UserResponse

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid authentication credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.JWT_EXPIRATION)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def create_reset_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    """Create temporary JWT access token for password resets."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.RESET_PASSWORD_JWT_EXPIRATION)
    )
    to_encode.update({"exp": expire})
    to_encode.update({"type": "reset"})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def verify_reset_token(token: str) -> str | None:
    """Verify reset JWT access token for password resets"""
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM
        )
        if payload.get("type") != "reset":
            return None
        return payload.get("sub")
    except JWTError:
        raise credentials_exception


# Import here to avoid circulat imports
from src.users.service import UserService


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserResponse:
    """Dependency to get current authenticated user."""

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    async for session in get_session():
        user = await UserService(session).get_user(int(user_id))
        if user is None:
            raise credentials_exception
        return user

    # if no loop
    raise credentials_exception
