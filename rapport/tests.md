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

## État de la validation finale

Les contrôles de construction, démarrage, lecture MongoDB, filtres,
réimport et reconstruction sont documentés ci-dessous.
La persistance a aussi été confirmée par la reprise des 1 500 offres
après arrêt puis redémarrage de MongoDB, sans réimport.

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


## Analyses complémentaires

### Comparaison LLM à pays et niveau déclaré comparables

Sans filtre :
- 22 groupes retenus, représentant 881 offres.
- Chaque groupe contient au moins 5 offres de chaque catégorie.
- Salaire LLM moyen standardisé : 217 766 USD.
- Salaire des autres rôles standardisé : 202 010 USD.
- Écart : environ 15 757 USD, soit 7,80 %.

Les deux moyennes utilisent les mêmes poids par groupe.
La comparaison est descriptive et ne démontre pas un effet causal.

### Sensibilité aux incohérences salariales

Sans filtre :
- Moyenne sur les 1 500 offres : 194 892 USD.
- Moyenne sur les 1 212 offres dont le salaire est dans la fourchette :
  environ 172 368 USD.
- Variation : environ -22 524 USD, soit -11,56 %.

L'exclusion concerne uniquement cette comparaison.
Elle ne garantit pas une meilleure représentation du marché.
Les données originales et les indicateurs principaux restent inchangés.

Les résultats affichés correspondent aux calculs indépendants
effectués depuis le CSV original.


## Cas limites et reprise après indisponibilité

### Sélection sans résultat

Filtres : France, Lead (10+ yrs), AI Agent Developer.

Résultat : message d'absence de résultat, sans anciens KPI ni graphiques.
La réinitialisation rétablit les 1 500 offres.

### Données insuffisantes pour la comparaison LLM

Filtres : France et Fully Remote.

Résultat : 26 offres affichées. La comparaison LLM indique qu'aucun
groupe ne satisfait le seuil de cinq offres par catégorie.
Les autres résultats restent accessibles.

### Indisponibilité de MongoDB

Après docker compose stop mongodb et actualisation de la page,
l'application affiche un message d'indisponibilité des données.

### Reprise

Après docker compose start mongodb et actualisation de la page,
les 1 500 offres et les indicateurs réapparaissent sans réimport
ni reconstruction d'image.

## Reconstruction dans un environnement isolé

Projet Compose utilisé : ai-jobs-validation.

Procédure :
1. Arrêt de l'application habituelle pour libérer le port 8501.
2. Construction des deux images avec --no-cache.
3. Démarrage de MongoDB avec un nouveau volume.
4. Exécution de l'import.
5. Démarrage de Streamlit.

Résultats observés :
- Nouveau réseau et nouveau volume créés.
- Initialisation automatique permettant l'accès au compte d'import.
- 1 500 documents insérés et vérifiés.
- MongoDB et Streamlit en état healthy.

Les conteneurs de validation ont ensuite été supprimés sans suppression
du volume, puis l'application habituelle a été redémarrée.

Ce test utilise une installation Docker existante et des ressources
Compose isolées ; il ne simule pas une réinstallation de Docker.