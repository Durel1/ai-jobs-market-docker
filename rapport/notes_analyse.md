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

## Contrôles numériques et de cohérence

Les 1 500 offres ont des valeurs convertibles dans les types numériques
attendus. Les indicateurs binaires valent tous 0 ou 1.

Les contrôles détectent :
- 288 salaires annuels hors de la fourchette min–max, soit 19,2 % ;
- 1 099 incompatibilités entre les années d'expérience et les intervalles
  indiqués dans les niveaux déclarés, soit environ 73,3 %.

Ces deux groupes peuvent se recouper.

Aucune anomalie n'a été détectée concernant les salaires non positifs,
l'ordre des bornes salariales, les expériences négatives, les mois,
les années attendues, le score d'avantages ou la cohérence du télétravail
selon la convention retenue.

### Décisions de traitement

Les valeurs originales seront conservées : aucune source ne permet
d'établir quelle colonne est correcte lorsqu'elles se contredisent.

Deux indicateurs booléens seront ajoutés aux données préparées :
- salary_outside_range ;
- experience_mismatch.

Les analyses distingueront le niveau d'expérience déclaré du nombre
d'années demandé. Les limites du dataset seront signalées dans le dashboard.

À ce stade, aucune donnée du CSV original n'a été modifiée.

## Contrôle des textes et des compétences

Aucun espace en début ou fin des champs textuels contrôlés.
Aucune variante de casse ou d'espacement détectée.
Aucun élément vide dans les listes de compétences.

Le dataset contient 93 libellés distincts de compétences.
119 offres contiennent des compétences répétées.

## Préparation reproductible

Commande :
python scripts/preparer_donnees.py

Fichier produit :
data/processed/ai_jobs_prepared.json

Transformations :
- Conversion des champs numériques en entiers ou nombres décimaux.
- Conversion des indicateurs binaires en booléens.
- Transformation de required_skills en liste.
- Suppression des compétences répétées à l'identique dans chaque offre,
  en conservant leur ordre.
- Ajout de salary_outside_range et experience_mismatch.

Résultats :
- 1 500 offres en entrée et en sortie.
- 120 répétitions supprimées dans 119 offres.
- 288 offres signalées pour salaire hors fourchette.
- 1 099 offres signalées pour incohérence d'expérience.
- Aucune offre supprimée.
- Aucune valeur salariale ou d'expérience corrigée.

Le CSV original reste inchangé.
Le JSON généré est exclu de Git et peut être reconstruit avec le script.