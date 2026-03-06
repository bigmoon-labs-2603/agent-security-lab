# Agent Security Lab

[中文说明 / Chinese README](./README.zh-CN.md)

> Frontier research + engineering project for securing tool-using AI agents.

## Vision

AI agents now touch shells, browsers, filesystems, and messaging channels. This project focuses on **practical, testable security controls** so agent systems can be deployed with confidence.

## What this project delivers

- **Threat modeling framework** for agent-native systems
- **Policy enforcement patterns** (least privilege, approval gates, deny-by-default)
- **Detector prototypes** for prompt injection and exfiltration hints
- **Evaluation harness design** for adversarial resilience testing
- **Defensive runbooks** for incident response and recovery

## Project status

- Phase: `v0.2 (research scaffold + defensive detector expansion)`
- Maturity: early-stage, defense-focused

## Repository layout

```text
agent-security-lab/
  docs/
    architecture.md
    threat-model.md
    controls.md
    evaluation.md
    quickstart.md
  src/
    policy/
      policy_engine.py
    detectors/
      prompt_injection.py
  examples/
    safe-workflows/
      openclaw-checklist.md
```

## Quick start

1. Read `docs/threat-model.md` to understand assets and trust boundaries.
2. Review `docs/controls.md` and adapt controls to your runtime.
3. Use `src/policy/policy_engine.py` as a baseline policy skeleton.
4. Extend `src/detectors/prompt_injection.py` with your own rules.

## Roadmap

### Phase 1 — Foundations
- [x] Security architecture draft
- [x] Threat taxonomy draft
- [x] Control checklist draft

### Phase 2 — Prototypes
- [x] Baseline policy engine skeleton
- [x] Prompt-injection detector skeleton
- [x] Exfiltration detector (baseline)
- [ ] High-risk action approval adapter

### Phase 3 — Evaluation
- [ ] Adversarial test corpus
- [ ] Scorecard (block rate / false positives / latency)
- [ ] CI security regression suite

## Security & ethics

- This repository is for **defensive security research**.
- No unauthorized exploitation guidance.
- Any red-team style scenario must be executed in authorized test environments.

## License

MIT

