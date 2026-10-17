import plotly.graph_objects as go
import streamlit as st

from filtres import ORDRE_EXPERIENCE


def afficher_barres(donnees, titre, mesure, axe, cle):
    st.subheader(titre)

    if not donnees:
        st.info("Aucune donnée disponible pour ce graphique.")
        return

    if mesure == "salaire_moyen":
        survol = (
            "%{y}<br>"
            "Salaire moyen : %{x:,.0f} USD<br>"
            "Nombre d'offres : %{customdata[0]}"
            "<extra></extra>"
        )
    else:
        survol = (
            "%{y}<br>"
            "Nombre d'offres : %{x:,.0f}"
            "<extra></extra>"
        )

    libelles = [ligne["_id"] for ligne in donnees]

    figure = go.Figure(
        go.Bar(
            x=[ligne[mesure] for ligne in donnees],
            y=libelles,
            orientation="h",
            customdata=[
                [ligne["effectif"]]
                for ligne in donnees
            ],
            marker_color="#4C78A8",
            hovertemplate=survol,
        )
    )

    figure.update_layout(
        height=max(280, 32 * len(donnees) + 80),
        margin=dict(l=10, r=20, t=10, b=45),
        xaxis_title=axe,
        yaxis_title=None,
        showlegend=False,
    )

    figure.update_xaxes(rangemode="tozero")
    figure.update_yaxes(
        categoryorder="array",
        categoryarray=libelles,
        autorange="reversed",
        automargin=True,
    )

    st.plotly_chart(
        figure,
        use_container_width=True,
        key=cle,
    )


def afficher_graphiques(resultats):
    st.divider()
    st.header("Analyses graphiques")
    st.caption(
        "Tous les graphiques suivent les filtres actifs. "
        "Survolez les barres pour consulter les valeurs et les effectifs."
    )

    onglet_salaires, onglet_offres = st.tabs(
        ["Salaires", "Télétravail et compétences"]
    )

    with onglet_salaires:
        afficher_barres(
            resultats["metiers"],
            "Les 10 métiers aux salaires moyens les plus élevés",
            "salaire_moyen",
            "Salaire annuel moyen (USD)",
            "salaires_metiers",
        )

        afficher_barres(
            resultats["pays"],
            "Salaire moyen par pays",
            "salaire_moyen",
            "Salaire annuel moyen (USD)",
            "salaires_pays",
        )
        st.caption(
            "La catégorie « Global » est exclue de cette comparaison. "
            "Les écarts ne sont pas ajustés au coût de la vie "
            "ni à la composition des offres."
        )

        rangs = {
            niveau: position
            for position, niveau in enumerate(ORDRE_EXPERIENCE)
        }
        experience = sorted(
            resultats["experience"],
            key=lambda ligne: (
                rangs.get(ligne["_id"], len(rangs)),
                ligne["_id"],
            ),
        )

        afficher_barres(
            experience,
            "Salaire moyen par niveau d'expérience déclaré",
            "salaire_moyen",
            "Salaire annuel moyen (USD)",
            "salaires_experience",
        )
        st.caption(
            "Le niveau déclaré peut être incohérent avec les années "
            "d'expérience demandées."
        )

        st.caption(
            "Les moyennes sont descriptives : les groupes peuvent avoir "
            "des effectifs et des profils différents. "
            "Les offres présentant des incohérences restent incluses."
        )

    with onglet_offres:
        afficher_barres(
            resultats["teletravail"],
            "Répartition des offres par mode de travail",
            "effectif",
            "Nombre d'offres",
            "repartition_teletravail",
        )

        afficher_barres(
            resultats["competences"],
            "Les 15 compétences les plus présentes",
            "effectif",
            "Nombre d'offres mentionnant la compétence",
            "frequence_competences",
        )
        st.caption(
            "Une compétence est comptée au maximum une fois par offre. "
            "Une offre peut mentionner plusieurs compétences : "
            "les effectifs ne doivent donc pas être additionnés "
            "pour retrouver le nombre total d'offres."
        )