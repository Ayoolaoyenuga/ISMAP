# ISMAP Deployment Guide

This project is best deployed as:

1. Frontend on Vercel
2. Backend on Render
3. Database on Render Postgres

## Why

- The frontend is a React/Vite app and fits Vercel well.
- The backend uses Flask, background scheduling, and a relational database.
- SQLite is fine locally, but for deployment you should use Postgres.

## Before You Push

Make sure these are not committed:

- `.env`
- `ismap.db`
- Slack webhooks
- Telegram bot tokens

If you exposed a webhook or bot token during testing, rotate it before deployment.

## 1. Push To GitHub

From the project root:

```bash
git init
git add .
git commit -m "Prepare ISMAP for deployment"
git branch -M main
git remote add origin <your-github-repo-url>
git push -u origin main
```

## 2. Deploy Backend On Render

This repo includes [render.yaml](/c:/Users/Ayool/Documents/final-year/ismap-main/render.yaml).

In Render:

1. Create a new Blueprint or Web Service from your GitHub repo
2. Use the `ismap-main` directory as the backend root
3. Let Render create the Postgres database from `render.yaml`

Set these environment variables in Render:

- `CORS_ORIGINS=https://your-frontend-domain.vercel.app`
- `RECOVERY_ADMINS_JSON=[{"email":"admin@example.com","username":"admin","password":"strong-password"}]`

Render already gets:

- `DATABASE_URL`
- `JWT_SECRET_KEY`

from the blueprint config

## 3. Deploy Frontend On Vercel

In Vercel:

1. Import the same GitHub repo
2. Set the project root to `ismap-main/frontend`
3. Add this environment variable:

```text
VITE_API_URL=https://your-render-backend.onrender.com
```

Then deploy.

## 4. Update Backend CORS

Your backend must allow the frontend origin.

In Render, set:

```text
CORS_ORIGINS=https://your-vercel-project.vercel.app
```

If you use a custom frontend domain later, add it too:

```text
CORS_ORIGINS=https://your-vercel-project.vercel.app,https://app.yourdomain.com
```

## 5. First Production Login

You have two options:

1. Leave `RECOVERY_ADMINS_JSON` empty and create the first account manually
2. Set `RECOVERY_ADMINS_JSON` so Render creates your admin account on startup

## Notes

- Local development can still use SQLite
- Production should use Postgres
- Render runs the Flask app with one worker in order to avoid duplicate schedulers
- Vercel hosts only the frontend in this setup
