import logging
from statistics import mean, median

import streamlit as st
from pymongo.errors import PyMongoError

from db import charger_offres, charger_options_filtres
from filtres import afficher_filtres


LOGGER = logging.getLogger(__name__)

st.set_page_config(
    page_title="AI Jobs Market",
    page_icon="📊",
    layout="wide",
)


def formater_nombre(valeur, decimales=0):
    texte = f"{valeur:,.{decimales}f}"
    return texte.replace(",", " ").replace(".", ",")


def main():
    st.title("Marché de l'emploi en intelligence artificielle")
    st.caption("Analyse du dataset AI Jobs Market 2025–2026")

    st.write(
        "Explorez les rémunérations, les compétences et les caractéristiques "
        "des offres d'emploi en intelligence artificielle."
    )

    st.info(
        "Ce dataset est utilisé dans un cadre pédagogique. "
        "Il ne constitue pas un recensement exhaustif du marché de l'emploi."
    )

    st.button("Actualiser les données")

    try:
        options = charger_options_filtres()
        filtres = afficher_filtres(options)
        offres = charger_offres(filtres)
    except (PyMongoError, KeyError):
        LOGGER.exception("Échec du chargement des offres")
        st.error(
            "Les données sont momentanément indisponibles. "
            "Réessayez avec le bouton d'actualisation."
        )
        st.stop()

    if not offres:
        if filtres:
            st.warning(
                "Aucune offre ne correspond à cette combinaison. "
                "Modifiez ou réinitialisez les filtres."
            )
        else:
            st.warning(
                "Aucune offre disponible. Les données doivent être importées."
            )
        st.stop()

    salaires = [offre["annual_salary_usd"] for offre in offres]
    scores_demande = [offre["demand_score"] for offre in offres]

    st.subheader("Résultats de la sélection")
    st.caption(
        "Les indicateurs et les informations de qualité portent "
        "sur les offres correspondant aux filtres."
    )

    colonne1, colonne2, colonne3, colonne4 = st.columns(4)

    colonne1.metric(
        "Nombre d'offres",
        formater_nombre(len(offres)),
    )
    colonne2.metric(
        "Salaire annuel moyen",
        f"{formater_nombre(mean(salaires))} USD",
    )
    colonne3.metric(
        "Salaire annuel médian",
        f"{formater_nombre(median(salaires))} USD",
    )
    colonne4.metric(
        "Score moyen de demande",
        formater_nombre(mean(scores_demande), 2),
    )

    with st.expander("Qualité et interprétation des données"):
        salaires_signales = sum(
            offre["salary_outside_range"] for offre in offres
        )
        experiences_signalees = sum(
            offre["experience_mismatch"] for offre in offres
        )

        st.write(
            f"**{salaires_signales} offres** présentent un salaire annuel "
            "hors de la fourchette annoncée."
        )
        st.write(
            f"**{experiences_signalees} offres** présentent une incohérence "
            "entre le niveau déclaré et les années d'expérience."
        )
        st.write(
            "Ces offres sont conservées dans les indicateurs. "
            "Les valeurs originales n'ont pas été corrigées."
        )
        st.caption(
            "Les salaires sont exprimés en dollars américains par an. "
            "Le score de demande est celui fourni par le dataset."
        )


if __name__ == "__main__":
    main()