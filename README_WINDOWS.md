# ISMAP Windows Quick Start

ISMAP supports two Windows workflows:

1. Quick local run with the included batch scripts
2. Two-terminal development mode for backend and frontend work

## Prerequisites

- Python 3.10 or newer
- Node.js LTS

Make sure Python was installed with `Add python.exe to PATH`.

## Fastest Option

From the project root:

```cmd
install_windows.bat
run_windows.bat
```

Then open:

```text
http://localhost:5000
```

`install_windows.bat` creates `venv`, installs backend packages, installs frontend packages, and builds the frontend. `run_windows.bat` starts the Flask app and serves the built frontend.

## Development Mode

If you want live frontend reloads:

Backend terminal:

```cmd
cd path\to\ismap-main
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python app.py
```

Frontend terminal:

```cmd
cd path\to\ismap-main\frontend
npm install
npm run dev
```

Open:

```text
http://localhost:5173
```

Important:

- Set `JWT_SECRET_KEY` in `.env` before starting the backend.
- The first registered user becomes the administrator on a new database.

For full instructions and troubleshooting, see [WINDOWS_INSTALLATION_GUIDE.md](/c:/Users/Ayool/Documents/final-year/ismap-main/WINDOWS_INSTALLATION_GUIDE.md).
