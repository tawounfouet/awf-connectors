from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ConnectorResult:
    """Standardized result structure for connector execution."""

    success: bool
    data: Any = None
    error: Optional[str] = None
    duration: float = 0.0
    metadata: Dict[str, Any] = field(default_factory=dict)
