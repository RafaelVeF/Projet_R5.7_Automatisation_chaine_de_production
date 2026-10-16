"""
Service Ambassadeur (API Gateway & Orchestrateur)
Responsabilité : Point d'entrée unique de la logique métier. Reçoit les requêtes de l'IHM Web,
les achemine vers les micro-services spécialisés (Post-traitement, Datawarehouse) et consolide la réponse.
"""
import os
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI(
    title="Ambassadeur API",
    description="Orchestrateur de la chaîne de gestion de stocks"
)

# Configuration CORS pour autoriser l'IHM Web
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# URLs des micro-services cibles (configurables via variables d'environnement)
POST_TRAITEMENT_URL = os.getenv("POST_TRAITEMENT_URL", "http://localhost:8002")
DATAWAREHOUSE_URL = os.getenv("DATAWAREHOUSE_URL", "http://localhost:8081")


@app.get("/health")
async def health():
    """Contrôle de santé du service."""
    return {"status": "ok", "service": "ambassadeur"}


@app.post("/api/scan")
async def process_scan(file: UploadFile = File(...)):
    """
    Orchestration d'un scan :
    1. Transmet l'image au service de Post-traitement pour décodage.
    2. Récupère la valeur du code (QR ou code-barres).
    3. Renvoie le résultat consolidé à l'IHM.
    """
    content = await file.read()
    if not content:
        return {"status": "error", "message": "Aucun fichier fourni.", "data": None}

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{POST_TRAITEMENT_URL}/api/decode",
                files={"file": (file.filename or "image.png", content, file.content_type or "image/png")},
            )

        if response.status_code == 200:
            return response.json()

        return {
            "status": "error",
            "message": f"Erreur du service de décodage (HTTP {response.status_code})",
            "data": None,
        }
    except httpx.RequestError as exc:
        return {
            "status": "error",
            "message": f"Service de post-traitement injoignable ({exc})",
            "data": None,
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)