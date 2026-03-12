from edge_traffic.config import get_settings


def test_settings_defaults() -> None:
    settings = get_settings()
    assert settings.app_name == "edge-traffic"
    assert settings.environment in {"dev", "prod", "pi"}
