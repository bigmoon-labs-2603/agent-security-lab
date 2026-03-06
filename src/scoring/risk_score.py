from dataclasses import dataclass
from typing import Dict, Iterable


@dataclass
class Signal:
    name: str
    score: float
    weight: float


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def aggregate_risk(signals: Iterable[Signal]) -> Dict[str, float | str]:
    sigs = list(signals)
    if not sigs:
        return {"score": 0.0, "level": "low", "confidence": 0.0}

    total_w = sum(max(0.0, s.weight) for s in sigs)
    if total_w <= 1e-9:
        return {"score": 0.0, "level": "low", "confidence": 0.0}

    weighted = sum(clamp(s.score) * max(0.0, s.weight) for s in sigs)
    score = clamp(weighted / total_w)
    confidence = clamp(min(1.0, total_w / 1.8))

    # Baseline thresholding
    if score >= 0.85:
        level = "critical"
    elif score >= 0.65:
        level = "high"
    elif score >= 0.35:
        level = "medium"
    else:
        level = "low"

    # Escalation rule: if multiple detectors are non-trivial, avoid under-classifying.
    medium_or_higher = sum(1 for s in sigs if clamp(s.score) >= 0.40)
    high_or_higher = sum(1 for s in sigs if clamp(s.score) >= 0.65)
    if level == "low" and medium_or_higher >= 2:
        level = "medium"
    if level in {"low", "medium"} and high_or_higher >= 2:
        level = "high"

    return {"score": round(score, 4), "level": level, "confidence": round(confidence, 4)}
