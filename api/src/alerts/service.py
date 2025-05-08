from fastapi import HTTPException, status

from src.alerts.models import UserAlert, UserAlertResponse
from src.alerts.repository import AlertRepository
from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class AlertService:
    """Service for handling user business logic."""

    def __init__(self, repository: AlertRepository):
        self.repository = repository

    async def get_user_alerts(self, user_id: int) -> list[UserAlertResponse]:
        """Create user alert"""
        alerts = await self.repository.get_all(user_id)
        return [UserAlertResponse.model_validate(alert) for alert in alerts]

    async def create_alert(
        self,
        user_id: int,
        size: str | None,
        brand: str | None,
        tag: str | None,
        keyword: str | None,
    ) -> UserAlert:
        """Create user alert"""
        alerts = await self.repository.get_all(user_id)
        if len(alerts) >= settings.MAX_ALERTS:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Only {settings.MAX_ALERTS} alerts allowed per user",
            )

        return await self.repository.create(
            user_id=user_id,
            size=size,
            brand=brand,
            tag=tag,
            keyword=keyword,
        )

    async def delete_alert(self, alert_id: int) -> None:
        """Create user alert"""
        return await self.repository.delete(alert_id)
