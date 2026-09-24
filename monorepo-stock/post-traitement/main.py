from fastapi import FastAPI, File, UploadFile
import cv2 as cv
import numpy as np

app = FastAPI(title="Post-Traitement API")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "post-traitement"}


@app.post("/api/decode")
async def decode_image(file: UploadFile = File(...)):
    content = await file.read()

    # Convertir le contenu binaire en tableau numpy
    nptab = np.frombuffer(content, np.uint8)
    image = cv.imdecode(nptab, cv.IMREAD_COLOR)

    if image is None:
        return {
            "status": "error",
            "message": "Fichier image invalide ou non supporté.",
            "data": None
        }

    detecteur = cv.QRCodeDetector()
    data, points, _ = detecteur.detectAndDecode(image)

    if data:
        return {
            "status": "ok",
            "message": "QR Code détecté avec succès",
            "data": data
        }

    return {
        "status": "error",
        "message": "Aucun QR code n'a été détecté dans l'image.",
        "data": None
    }