from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.alerts.models import QueryParams, UserAlert, UserAlertResponse
from src.alerts.repository import AlertRepository
from src.alerts.service import AlertService
from src.core.database import get_session
from src.core.logging import get_logger
from src.core.security import get_current_user
from src.users.models import Users

logger = get_logger(__name__)

router = APIRouter(prefix="/alerts", tags=["alerts"])


def get_alert_service(session: AsyncSession = Depends(get_session)) -> AlertService:
    """Dependency for getting deal service instance."""
    repository = AlertRepository(session)
    return AlertService(repository)


@router.get("/", response_model=list[UserAlertResponse])
async def get_user_alerts(
    user: Users = Depends(get_current_user),
    service: AlertService = Depends(get_alert_service),
) -> list[UserAlertResponse]:
    """Get all alerts for current user"""
    logger.debug(f"Getting alerts for user {user.email}")
    try:
        alerts = await service.get_user_alerts(user)
        logger.debug(f"Got {len(alerts)} alerts for user {user.email}")
        return alerts
    except Exception as e:
        logger.error(f"Failed to get alerts for user {user.email}: {e}")
        raise


@router.post("/", response_model=UserAlertResponse)
async def create_alert(
    query_params: Annotated[QueryParams, Query()],
    user: Users = Depends(get_current_user),
    service: AlertService = Depends(get_alert_service),
) -> UserAlert:
    """Create user alert"""
    logger.debug(f"Creating alert for user {user}")
    try:
        alert = await service.create_alert(user, query_params.kw, query_params.f)
        logger.debug(f"Succesfully created alert for user {user}")
        return alert
    except Exception as e:
        logger.error(f"Failed to create alert for user {user}: {e}")
        raise


@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    user: Users = Depends(get_current_user),
    service: AlertService = Depends(get_alert_service),
) -> None:
    """Delete alert by id"""
    logger.debug(f"Deleting alert {alert_id}")
    try:
        await service.delete_alert(alert_id)
        logger.debug(f"Deleted alert {alert_id}")
    except Exception as e:
        logger.error(f"Failed to delete alert {alert_id}: {e}")
        raise
