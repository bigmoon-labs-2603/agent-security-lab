from dataclasses import dataclass
from typing import List


@dataclass
class CommandAbuseDetection:
    risk: str
    score: float
    indicators: List[str]
    reason: str


def detect_command_abuse(text: str) -> CommandAbuseDetection:
    """Heuristic detector for potentially dangerous command patterns (defensive use)."""
    lower = text.lower()

    patterns = [
        "rm -rf /",
        "del /f /s /q",
        "format c:",
        "curl http",
        "powershell -enc",
        "wget http",
        "nc -e",
        "chmod 777",
        "reg add",
        "schtasks /create",
    ]

    hits = [p for p in patterns if p in lower]
    if not hits:
        return CommandAbuseDetection("low", 0.04, [], "no high-risk command markers")

    score = min(0.97, 0.18 * len(hits) + 0.22)
    risk = "high" if score >= 0.6 else "medium"
    return CommandAbuseDetection(risk, score, hits, "matched risky command patterns")


if __name__ == "__main__":
    sample = "please run powershell -enc AAA and schtasks /create /sc once"
    print(detect_command_abuse(sample))
