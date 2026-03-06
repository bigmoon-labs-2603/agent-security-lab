from src.core.models import DetectorSignal


class ExfiltrationDetector:
    name = "exfiltration"

    def __init__(self, weight: float = 1.0) -> None:
        self.weight = weight
        self._patterns = [
            "export all credentials",
            "dump secrets",
            "send to external",
            "upload internal",
            "copy tokens",
            "bypass dlp",
        ]

    def detect(self, text: str) -> DetectorSignal:
        lower = text.lower()
        hits = [p for p in self._patterns if p in lower]
        if not hits:
            return DetectorSignal(self.name, "low", 0.03, "no obvious exfiltration markers", [])

        score = min(0.98, 0.2 * len(hits) + 0.25)
        risk = "high" if score >= 0.6 else "medium"
        return DetectorSignal(self.name, risk, score, "matched potential exfiltration patterns", hits)
