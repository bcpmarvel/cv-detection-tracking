from fastapi import Request

from src.detection.service import DetectionService


def get_detection_service(request: Request) -> DetectionService:
    return request.app.state.detection_service
