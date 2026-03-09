import pytest
from pyconnectors.base import BaseConnector
from pyconnectors.config import ConnectorConfig
from pyconnectors.result import ConnectorResult


class DummyConnector(BaseConnector):
    def execute(self, should_fail: bool = False) -> str:
        if should_fail:
            raise ValueError("Intentional failure")
        return "success"


def test_safe_execute_success():
    conn = DummyConnector(ConnectorConfig())
    result = conn.safe_execute()

    assert isinstance(result, ConnectorResult)
    assert result.success is True
    assert result.data == "success"
    assert result.error is None
    assert result.duration > 0


def test_safe_execute_failure():
    conn = DummyConnector(ConnectorConfig())
    result = conn.safe_execute(should_fail=True)

    assert result.success is False
    assert result.data is None
    assert "Intentional failure" in result.error
    assert result.metadata["exception_type"] == "ValueError"


def test_hooks():
    hooks_called = []

    def pre_hook(connector, *args, **kwargs):
        hooks_called.append("pre")

    def post_hook(connector, result, *args, **kwargs):
        hooks_called.append("post")
        assert result.success is True

    def error_hook(connector, result, *args, **kwargs):
        hooks_called.append("error")
        assert result.success is False

    conn = DummyConnector(ConnectorConfig())
    conn.add_hook("pre_execute", pre_hook)
    conn.add_hook("post_execute", post_hook)
    conn.add_hook("on_error", error_hook)

    # Success case
    conn.safe_execute()
    assert hooks_called == ["pre", "post"]

    hooks_called.clear()

    # Error case
    conn.safe_execute(should_fail=True)
    assert hooks_called == ["pre", "error"]


def test_invalid_hook():
    conn = DummyConnector(ConnectorConfig())
    with pytest.raises(ValueError):
        conn.add_hook("invalid_event", lambda: None)
