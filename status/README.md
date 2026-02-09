# Agent Status Directory

This directory contains the runtime status files for all active agents.
Do not edit these files manually unless you are simulating an agent or correcting a stalled state.

## Format
Filename: `<role_id>_<role_name>.md`

```markdown
# Agent Status
Role: [Role Name]
Status: [BOOTING | READY | BUSY | ERROR]
Current_Task: [Short description]
Last_Update: [Timestamp/Step]
```
