from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from .models import VerbatimRequest, VerbatimResponse
from .claude.claude_interface import classify_with_claude
from dotenv import load_dotenv
import secrets
import os

# Charger les variables d'environnement
load_dotenv()

# Lecture des identifiants depuis .env
API_USER = os.getenv("API_USER", "admin")
API_PASS = os.getenv("API_PASS", "verbatim123")

security = HTTPBasic()
app = FastAPI()


def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Vérifie les identifiants transmis dans la requête (HTTP Basic Auth).
    """
    correct_username = secrets.compare_digest(credentials.username, API_USER)
    correct_password = secrets.compare_digest(credentials.password, API_PASS)

    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Identifiants invalides")
    
    return credentials.username  # Peut être utilisé dans les logs si besoin


@app.get("/")
def read_root():
    return {"message": "Bienvenue dans l’API d’analyse de verbatim client."}


@app.post("/analyze", response_model=VerbatimResponse)
def analyze_text(
    verbatim: VerbatimRequest,
    username: str = Depends(authenticate)
):
    """
    Analyse un verbatim client et retourne les thèmes détectés avec leur note.
    Nécessite une authentification via identifiant/mot de passe.
    """
    try:
        results = classify_with_claude(verbatim.text)
        if results is None:
            raise HTTPException(status_code=500, detail="Échec de l’analyse.")
        return VerbatimResponse(themes=results)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur inattendue : {str(e)}")
