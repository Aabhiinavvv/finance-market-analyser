# Finance Market Analyser

AI-assisted market intelligence for Indian equities: market data, financial news, fundamental analysis, event-impact analysis, ML experiments, and finance explanations.

> **Status: Production hardening in progress.** This repository is an engineering project and is not investment advice. Market data and AI outputs can be delayed, incomplete, or wrong.

## What it does

- Live market and stock-price views using provider APIs
- Fundamental and financial-statement analysis
- Market news ingestion
- Event-impact classification and rule-based sector mapping
- Experimental stock prediction
- AI-assisted financial explanations and market analysis
- Stock screening and peer comparison

## Architecture direction

The target architecture separates the Streamlit UI from application services, external data adapters, analytics/ML, AI providers, persistence, and observability. See [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md).

## Run locally

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

copy .env.example .env  # Windows
# cp .env.example .env  # macOS/Linux

streamlit run app.py
```

Never commit `.env` or provider credentials. Production deployments must inject secrets through the platform's secret manager.

## Test

```bash
pip install -r requirements.txt
pip install pytest
pytest -q
```

CI runs automatically on pushes to `main` and pull requests.

## Container

```bash
docker build -t finance-market-analyser .
docker run --rm -p 8501:8501 --env-file .env finance-market-analyser
```

The image includes a Streamlit health check. Do not bake API keys into the image.

## Production readiness

Production readiness is more than a working demo. Before calling this application production-ready, the release must pass the gates in [`docs/PRODUCTION_READINESS.md`](docs/PRODUCTION_READINESS.md), including security scanning, reproducible dependencies, tests, provider resilience, observability, model evaluation, data provenance, financial disclosures, deployment/rollback, and incident response.

## Security

See [`SECURITY.md`](SECURITY.md). A credential previously committed to source control must be revoked/rotated at the provider even after it is removed from the latest source tree.
