def test_logging_on_success(service, log) -> None:
    service.get_forecast("Kigali")

    assert "Received forecast request" in log.text
    assert "Returning forecast" in log.text
