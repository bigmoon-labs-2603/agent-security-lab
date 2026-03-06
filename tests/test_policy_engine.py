from src.policy.policy_engine import PolicyEngine, ActionRequest


def test_allow_read_low_risk():
    engine = PolicyEngine()
    d, _ = engine.evaluate(ActionRequest(tool="read", action="open", risk_level="low"))
    assert d == "allow"


def test_require_approval_high_risk_level():
    engine = PolicyEngine()
    d, meta = engine.evaluate(ActionRequest(tool="read", action="open", risk_level="high"))
    assert d == "require_approval"
    assert "risk level" in meta["reason"]


def test_require_approval_external_effect():
    engine = PolicyEngine()
    d, _ = engine.evaluate(
        ActionRequest(
            tool="message",
            action="send",
            requires_external_side_effect=True,
            risk_level="medium",
        )
    )
    assert d == "require_approval"


def test_deny_unknown_tool():
    engine = PolicyEngine()
    d, _ = engine.evaluate(ActionRequest(tool="unknown_tool", action="x", risk_level="low"))
    assert d == "deny"
