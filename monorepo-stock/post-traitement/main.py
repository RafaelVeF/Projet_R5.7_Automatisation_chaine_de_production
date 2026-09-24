# fichier main.py du module post-traitement
from fastapi import FastAPI, File, UploadFile
import cv2 as cv
import numpy as np

app = FastAPI()


@app.post("/api/decode")
async def decode_image(file: UploadFile = File(...)):
    contenue = await file.read()

    # Convertir le contenu en tableau numpy
    nptab = np.frombuffer(contenue, np.uint8)

    # Lire l'image à partir du tableau numpy
    image = cv.imdecode(nptab, cv.IMREAD_COLOR)

    detecteur = cv.QRCodeDetector()
    data, points, _ = detecteur.detectAndDecode(image)

    if data:
        return {
            "status" : "ok",
            "data": data
        }

    return {
        "status" : "error",
        "data": None
    }