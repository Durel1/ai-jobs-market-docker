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