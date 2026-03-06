import argparse
from src.detectors.prompt_injection import detect_prompt_injection
from src.detectors.exfiltration import detect_exfiltration_risk
from src.detectors.command_abuse import detect_command_abuse
from src.scoring.risk_score import Signal, aggregate_risk


def main() -> None:
    parser = argparse.ArgumentParser(description="Agent Security Lab risk scorer CLI")
    parser.add_argument("text", help="Input text to evaluate")
    args = parser.parse_args()

    text = args.text
    inj = detect_prompt_injection(text)
    exf = detect_exfiltration_risk(text)
    cmd = detect_command_abuse(text)

    risk = aggregate_risk([
        Signal("prompt_injection", inj.score, 0.9),
        Signal("exfiltration", exf.score, 1.0),
        Signal("command_abuse", cmd.score, 0.9),
    ])

    print({
        "overall": risk,
        "signals": {
            "prompt_injection": {"risk": inj.risk, "score": inj.score, "reason": inj.reason},
            "exfiltration": {"risk": exf.risk, "score": exf.score, "reason": exf.reason},
            "command_abuse": {"risk": cmd.risk, "score": cmd.score, "reason": cmd.reason},
        },
    })


if __name__ == "__main__":
    main()
