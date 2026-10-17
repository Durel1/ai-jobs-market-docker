# AI Jobs Market 2025–2026

Projet de virtualisation et conteneurisation — 4A.

Application Web d'analyse d'offres d'emploi en intelligence artificielle,
déployée avec Docker Compose.

## Fonctionnalités

- Quatre indicateurs : nombre d'offres, salaires moyen et médian,
  score moyen de demande.
- Cinq filtres : pays, expérience, secteur, mode de travail et métier.
- Cinq graphiques : salaires par métier, pays et expérience,
  répartition du télétravail et compétences fréquentes.
- Comparaison des salaires LLM à pays et niveau déclaré comparables.
- Analyse de sensibilité aux incohérences salariales.
- Gestion des sélections vides et des erreurs de connexion.

## Prérequis

- Docker Desktop démarré en mode conteneurs Linux.
- Docker Compose disponible.
- Connexion Internet pour télécharger les images et les dépendances.
- Port local 8501 disponible.

Python et MongoDB ne sont pas nécessaires sur la machine hôte
pour exécuter le projet.

## Architecture

| Service | Rôle | Fonctionnement |
|---|---|---|
| mongodb | Stockage des offres | Service permanent |
| app | Interface Streamlit | Service permanent |
| import-data | Préparation et import | Conteneur temporaire |

Les services communiquent par le réseau Docker ai_jobs_network.
L'application contacte la base avec le nom de service mongodb.

Le volume mongo_data conserve les données.
Seul le port Web est publié, sur 127.0.0.1:8501.

## Premier lancement

Exécuter les commandes depuis le dossier contenant compose.yaml.

1. Copier .env.example vers .env.
2. Remplacer les trois mots de passe d'exemple dans .env.
3. Valider la configuration :

```bash
docker compose config --quiet
```

4. Démarrer MongoDB :

```bash
docker compose up -d mongodb
```

5. Construire et exécuter l'import :

```bash
docker compose --profile tools run --rm --build import-data
```

L'import attend que MongoDB soit disponible.
Il doit annoncer 1 500 documents présents et conformes.

6. Construire et démarrer l'application :

```bash
docker compose up -d --build app
docker compose ps
```

7. Ouvrir http://localhost:8501.

Les services app et mongodb doivent passer à l'état healthy.

## Valeurs de référence sans filtre

| Indicateur | Valeur |
|---|---:|
| Nombre d'offres | 1 500 |
| Salaire annuel moyen | 194 892 USD |
| Salaire annuel médian | 180 000 USD |
| Score moyen de demande | 87,52 |

## Utilisation des filtres

Une sélection vide conserve toutes les valeurs.
Plusieurs valeurs d'un même filtre sont combinées avec « ou ».
Les différents filtres sont combinés avec « et ».

Le bouton de réinitialisation efface toutes les sélections.

Exemple France + Fully Remote :
26 offres, salaire moyen de 194 938 USD et médian de 175 000 USD.

## Import reproductible

Le conteneur d'import prépare le CSV original, puis charge MongoDB.

Pour réimporter sans modification des sources :

```bash
docker compose --profile tools run --rm import-data
```

Après modification des scripts ou du CSV, ajouter --build.

Les offres sont identifiées par job_id, repris dans _id.
Un réimport identique ne crée aucun doublon et ne modifie aucun document.

L'import ne supprime pas automatiquement les offres absentes du fichier source.
Le JSON intermédiaire est régénéré dans le conteneur temporaire.

## Arrêt et redémarrage

Arrêter et supprimer les conteneurs tout en conservant les données :

```bash
docker compose down
```

Redémarrer après un premier lancement réussi :

```bash
docker compose up -d
```

L'option -v de docker compose down supprime les volumes et leurs données.
Elle ne doit pas être utilisée pour un arrêt normal.

## Configuration et comptes

| Compte par défaut | Rôle | Base d'authentification |
|---|---|---|
| ai_jobs_admin | root | admin |
| ai_jobs_reader | read sur ai_jobs | ai_jobs |
| ai_jobs_importer | readWrite sur ai_jobs | ai_jobs |

Les identifiants sont configurés dans .env.
Ce fichier est exclu de Git et du contexte de construction Docker.

Les comptes sont créés automatiquement sur un volume vide.
Modifier .env ne change pas les mots de passe des comptes déjà créés.

## Diagnostic

État des services :

```bash
docker compose ps
```

Derniers logs :

```bash
docker compose logs --tail 50 app
docker compose logs --tail 50 mongodb
```

Si aucune offre n'est disponible, exécuter l'import.
Si MongoDB est indisponible, vérifier son état et ses logs,
puis actualiser les données dans l'interface.

L'état healthy de Streamlit vérifie le serveur Web.
Il ne garantit pas à lui seul l'accès à MongoDB.

## Données et limites

Le CSV contient 1 500 offres et 25 colonnes.

La préparation :
- convertit les types numériques et booléens ;
- transforme les compétences en listes ;
- retire 120 répétitions de compétences dans 119 offres ;
- signale 288 salaires hors fourchette ;
- signale 1 099 incohérences d'expérience.

Les valeurs originales sont conservées.
Le dataset est un support pédagogique, pas un recensement exhaustif du marché.
Les analyses sont descriptives et ne démontrent pas de causalité.

## Organisation

- app/ : interface, accès aux données, filtres et analyses.
- data/ : CSV original.
- database/ : initialisation MongoDB et import.
- scripts/ : exploration et préparation des données.
- rapport/ : notes, tests, captures et rapport final.

Le modèle est détaillé dans [database/modele.md](database/modele.md).
Les tests sont documentés dans [rapport/tests.md](rapport/tests.md).