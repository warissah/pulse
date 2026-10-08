# Pulse

Pulse is a backend platform that helps junior and solo developers
understand their applications.

Applications send Pulse events such as requests, errors, and deployments.
Pulse uses those events to provide health monitoring and build a readable
project timeline.

The timeline is the main product. Monitoring provides the evidence used
to explain what happened and when.

## Current status

Phase 0 is complete.

Phase 1 is in progress: PostgreSQL and SQLAlchemy are connected. The next
step is creating the User and Project models and the first Alembic
migration.

## Technology

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Redis
- RQ

Redis and RQ will be introduced in a later phase.

## Run locally

Activate the virtual environment:

`source venv/bin/activate`

Start PostgreSQL:

`brew services start postgresql@16`

Start FastAPI:

`uvicorn app.main:app --reload`

Open:

`http://127.0.0.1:8000/docs`