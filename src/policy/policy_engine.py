from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class ActionRequest:
    tool: str
    action: str
    target: str = ""
    requires_external_side_effect: bool = False
    risk_level: str = "low"


class PolicyEngine:
    """Defensive policy engine with approval adapter semantics."""

    def __init__(self) -> None:
        self.allow_tools = {"read", "memory_search", "memory_get", "session_status"}
        self.high_risk_tools = {"exec", "message", "browser", "write", "edit"}

    def evaluate(self, req: ActionRequest) -> Tuple[str, Dict[str, str]]:
        if req.tool in self.allow_tools and req.risk_level in {"low", "medium"}:
            return "allow", {"reason": "tool in allow-list and acceptable risk"}

        if req.risk_level in {"high", "critical"}:
            return "require_approval", {"reason": f"risk level is {req.risk_level}"}

        if req.tool in self.high_risk_tools:
            if req.requires_external_side_effect:
                return "require_approval", {"reason": "external side effect"}
            return "require_approval", {"reason": "high-risk tool"}

        return "deny", {"reason": "tool not recognized / deny-by-default"}
