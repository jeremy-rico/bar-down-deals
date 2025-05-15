import tracemalloc
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.alerts.routes import router as alerts_router
from src.core.config import settings
from src.core.database import engine
from src.core.logging import get_logger, setup_logging
from src.core.utils import populate_tags, run_migrations
from src.deals.routes import router as deals_router
from src.products.routes import router as products_router
from src.search.routes import router as search_router
from src.users.routes import router as auth_router

tracemalloc.start()

# Set up logging configuration
setup_logging()

# Set up logger for this module
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting server...")
    # Better off running these manually only when needed.
    # run_migrations()
    # await populate_tags(TAGS)
    yield
    logger.info("Shutting down...")
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "x-total-page-count",
        "x-items-per-page",
        "x-total-item-count",
        "x-avail-sizes",
        "x-avail-brands",
        "x-avail-tags",
        "x-avail-stores",
        "x-max-price",
    ],
)

# Include routers
app.include_router(deals_router)
app.include_router(products_router)
app.include_router(search_router)
app.include_router(auth_router)
app.include_router(alerts_router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}


@app.get("/")
async def root():
    """Root endpoint."""
    logger.debug("Root endpoint called")
    return {"message": "Welcome to Bar Down Deals API!"}


@app.get("/debug/mem")
async def memory_snapshot():
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")
    return {"top": [str(stat) for stat in top_stats[:5]]}
