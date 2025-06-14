from .themes import THEMES

def build_prompt(verbatim: str) -> str:
    theme_list = "\n".join([f'- {t["nom"]} : {t["description"]}' for t in THEMES])

    return f"""
Tu es un expert en analyse de la satisfaction client pour une enseigne spécialisée dans la rénovation de l’habitat (bricolage, aménagement, matériaux, outillage).

Voici un avis client à analyser :
"{verbatim}"

Ta mission est de détecter les **thèmes abordés** dans cet avis client parmi ceux listés ci-dessous, et d’attribuer à chacun une **note de satisfaction** sur 5 (avec décimale possible).

---

Tu dois respecter scrupuleusement les **étapes suivantes** :

**Étape 1 — Vérification du contexte**
- Est-ce que l’avis concerne une **expérience client réelle et identifiable** avec l’enseigne ?
  (produit, service, relation client, magasin, site web, livraison, etc.)
- Si ce n’est pas le cas, **ne continue pas** l’analyse et retourne exactement :
```json
{{ "themes": [] }}

Étape 2 — Détection des thèmes

    Si l’avis est pertinent, identifie tous les thèmes présents parmi ceux de la liste ci-dessous.

    Ne détecte aucun thème si rien ne correspond exactement aux thèmes listés.

    N’invente jamais de nouveaux thèmes.

Étape 3 — Attribution des notes

    Pour chaque thème détecté, attribue une note entre 1 et 5 (décimale autorisée).

        1 = très insatisfait

        5 = très satisfait

Liste des thèmes disponibles (tu dois utiliser les noms exactement tels quels) :
{theme_list}

Consignes supplémentaires :

    🚫 N’invente jamais de thème. Utilise uniquement les noms fournis.
    🚫 Ne retourne **aucun commentaire, explication ou texte autour du JSON**.
    ✅ Réponds uniquement avec un **bloc JSON strictement conforme**, sans aucun mot en dehors.

    ✅ Plusieurs thèmes peuvent être présents dans un même avis.

    ✅ Respecte les nuances entre thèmes proches :

        Service client / SAV : interactions après l’achat avec un conseiller ou service dédié.

        Retour et remboursement : processus de reprise d’un produit ou d’un remboursement.

        Achat en magasin : expérience du client lors de l’achat physique (accueil, conseil).

        Qualité de la communication : clarté, précision, compréhension des infos reçues.

        Prix et promotions : perception du coût, des remises, des réductions ou offres.

Format attendu

Ta réponse doit commencer immédiatement par une accolade ouvrante '{{' et se terminer par une accolade fermante '}}'.
Exemple valide :

{{
  "themes": [
    {{
      "theme": "Qualité des produits",
      "note": 2.5
    }},
    {{
      "theme": "Service client / SAV",
      "note": 1.0
    }}
  ]
}}

Si aucun thème détecté :

{{"themes": []}}

"""