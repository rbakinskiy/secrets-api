from fastapi import FastAPI, Header, HTTPException, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")

class SecretRequest(BaseModel):
    key_name: str

@app.post("/api/get-key/")
async def get_key(
    request: Request,
    payload: SecretRequest,
    authorization: str = Header(None)
):
    origin = request.headers.get("origin")

    if authorization != f"Bearer {AUTH_TOKEN}":
        raise HTTPException(status_code=403, detail="Invalid token")

    if origin and origin not in ALLOWED_ORIGINS:
        raise HTTPException(status_code=403, detail="Origin not allowed")

    secrets = {
        "firebase_api_key": os.getenv("FIREBASE_API_KEY"),
        "supabase_api_key": os.getenv("SUPABASE_API_KEY"),
        "postgres_url": os.getenv("POSTGRES_URL"),
    }

    key_value = secrets.get(payload.key_name)
    if not key_value:
        raise HTTPException(status_code=404, detail="Key not found")

    return {"key": key_value}