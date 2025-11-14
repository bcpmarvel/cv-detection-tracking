import numpy as np
from src.tracking.models import Tracker
from src.config import settings


class TrackingService:
    def __init__(
        self,
        max_age: int | None = None,
        min_hits: int | None = None,
        iou_threshold: float | None = None,
    ):
        self.tracker = Tracker(
            max_age=max_age or settings.tracker_max_age,
            min_hits=min_hits or settings.tracker_min_hits,
            iou_threshold=iou_threshold or settings.tracker_iou_threshold,
        )

    def update(self, results):
        if results.boxes is None or len(results.boxes) == 0:
            return np.empty((0, 6))

        detections = results.boxes.data.cpu().numpy()
        img_shape = results.orig_shape

        tracks = self.tracker.update(detections, img_shape)

        return tracks

    def reset(self):
        self.tracker.reset()
