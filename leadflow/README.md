# LeadFlow — agency lead automation & CRM demo

Self-built portfolio demonstration for agency overflow engineering. No client project or experience claim is implied.

## Run
Requires Python 3.10+; no third-party dependencies.

```sh
python3 server.py
```
Open http://127.0.0.1:8000 and enter the access token printed in the terminal. The server binds to localhost only. Use synthetic data for demonstration.

## Features
- Responsive dashboard, lead capture, search and JSON export
- SQLite records that survive server restarts
- Case-insensitive email deduplication
- Transparent deterministic lead scoring (not an AI model)
- Pipeline stages, follow-up dates and audit activity
- Authenticated JSON endpoints and input validation

## Demo walkthrough
1. Add a synthetic contact with a $1,500 automation/integration/dashboard brief.
2. See the score of 100; add a second low-budget lead to compare.
3. Change stage to Contacted, choose a follow-up date and inspect the activity.
4. Retry the same email: a duplicate is rejected.
5. Mark a lead Won and export the pipeline.

## Configuration
`LEADFLOW_DB` sets the SQLite path. `LEADFLOW_TOKEN` sets a stable token; otherwise a new token is generated each startup. Never commit tokens or the database.

## HTTP integration
Use `Authorization: Bearer <token>` for GET `/api/leads`, GET `/api/events`, POST `/api/leads`, and POST `/api/update`. Capture payload: `name`, `email`, `company`, `budget` (USD integer), `message`. Update payload: `id`, `stage`, `followup` (YYYY-MM-DD or empty).

## Scope and handover
This is a single-operator local prototype. It does not send emails, call AI, integrate a live CRM, or expose a public webhook. Follow-ups are stored dates, not a scheduled notification service. Before public deployment add TLS, proper multi-user authentication, rate limiting, backup/retention policies, notification worker and integration-specific retries. Do not expose this development HTTP server publicly.

All source files are included for review and handover. Commercial NDA/IP terms must be agreed separately; this demo is not a contract.

## Verification
`python3 -m unittest discover -s tests -v`
