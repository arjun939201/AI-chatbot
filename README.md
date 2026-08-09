# Melimi Telugu AI

Initial FastAPI backend foundation for the Melimi Telugu AI chatbot.

## Run locally

1. Install dependencies:

```powershell
py -m pip install -r backend/requirements.txt
```

2. Create a `.env` file from `.env.example` and set the values.

3. Start the backend:

```powershell
py -m uvicorn backend.app.main:app --host 0.0.0.0 --port 5000
```

4. Open the API docs:

```text
http://127.0.0.1:5000/docs
```

