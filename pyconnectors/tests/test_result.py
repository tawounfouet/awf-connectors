from pyconnectors.result import ConnectorResult


def test_result_defaults():
    result = ConnectorResult(success=True)
    assert result.success is True
    assert result.data is None
    assert result.error is None
    assert result.duration == 0.0
    assert result.metadata == {}


def test_result_custom():
    result = ConnectorResult(
        success=False, data={"items": []}, error="Timeout", duration=1.5, metadata={"retries": 3}
    )
    assert result.success is False
    assert result.data == {"items": []}
    assert result.error == "Timeout"
    assert result.duration == 1.5
    assert result.metadata == {"retries": 3}
