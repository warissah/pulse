Pulse — Phase-by-Phase Roadmap
Your 4-week build plan, broken into phases you can follow in order. Each phase says what to build, what you'll learn, how to know you're done, and what you must be able to explain before moving on.
How to use this roadmap
• Work top to bottom. Don't start a phase until the previous one's "Done when" is true.
• "Working" is not "done." Done means it works and you can answer the explain-it questions in your own words.
• Write a few simple tests as you go (signup works, wrong password fails, user A can't see user B's project). Don't save all testing for the end.
• Keep a plain text file of decisions and "why" as you build. Later you'll move these into Pulse itself.
• If a phase takes longer than planned, cut scope from later phases, never skip understanding.
Week 1 — Foundation
Phase 0: Setup (Day 1)
Build: Python virtual environment, FastAPI + uvicorn, a hello-world endpoint, PostgreSQL running locally, the folder structure.
Learn: what a virtual environment is, what a web server is, what a port is, what an API route is.
Done when: /docs loads in your browser and psql pulse_db connects.
Explain it: What does uvicorn app.main:app mean? Which port does each service use, and what must match when your app connects to Postgres?
Phase 1: Database and migrations (Days 2-3)
Build: SQLAlchemy engine and session setup, User and Project models, Alembic initialized, first migration applied.
Learn: models vs tables, primary keys, foreign keys, one-to-many relationships, what a migration is and why it exists.
Done when: users and projects tables exist in Postgres, created by a migration (not by hand).
Explain it: Why use migrations instead of editing tables manually? What does the foreign key from projects to users enforce?
Phase 2: Authentication (Day 4)
Build: signup endpoint, login endpoint, password hashing (bcrypt), JWT creation and verification.
Learn: hashing vs encryption, why bcrypt is deliberately slow, what a JWT contains, what happens when it expires, HTTP status codes (200, 201, 400, 401, 409).
Done when: you can sign up, log in, and get a token back; wrong passwords return 401.
Explain it: How does login work if hashing is one-way? What does a JWT prove? What's stored on the server vs in the token?
Phase 3: Projects and authorization (Day 5)
Build: create project, list my projects, get one project, all requiring a valid JWT.
Learn: authentication vs authorization, dependency injection in FastAPI, request validation with Pydantic.
Done when: user A cannot see or fetch user B's project (test this explicitly, including by guessing IDs).
Explain it: What's the difference between 401 and 403 (and why some apps return 404 instead)? Where does the ownership check live in your code?
Phase 4: API keys and basic ingestion (Days 6-7)
Build: api_keys table + migration, generate-key endpoint (show raw key once, store only the hash), events table, POST /api/events authenticated by API key, saving synchronously for now.
Learn: why API keys differ from JWTs, key hashing, event schema design, nullable columns, request validation for different event types.
Done when: a script with a valid key can post an event and it appears in the database; an invalid key gets 401.
Explain it: Why do apps use API keys but users use JWTs? Why is the raw key shown only once? What happens if someone steals the database?
Week 2 — Production-style processing
Phase 5: Queue and worker
Build: Redis running, RQ queue, ingestion endpoint now pushes a job and returns immediately, a worker process saves the event to Postgres, retry logic, failed-job handling.
Learn: why queues exist, what a worker does, sync vs async, what happens when a worker crashes, retries, dead-letter handling.
Done when: you can kill the worker mid-stream, restart it, and no events are lost.
Explain it: Why not just save to the database inside the request? What happens if Redis goes down? If a worker crashes mid-job? What's the downside of retries?
Phase 6: Querying and metrics
Build: endpoints for total requests, error count, error percentage, average response time, recent events, events by endpoint, events over time. Filters for time range, type, endpoint, status code. Pagination.
Learn: SQL aggregation (COUNT, AVG, GROUP BY), indexes and how to check one is used (EXPLAIN), offset vs cursor pagination, time-bucketing.
Done when: metrics match what you computed by hand on a small known dataset.
Explain it: What index did you add to events and why? What gets slow at 10 million rows? Why paginate?
Phase 7: Rate limiting and idempotency
Build: per-API-key rate limit in Redis (start with a fixed window counter), return 429 when exceeded. Optional event_id on events with a unique constraint so duplicates are ignored.
Learn: what rate limiting protects against, fixed window vs sliding window vs token bucket, why retries create duplicates, idempotency, unique constraints.
Done when: the 101st event in a minute gets 429, and sending the same event_id twice stores one row.
Explain it: What's the weakness of a fixed window counter? Where should the duplicate check happen (API or worker) and why?
Phase 8: Caching and health endpoint
Build: cache one expensive dashboard calculation (e.g. error rate for the last hour) in Redis with a short TTL. GET /health that checks the database and Redis.
Learn: when caching helps, TTLs, stale data tradeoffs, cache invalidation, when not to cache.
Done when: the second request is served from cache and you can show the difference.
Explain it: What data would be wrong to cache? What does a stale number cost you here?
Week 3 — Connect monitoring with project memory
Phase 9: Error grouping, alerts, and cooldowns
Build: group repeated errors (first seen, last seen, count, endpoint). Alert rules (e.g. error rate above 5% for 5 minutes). A scheduled job evaluates rules. Cooldown and alert state so a sustained problem doesn't alert every minute.
Learn: how to define "same error" (message normalization, fingerprinting), scheduled jobs, time-window calculations, alert state machines.
Done when: a simulated error spike triggers exactly one alert, and recovery is recorded.
Explain it: How do you decide two errors are the same? Why is alert spam a real problem? What if the scheduler runs twice?
Phase 10: Project memory — documents and journal
Build: documents with Markdown content and templates (architecture, setup, decisions), document_revisions saved on each edit, journal_entries (learning, debugging, decision) with the guided questions.
Learn: versioning data, relational modeling for history, structured vs free-form content, full-text search basics in Postgres (optional).
Done when: you can edit a document, see older versions, and restore one.
Explain it: Why store revisions as separate rows rather than overwriting? What's the storage cost, and how would you limit it?
Phase 11: Timeline, deployments, GitHub, status
Build: timeline_events table (written whenever a deployment, document, entry, incident or recovery happens), deployments recorded manually and via GitHub webhook (with signature validation), correlation ("error spike 7 minutes after deployment"), a project status endpoint that answers "what's going on right now?"
Learn: webhooks, HMAC signature validation, fan-out on write, event correlation, building a status from real facts first.
Done when: a fake deployment followed by a fake error spike produces a timeline entry linking the two.
Explain it: Why validate webhook signatures? Why a dedicated timeline table instead of merging tables on read? What if the webhook arrives twice?
Week 4 — Polish and prove it
Phase 12: Python SDK
Build: a small installable package with track_request and capture_error that call your API, with timeouts and safe error handling (the SDK must never crash the host app).
Learn: packaging, API client design, retries with backoff, failing safely.
Done when: a separate demo app installs the SDK and its events appear in Pulse.
Phase 13: Docker, CI/CD, deployment
Build: Dockerfile, Docker Compose running API + Postgres + Redis + worker, environment variables via .env, GitHub Actions running tests on every push, deploy somewhere simple.
Learn: containers, volumes, networking between services (service names vs localhost), secrets handling, what a pipeline does step by step.
Done when: docker compose up starts everything and CI goes red when a test fails.
Explain it: Why does the app connect to db:5432 inside Compose but localhost outside? What should never be committed to Git?
Phase 14: Load testing and interview prep
Build: a script that sends 1,000 / 10,000 / 50,000 events and records requests per second, response times, queue size, processing throughput, and error rate.
Learn: how to find bottlenecks, reading real measurements, honest reporting.
Done when: you have a table of actual measured results (never invented numbers) and a short note on what the bottleneck was.
Explain it: What broke first and why? How would the design change at 100x traffic?
Final checklist
Before calling it finished, you should be able to explain, without notes:
• the full path of one event from app to database
• what is synchronous and what is asynchronous
• what happens when Redis, the worker, or Postgres fails
• how auth, API keys, and rate limiting each protect the system
• why every table exists
• one thing you'd redesign and why
If you fall behind
Cut in this order: SDK polish, search, GitHub integration, caching, error grouping sophistication. Never cut: auth, ownership checks, ingestion, the queue, tests, and the timeline.