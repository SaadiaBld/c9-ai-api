#!/bin/bash

echo "Démarrage de l'API FastAPI avec uvicorn..."
source venv/bin/activate
uvicorn api.main:app --reload
