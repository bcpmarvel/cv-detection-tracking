from ultralytics.trackers.bot_sort import BOTSORT
import numpy as np


class Tracker:
    def __init__(
        self,
        max_age: int = 30,
        min_hits: int = 3,
        iou_threshold: float = 0.3,
    ):
        self.tracker = BOTSORT(
            track_high_thresh=0.5,
            track_low_thresh=0.1,
            new_track_thresh=0.6,
            track_buffer=max_age,
            match_thresh=iou_threshold,
            fuse_score=True,
        )
        self.frame_id = 0

    def update(self, detections, img_shape):
        if detections is None or len(detections) == 0:
            self.frame_id += 1
            return np.empty((0, 5))

        self.frame_id += 1
        tracks = self.tracker.update(detections, img_shape)
        return tracks

    def reset(self):
        self.tracker = BOTSORT(
            track_high_thresh=0.5,
            track_low_thresh=0.1,
            new_track_thresh=0.6,
            track_buffer=30,
            match_thresh=0.3,
            fuse_score=True,
        )
        self.frame_id = 0
