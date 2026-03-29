# ISMAP Deployment Guide

This project can be deployed most simply on Render as:

1. One Docker-based web service for the Flask backend and built frontend
2. One Render Postgres database

In this setup, Flask serves the built React frontend from `frontend/dist`, so you do not need Vercel.

## Before You Push

Make sure these are not committed:

- `.env`
- `ismap.db`
- Slack webhooks
- Telegram bot tokens

If you exposed any secrets during testing, rotate them before deployment.

## Files Already Prepared

This repo already includes:

- [Dockerfile](/c:/Users/Ayool/Documents/final-year/ismap-main/Dockerfile)
- [start.sh](/c:/Users/Ayool/Documents/final-year/ismap-main/start.sh)
- [render.yaml](/c:/Users/Ayool/Documents/final-year/ismap-main/render.yaml)
- [.dockerignore](/c:/Users/Ayool/Documents/final-year/ismap-main/.dockerignore)

## Render Deployment

### Option A: Blueprint

1. In Render, click `New +`
2. Choose `Blueprint`
3. Select your GitHub repo
4. Let Render read `render.yaml`

This should create:

- web service: `ismap`
- database: `ismap-db`

### Option B: Manual

If Blueprint is confusing, create these manually:

1. `New +` -> `Web Service`
2. Select your repo
3. Choose Docker runtime
4. Let Render build from the repo `Dockerfile`
5. Create a separate `PostgreSQL` database in Render

## Required Environment Variables

Render should provide or allow you to set:

- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `CORS_ORIGINS`

Optional:

- `RECOVERY_ADMINS_JSON`

Example:

```text
CORS_ORIGINS=https://your-render-app.onrender.com
```

```text
RECOVERY_ADMINS_JSON=[{"email":"admin@example.com","username":"admin","password":"strong-password"}]
```

## How It Works

- Docker builds the frontend with Vite
- the built frontend is copied into `frontend/dist`
- Flask serves that built frontend
- Gunicorn runs the backend with one worker
- Postgres stores production data

## First Production Login

You have two choices:

1. Leave `RECOVERY_ADMINS_JSON` empty and register the first user manually
2. Set `RECOVERY_ADMINS_JSON` so Render creates an admin account on startup

## Notes

- Local development can still use SQLite
- Production should use Postgres
- The `/` route will work in Render once the Docker build includes the frontend dist output
