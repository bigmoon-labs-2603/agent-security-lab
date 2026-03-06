from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Any, Dict, List


@dataclass
class DetectorSignal:
    name: str
    risk: str
    score: float
    reason: str
    indicators: List[str] = field(default_factory=list)


@dataclass
class PolicyDecision:
    decision: str
    reason: str


@dataclass
class AnalysisResult:
    text: str
    created_at: str
    overall: Dict[str, Any]
    signals: List[DetectorSignal]
    policy: PolicyDecision


def now_iso() -> str:
    return datetime.now(UTC).isoformat()
