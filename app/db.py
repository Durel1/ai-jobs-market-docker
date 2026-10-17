import os

import streamlit as st
from pymongo import MongoClient


@st.cache_resource
def obtenir_client():
    return MongoClient(
        host=os.environ["MONGO_HOST"],
        port=27017,
        username=os.environ["MONGO_USERNAME"],
        password=os.environ["MONGO_PASSWORD"],
        authSource=os.environ["MONGO_DATABASE"],
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=5000,
        socketTimeoutMS=10000,
    )


def charger_offres(filtres=None):
    client = obtenir_client()
    collection = client[os.environ["MONGO_DATABASE"]]["jobs"]

    return list(
        collection.find(
            filtres or {},
            {"_id": 0},
        )
    )


def charger_options_filtres():
    client = obtenir_client()
    collection = client[os.environ["MONGO_DATABASE"]]["jobs"]

    champs = [
        "country",
        "experience_level",
        "industry",
        "remote_work",
        "job_title",
    ]

    return {
        champ: sorted(collection.distinct(champ))
        for champ in champs
    }