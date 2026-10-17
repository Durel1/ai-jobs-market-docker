# AI Jobs Market 2025–2026

Projet de cours de virtualisation et conteneurisation — 4A.

## Objectif

Créer une application Streamlit d’analyse des offres d’emploi en IA,
connectée à une base MongoDB ou MySQL et déployée avec Docker Compose.

## Technologies

- Python
- Streamlit
- MongoDB — stockage des offres et de leurs compétences
- Docker et Docker Compose
- Git

## Avancement

- [x] Vérification de Docker, Docker Compose et Python
- [x] Initialisation du suivi Git
- [ ] Analyse et préparation des données
- [ ] Conception de la base
- [ ] Import des données
- [ ] Développement de l’application
- [ ] Conteneurisation et orchestration
- [ ] Dashboard et analyses
- [ ] Tests et documentation

## Organisation du projet

- data/ : dataset original et éventuelles données nettoyées.
- app/ : application Streamlit et configuration de son image Docker.
- scripts/ : analyse et préparation des données.
- database/ : initialisation et import en base de données.
- rapport/ : notes, preuves de tests et rapport final.

Le CSV original est conservé sans modification afin de garantir
la reproductibilité des traitements.

## Modèle de données

Le choix de MongoDB, la structure des documents et la stratégie
d'import sont décrits dans [database/modele.md](database/modele.md).

## Démarrer MongoDB

Prérequis : Docker Desktop démarré en mode conteneurs Linux,
avec Docker Compose disponible.

1. Copier `.env.example` vers `.env`.
2. Définir un mot de passe local dans `.env`.
3. Valider la configuration :

```bash
docker compose config --quiet
```

4. Démarrer MongoDB et vérifier son état :

```bash
docker compose up -d
docker compose ps
```

Le service mongodb doit passer à l'état healthy.

L'image configurée est mongo:8.0.
Version observée lors du premier test : MongoDB 8.0.34.

Les données sont stockées dans le volume nommé mongo_data,
préfixé par le nom du projet Docker Compose.

Les identifiants d'initialisation sont appliqués uniquement lorsque
le répertoire de données est vide. Modifier `.env` ne change pas
le mot de passe d'un utilisateur déjà créé.

## Arrêter les services

```bash
docker compose down
```

Cette commande conserve le volume de données.
L'option `-v` supprime les volumes et leurs données ; elle n'est pas
utilisée pour un arrêt normal.

## Importer les données

L'import est exécuté dans un conteneur Python temporaire.
Il prépare les données depuis le CSV original, puis les charge dans MongoDB.

Premier lancement ou après modification des scripts :

```bash
docker compose --profile tools run --rm --build import-data
```

Relancer l'import sans modification des sources :

```bash
docker compose --profile tools run --rm import-data
```

Le service attend que MongoDB soit disponible et utilise le compte
ai_jobs_importer.

Chaque offre est identifiée par son job_id, également utilisé comme _id.
Un réimport du même dataset ne crée aucun doublon et ne modifie pas
les documents identiques.

Le script relit les documents importés et compare leur contenu aux
données préparées.

L'import ne supprime pas les documents absents du fichier source.