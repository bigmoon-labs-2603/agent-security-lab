# Agent Security Lab（中文说明）

> 面向工具型 AI Agent 的前沿安全研究与工程化项目。

[English README](./README.md)

## 项目愿景

随着 AI Agent 可调用 Shell、浏览器、文件系统与消息通道，系统攻击面显著扩大。
本项目聚焦**可落地、可验证、可持续演进**的防御能力建设，帮助团队安全地部署 Agent。

## 核心能力

- Agent 原生系统威胁建模框架
- 策略执行机制（最小权限、审批闸门、默认拒绝）
- 提示注入与数据外泄检测原型
- 对抗评测方法与安全评分思路
- 防御与响应 runbook（操作清单）

## 当前版本

- 版本阶段：`v0.2`
- 成熟度：早期（以防御研究为主）

## 目录结构

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
      exfiltration.py
  examples/
    safe-workflows/
      openclaw-checklist.md
```

## 快速开始

1. 阅读 `docs/threat-model.md`，确认资产与信任边界。
2. 阅读 `docs/controls.md`，将控制策略映射到你的运行环境。
3. 使用 `src/policy/policy_engine.py` 作为基线策略引擎。
4. 结合 `src/detectors/*.py` 扩展检测规则与告警策略。

## 路线图

### Phase 1 — Foundations
- [x] 安全架构草案
- [x] 威胁分类草案
- [x] 控制项清单草案

### Phase 2 — Prototypes
- [x] 基线策略引擎
- [x] 提示注入检测器
- [x] 外泄风险检测器（基础版）
- [ ] 高风险动作审批适配器

### Phase 3 — Evaluation
- [ ] 对抗测试语料集
- [ ] 安全评分卡（拦截率 / 误报率 / 时延）
- [ ] CI 安全回归测试

## 安全与伦理

- 本仓库仅用于**防御性安全研究**。
- 不提供未授权攻击指导。
- 红队测试需在合法授权环境中进行。

## 许可证

MIT
