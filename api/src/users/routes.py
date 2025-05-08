from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import get_session
from src.core.logging import get_logger
from src.core.security import get_current_user
from src.users.models import LoginData, Token, UserCreate, UserResponse, UserUpdate
from src.users.service import UserService

logger = get_logger(__name__)

router = APIRouter(prefix="/auth", tags=["auth"])

# Resolve nested model forward references
from src.alerts.models import UserAlertResponse

UserResponse.model_rebuild()


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
async def get_me(user: UserResponse = Depends(get_current_user)) -> UserResponse:
    """Get current authenticated user."""
    return user


@router.patch("/me", response_model=UserResponse)
async def update_hero(
    user_data: UserUpdate,
    user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Update user"""
    logger.debug(f"Updating user {user.id}")
    try:
        hero = await UserService(session).update_user(user.id, user_data)
        logger.info(f"Updated user {hero.id}")
        return hero
    except Exception as e:
        logger.error(f"Failed to update user {user.id}: {str(e)}")
        raise


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> None:
    """Get current authenticated user."""
    # TODO: Expire session on delete
    try:
        await UserService(session).delete_user(user.id)
        logger.info(f"Deleted user {user.id}")
    except Exception as e:
        logger.error(f"Failed to delete user {user.id}: {e}")
