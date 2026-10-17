import json
import os
from pathlib import Path

from pymongo import MongoClient, ReplaceOne


RACINE = Path(__file__).resolve().parent.parent
SOURCE = RACINE / "data" / "processed" / "ai_jobs_prepared.json"


def main():
    with SOURCE.open(encoding="utf-8") as fichier:
        offres = json.load(fichier)

    if not isinstance(offres, list) or not offres:
        raise ValueError("Le fichier doit contenir une liste non vide d'offres.")

    documents = []
    identifiants = set()

    # Valider tous les identifiants avant toute écriture en base.
    for offre in offres:
        identifiant = offre["job_id"]

        if not isinstance(identifiant, str) or not identifiant.strip():
            raise ValueError("Identifiant vide ou invalide.")

        if identifiant in identifiants:
            raise ValueError(f"Identifiant répété : {identifiant}")

        identifiants.add(identifiant)
        documents.append({"_id": identifiant, **offre})

    nom_base = os.environ["MONGO_DATABASE"]

    with MongoClient(
        host=os.environ["MONGO_HOST"],
        port=27017,
        username=os.environ["MONGO_USERNAME"],
        password=os.environ["MONGO_PASSWORD"],
        authSource=nom_base,
        serverSelectionTimeoutMS=10000,
    ) as client:
        client.admin.command("ping")
        collection = client[nom_base]["jobs"]

        operations = [
            ReplaceOne(
                {"_id": document["_id"]},
                document,
                upsert=True,
            )
            for document in documents
        ]

        resultat = collection.bulk_write(operations, ordered=True)

        print(f"Documents préparés : {len(documents)}")
        print(f"Documents insérés : {resultat.upserted_count}")
        print(f"Documents existants trouvés : {resultat.matched_count}")
        print(f"Documents modifiés : {resultat.modified_count}")
        print(f"Total dans la collection : {collection.count_documents({})}")

        # Relire les documents pour vérifier leur contenu réellement stocké.
        documents_stockes = {
            document["_id"]: document
            for document in collection.find(
                {"_id": {"$in": list(identifiants)}}
            )
        }

        for document in documents:
            if documents_stockes.get(document["_id"]) != document:
                raise RuntimeError(
                    f"Vérification échouée : {document['_id']}"
                )

        print(f"Vérification réussie : {len(documents)} documents conformes.")


if __name__ == "__main__":
    main()