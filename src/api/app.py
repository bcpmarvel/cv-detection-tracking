from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import settings
from src.detection.models import YOLODetector
from src.detection.service import DetectionService
from src.api.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Loading YOLO model...")
    detector = YOLODetector(settings.model_path, settings.device)

    app.state.detector = detector
    app.state.detection_service = DetectionService(
        detector=detector,
        enable_tracking=False,
    )
    app.state.device = settings.device

    print(f"Model loaded on device: {settings.device}")

    yield

    print("Shutting down...")


def create_app() -> FastAPI:
    app = FastAPI(
        title="CV Detection API",
        description="Object detection and tracking API",
        version="1.0.0",
        lifespan=lifespan,
    )

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
