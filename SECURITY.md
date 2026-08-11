# Security Policy

## Reporting a vulnerability

Please do not open a public issue for security vulnerabilities. Contact the repository owner privately through GitHub with a description, reproduction steps, and impact.

## Secrets

Never commit API keys, access tokens, credentials, model-provider secrets, or local `.env` files. Use GitHub Actions secrets and deployment-platform secret stores for production values.

If a credential was ever committed, assume it is compromised: revoke/rotate it at the provider and then remove it from the repository history.

## Financial safety

This application provides market analysis and educational information. It must not be presented as personalized investment advice or as a guarantee of future returns. Any production deployment should display appropriate risk disclosures and clearly distinguish market data, model output, and human-authored rules.
