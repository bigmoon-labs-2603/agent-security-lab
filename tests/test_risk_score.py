from src.scoring.risk_score import Signal, aggregate_risk


def test_empty_signals():
    out = aggregate_risk([])
    assert out["score"] == 0.0
    assert out["level"] == "low"
    assert out["confidence"] == 0.0


def test_high_risk_path():
    out = aggregate_risk([
        Signal("prompt_injection", 0.9, 1.0),
        Signal("exfiltration", 0.8, 1.0),
    ])
    assert out["level"] in {"high", "critical"}
    assert out["score"] >= 0.8


def test_low_risk_path():
    out = aggregate_risk([
        Signal("prompt_injection", 0.1, 0.5),
        Signal("exfiltration", 0.2, 0.5),
    ])
    assert out["level"] == "low"
    assert out["score"] < 0.35
