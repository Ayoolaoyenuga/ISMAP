# Complete ISMAP Installation and Startup Guide for Windows

This guide walks you through setting up and running ISMAP on Windows from scratch.

ISMAP can be used in two ways:

1. Development mode: run the Flask backend and Vite frontend in two terminals.
2. Simple local mode: use the included Windows scripts and access the app from `http://localhost:5000`.

Use development mode if you want live frontend reloads while editing the project. Use the script-based mode if you just want to run the app locally.

---

## Part 1: Prerequisites

Install these first:

1. Python 3.10 or newer from [python.org](https://www.python.org/downloads/).
   During installation, enable `Add python.exe to PATH`.
2. Node.js LTS from [nodejs.org](https://nodejs.org/).
3. Git from [git-scm.com](https://git-scm.com/) if you want easier cloning and updates.

To confirm installation, open Command Prompt or PowerShell and run:

```cmd
python --version
node --version
npm --version
```

---

## Part 2: Backend Setup

Open a terminal in the project root:

```cmd
cd path\to\your\ismap-main
```

Create a virtual environment:

```cmd
python -m venv venv
```

Activate it:

```cmd
venv\Scripts\activate
```

Install backend dependencies:

```cmd
pip install -r requirements.txt
```

Create your local environment file:

```cmd
copy .env.example .env
```

Open `.env` and make sure `JWT_SECRET_KEY` is set to a long random string. The backend will not start without it.

The default SQLite database file, `ismap.db`, is created automatically on first run.

---

## Part 3: Frontend Setup

Open a second terminal and move into the frontend folder:

```cmd
cd path\to\your\ismap-main\frontend
```

Install frontend dependencies:

```cmd
npm install
```

---

## Part 4: Start ISMAP in Development Mode

Development mode uses two terminals.

Terminal 1, backend:

```cmd
cd path\to\your\ismap-main
venv\Scripts\activate
python app.py
```

Success indicator:

```text
Running on http://127.0.0.1:5000
```

Terminal 2, frontend:

```cmd
cd path\to\your\ismap-main\frontend
npm run dev
```

Success indicator:

```text
VITE ready
Local: http://localhost:5173/
```

Open your browser at:

```text
http://localhost:5173
```

In this mode, the Vite dev server serves the UI and proxies `/api` requests to the Flask backend on port `5000`.

---

## Part 5: Start ISMAP with the Included Windows Scripts

If you do not need live frontend reloads, you can use the bundled scripts instead.

From the project root:

```cmd
install_windows.bat
run_windows.bat
```

This flow:

1. Creates `venv`
2. Installs Python dependencies
3. Installs frontend dependencies
4. Builds the frontend into `frontend\dist`
5. Starts the Flask app, which serves the built frontend directly

Open your browser at:

```text
http://localhost:5000
```

This mode uses only one running server after setup.

---

## Part 6: First Login

On a brand-new database:

1. Open the app in your browser.
2. Go to the Register page.
3. Create the first user account.
4. The first registered user becomes the administrator.
5. Log in with that account and start using ISMAP.

---

## Daily Usage

For development mode:

Terminal 1:

```cmd
cd path\to\ismap-main
venv\Scripts\activate
python app.py
```

Terminal 2:

```cmd
cd path\to\ismap-main\frontend
npm run dev
```

Then open:

```text
http://localhost:5173
```

For script-based local usage:

```cmd
cd path\to\ismap-main
run_windows.bat
```

Then open:

```text
http://localhost:5000
```

---

## Troubleshooting

`python` is not recognized:

- Reinstall Python and enable `Add python.exe to PATH`.

`node` or `npm` is not recognized:

- Reinstall Node.js LTS and reopen the terminal.

`Import "dotenv" could not be resolved` or similar VS Code errors:

- Select the project interpreter at `ismap-main\venv\Scripts\python.exe` or `ismap-main\.venv\Scripts\python.exe`, depending on the environment you created and installed packages into.

Backend fails with missing `JWT_SECRET_KEY`:

- Create `.env` from `.env.example` and set `JWT_SECRET_KEY`.

Frontend loads but API calls fail:

- Make sure `python app.py` is still running on port `5000`.

Port already in use:

- Stop the process using port `5000` or `5173`, or restart your machine and try again.
