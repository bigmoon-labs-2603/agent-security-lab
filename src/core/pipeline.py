from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, List

from src.core.models import AnalysisResult, DetectorSignal, PolicyDecision, now_iso
from src.detectors.base import Detector
from src.policy.policy_engine import ActionRequest, PolicyEngine
from src.scoring.risk_score import Signal, aggregate_risk


class AnalysisPipeline:
    def __init__(self, detectors: Iterable[Detector], policy_engine: PolicyEngine | None = None) -> None:
        self.detectors: List[Detector] = list(detectors)
        self.policy_engine = policy_engine or PolicyEngine()

    def analyze_text(self, text: str, tool: str = "read", action: str = "analyze") -> AnalysisResult:
        detector_signals: List[DetectorSignal] = []
        score_signals: List[Signal] = []

        for detector in self.detectors:
            out = detector.detect(text)
            detector_signals.append(out)
            score_signals.append(Signal(out.name, out.score, detector.weight))

        overall = aggregate_risk(score_signals)
        req = ActionRequest(
            tool=tool,
            action=action,
            requires_external_side_effect=tool in {"message", "exec", "browser", "write", "edit"},
            risk_level=str(overall["level"]),
        )
        decision, meta = self.policy_engine.evaluate(req)

        return AnalysisResult(
            text=text,
            created_at=now_iso(),
            overall=overall,
            signals=detector_signals,
            policy=PolicyDecision(decision=decision, reason=meta.get("reason", "n/a")),
        )

    @staticmethod
    def to_dict(result: AnalysisResult) -> dict:
        d = asdict(result)
        return d
