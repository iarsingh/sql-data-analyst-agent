# Sql Data Analyst Agent: process flows

## Domain request

Endpoint: `POST /agent/run`. Input: goal + rows payload. The processing stages below summarize [agent.py](../src/sqlagent/agent.py); they are local function behavior, not externally executed tools.

```mermaid
flowchart TD
  A["POST /agent/run"] --> B{"Non-empty string goal?"}
  B -->|"No"| E["HTTP 422"]
  B -->|"Yes"| C{"Contains a blocked write token?"}
  C -->|"Yes"| R["Refused: no writes"]
  C -->|"No"| P["Read posted rows or empty list"]
  P --> F["Validate finite decimal revenue; group by region"]
  F --> O["Return exact totals, compatible numeric totals, and row counts"]
  F -->|"Malformed rows / conversion errors"| X["HTTP 422"]
```

Refusal responses, where implemented, are normal domain results rather than successful execution of a requested write. Detailed edge cases are covered in [INTERVIEW_QA.md](../INTERVIEW_QA.md).

## Workspace and job approval

```mermaid
flowchart TD
  C["Create tenant-scoped workspace"] --> J["Submit job: workspace + payload + target"]
  J --> V{"Workspace belongs to selected tenant?"}
  V -->|"No"| E["HTTP 404"]
  V -->|"Yes"| P{"Normalized target is prod or production?"}
  P -->|"Yes"| Q["pending_approval"]
  P -->|"No"| L["queued"]
  Q --> A["Approval request"]
  A --> X["HTTP 403: production apply disabled"]
  L --> B["Approval request"]
  B --> K["approved: status update only"]
  K --> S["No executor / no production apply"]
```

Approval first checks job ownership using the selected tenant. Status changes and audit records remain in memory. Repeated lab approval returns the original approval without duplicating its event or counter. Ops transitions are protected by an in-process lock. The domain request flow and this job-record flow are independent. Source: [ops.py](../src/sqlagent/ops.py).
