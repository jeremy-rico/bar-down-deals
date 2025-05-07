from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.core.security import get_current_user
from src.users.models import LoginData, Token, UserCreate, UserResponse, Users
from src.users.service import UserService

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate, session: AsyncSession = Depends(get_session)
) -> Token:
    """Register a new user."""
    logger.debug(f"Registering user: {user_data.email}")
    login_data = LoginData(email=user_data.email, password=user_data.password)
    await UserService(session).create_user(user_data)
    return await UserService(session).authenticate(login_data)


@router.post("/login", response_model=Token)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_session),
) -> Token:
    """Authenticate user and return token."""
    login_data = LoginData(email=form_data.username, password=form_data.password)
    logger.debug(f"Login attempt: {login_data.email}")
    return await UserService(session).authenticate(login_data)


@router.get("/me", response_model=UserResponse)
async def get_me(user: Users = Depends(get_current_user)) -> Users:
    """Get current authenticated user."""
    return user
