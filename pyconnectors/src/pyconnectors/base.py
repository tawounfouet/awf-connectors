import time
from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from pyconnectors.config import ConnectorConfig
from pyconnectors.result import ConnectorResult


class BaseConnector(ABC):
    """Abstract base class for all connectors."""

    def __init__(self, config: ConnectorConfig) -> None:
        self.config = config
        self._hooks: Dict[str, List[Callable[..., Any]]] = {
            "pre_execute": [],
            "post_execute": [],
            "on_error": [],
        }

    def add_hook(self, event: str, hook: Callable[..., Any]) -> None:
        """Register a hook to execute on specific events."""
        if event not in self._hooks:
            raise ValueError(f"Invalid hook event: {event}")
        self._hooks[event].append(hook)

    def _trigger_hooks(self, event: str, *args: Any, **kwargs: Any) -> None:
        """Trigger registered hooks for the specified event."""
        for hook in self._hooks[event]:
            try:
                hook(*args, **kwargs)
            except Exception:
                # Catch hook errors so they don't break the main execution loop
                # This could log them later
                pass

    @abstractmethod
    def execute(self, *args: Any, **kwargs: Any) -> Any:
        """Core connector logic to be implemented by child classes."""
        pass

    def safe_execute(self, *args: Any, **kwargs: Any) -> ConnectorResult:
        """
        Execute the connector safely by capturing timing, exceptions,
        and creating the standard ConnectorResult. Also triggers hooks.
        """
        start_time = time.perf_counter()

        self._trigger_hooks("pre_execute", self, *args, **kwargs)

        try:
            result_data = self.execute(*args, **kwargs)
            duration = time.perf_counter() - start_time
            result = ConnectorResult(success=True, data=result_data, duration=duration)

            self._trigger_hooks("post_execute", self, result, *args, **kwargs)

            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            result = ConnectorResult(
                success=False,
                error=str(e),
                duration=duration,
                metadata={"exception_type": type(e).__name__},
            )

            self._trigger_hooks("on_error", self, result, *args, **kwargs)

            return result
