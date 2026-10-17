# Analyse et préparation des données

## Première exploration

Le fichier original contient 1 500 offres et 25 colonnes.
Le script scripts/analyse_donnees.py permet de reproduire les contrôles.

### Résultats

- Aucune cellule vide ou composée uniquement d'espaces.
- Aucune ligne entièrement dupliquée.
- Aucun identifiant job_id répété.
- 624 offres pour 2025 et 876 pour 2026.
- Les compétences sont séparées par le caractère |.
- La catégorie Global doit être distinguée des pays.
- Les États-Unis représentent 515 offres, soit environ 34,3 % du dataset.

### Décisions à ce stade

Aucune ligne supprimée et aucune valeur remplacée.
Le CSV original reste inchangé.

### Contrôles restant à réaliser

- Validité des types numériques et des indicateurs binaires.
- Cohérence des salaires et de leurs bornes.
- Validité des mois et des années.
- Cohérence entre niveau et années d'expérience.
- Cohérence des indicateurs de télétravail.
- Espaces superflus et variantes de compétences.