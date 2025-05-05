from src.alerts.models import UserAlert, UserAlertResponse
from src.alerts.repository import AlertRepository
from src.core.logging import get_logger
from src.users.models import Users

logger = get_logger(__name__)


class AlertService:
    """Service for handling user business logic."""

    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def get_user_alerts(self, user: Users) -> list[UserAlertResponse]:
        """Create user alert"""
        return await self.repository.get_all(user)

    async def create_alert(
        self, user: Users, keyword: str, frequency: str
    ) -> UserAlert:
        """Create user alert"""
        return await self.repository.create(user, keyword, frequency)

    async def delete_alert(self, alert_id: int) -> None:
        """Create user alert"""
        return await self.repository.delete(alert_id)
