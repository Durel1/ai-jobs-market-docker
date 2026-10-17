# Suivi des tests

## Validation de Docker Compose

Commande : docker compose config --quiet

Résultat : configuration acceptée sans erreur.

## Disponibilité de MongoDB

Commande : docker compose ps

Résultat : service mongodb démarré, état healthy.
Version observée : MongoDB 8.0.34.

## Authentification du compte de lecture

Connexion avec ai_jobs_reader, authentifié sur ai_jobs.

Résultat : rôle read sur ai_jobs confirmé avec connectionStatus.
Lecture des offres autorisée.

## Import initial

Résultats :
- 1 500 documents préparés.
- 1 500 documents insérés.
- 1 500 documents présents dans la collection.
- Contenu des 1 500 documents relu et vérifié.

## Réimport du même dataset

Résultats après correction de l'ordre du champ _id :
- 0 document inséré.
- 1 500 documents existants trouvés.
- 0 document modifié.
- Total inchangé : 1 500 documents.
- Contenu des 1 500 documents relu et vérifié.

## Point technique rencontré

Le premier code construisait les documents avec _id en dernière position.
Le réimport signalait 1 500 modifications malgré des valeurs identiques.

Placer _id en première position a permis d'obtenir 0 modification
lors du réimport.

## Tests restant à compléter

- Preuve de persistance après recréation du conteneur sans réimport.
- Construction et démarrage de Streamlit.
- Communication Streamlit–MongoDB.
- Fonctionnement des filtres, KPI et graphiques.
- Reconstruction complète selon le README.

## Première page Streamlit

L'image applicative a été construite et la page est accessible
sur http://localhost:8501.

Les données sont récupérées depuis MongoDB avec le compte de lecture.

Valeurs observées :
- Nombre d'offres : 1 500.
- Salaire annuel moyen : 194 892 USD.
- Salaire annuel médian : 180 000 USD.
- Score moyen de demande : 87,52.

Les quatre indicateurs correspondent aux valeurs calculées
indépendamment sur le CSV original.


## Filtres interactifs

Les cinq filtres sont présents :
pays, niveau d'expérience, secteur, mode de travail et métier.

La combinaison France + Fully Remote a été vérifiée :
- 26 offres.
- Salaire annuel moyen : 194 938 USD.
- Salaire annuel médian : 175 000 USD.
- Score moyen de demande : 88,54.

Les résultats correspondent au calcul indépendant sur le CSV original.
Le bouton de réinitialisation efface les sélections et rétablit
les 1 500 offres du dataset.

## Visualisations et agrégations MongoDB

Cinq graphiques sont disponibles :
- Salaires moyens par métier : les 10 premiers.
- Salaires moyens par pays, hors catégorie Global.
- Salaires moyens par niveau d'expérience déclaré.
- Répartition des offres par mode de travail.
- Les 15 compétences les plus présentes.

Les résultats sont calculés dans MongoDB après application des filtres.

Contrôles réalisés :
- France + Fully Remote : 26 offres et une seule catégorie de télétravail.
- Salaire moyen France + Fully Remote : environ 194 938 USD.
- Sans filtre : 686 offres Hybrid, 445 Fully Remote et 369 On-site.
- Sans filtre : Python apparaît dans 942 offres, SQL dans 422 et Cloud dans 402.
- Les infobulles des salaires présentent les moyennes et les effectifs.
