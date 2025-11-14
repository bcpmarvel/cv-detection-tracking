import cv2
import numpy as np


def draw_tracks(frame, tracks, fps: float | None = None):
    annotated_frame = frame.copy()

    for track in tracks:
        if len(track) < 6:
            continue

        x1, y1, x2, y2, track_id, conf = track[:6]
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        track_id = int(track_id)

        color = get_track_color(track_id)

        cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)

        label = f"ID:{track_id} {conf:.2f}"
        label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        cv2.rectangle(
            annotated_frame,
            (x1, y1 - label_size[1] - 10),
            (x1 + label_size[0], y1),
            color,
            -1,
        )
        cv2.putText(
            annotated_frame,
            label,
            (x1, y1 - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2,
        )

    if fps is not None:
        cv2.putText(
            annotated_frame,
            f"FPS: {fps:.1f}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2,
        )

    return annotated_frame


def get_track_color(track_id: int) -> tuple[int, int, int]:
    colors = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (255, 255, 0),
        (255, 0, 255),
        (0, 255, 255),
        (128, 0, 0),
        (0, 128, 0),
        (0, 0, 128),
        (128, 128, 0),
    ]
    return colors[track_id % len(colors)]
