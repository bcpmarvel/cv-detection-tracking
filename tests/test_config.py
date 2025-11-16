from sentinel.config import Settings


def test_settings_defaults():
    settings = Settings()
    assert settings.model_path.name == "yolov8n.pt"
    assert settings.conf_threshold == 0.5
    assert settings.iou_threshold == 0.45
