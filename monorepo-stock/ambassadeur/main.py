from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import asyncio

app = FastAPI(title="Ambassadeur API")

# Configuration CORS indispensable pour que React (sur un autre port) puisse communiquer
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/scan")
async def process_scan(file: UploadFile = File(...)):
    # 1. On lit le fichier (pour vérifier qu'on le reçoit bien)
    content = await file.read()
    
    # 2. On simule un délai de traitement de 1.5 seconde (comme si on appelait le post-traitement)
    await asyncio.sleep(1.5)
    
    # 3. On renvoie une fausse réponse de succès pour valider la communication
    return {
        "status": "success",
        "message": f"Fichier '{file.filename}' reçu par l'Ambassadeur (taille: {len(content)} octets).",
        "post_traitement_data": {"code_detecte": "QR-TEST-123", "action": "entree_stock"},
        "datawarehouse_result": {"stock_mis_a_jour": True, "nouveau_stock": 42}
    }