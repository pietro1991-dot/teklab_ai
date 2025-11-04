#!/usr/bin/env python3
"""Verifica quale modello è salvato nella cache embeddings"""
import pickle
from pathlib import Path

cache_path = Path("ai_system/Embedding/embeddings_cache.pkl")

with open(cache_path, 'rb') as f:
    cache = pickle.load(f)

print(f"✅ Cache trovata: {cache_path}")
print(f"📊 Modello salvato: {cache.get('model', 'NON TROVATO')}")

if cache.get('chunk_embeddings'):
    first_emb = list(cache['chunk_embeddings'].values())[0]
    print(f"📏 Dimensione embeddings: {first_emb.shape}")
    print(f"📦 Numero chunk embeddings: {len(cache['chunk_embeddings'])}")
    
print(f"📦 Numero Q&A embeddings: {len(cache.get('qa_embeddings', {}))}")
print(f"📦 Numero summary embeddings: {len(cache.get('summary_embeddings', {}))}")
