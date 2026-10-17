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