import csv
from collections import Counter
from pathlib import Path
import math


# Retrouver le CSV indépendamment du dossier depuis lequel le script est lancé.
RACINE_PROJET = Path(__file__).resolve().parent.parent
CHEMIN_CSV = RACINE_PROJET / "data" / "ai_jobs_market_2025_2026.csv"


def verifier_coherence(lignes):
    # Type attendu pour chaque colonne numérique.
    types_numeriques = {
        "years_of_experience": int,
        "annual_salary_usd": float,
        "salary_min_usd": float,
        "salary_max_usd": float,
        "ai_salary_premium_pct": float,
        "demand_score": float,
        "demand_growth_yoy_pct": float,
        "benefits_score_10": float,
        "posting_year": int,
        "posting_month": int,
        "is_senior": int,
        "is_remote_friendly": int,
        "is_llm_role": int,
    }

    donnees_converties = []
    erreurs_types = []

    for ligne in lignes:
        offre = dict(ligne)
        ligne_valide = True

        for colonne, conversion in types_numeriques.items():
            try:
                valeur = conversion(ligne[colonne])

                if not math.isfinite(valeur):
                    raise ValueError("Valeur non finie")

                offre[colonne] = valeur

            except (ValueError, TypeError, OverflowError):
                erreurs_types.append(
                    (ligne["job_id"], colonne, ligne[colonne])
                )
                ligne_valide = False

        if ligne_valide:
            donnees_converties.append(offre)

    print("\n=== TYPES NUMÉRIQUES ===")
    print(f"Cellules numériques invalides : {len(erreurs_types)}")
    for erreur in erreurs_types[:5]:
        print(f"  Identifiant, colonne, valeur : {erreur}")

    # Une ligne avec erreur de type est exclue uniquement des contrôles
    # numériques suivants. Elle reste présente dans le CSV original.
    print(
        "Offres utilisables pour les contrôles numériques : "
        f"{len(donnees_converties)} / {len(lignes)}"
    )

    print("\n=== ÉTENDUE DES VALEURS NUMÉRIQUES ===")
    if not donnees_converties:
        print("Aucune offre utilisable.")
        return

    for colonne in types_numeriques:
        valeurs = [offre[colonne] for offre in donnees_converties]
        print(f"{colonne} : min={min(valeurs)}, max={max(valeurs)}")

    niveaux_experience = {
        "Entry (0-2 yrs)": (0, 2),
        "Mid (3-5 yrs)": (3, 5),
        "Senior (6-9 yrs)": (6, 9),
        "Lead (10+ yrs)": (10, math.inf),
    }

    anomalies = {
        "Salaire ou borne de salaire non positif": [],
        "Salaire minimum supérieur au maximum": [],
        "Salaire annuel hors de la fourchette": [],
        "Années d'expérience négatives": [],
        "Niveau d'expérience inconnu": [],
        "Années incompatibles avec le niveau affiché": [],
        "Mois hors de 1 à 12": [],
        "Année hors de 2025 et 2026": [],
        "Score d'avantages hors de 0 à 10": [],
        "Indicateur binaire différent de 0 ou 1": [],
        "Mode de travail inconnu": [],
        "Indicateur de télétravail incohérent": [],
    }

    for offre in donnees_converties:
        identifiant = offre["job_id"]

        def signaler(libelle, condition):
            if condition:
                anomalies[libelle].append(identifiant)

        salaire = offre["annual_salary_usd"]
        minimum = offre["salary_min_usd"]
        maximum = offre["salary_max_usd"]

        signaler(
            "Salaire ou borne de salaire non positif",
            min(salaire, minimum, maximum) <= 0,
        )
        signaler(
            "Salaire minimum supérieur au maximum",
            minimum > maximum,
        )
        signaler(
            "Salaire annuel hors de la fourchette",
            not minimum <= salaire <= maximum,
        )

        experience = offre["years_of_experience"]
        niveau = offre["experience_level"]
        signaler("Années d'expérience négatives", experience < 0)
        signaler(
            "Niveau d'expérience inconnu",
            niveau not in niveaux_experience,
        )

        if niveau in niveaux_experience:
            borne_min, borne_max = niveaux_experience[niveau]
            signaler(
                "Années incompatibles avec le niveau affiché",
                not borne_min <= experience <= borne_max,
            )

        signaler("Mois hors de 1 à 12", not 1 <= offre["posting_month"] <= 12)
        signaler(
            "Année hors de 2025 et 2026",
            offre["posting_year"] not in (2025, 2026),
        )
        signaler(
            "Score d'avantages hors de 0 à 10",
            not 0 <= offre["benefits_score_10"] <= 10,
        )
        signaler(
            "Indicateur binaire différent de 0 ou 1",
            any(
                offre[colonne] not in (0, 1)
                for colonne in [
                    "is_senior", "is_remote_friendly", "is_llm_role"
                ]
            ),
        )

        mode = offre["remote_work"]
        modes_attendus = {"On-site": 0, "Hybrid": 1, "Fully Remote": 1}
        signaler("Mode de travail inconnu", mode not in modes_attendus)

        if mode in modes_attendus:
            signaler(
                "Indicateur de télétravail incohérent",
                offre["is_remote_friendly"] != modes_attendus[mode],
            )

    print("\n=== CONTRÔLES DE COHÉRENCE ===")
    for libelle, identifiants in anomalies.items():
        print(f"{libelle} : {len(identifiants)}")
        if identifiants:
            print(f"  Exemples : {', '.join(identifiants[:5])}")

def verifier_textes_et_competences(lignes):
    colonnes_texte = [
        "job_id",
        "job_title",
        "job_category",
        "experience_level",
        "education_required",
        "city",
        "country",
        "remote_work",
        "company_size",
        "industry",
        "salary_tier",
    ]

    print("\n=== ESPACES EN DÉBUT OU FIN DE TEXTE ===")
    for colonne in colonnes_texte:
        identifiants = [
            ligne["job_id"]
            for ligne in lignes
            if ligne[colonne] != ligne[colonne].strip()
        ]
        print(f"{colonne} : {len(identifiants)}")

    print("\n=== VARIANTES DE CASSE OU D'ESPACEMENT ===")
    for colonne in colonnes_texte:
        variantes = {}

        for ligne in lignes:
            valeur = ligne[colonne]
            # Clé de comparaison uniquement : aucune donnée modifiée.
            cle = " ".join(valeur.split()).casefold()
            variantes.setdefault(cle, set()).add(valeur)

        groupes = [
            sorted(valeurs)
            for valeurs in variantes.values()
            if len(valeurs) > 1
        ]

        print(f"{colonne} : {len(groupes)} groupe(s)")
        for groupe in groupes[:5]:
            print(f"  {groupe}")

    print("\n=== FORMAT DES COMPÉTENCES ===")
    offres_avec_element_vide = []
    offres_avec_espaces = []
    offres_avec_doublons = []
    variantes_competences = {}
    frequences = Counter()
    nombres_competences = []

    for ligne in lignes:
        elements = ligne["required_skills"].split("|")
        competences = [
            element.strip()
            for element in elements
            if element.strip()
        ]

        if any(not element.strip() for element in elements):
            offres_avec_element_vide.append(ligne["job_id"])

        if any(element != element.strip() for element in elements):
            offres_avec_espaces.append(ligne["job_id"])

        cles = [
            " ".join(competence.split()).casefold()
            for competence in competences
        ]

        if len(cles) != len(set(cles)):
            offres_avec_doublons.append(ligne["job_id"])

        for competence, cle in zip(competences, cles):
            variantes_competences.setdefault(cle, set()).add(competence)

        # Une compétence compte au maximum une fois par offre.
        frequences.update(set(competences))
        nombres_competences.append(len(competences))

    print(f"Offres avec élément vide : {len(offres_avec_element_vide)}")
    print(f"Offres avec espaces superflus : {len(offres_avec_espaces)}")
    print(f"Offres avec compétences répétées : {len(offres_avec_doublons)}")
    print(f"Nombre de libellés distincts après strip : {len(frequences)}")
    print(
        "Nombre de compétences par offre : "
        f"min={min(nombres_competences)}, "
        f"max={max(nombres_competences)}"
    )

    print("\nVariantes de compétences à examiner :")
    groupes = [
        sorted(valeurs)
        for valeurs in variantes_competences.values()
        if len(valeurs) > 1
    ]
    if not groupes:
        print("  Aucune variante de casse ou d'espacement détectée.")
    else:
        for groupe in groupes:
            print(f"  {groupe}")

    print("\nLes 15 compétences les plus présentes :")
    classement = sorted(
        frequences.items(),
        key=lambda element: (-element[1], element[0]),
    )
    for competence, nombre in classement[:15]:
        print(f"  {competence} : {nombre} offres")


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
    verifier_coherence(lignes)
    verifier_textes_et_competences(lignes)


if __name__ == "__main__":
    main()