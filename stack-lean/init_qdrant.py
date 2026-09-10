#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Initialisation de la base vectorielle — VERSION CORRIGÉE.

Corrections par rapport au script du plan initial :
  1. Il y avait une erreur de syntaxe : QDRANT_URL et COLLECTION_NAME étaient
     collés sur la même ligne (le fichier ne démarrait même pas).
  2. La taille de vecteurs (768) était posée "au hasard" : elle doit être
     EXACTEMENT celle du modèle d'embedding choisi, sinon Qdrant refuse
     l'insertion. multilingual-e5-large = 1024, mistral-embed = 1024,
     BGE-M3 = 1024, sentence-transformers all-mpnet = 768.
  3. Le plan ne déployait AUCUN modèle d'embedding : le RAG ne pouvait pas
     fonctionner. On interroge donc le routeur LiteLLM pour le vérifier.
  4. Gestion des erreurs réseau, timeouts, et clé API (Qdrant sans auth =
     fuite de données clients = sinistre RGPD).
"""

import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
LITELLM_URL = os.getenv("LITELLM_URL", "http://localhost:4000/v1")
LITELLM_KEY = os.getenv("LITELLM_MASTER_KEY")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "scaleway/multilingual-e5-large")

COLLECTION_NAME = os.getenv("COLLECTION_NAME", "agence_connaissances")
TIMEOUT = 10


def qdrant_headers() -> dict:
    headers = {"Content-Type": "application/json"}
    if QDRANT_API_KEY:
        headers["api-key"] = QDRANT_API_KEY
    return headers


def detecter_dimension() -> int:
    """Demande sa dimension au modèle d'embedding au lieu de la deviner."""
    print(f"[*] Interrogation du modèle d'embedding '{EMBEDDING_MODEL}'...")
    try:
        r = requests.post(
            f"{LITELLM_URL}/embeddings",
            headers={"Authorization": f"Bearer {LITELLM_KEY}"},
            json={"model": EMBEDDING_MODEL, "input": ["sonde"]},
            timeout=30,
        )
        r.raise_for_status()
        dim = len(r.json()["data"][0]["embedding"])
        print(f"[+] Dimension détectée : {dim}")
        return dim
    except Exception as e:
        print(f"[!] Impossible d'interroger le routeur ({e}).")
        print("    -> Vérifiez que LiteLLM tourne et que EMBEDDING_MODEL existe dans")
        print("       litellm_config.yaml. Le RAG a besoin d'un modèle d'embedding :")
        print("       c'était le trou principal du plan initial.")
        sys.exit(1)


def init_vector_db(dim: int) -> bool:
    payload = {
        "vectors": {"size": dim, "distance": "Cosine"},
        # Indexation plein texte pour l'hybride (mot-clé + sémantique) :
        # indispensable sur des documents administratifs / délibérations.
        "optimizers_config": {"default_segment_number": 2},
        "replication_factor": 1,
    }
    print(f"[*] Création de la collection '{COLLECTION_NAME}' ({dim} dims)...")
    r = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}",
        json=payload,
        headers=qdrant_headers(),
        timeout=TIMEOUT,
    )
    if r.status_code == 200:
        print("[+] Base vectorielle initialisée. Prête pour le RAG.")
        return True
    if r.status_code == 409 or "already exists" in r.text.lower():
        print("[=] La collection existe déjà, rien à faire.")
        return True
    print(f"[-] Échec ({r.status_code}) : {r.text}")
    return False


def creer_index_texte() -> None:
    """Index de texte intégral sur le champ 'text' pour la recherche hybride."""
    r = requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}/index",
        json={"field_name": "text", "field_schema": "text"},
        headers=qdrant_headers(),
        timeout=TIMEOUT,
    )
    if r.status_code in (200, 409):
        print("[+] Index texte intégral prêt (recherche hybride activée).")
    else:
        print(f"[!] Index texte non créé ({r.status_code}) : {r.text}")


if __name__ == "__main__":
    dim = int(os.getenv("EMBEDDING_DIM", "0")) or detecter_dimension()
    if init_vector_db(dim):
        creer_index_texte()
