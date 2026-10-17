import streamlit as st


FILTRES = [
    ("country", "Pays"),
    ("experience_level", "Niveau d'expérience déclaré"),
    ("industry", "Secteur"),
    ("remote_work", "Mode de travail"),
    ("job_title", "Métier"),
]

ORDRE_EXPERIENCE = [
    "Entry (0-2 yrs)",
    "Mid (3-5 yrs)",
    "Senior (6-9 yrs)",
    "Lead (10+ yrs)",
]


def reinitialiser_filtres():
    for champ, _ in FILTRES:
        st.session_state[f"filtre_{champ}"] = []


def afficher_filtres(options):
    requete = {}

    with st.sidebar:
        st.header("Filtrer les offres")
        st.caption(
            "Une sélection vide conserve toutes les valeurs. "
            "Les filtres se cumulent."
        )

        st.button(
            "Réinitialiser les filtres",
            on_click=reinitialiser_filtres,
        )

        for champ, libelle in FILTRES:
            valeurs = options[champ]

            if champ == "experience_level":
                valeurs = [
                    niveau
                    for niveau in ORDRE_EXPERIENCE
                    if niveau in valeurs
                ] + [
                    niveau
                    for niveau in valeurs
                    if niveau not in ORDRE_EXPERIENCE
                ]

            selection = st.multiselect(
                libelle,
                options=valeurs,
                key=f"filtre_{champ}",
                placeholder="Toutes les valeurs",
            )

            if selection:
                requete[champ] = {"$in": selection}

        st.caption(
            "« Global » désigne une catégorie géographique du dataset, "
            "pas un pays."
        )

    return requete