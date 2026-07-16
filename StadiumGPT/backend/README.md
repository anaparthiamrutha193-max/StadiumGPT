# StadiumGPT Backend

FastAPI backend for an AI-powered FIFA World Cup 2026 smart stadium assistant.

## Start

```powershell
cd backend
Copy-Item .env.example .env
python -m pip install -r requirements.txt
python -m uvicorn app:app --reload
```

Open `http://127.0.0.1:8000/docs` for Swagger. Set a strong `JWT_SECRET_KEY` and `GEMINI_API_KEY` in `.env` before deployment. Login accepts OAuth2 form data (`username` is the registered email) and returns a bearer JWT for protected endpoints.

Chat and translation call Google Gemini directly and return HTTP 503 if no Gemini key is configured or the service is unavailable. The local SQLite database file is created automatically on startup.