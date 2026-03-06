# Quickstart

## 1) Define trust boundaries

Separate:
- Agent reasoning plane
- Tool execution plane
- Secrets/config plane
- External channel plane

## 2) Turn on policy checks

Use `src/policy/policy_engine.py` as a reference to enforce:
- deny-by-default for dangerous tools
- explicit allow lists
- human approval for external side effects

## 3) Add runtime detectors

Start with `src/detectors/prompt_injection.py`, then add:
- exfiltration pattern detector
- command abuse detector
- suspicious workflow chaining detector

## 4) Observe + iterate

Track:
- blocked action count
- false positive/negative rate
- mean response latency under policy enforcement
