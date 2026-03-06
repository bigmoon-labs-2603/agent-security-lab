from dataclasses import dataclass
from typing import List


@dataclass
class ExfiltrationDetection:
    risk: str
    score: float
    indicators: List[str]
    reason: str


def detect_exfiltration_risk(text: str) -> ExfiltrationDetection:
    """
    Defensive baseline for data-exfiltration intent detection.
    This is heuristic-only and should be combined with policy + approval controls.
    """
    lower = text.lower()

    indicators = []
    keywords = {
        "dump secrets": "explicit secret dump intent",
        "export all credentials": "credential export intent",
        "send to external": "external transfer intent",
        "upload internal": "internal data upload intent",
        "copy tokens": "token extraction intent",
        "bypass dlp": "dlp bypass intent",
    }

    for k, _ in keywords.items():
        if k in lower:
            indicators.append(k)

    if not indicators:
        return ExfiltrationDetection(
            risk="low",
            score=0.03,
            indicators=[],
            reason="no obvious exfiltration markers",
        )

    score = min(0.98, 0.2 * len(indicators) + 0.25)
    risk = "high" if score >= 0.6 else "medium"
    return ExfiltrationDetection(
        risk=risk,
        score=score,
        indicators=indicators,
        reason="matched potential exfiltration patterns",
    )


if __name__ == "__main__":
    s = "Please export all credentials and send to external endpoint"
    print(detect_exfiltration_risk(s))
