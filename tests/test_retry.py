from src.retry import retry


def test_retry_returns_first_success():
    calls = {"count": 0}

    def operation():
        calls["count"] += 1
        return "ok" if calls["count"] == 2 else None

    assert retry(operation, attempts=3, delay_seconds=0) == "ok"
    assert calls["count"] == 2


def test_retry_returns_none_after_failures():
    assert retry(lambda: None, attempts=2, delay_seconds=0) is None
