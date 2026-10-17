import csv
import json
import math
from pathlib import Path


RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "data" / "ai_jobs_market_2025_2026.csv"
DESTINATION = RACINE / "data" / "processed" / "ai_jobs_prepared.json"

COLONNES_ENTIERES = [
    "years_of_experience",
    "posting_year",
    "posting_month",
]

COLONNES_DECIMALES = [
    "annual_salary_usd",
    "salary_min_usd",
    "salary_max_usd",
    "ai_salary_premium_pct",
    "demand_score",
    "demand_growth_yoy_pct",
    "benefits_score_10",
]

COLONNES_BOOLEENNES = [
    "is_senior",
    "is_remote_friendly",
    "is_llm_role",
]

NIVEAUX_EXPERIENCE = {
    "Entry (0-2 yrs)": (0, 2),
    "Mid (3-5 yrs)": (3, 5),
    "Senior (6-9 yrs)": (6, 9),
    "Lead (10+ yrs)": (10, math.inf),
}


def preparer_offre(ligne):
    offre = {
        colonne: valeur.strip()
        for colonne, valeur in ligne.items()
    }

    for colonne in COLONNES_ENTIERES:
        offre[colonne] = int(offre[colonne])

    for colonne in COLONNES_DECIMALES:
        valeur = float(offre[colonne])
        if not math.isfinite(valeur):
            raise ValueError(f"Valeur non finie : {colonne}")
        offre[colonne] = valeur

    for colonne in COLONNES_BOOLEENNES:
        valeur = int(offre[colonne])
        if valeur not in (0, 1):
            raise ValueError(f"Indicateur binaire invalide : {colonne}")
        offre[colonne] = bool(valeur)

    competences = [
        element.strip()
        for element in offre["required_skills"].split("|")
        if element.strip()
    ]

    # Retirer les répétitions exactes en conservant l'ordre initial.
    offre["required_skills"] = list(dict.fromkeys(competences))
    repetitions_supprimees = (
        len(competences) - len(offre["required_skills"])
    )

    offre["salary_outside_range"] = not (
        offre["salary_min_usd"]
        <= offre["annual_salary_usd"]
        <= offre["salary_max_usd"]
    )

    niveau = offre["experience_level"]
    if niveau not in NIVEAUX_EXPERIENCE:
        raise ValueError(f"Niveau d'expérience inconnu : {niveau}")

    minimum, maximum = NIVEAUX_EXPERIENCE[niveau]
    offre["experience_mismatch"] = not (
        minimum <= offre["years_of_experience"] <= maximum
    )

    return offre, repetitions_supprimees


def main():
    with SOURCE.open(encoding="utf-8-sig", newline="") as fichier:
        lignes = list(csv.DictReader(fichier))

    if not lignes:
        raise ValueError("Le CSV ne contient aucune offre.")

    offres = []
    identifiants = set()
    offres_dedoublonnees = 0
    total_repetitions = 0

    for ligne in lignes:
        try:
            offre, repetitions = preparer_offre(ligne)
        except (ValueError, TypeError, AttributeError) as erreur:
            raise ValueError(
                f"Offre {ligne.get('job_id', '?')} : {erreur}"
            ) from erreur

        identifiant = offre["job_id"]
        if not identifiant or identifiant in identifiants:
            raise ValueError(
                f"Identifiant vide ou dupliqué : {identifiant!r}"
            )

        identifiants.add(identifiant)
        offres.append(offre)
        offres_dedoublonnees += int(repetitions > 0)
        total_repetitions += repetitions

    # Préparer tout le contenu avant d'écrire le résultat.
    contenu = json.dumps(
        offres,
        ensure_ascii=False,
        indent=2,
        allow_nan=False,
    )

    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(contenu + "\n", encoding="utf-8")

    print(f"Offres lues : {len(lignes)}")
    print(f"Offres préparées : {len(offres)}")
    print(f"Offres avec compétences dédoublonnées : {offres_dedoublonnees}")
    print(f"Total des répétitions supprimées : {total_repetitions}")
    print(
        "Salaires hors fourchette : "
        f"{sum(offre['salary_outside_range'] for offre in offres)}"
    )
    print(
        "Incohérences d'expérience : "
        f"{sum(offre['experience_mismatch'] for offre in offres)}"
    )
    print(f"Fichier créé : {DESTINATION}")


if __name__ == "__main__":
    main()