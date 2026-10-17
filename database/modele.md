# Modèle de données — MongoDB

## 1. Choix de la technologie

MongoDB est retenu pour stocker les offres d'emploi.

Avantages pour ce projet :
- Les compétences peuvent être stockées directement dans un tableau.
- Chaque offre regroupe les informations nécessaires au dashboard dans
  un document, sans table de liaison pour les compétences.

Limite :
Les libellés des compétences sont répétés entre les documents.
Une modification globale demanderait de mettre à jour plusieurs offres.
La préparation des données garantit leur cohérence avant l'import.

## 2. Organisation

- Base de données : ai_jobs
- Collection : jobs
- Un document représente une offre.
- Le dataset initial contient 1 500 offres.
- Aucune collection séparée n'est prévue pour les compétences.

## 3. Identifiants

Le champ _id reprend la valeur de job_id.

Exemple :
- _id : "AIJOB0001"
- job_id : "AIJOB0001"

Le champ job_id est conservé pour faciliter le rapprochement avec le CSV.
L'identifiant _id permet d'éviter plusieurs documents pour la même offre.

## 4. Types des champs

| Type logique | Champs |
|---|---|
| Texte | _id, job_id, job_title, job_category, experience_level, education_required, city, country, remote_work, company_size, industry, salary_tier |
| Entier | years_of_experience, posting_year, posting_month |
| Nombre décimal | annual_salary_usd, salary_min_usd, salary_max_usd, ai_salary_premium_pct, demand_score, demand_growth_yoy_pct, benefits_score_10 |
| Booléen | is_senior, is_remote_friendly, is_llm_role, salary_outside_range, experience_mismatch |
| Tableau de textes | required_skills |

Les nombres décimaux Python seront stockés comme nombres BSON double.
Les salaires servent à des analyses statistiques, pas à des opérations
comptables exigeant une représentation décimale exacte.

Le document contient 28 champs : les 27 champs préparés et _id.

## 5. Compétences

required_skills contient une liste sans répétitions, par exemple :

["Python", "SQL", "Cloud"]

La relation entre une offre et ses compétences est intégrée au document.
Une même compétence peut apparaître dans plusieurs offres.

## 6. Qualité des données

Les valeurs originales de salaire et d'expérience sont conservées.

Deux indicateurs signalent les incohérences :
- salary_outside_range : salaire annuel hors de la fourchette min–max.
- experience_mismatch : années incompatibles avec le niveau déclaré.

La catégorie géographique Global est conservée et distinguée des pays
dans les analyses géographiques.

## 7. Stratégie d'import reproductible

1. Lire le CSV avec le script de préparation.
2. Générer data/processed/ai_jobs_prepared.json.
3. Lire le JSON avec le script d'import.
4. Affecter job_id au champ _id.
5. Insérer ou remplacer chaque document selon son _id.
6. Vérifier le nombre de documents et quelques offres importées.

Un nouvel import du même fichier ne doit pas créer de doublons.
L'import sera exécuté explicitement, et non à chaque interaction
avec le dashboard.

Cette stratégie ne supprime pas automatiquement les documents absents
d'une nouvelle version du dataset. Le remplacement complet d'un dataset
nécessitera une procédure distincte et documentée.

## 8. Requêtes prévues

| Besoin | Traitement prévu |
|---|---|
| Filtres du dashboard | Sélection par pays, expérience, secteur, mode de travail et métier |
| Nombre d'offres | Comptage après filtrage |
| Salaires moyen et médian | Calcul sur les offres filtrées |
| Demande moyenne | Moyenne de demand_score après filtrage |
| Salaires par métier | Regroupement par job_title |
| Salaires par pays | Regroupement par country, en distinguant Global |
| Télétravail | Comptage par remote_work |
| Compétences fréquentes | Décomposition du tableau required_skills et comptage |
| Comparaison LLM | Regroupement selon is_llm_role |
| Qualité | Comptage selon les deux indicateurs d'incohérence |

Les agrégations adaptées seront réalisées dans MongoDB.
La médiane pourra être calculée en Python sur les salaires filtrés.

## 9. Index

L'index unique sur _id est fourni par MongoDB.

Avec seulement 1 500 documents, aucun index secondaire n'est ajouté
sans justification. Leur intérêt sera évalué selon les requêtes utilisées.

## 10. Accès aux données

Le dashboard interrogera MongoDB.
Le CSV et le JSON intermédiaire serviront à la préparation et à l'import,
pas de source principale au dashboard opérationnel.

## 11. Comptes et droits d'accès

| Compte | Base d'authentification | Rôle | Utilisation |
|---|---|---|---|
| ai_jobs_admin | admin | root | Administration |
| ai_jobs_reader | ai_jobs | read | Dashboard Streamlit |
| ai_jobs_importer | ai_jobs | readWrite | Import des offres |

Les mots de passe sont définis dans .env, exclu de Git.
.env.example contient uniquement des valeurs d'exemple.

Le script database/scripts_initialisation/01-create-users.js crée
les comptes absents et laisse les comptes existants inchangés.

Sur un volume vide, il est exécuté automatiquement par l'image MongoDB.
Sur un volume déjà initialisé, il peut être lancé explicitement avec
mongosh après authentification administrateur.

Modifier .env ne modifie pas les mots de passe des comptes existants.