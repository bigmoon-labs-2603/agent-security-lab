from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass
class ActionRequest:
    tool: str
    action: str
    target: str = ""
    requires_external_side_effect: bool = False


class PolicyEngine:
    """Baseline defensive policy engine (reference implementation)."""

    def __init__(self) -> None:
        self.allow_tools = {"read", "memory_search", "memory_get", "session_status"}
        self.high_risk_tools = {"exec", "message", "browser", "write", "edit"}

    def evaluate(self, req: ActionRequest) -> Tuple[str, Dict[str, str]]:
        """
        Returns: (decision, metadata)
        decision in {allow, deny, require_approval}
        """
        if req.tool in self.allow_tools:
            return "allow", {"reason": "tool in allow-list"}

        if req.tool in self.high_risk_tools:
            if req.requires_external_side_effect:
                return "require_approval", {"reason": "external side effect"}
            return "require_approval", {"reason": "high-risk tool"}

        return "deny", {"reason": "tool not recognized / deny-by-default"}


if __name__ == "__main__":
    engine = PolicyEngine()
    sample = ActionRequest(tool="message", action="send", requires_external_side_effect=True)
    decision, meta = engine.evaluate(sample)
    print({"decision": decision, **meta})
