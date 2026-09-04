"""
Générateur simple de mots-clés long-tail (offline).
Ne fait pas appel à des APIs externes : combine seed phrases avec question-words et modifiers.
"""
from itertools import product

QUESTION_WORDS = ["pourquoi", "comment", "meilleur", "moins cher", "avis", "2026", "guide", "comparatif"]
MODIFIERS = ["pour débutant", "pas cher", "haut de gamme", "alternatives", "avis francais"]

def generate_keywords(seeds, max_out=100):
    """
    seeds: liste de phrases de départ
    renvoie une liste unique de mots-clés long-tail
    """
    out = []
    for s in seeds:
        s = s.strip()
        out.append(s)
        for q in QUESTION_WORDS:
            out.append(f"{s} {q}")
        for m in MODIFIERS:
            out.append(f"{s} {m}")
        # variantes courtes
        for i in range(1,4):
            out.append(f"{s} {i} avis")
    # dédupliquer en gardant l'ordre
    seen = set()
    result = []
    for k in out:
        if k not in seen:
            seen.add(k)
            result.append(k)
        if len(result) >= max_out:
            break
    return result
