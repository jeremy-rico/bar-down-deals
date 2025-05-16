from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, delete, select, update

from src.core.exceptions import (
    AlreadyExistsException,
    NotFoundException,
    NoValueException,
)
from src.core.logging import get_logger
from src.core.security import get_password_hash
from src.users.models import UserCreate, Users, UserUpdate

logger = get_logger(__name__)


class UserRepository:
    """Repository for handling user database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_data: UserCreate) -> Users:
        """
        Create a new user.

        Args:
            user_data: User creation data

        Returns:
            User: Created user

        Raises:
            AlreadyExistsException: If user with same email already exists
        """
        # Check if user exists
        existing_user = await self.get_by_email(user_data.email)
        if existing_user:
            raise AlreadyExistsException(
                f"User with email {user_data.email} already exists"
            )

        # Create user
        user = Users(
            email=user_data.email,
            hashed_password=get_password_hash(user_data.password),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        logger.info(f"Created user: {user.email}")
        return user

    async def get_by_id(self, user_id: int) -> Users:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User: Found user

        Raises:
            NotFoundException: If user not found
        """
        stmt = select(Users).where(Users.id == user_id)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()

        if not user:
            raise NotFoundException("User not found")

        return user

    async def get_by_email(self, email: str) -> Users | None:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            Optional[User]: Found user or None if not found
        """
        query = select(Users).where(Users.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def update_by_id(self, user_id: int, user_data: UserUpdate) -> Users:
        """Update user by ID.

        Args:
            user_id: User ID
            user_data: User update data

        Returns:
            Users: Updated User

        Raises:
            NotFoundException: If user not found
        """
        update_data = user_data.model_dump(exclude_unset=True)
        if not update_data:
            raise NoValueException("No fields to update")

        if update_data.get("password"):
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            update_data.pop("password")

        query = update(Users).where(col(Users.id) == user_id).values(**update_data)
        result = await self.session.execute(query)

        if result.rowcount == 0:
            raise NotFoundException(f"User with id {user_id} not found")

        await self.session.commit()
        return await self.get_by_id(user_id)

    async def delete(self, user_id: int) -> None:
        """
        Delete user by id

        Args:
            user_id: user id

        Returns:
            None
        """
        stmt = delete(Users).where(col(Users.id) == user_id)
        await self.session.execute(stmt)
        await self.session.commit()
