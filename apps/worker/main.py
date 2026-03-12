from edge_traffic.config import get_settings


def main() -> None:
    settings = get_settings()
    print(f"worker started: app={settings.app_name} env={settings.environment}")


if __name__ == "__main__":
    main()
