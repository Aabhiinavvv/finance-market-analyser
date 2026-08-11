# Production Readiness Plan

This document defines what “production ready” means for Finance Market Analyser.

## 1. Current blockers

- [ ] Rotate the NewsAPI key that was previously committed to source control.
- [ ] Remove all other historical credentials from Git history if any are found.
- [ ] Pin and lock Python dependencies for reproducible builds.
- [ ] Add unit tests for data providers, analytics, prediction, and AI adapters.
- [ ] Add integration tests for the critical user journeys.
- [ ] Separate Streamlit presentation code from domain/application services.
- [ ] Add timeouts, retries, rate-limit handling, and provider-specific error handling.
- [ ] Add structured logs and request/provider latency metrics.
- [ ] Define market-data freshness and missing-data policies.
- [ ] Validate ticker input and enforce bounded query sizes.
- [ ] Add model evaluation with a time-based holdout; never claim predictive quality from training fit alone.
- [ ] Add financial-data provenance and timestamps to displayed results.
- [ ] Add explicit investment-risk disclaimers and avoid unsupported BUY/SELL claims.
- [ ] Add authentication/authorization if private or paid features are introduced.
- [ ] Add dependency and secret scanning to CI.
- [ ] Add a deployment environment with secrets stored outside the image.
- [ ] Add monitoring, alerting, backup/restore procedures, and an incident runbook.

## 2. Target architecture

```text
Streamlit UI
    |
    v
Application services
    |---- Market Data Adapter ----> Yahoo/provider APIs
    |---- News Adapter -----------> News provider
    |---- AI Adapter -------------> Hugging Face / LLM provider
    |---- Analytics Engine -------> deterministic Python services
    |---- Persistence ------------> database/cache
    |
    v
Observability: logs + metrics + health/dependency checks
```

The UI should orchestrate services, not contain provider calls, financial rules, model execution, and presentation logic in one file.

## 3. Release gates

A release can be called production-ready only when:

1. CI is green on the exact commit being deployed.
2. Tests cover critical paths and known failure modes.
3. No high/critical dependency or secret findings remain.
4. Secrets are supplied only through the deployment secret store.
5. External providers have bounded timeouts and graceful degradation.
6. The application has a documented rollback path.
7. Monitoring can detect provider failures and application errors.
8. Data timestamps and source/provenance are visible where financially material.
9. Prediction models have out-of-sample evaluation and a documented baseline.
10. Security, privacy, and financial-risk disclosures are reviewed.

## 4. Recommended maturity stages

### Stage A — Engineering baseline

Tests, CI, formatting/linting, dependency lock, environment configuration, logging, Docker, and clean repository history.

### Stage B — Reliable data platform

Provider adapters, retries/backoff, caching, rate-limit handling, freshness checks, schema validation, and a database/cache strategy.

### Stage C — ML/AI reliability

Versioned models/prompts, time-series validation, evaluation datasets, model metadata, deterministic fallbacks, latency/cost limits, and AI output validation.

### Stage D — Production operations

Deployment pipeline, staging environment, observability, alerts, rollback, backups, incident response, and security scanning.

### Stage E — Commercial product

Authentication, tenancy, quotas, billing, audit logs, privacy controls, terms/disclosures, support workflow, and product analytics.
