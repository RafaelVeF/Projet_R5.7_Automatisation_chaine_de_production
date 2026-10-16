"""
Service de Post-traitement (Vision par Ordinateur)
Responsabilité : Analyse une image reçue et extrait le texte encodé (QR Code ou Code-barres 1D).
"""
from fastapi import FastAPI, File, UploadFile
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode as zbar_decode

app = FastAPI(title="Post-Traitement API", description="Décodage optique QR Code et Codes-Barres")


@app.get("/health")
async def health():
    """Contrôle de santé du service."""
    return {"status": "ok", "service": "post-traitement"}


def decode_optical_code(image: np.ndarray) -> tuple[bool, str, str]:
    results = zbar_decode(image)
    if results:
        code = results[0]
        code_type = code.type  # ex: "QRCODE", "EAN13", "CODE128"
        value = code.data.decode("utf-8")
        return True, code_type, value

    return False, "", ""


@app.post("/api/decode")
async def decode_image(file: UploadFile = File(...)):
    """Point d'entrée de décodage d'image."""
    content = await file.read()
    if not content:
        return {"status": "error", "message": "Fichier image vide.", "data": None}

    # Décodage de l'image en mémoire
    image = cv.imdecode(np.frombuffer(content, np.uint8), cv.IMREAD_COLOR)
    if image is None:
        return {"status": "error", "message": "Format d'image non reconnu ou corrompu.", "data": None}

    found, code_type, value = decode_optical_code(image)
    if found:
        return {"status": "ok", "message": f"{code_type} détecté avec succès", "data": value}

    return {"status": "error", "message": "Aucun QR code ni code-barres détecté dans l'image.", "data": None}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
