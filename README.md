# AI Verbatim API

API REST développée avec **FastAPI** permettant d’analyser automatiquement des verbatims clients grâce à un modèle d’intelligence artificielle (Claude 3 Haiku).

---

## Fonctionnalités

- 🔐 Authentification sécurisée via identifiant/mot de passe (HTTP Basic Auth)
- 🧠 Appel au modèle Claude 3 Haiku (Anthropic) pour classifier les verbatims
- 📈 Renvoie les thèmes détectés et leur note de satisfaction (sur 5)
- ✅ Conformité avec le standard OpenAPI (docs auto-générées)
- 🧪 Suite de tests automatisés avec `pytest`

---

## Arborescence

ai_verbatim_api_starter/
├── api/
│ ├── main.py # Point d'entrée FastAPI
│ ├── models.py # Pydantic models pour validation
│ ├── claude/
│ │ ├── claude_interface.py # Interaction avec Claude + nettoyage
│ │ ├── prompt_utils.py # Génération du prompt Claude
│ │ └── themes.py # Liste des thèmes et labels autorisés
├── tests/
│ └── test_main.py # Suite de tests unitaires
├── .env # Clé API Anthropic + identifiants
├── requirements.txt
├── run_tests.sh # Script pour exécuter les tests
└── README.md


---

## Installation

1. **Clone le dépôt** :

```bash
git clone https://github.com/ton-utilisateur/ai-verbatim-api.git
cd ai-verbatim-api
```

2. **Crée un environnement virtuel :** :

```bash
python -m venv venv
source venv/bin/activate
```

2. **Installer les dépendances :** :

```bash
pip install -r requirements.txt
```

2. **Configurer les variables d'environnement dans .env à la racine :** :

```bash
API_KEY=sk-...                   # clé pour appeler le llm
API_USER=mon_id                  
API_PASS=mon_mot_de_passe        
```
---

## Lancer l'API

2. **Configurer les variables d'environnement dans .env à la racine :** :

Depuis la racine du projet :

```bash
uvicorn api.main:app --reload
```
Visite ensuite http://127.0.0.1:8000/docs pour accéder à l'interface interactive Swagger UI.

---

## Authentification

Toutes les routes protégées (comme /analyze) nécessitent une authentification HTTP Basic.

## Lancer les tests

Executer le fichier à la racine:
```bash
chmod +x run_tests.sh
./run_tests.sh
```bash

