from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import os
import httpx

app = FastAPI(title="Ambassadeur API")

# Configuration CORS pour autoriser l'interface Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

POST_TRAITEMENT_URL = os.getenv("POST_TRAITEMENT_URL", "http://localhost:8002")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "ambassadeur"}


@app.post("/api/scan")
async def process_scan(file: UploadFile = File(...)):
    content = await file.read()

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{POST_TRAITEMENT_URL}/api/decode",
                files={"file": (file.filename, content, file.content_type or "image/png")},
            )
        
        if response.status_code == 200:
            return response.json()
        else:
            return {
                "status": "error",
                "message": f"Erreur du service post-traitement (HTTP {response.status_code})",
                "data": None
            }
    except httpx.RequestError as exc:
        return {
            "status": "error",
            "message": f"Impossible de contacter le service post-traitement ({exc})",
            "data": None
        }