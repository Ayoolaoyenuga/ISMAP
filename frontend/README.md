# ISMAP Frontend

This frontend is built with React and Vite.

## Development

From this `frontend` directory:

```cmd
npm install
npm run dev
```

The Vite dev server runs on:

```text
http://localhost:5173
```

During development, `/api` requests are proxied to the Flask backend at:

```text
http://localhost:5000
```

Make sure the backend is running before using the UI.

## Production Build

Build the frontend with:

```cmd
npm run build
```

The output is written to `dist`. The Flask app serves this built frontend from `frontend/dist` when you use the batch-script flow or run the backend directly without the Vite dev server.
