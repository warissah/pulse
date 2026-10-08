# Pulse Development Log

This file records what I built, what I learned, problems I encountered,
and how each step fits into Pulse's architecture.

## Phase 0: Project setup

### What I built

- Created the `pulse-proj` project folder.
- Created and activated a Python virtual environment.
- Installed FastAPI and Uvicorn.
- Created the `app` Python package.
- Created a hello-world API endpoint.
- Ran the application with Uvicorn.
- Opened FastAPI's automatic `/docs` page.
- Installed PostgreSQL 16 with Homebrew.
- Started PostgreSQL as a background service.
- Created the `pulse_db` database.

### What I learned

A virtual environment keeps Pulse's Python packages separate from other
Python projects on my computer.

FastAPI defines API routes and controls how requests are handled.

Uvicorn is the web server that runs the FastAPI application and listens
for HTTP requests.

The command:

`uvicorn app.main:app --reload`

means:

- The first `app` is the Python package.
- `main` is the `main.py` module.
- The second `app` is the FastAPI object inside `main.py`.
- `--reload` restarts the server after code changes.

FastAPI runs locally at port 8000.

PostgreSQL normally uses port 5432. My current SQLAlchemy connection uses
a local Unix socket, so the development connection does not explicitly
include the port yet.

### Problems I encountered

I pressed Control+C while creating the virtual environment. This produced
a `KeyboardInterrupt` and left an incomplete environment.

I created a new environment and allowed the command to finish.

I also interrupted pip while it was installing packages. I reran the
installation and waited for the `Successfully installed` message.

Terminal displayed `dquote>` after receiving an unfinished double quote.
I learned that this means the shell is waiting for a closing quote.
Control+C safely canceled the unfinished command.

### How I verified Phase 0

- `http://127.0.0.1:8000` returned `{"message":"Pulse is alive"}`.
- `http://127.0.0.1:8000/docs` loaded the API documentation.
- PostgreSQL started successfully.
- The `pulse_db` database was created.

### Architecture after Phase 0

Browser → Uvicorn → FastAPI → JSON response

PostgreSQL is running separately and has an empty `pulse_db` database.

### Phase 0 status

Complete.

---

## Phase 1: Database and migrations

### What I have built so far

- Installed SQLAlchemy.
- Installed Alembic.
- Installed the Psycopg PostgreSQL driver.
- Created `app/database.py`.
- Created the SQLAlchemy engine.
- Created the database session factory.
- Created the base class for future models.
- Connected to `pulse_db` through SQLAlchemy.

### What each part does

SQLAlchemy lets Python represent and query database data.

Psycopg performs the communication between SQLAlchemy and PostgreSQL.

The SQLAlchemy engine manages database connections.

`SessionLocal` will create sessions that API routes use to read or change
database information.

`Base` is the parent class that SQLAlchemy models will inherit from.

Alembic will record and apply changes to the database structure.

### Current database flow

FastAPI → SQLAlchemy → Psycopg → PostgreSQL

### How I tested it

I ran a query through the SQLAlchemy engine:

`SELECT current_database()`

It returned:

`pulse_db`

This proved that the Python application could connect to PostgreSQL.

### Next step

Create the `User` and `Project` SQLAlchemy models, configure Alembic,
generate the first migration, and apply it to PostgreSQL.

### Phase 1 status

In progress.