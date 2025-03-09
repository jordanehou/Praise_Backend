from fastapi import APIRouter, File, UploadFile
import os

router = APIRouter()
UPLOAD_FOLDER = 'uploads/'  # Dossier où les images seront sauvegardées

# Créer le dossier si il n'existe pas
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_FOLDER}{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())
    return {"imagePath": file_location}