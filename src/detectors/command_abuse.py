from src.core.models import DetectorSignal


class CommandAbuseDetector:
    name = "command_abuse"

    def __init__(self, weight: float = 0.9) -> None:
        self.weight = weight
        self._patterns = [
            "rm -rf /",
            "del /f /s /q",
            "format c:",
            "powershell -enc",
            "nc -e",
            "chmod 777",
            "reg add",
            "schtasks /create",
        ]

    def detect(self, text: str) -> DetectorSignal:
        lower = text.lower()
        hits = [p for p in self._patterns if p in lower]
        if not hits:
            return DetectorSignal(self.name, "low", 0.04, "no high-risk command markers", [])

        score = min(0.97, 0.18 * len(hits) + 0.22)
        risk = "high" if score >= 0.6 else "medium"
        return DetectorSignal(self.name, risk, score, "matched risky command patterns", hits)
