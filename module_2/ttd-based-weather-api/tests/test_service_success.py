def test_get_forecast_success(service):
    forecast = service.get_forecast("Kigali")

    assert forecast.city == "Kigali"
    assert forecast.temperature_c == 26.0
