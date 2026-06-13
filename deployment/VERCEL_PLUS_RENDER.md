# Deploy Frontend on Vercel and API on Render

Use this option if you prefer Vercel for the Next.js dashboard.

## Backend

Deploy `backend/` as a Docker web service on Render.

Environment variables:

```text
AGENOVA_ENV=production
AGENOVA_LLM_PROVIDER=mock
AGENOVA_USE_SENTENCE_TRANSFORMERS=false
```

Health path:

```text
/health
```

## Frontend

Create a Vercel project from the same GitHub repository.

Settings:

```text
Framework Preset: Next.js
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
```

Environment variable:

```text
NEXT_PUBLIC_API_URL=https://<your-render-api>.onrender.com
```
