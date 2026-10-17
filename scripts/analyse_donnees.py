import csv
from collections import Counter
from pathlib import Path


# Retrouver le CSV indépendamment du dossier depuis lequel le script est lancé.
RACINE_PROJET = Path(__file__).resolve().parent.parent
CHEMIN_CSV = RACINE_PROJET / "data" / "ai_jobs_market_2025_2026.csv"


def main():
    if not CHEMIN_CSV.is_file():
        raise FileNotFoundError(f"CSV introuvable : {CHEMIN_CSV}")

    # utf-8-sig accepte aussi les fichiers UTF-8 avec marqueur BOM.
    with CHEMIN_CSV.open(encoding="utf-8-sig", newline="") as fichier:
        lecteur = csv.DictReader(fichier)
        colonnes = lecteur.fieldnames
        lignes = list(lecteur)

    if not colonnes or not lignes:
        raise ValueError("Le CSV est vide ou ne contient pas de données.")

    print("=== DIMENSIONS ===")
    print(f"Nombre de lignes : {len(lignes)}")
    print(f"Nombre de colonnes : {len(colonnes)}")

    print("\n=== COLONNES ===")
    for colonne in colonnes:
        print(f"- {colonne}")

    print("\n=== VALEURS MANQUANTES ===")
    for colonne in colonnes:
        nombre = sum(
            ligne[colonne] is None or ligne[colonne].strip() == ""
            for ligne in lignes
        )
        print(f"{colonne} : {nombre}")

    print("\n=== DOUBLONS ===")
    identifiants = Counter(ligne["job_id"] for ligne in lignes)
    ids_repetes = {
        identifiant: nombre
        for identifiant, nombre in identifiants.items()
        if nombre > 1
    }

    lignes_uniques = {
        tuple(ligne[colonne] for colonne in colonnes)
        for ligne in lignes
    }

    print(f"Lignes entièrement dupliquées : {len(lignes) - len(lignes_uniques)}")
    print(f"Identifiants répétés : {len(ids_repetes)}")
    if ids_repetes:
        print(ids_repetes)

    print("\n=== RÉPARTITION DES CATÉGORIES ===")
    for colonne in [
        "experience_level",
        "remote_work",
        "country",
        "posting_year",
    ]:
        print(f"\n{colonne} :")
        occurrences = Counter(ligne[colonne] for ligne in lignes)
        for valeur, nombre in sorted(occurrences.items()):
            print(f"  {valeur} : {nombre}")

    print("\n=== EXEMPLE DE COMPÉTENCES ===")
    valeur_originale = lignes[0]["required_skills"]
    competences = [
        competence.strip()
        for competence in valeur_originale.split("|")
        if competence.strip()
    ]
    print(f"Valeur originale : {valeur_originale}")
    print(f"Liste obtenue : {competences}")


if __name__ == "__main__":
    main()