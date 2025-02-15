from fastapi import FastAPI

from core.config import settings
from core.logging import get_logger, setup_logging
from src.deals.routes import router as deals_router
from src.users.routes import router as auth_router
from utils.migrations import run_migrations

# Set up logging configuration
setup_logging()

# Optional: Run migrations on startup
run_migrations()

# Set up logger for this module
logger = get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
)

# Include routers
app.include_router(auth_router)
app.include_router(deals_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint."""
    logger.debug("Root endpoint called")
    return {"message": "Welcome to Bar Down Deals API!"}
