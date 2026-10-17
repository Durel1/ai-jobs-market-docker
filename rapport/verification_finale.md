# Vérification finale - 17 octobre 2026

## Périmètre

La revue porte sur les fichiers remis dans ai-jobs-market-sources.zip,
exportés depuis le commit de333b32601a1e77dedc5534a407c417c7e3878d.
Les sources applicatives et la configuration Docker n'ont pas été modifiées.

## Contrôles locaux exécutés

- Syntaxe de tous les fichiers Python : valide.
- Structure YAML : trois services, réseau partagé et volume nommé.
- Chemins des deux Dockerfiles : présents.
- Port MongoDB non publié ; Streamlit limité à 127.0.0.1:8501.
- Aucun fichier .env réel dans l'archive.
- Préparation déterministe sur deux exécutions de la fonction de transformation.
- 1 500 identifiants uniques ; 120 répétitions de compétences retirées dans 119 offres.
- 288 indicateurs salariaux et 1 099 indicateurs d'expérience.
- Valeurs salariales et années d'expérience préservées.
- Moyenne : 194 892 USD ; médiane : 180 000 USD.
- Comparaison LLM : 22 groupes et 881 offres.

## Portée des tests Docker

Les tests Docker sont étayés par les logs et captures transmis pendant
la réalisation sous Windows. Aucun moteur Docker n'est disponible dans
l'environnement de revue : ils n'y ont pas été réexécutés.

## Finalisation des livrables

- Rapport PDF de 20 pages et source Markdown ajoutés.
- Captures existantes organisées avec des noms descriptifs ; captures de
  session ajoutées pour les KPI sans filtre et les résultats complets.
- Ancienne liste de tests restant à compléter remplacée par l'état final.
- Fichier app/.gitkeep devenu inutile supprimé.
- Liens vers le rapport ajoutés au README.

Le ZIP contient les sources et les preuves, sans .git, .env ni cache.
Le dépôt Git local reste la référence pour l'historique des commits.
