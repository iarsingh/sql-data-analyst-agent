# Sql Data Analyst Agent: interview questions and answers

Answers describe this repository's current implementation. Suggested production changes are explicitly labeled as future work.

## 1. Does this agent connect to SQL?

No. It aggregates the rows supplied in the JSON payload. The `profile_table` and `aggregate` tool names are constant labels, not SQL execution calls or a real tool orchestration trace.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 2. How are regional totals computed?

For each row, the code uses `row.get("region", "unknown")` as the key and adds `float(row.get("revenue", 0))`. Two rows for the same region are summed in a Python dictionary.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 3. What is a concrete request and result?

For goal `revenue by region` and rows `[{"region":"north","revenue":10},{"region":"north","revenue":20}]`, the totals contain `north: 30.0`; the response says `wrote: false` and `applied: false`.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 4. Which goals are refused?

Goals containing `delete`, `drop`, `update`, or `insert` return a refusal response. The matching is case-insensitive substring matching, not a SQL parser or execution permission system.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 5. What happens when rows are absent?

The code uses an empty list and returns empty totals. Missing revenue defaults to zero and a missing region defaults to `unknown`; explicit null or malformed rows have different behavior.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 6. Are invalid rows converted into InputError?

Not consistently. Invalid numeric strings can raise `ValueError` from `float`, and non-mapping rows can raise attribute errors. The handler catches only `InputError`, so these cases can surface as server errors.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 7. Is float appropriate for financial totals?

The prototype uses binary floating point. For precise monetary accounting, use integer minor units or a defined decimal representation and specify rounding behavior.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 8. What should production input validation add?

Validate payload shape, row types, required dimensions, finite numeric values, maximum row count, and permitted aggregation operations before running the calculation.

Source: [src/sqlagent/agent.py](src/sqlagent/agent.py).

## 9. How are the domain API and ops plane connected?

The app registers the ops router under `/v1`, alongside the domain endpoint. Creating or approving a job updates ops records; it does not call the domain function. There is no background worker or job executor.

Source: [src/sqlagent/main.py](src/sqlagent/main.py).

## 10. Does X-Tenant-Id authenticate a user?

No. It is a caller-supplied header defaulting to `default`. Workspace and job reads filter by that value, but a caller can choose another value. Real identity and authorization would need to precede this lab tenant selector.

Source: [src/sqlagent/ops.py](src/sqlagent/ops.py).

## 11. What survives a process restart?

Nothing in the ops dictionaries or audit list is persisted. Multiple server workers would also have separate state. Durable storage, transactions, and a shared job queue are future changes.

Source: [src/sqlagent/ops.py](src/sqlagent/ops.py).

## 12. What happens when a production job is approved?

Targets exactly equal to `prod` or `production` create a `pending_approval` job and approval returns HTTP 403. Other target strings are queued. Approval of a lab job changes its status only; it does not execute a workload.

Source: [src/sqlagent/ops.py](src/sqlagent/ops.py).

## 13. Are audit and metrics equally tenant-scoped?

Audit results filter events by the tenant and its workspace/job identifiers. `/v1/metrics` returns process-wide counters without tenant filtering, so it is not a tenant-specific dashboard. Domain requests are not automatically audited.

Source: [src/sqlagent/ops.py](src/sqlagent/ops.py).

## 14. What would you prioritize before a customer deployment?

Define authenticated identities and permission checks, durable state, typed domain inputs, bounded requests, concurrency behavior, and observable execution semantics. Use the existing tests as a baseline, then test failure and access boundaries rather than claiming the lab is production-ready.

Source: [src/sqlagent/ops.py](src/sqlagent/ops.py).
