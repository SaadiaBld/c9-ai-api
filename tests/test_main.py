#tester l'api avec quelques appels
import os
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

# Identifiants depuis .env
USERNAME = os.getenv("API_USER")
PASSWORD = os.getenv("API_PASS")

#verifier que l'api repond à la racine avec 200 OK
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenue" in response.json()["message"]

#verifie que l'api repond à /analyze avec 200 OK
def test_analyze_authenticated():
    response = client.post(
        "/analyze",
        auth=(USERNAME, PASSWORD),
        json={"text": "Produit arrivé cassé et aucun retour du service client."}
    )
    assert response.status_code == 200
    assert "themes" in response.json()
    assert isinstance(response.json()["themes"], list)


#verifie que l'api repond à /analyze sans authentification avec message d'erreur
def test_analyze_unauthenticated():
    response = client.post(
        "/analyze",
        json={"text": "Test sans authentification."}
    )
    assert response.status_code == 401

#verifie que l'api repond avec erreur si texte vide
def test_analyze_empty_text():
    response = client.post(
        "/analyze",
        auth=(USERNAME, PASSWORD),
        json={"text": ""}
    )
    assert response.status_code==422 
    assert "detail" in response.json()

    # Vérifie que le message d’erreur attendu est dans la réponse
    error_messages = [err["msg"] for err in response.json()["detail"]]
    assert any("Le texte ne peut pas être vide" in msg for msg in error_messages)