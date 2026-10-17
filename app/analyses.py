from collections import defaultdict
from statistics import mean

import streamlit as st


def formater(valeur, decimales=0):
    texte = f"{valeur:,.{decimales}f}"
    return texte.replace(",", " ").replace(".", ",")


def comparer_profils(offres):
    groupes = defaultdict(lambda: {True: [], False: []})

    for offre in offres:
        # Global ne correspond pas à un pays.
        if offre["country"] == "Global":
            continue

        profil = (
            offre["country"],
            offre["experience_level"],
        )

        groupes[profil][offre["is_llm_role"]].append(
            offre["annual_salary_usd"]
        )

    resultats = []

    for (pays, niveau), salaires in sorted(groupes.items()):
        llm = salaires[True]
        autres = salaires[False]

        # Seuil pédagogique pour éviter les groupes les plus petits.
        if len(llm) < 5 or len(autres) < 5:
            continue

        resultats.append({
            "pays": pays,
            "niveau": niveau,
            "n_llm": len(llm),
            "n_autres": len(autres),
            "moyenne_llm": mean(llm),
            "moyenne_autres": mean(autres),
            "poids": len(llm) + len(autres),
        })

    return resultats


def afficher_comparaison_llm(offres):
    st.subheader("1. Comparer les salaires LLM à profils comparables")

    st.write(
        "**Question :** dans un même pays et pour un même niveau "
        "d'expérience déclaré, les rôles LLM présentent-ils "
        "des salaires moyens différents des autres rôles ?"
    )

    profils = comparer_profils(offres)

    if not profils:
        st.info(
            "Cette sélection ne contient aucun groupe pays–expérience "
            "avec au moins 5 offres LLM et 5 autres offres. "
            "Élargissez les filtres pour effectuer la comparaison."
        )
        return

    total = sum(profil["poids"] for profil in profils)

    # Les deux moyennes utilisent exactement les mêmes poids.
    moyenne_llm = sum(
        profil["poids"] * profil["moyenne_llm"]
        for profil in profils
    ) / total

    moyenne_autres = sum(
        profil["poids"] * profil["moyenne_autres"]
        for profil in profils
    ) / total

    ecart = moyenne_llm - moyenne_autres
    ecart_pct = 100 * ecart / moyenne_autres

    gauche, droite = st.columns(2)

    gauche.metric(
        "Salaire LLM moyen standardisé",
        f"{formater(moyenne_llm)} USD",
    )
    droite.metric(
        "Salaire des autres rôles standardisé",
        f"{formater(moyenne_autres)} USD",
    )

    st.write(
        f"**Écart LLM − autres : {formater(ecart)} USD**, "
        f"soit **{formater(ecart_pct, 2)} %** "
        "de la moyenne standardisée des autres rôles."
    )

    st.caption(
        f"Comparaison sur {len(profils)} groupes et {total} offres. "
        "Chaque groupe contient au moins 5 offres de chaque catégorie. "
        "Les deux moyennes sont pondérées par le même effectif total "
        "de chaque groupe pays–expérience."
    )

    st.write(
        "Cette comparaison réduit les différences de composition par pays "
        "et niveau déclaré. Elle ne tient pas compte de toutes les autres "
        "caractéristiques, comme le secteur ou la taille de l'entreprise. "
        "Elle ne démontre ni un effet causal ni une différence "
        "statistiquement significative."
    )

    st.caption(
        "La catégorie Global est exclue. Les incohérences entre niveau "
        "déclaré et années d'expérience limitent aussi l'interprétation."
    )

    with st.expander("Voir les groupes retenus"):
        st.dataframe(
            [
                {
                    "Pays": profil["pays"],
                    "Niveau déclaré": profil["niveau"],
                    "Offres LLM": profil["n_llm"],
                    "Autres offres": profil["n_autres"],
                    "Salaire moyen LLM (USD)": round(
                        profil["moyenne_llm"], 2
                    ),
                    "Salaire moyen autres (USD)": round(
                        profil["moyenne_autres"], 2
                    ),
                }
                for profil in profils
            ],
            hide_index=True,
        )


def afficher_sensibilite_salaires(offres):
    st.subheader("2. Sensibilité du salaire moyen aux offres signalées")

    st.write(
        "**Question :** comment le salaire moyen change-t-il lorsque "
        "les offres dont le salaire est hors de la fourchette annoncée "
        "sont exclues du calcul ?"
    )

    retenues = [
        offre for offre in offres
        if not offre["salary_outside_range"]
    ]

    if not retenues:
        st.info(
            "Toutes les offres sélectionnées ont un salaire hors "
            "fourchette : aucune moyenne restreinte ne peut être calculée."
        )
        return

    moyenne_complete = mean(
        offre["annual_salary_usd"] for offre in offres
    )
    moyenne_restreinte = mean(
        offre["annual_salary_usd"] for offre in retenues
    )

    variation = moyenne_restreinte - moyenne_complete
    variation_pct = 100 * variation / moyenne_complete

    gauche, droite = st.columns(2)

    gauche.metric(
        "Toutes les offres sélectionnées",
        f"{formater(moyenne_complete)} USD",
    )
    droite.metric(
        "Offres avec salaire dans la fourchette",
        f"{formater(moyenne_restreinte)} USD",
    )

    st.write(
        f"**Variation après exclusion : {formater(variation)} USD**, "
        f"soit **{formater(variation_pct, 2)} %** "
        "de la moyenne initiale."
    )

    exclues = len(offres) - len(retenues)
    st.caption(
        f"{len(retenues)} offres retenues sur {len(offres)} ; "
        f"{exclues} offres exclues pour cette comparaison uniquement."
    )

    st.write(
        "Cette variation mesure la sensibilité du résultat à une règle "
        "d'exclusion. Elle ne prouve pas que la moyenne restreinte "
        "représente mieux le marché : les offres exclues peuvent avoir "
        "des profils différents et nous ignorons quel champ salarial "
        "est incorrect."
    )

    st.caption(
        "Ce contrôle porte uniquement sur la cohérence salariale. "
        "Les incohérences d'expérience ne sont pas exclues. "
        "Les KPI et graphiques principaux restent inchangés."
    )


def afficher_analyses(offres):
    st.divider()
    st.header("Analyses complémentaires")
    st.caption("Ces deux analyses suivent les filtres actifs.")

    afficher_comparaison_llm(offres)
    st.divider()
    afficher_sensibilite_salaires(offres)