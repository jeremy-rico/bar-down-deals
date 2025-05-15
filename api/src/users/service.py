from datetime import timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import settings
from src.core.emails import send_reset_email, send_welcome_email
from src.core.exceptions import NotFoundException, UnauthorizedException
from src.core.logging import get_logger
from src.core.security import (
    create_access_token,
    create_reset_access_token,
    verify_password,
    verify_reset_token,
)
from src.users.models import (
    ForgotPasswordResponse,
    LoginData,
    Token,
    UserCreate,
    UserResponse,
    Users,
    UserUpdate,
)
from src.users.repository import UserRepository

logger = get_logger(__name__)


class UserService:
    """Service for handling user business logic."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UserRepository(session)

    async def create_user(self, user_data: UserCreate) -> Users:
        """Create a new user."""
        await send_welcome_email(user_data.email)
        return await self.repository.create(user_data)

    async def authenticate(self, login_data: LoginData) -> Token:
        """Authenticate user and return token."""
        # Get user
        user = await self.repository.get_by_email(login_data.email)

        # Verify credentials
        if not user or not verify_password(
            login_data.password, str(user.hashed_password)
        ):
            raise UnauthorizedException(detail="Incorrect email or password")

        # Create access token
        access_token = create_access_token(
            data={"sub": str(user.id)},
            expires_delta=timedelta(minutes=settings.JWT_EXPIRATION),
        )

        logger.info(f"User authenticated: {user.email}")
        return Token(access_token=access_token)

    async def get_user(self, user_id: int) -> UserResponse:
        """Get user by ID."""
        user = await self.repository.get_by_id(user_id)
        return UserResponse.model_validate(user)

    async def update_user(self, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = await self.repository.update_by_id(user_id, user_data)
        return UserResponse.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        """Delete user by id"""
        await self.repository.delete(user_id)

    async def forgot_password(self, user_email: str) -> ForgotPasswordResponse:
        """Generate temp token for passowrd reset. No repo call"""
        user = await self.repository.get_by_email(user_email)
        if not user:
            raise NotFoundException(f"No user with email {user_email} found")

        access_token = create_reset_access_token(
            data={"sub": str(user_email)},
            expires_delta=timedelta(minutes=settings.RESET_PASSWORD_JWT_EXPIRATION),
        )
        response = ForgotPasswordResponse(email=user_email, token=access_token)
        await send_reset_email(
            to=user_email,
            reset_link=f"https://bardowndeals.com/password/reset?token={response.token}",
        )

        return response

    async def reset_password(self, token: str, new_password: str) -> UserResponse:
        user_email = verify_reset_token(token)
        user = await self.repository.get_by_email(user_email)
        user_data = UserUpdate(password=new_password)
        user = await self.repository.update_by_id(user_id=user.id, user_data=user_data)
        return UserResponse.model_validate(user)
