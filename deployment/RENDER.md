# Deploy on Render

This repository includes `render.yaml` for Render Blueprint deployment.

## Steps

1. Push this repository to `https://github.com/Ani-sha23/AgeNova`.
2. Open Render and choose **New > Blueprint**.
3. Connect the `Ani-sha23/AgeNova` repository.
4. Render will detect `render.yaml` and create:
   - `agenova-api`
   - `agenova-dashboard`
5. After the API deploys, set the dashboard environment variable if needed:

```text
NEXT_PUBLIC_API_URL=https://<agenova-api-service>.onrender.com
```

The backend defaults to the mock LLM provider and hash embeddings so it can run on a free instance without external API keys.

## Health Check

```text
https://<agenova-api-service>.onrender.com/health
```

## Dashboard

```text
https://<agenova-dashboard-service>.onrender.com
```
