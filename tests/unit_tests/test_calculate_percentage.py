from app.services.check import CheckService


def test_calculate_percentage(mocker):
    mock_repo = mocker.patch("app.repositories.check.CheckRepository")
    mock_monitor_repo = mocker.patch("app.repositories.monitor.MonitorRepository")

    service = CheckService(mock_repo, mock_monitor_repo)
    result_success = service.calculate_percentage(100, 50)
    result_division_by_zero = service.calculate_percentage(0, 50)
    result_full = service.calculate_percentage(100, 100)

    assert result_success == 50.0
    assert result_division_by_zero == 0.0
    assert result_full == 100.0