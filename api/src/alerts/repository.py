from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, delete, select

from src.alerts.models import UserAlert, UserAlertResponse
from src.core.exceptions import NotFoundException
from src.core.logging import get_logger
from src.users.models import Users

logger = get_logger(__name__)


class AlertRepository:
    """Repository for handling user database operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, user: Users) -> list[UserAlert]:
        """
        Get all alerts for current user
        """
        stmt = select(UserAlert).where(UserAlert.user_id == user.id)
        result = await self.session.execute(stmt)

        return list(result.scalars().all())

    async def create(self, user: Users, keyword: str, frequency: str) -> UserAlert:
        """
        Create new user alert

        Args:
            user: current user
            kws: keywords to create alerts for

        Returns:
            UserAlert
        """
        user_alert = UserAlert(user_id=user.id, keyword=keyword, frequency=frequency)
        self.session.add(user_alert)
        await self.session.commit()
        await self.session.refresh(user_alert)
        return user_alert

    async def delete(self, alert_id: int) -> None:
        """Delete alert by ID.

        Args:
            alert_id: User ID

        Returns:
            UserAlert: Deleted alert

        Raises:
            NotFoundException: If user not found
        """
        stmt = delete(UserAlert).where(col(UserAlert.id) == alert_id)
        result = await self.session.execute(stmt)

        if result.rowcount == 0:
            raise NotFoundException("No alert with id {alert_id}")

        await self.session.commit()
