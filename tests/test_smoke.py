from src.app import healthcheck


def test_healthcheck():
    assert healthcheck() == "OK"
