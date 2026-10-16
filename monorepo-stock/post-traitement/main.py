"""
Service de Post-traitement (Vision par Ordinateur)
Responsabilité : Analyse une image reçue et extrait le texte encodé (QR Code ou Code-barres 1D).
"""
from fastapi import FastAPI, File, UploadFile
import cv2 as cv
import numpy as np

app = FastAPI(title="Post-Traitement API", description="Décodage optique QR Code et Codes-Barres")


@app.get("/health")
async def health():
    """Contrôle de santé du service."""
    return {"status": "ok", "service": "post-traitement"}


def decode_optical_code(image: np.ndarray) -> tuple[bool, str, str]:
    """
    Tente de décoder un QR code, puis à défaut un code-barres 1D.
    Retourne : (succès: bool, type_code: str, valeur: str)
    """
    # 1. Détection QR Code (2D)
    qr_detector = cv.QRCodeDetector()
    data, _, _ = qr_detector.detectAndDecode(image)
    if data:
        return True, "QR Code", data

    # 2. Détection Code-barres (1D)
    if hasattr(cv, "barcode"):
        barcode_detector = cv.barcode.BarcodeDetector()
        data_bc, _, _ = barcode_detector.detectAndDecode(image)
        if data_bc:
            val = data_bc[0] if isinstance(data_bc, (list, tuple)) else data_bc
            if val:
                return True, "Code-Barres", val

    return False, "", ""


@app.post("/api/decode")
async def decode_image(file: UploadFile = File(...)):
    """Point d'entrée de décodage d'image."""
    content = await file.read()
    if not content:
        return {"status": "error", "message": "Fichier image vide.", "data": None}

    # Décodage de l'image en mémoire
    nptab = np.frombuffer(content, np.uint8)
    image = cv.imdecode(nptab, cv.IMREAD_COLOR)

    if image is None:
        return {
            "status": "error",
            "message": "Format d'image non reconnu ou corrompu.",
            "data": None
        }

    found, code_type, value = decode_optical_code(image)
    if found:
        return {
            "status": "ok",
            "message": f"{code_type} détecté avec succès",
            "data": value
        }

    return {
        "status": "error",
        "message": "Aucun QR code ni code-barres détecté dans l'image.",
        "data": None
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)
