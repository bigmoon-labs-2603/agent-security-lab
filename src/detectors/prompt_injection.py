from src.core.models import DetectorSignal


class PromptInjectionDetector:
    name = "prompt_injection"

    def __init__(self, weight: float = 0.9) -> None:
        self.weight = weight
        self._patterns = [
            "ignore previous instructions",
            "reveal system prompt",
            "bypass safety",
            "disable guardrails",
            "act as unrestricted",
        ]

    def detect(self, text: str) -> DetectorSignal:
        lower = text.lower()
        hits = [p for p in self._patterns if p in lower]
        if not hits:
            return DetectorSignal(self.name, "low", 0.05, "no known prompt-injection markers", [])

        score = min(0.96, 0.24 * len(hits) + 0.2)
        risk = "high" if score >= 0.65 else "medium"
        return DetectorSignal(self.name, risk, score, "matched prompt-injection markers", hits)
