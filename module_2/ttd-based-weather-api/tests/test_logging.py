def test_logging_on_success(service, caplog):
    service.get_forecast("Kigali")

    assert "Received forecast request" in caplog.text
    assert "Returning forecast" in caplog.text
