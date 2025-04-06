from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

class SecretRequest(BaseModel):
    key_name: str

@app.post("/api/get-key/")
async def get_key(request: SecretRequest, authorization: str = Header(None)):
    auth_token = os.getenv("AUTH_TOKEN")
    if authorization != f"Bearer {auth_token}":
        raise HTTPException(status_code=403, detail="Unauthorized")

    secrets = {
        "firebase_api_key": os.getenv("FIREBASE_API_KEY"),
        "supabase_api_key": os.getenv("SUPABASE_API_KEY"),
        "postgres_url": os.getenv("POSTGRES_URL"),
    }

    key_value = secrets.get(request.key_name)
    if not key_value:
        raise HTTPException(status_code=404, detail="Key not found")

    return {"key": key_value}