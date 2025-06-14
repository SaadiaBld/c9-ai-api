import os
import json
import logging
from dotenv import load_dotenv
from anthropic import Anthropic

from .prompt_utils import build_prompt
from .themes import THEME_LABELS

# Configuration du logger
logger = logging.getLogger(__name__)

# Charger les variables d'environnement
load_dotenv()

# Initialiser le client Anthropic avec la clé API
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def sanitize_text(verbatim: str) -> str:
    """
    Nettoie les caractères problématiques (apostrophes brutes, espaces...).
    """
    return verbatim.replace("'", "’").strip()


def classify_with_claude(verbatim: str) -> list[dict] | None:
    """
    Envoie un verbatim nettoyé à Claude pour analyse,
    puis valide et retourne les résultats.
    """
    cleaned_verbatim = sanitize_text(verbatim)
    prompt = build_prompt(cleaned_verbatim)

    try:
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=500,
            temperature=0,
            system="Tu es un assistant d’analyse de satisfaction client.",
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.content[0].text.strip()
        print("\nRéponse brute de Claude :\n", content)

        validated = validate_claude_response(content)
        if not validated:
            logger.warning(f"❌ Réponse non valide : {content}")
            return []
        return validated

    except Exception as e:
        logger.error(f"Erreur API Claude : {e}")
        raise RuntimeError("Erreur lors de l'appel à Claude") from e


def validate_claude_response(response_text: str) -> list[dict] | None:
    """
    Valide et transforme la réponse JSON de Claude en structure exploitable.
    """
    try:
        data = json.loads(response_text)

        if "themes" not in data or not isinstance(data["themes"], list):
            logger.warning(f"Clé 'themes' manquante ou invalide : {response_text}")
            return None

        results = []

        for item in data["themes"]:
            if not isinstance(item, dict):
                logger.warning(f"Item non structuré : {item}")
                continue

            theme = item.get("theme")
            note = item.get("note")

            if theme not in THEME_LABELS:
                logger.warning(f"Thème inconnu : {theme}")
                continue

            if not isinstance(note, (int, float)) or not (1 <= note <= 5):
                logger.warning(f"Note invalide pour {theme} : {note}")
                continue

            results.append({"theme": theme, "note": note})

        return results

    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON : {e} dans : {response_text}")
        return []
