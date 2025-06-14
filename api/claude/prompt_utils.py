from .themes import THEMES, THEME_LABELS


def build_prompt(verbatim: str) -> str:
    theme_list = "\n".join([f'- {t["nom"]} : {t["description"]}' for t in THEMES])

    return f"""
Tu es un expert en analyse de la satisfaction client pour une enseigne spécialisée dans la rénovation de l’habitat (bricolage, aménagement, matériaux, outillage).

Voici un avis client à analyser :
\"{verbatim}\"

Ta mission est de détecter les **thèmes abordés** parmi ceux listés ci-dessous, et d’attribuer à chacun une **note de satisfaction** sur 5 (décimale possible).

AAvant toute analyse, demande-toi si l’avis concerne une expérience client **dans un contexte lié à la rénovation de l’habitat** (achat, projet, problème, service...).  
Même si l’enseigne n’est pas explicitement citée, considère l’avis comme pertinent s’il évoque **des produits, services ou situations** compatibles avec ce secteur (ex : pergola, livraison de matériel, outillage, chantier...).  
 
Si oui, demande-toi ensuite s’il traite **au moins un des thèmes** de la liste ci-dessous.

S’il ne traite d’aucun sujet lié à la rénovation de l’habitat ou aucun thème listé, retourne simplement :

{{ "themes": [] }}

---

**Liste des thèmes disponibles** :
{theme_list}

---

**Consignes importantes** :

- N’invente jamais de thèmes. Utilise uniquement ceux présents dans la liste ci-dessus.
- Plusieurs thèmes peuvent être présents dans un même avis.
- Tu dois faire la distinction entre certains thèmes proches :
  - **Service client / SAV** désigne toute interaction avec le service après-vente en point de vente physique, par téléphone ou via un formulaire en ligne pour réclamation, demande d'information, suivi, résolution de problème.
  - **Retour et remboursement** concerne uniquement le **traitement matériel ou financier** d'un retour, échange ou remboursement.
  - **Achat en magasin** concerne le **parcours d’achat en point de vente physique** : accueil, conseil, expertise vendeur.
  - **Qualité de la communication** = clarté et qualité des messages transmis (conditions de vente, emails, informations affichées ou transmises au client).
  - **Prix et promotions** = perception des prix et des réductions, ressenti de la transparence commerciale.

- Tu dois attribuer une note sur 5 (1 = très insatisfait, 5 = très satisfait), décimale possible (ex : 2.5, 4.0).

---

Réponds uniquement avec un JSON **valide** au format suivant :

```json
{{
  "themes": [
    {{
      "theme": "nom exact du thème 1",
      "note": 3.5
    }},
    {{
      "theme": "nom exact du thème 2",
      "note": 1.0
    }}
  ]
}}
```"""