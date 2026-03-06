# OpenClaw Safe Workflow Checklist (Defensive)

## Before execution
- Confirm user intent and authorization scope.
- Identify whether action has external side effects.
- Check if sensitive data may be exposed.

## During execution
- Apply least privilege tool usage.
- Prefer read-only operations first.
- Require explicit approval for sending/deleting/publishing.

## After execution
- Record decisions and rationale in memory logs.
- Store reproducible evidence (commit id, run id, message id).
- Create follow-up hardening tasks for repeated failures.
