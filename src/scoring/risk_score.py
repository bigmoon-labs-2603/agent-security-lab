from dataclasses import dataclass
from typing import Iterable, Dict


@dataclass
class Signal:
    name: str
    score: float  # 0~1
    weight: float # 0~1


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def aggregate_risk(signals: Iterable[Signal]) -> Dict[str, float | str]:
    """
    Weighted risk aggregation for defensive routing.

    Returns:
      {
        "score": float,      # 0~1
        "level": str,        # low/medium/high/critical
        "confidence": float  # 0~1, based on total effective weights
      }
    """
    sigs = list(signals)
    if not sigs:
        return {"score": 0.0, "level": "low", "confidence": 0.0}

    total_w = sum(max(0.0, s.weight) for s in sigs)
    if total_w <= 1e-9:
        return {"score": 0.0, "level": "low", "confidence": 0.0}

    weighted = sum(clamp(s.score) * max(0.0, s.weight) for s in sigs)
    score = clamp(weighted / total_w)
    confidence = clamp(min(1.0, total_w / 1.8))

    if score >= 0.85:
        level = "critical"
    elif score >= 0.65:
        level = "high"
    elif score >= 0.35:
        level = "medium"
    else:
        level = "low"

    return {
        "score": round(score, 4),
        "level": level,
        "confidence": round(confidence, 4),
    }


if __name__ == "__main__":
    demo = [
        Signal("prompt_injection", 0.81, 0.8),
        Signal("exfiltration", 0.72, 0.9),
        Signal("command_abuse", 0.25, 0.4),
    ]
    print(aggregate_risk(demo))
