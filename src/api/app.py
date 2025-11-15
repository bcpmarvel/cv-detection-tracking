from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.detection.models import YOLODetector
from src.detection.service import DetectionService
from src.api.routes import router
from src.api.middleware import RequestLoggingMiddleware
from src.logging import configure_logging, get_logger

configure_logging()
log = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("loading_model", model_path=str(settings.model_path), device=settings.device)
    detector = YOLODetector(settings.model_path, settings.device)

    app.state.detector = detector
    app.state.detection_service = DetectionService(
        detector=detector,
        enable_tracking=False,
    )
    app.state.device = settings.device

    log.info("model_loaded", device=settings.device)

    yield

    log.info("shutting_down")


def create_app() -> FastAPI:
    app = FastAPI(
        title="CV Detection API",
        description="Object detection and tracking API",
        version="1.0.0",
        lifespan=lifespan,
    )

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.api_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    return app


app = create_app()
