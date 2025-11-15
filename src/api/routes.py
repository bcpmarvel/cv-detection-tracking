import time
from fastapi import APIRouter, UploadFile, File, Depends, Request

from src.api.schemas import DetectionResponse, HealthResponse
from src.api.dependencies import get_detection_service
from src.api.utils import decode_image, results_to_detections
from src.detection.service import DetectionService

router = APIRouter(prefix="/api")


@router.post("/detect", response_model=DetectionResponse)
async def detect(
    file: UploadFile = File(..., description="Image file to process"),
    service: DetectionService = Depends(get_detection_service),
) -> DetectionResponse:
    start_time = time.time()

    image = await decode_image(file)
    height, width = image.shape[:2]

    results = service.process(image)

    detections = results_to_detections(results)

    processing_time = (time.time() - start_time) * 1000

    return DetectionResponse(
        detections=detections,
        image_width=width,
        image_height=height,
        processing_time_ms=processing_time,
    )


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    return HealthResponse(
        status="healthy",
        model_loaded=hasattr(request.app.state, "detection_service"),
        device=request.app.state.device,
    )
