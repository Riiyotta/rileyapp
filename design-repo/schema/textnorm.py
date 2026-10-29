"""Text normalisation shared by the leakage-pattern builder and the semantic validator (one implementation)."""
import re
import unicodedata

ZERO_WIDTH = dict.fromkeys(map(ord, "​‌‍⁠﻿­᠎"), None)
# common confusables NFKC does not fold (Cyrillic / Greek look-alikes of Latin letters)
HOMOGLYPHS = str.maketrans({
    "а": "a", "е": "e", "і": "i", "о": "o", "р": "p", "с": "c", "у": "y", "х": "x", "к": "k", "м": "m", "т": "t", "в": "b", "н": "h",
    "А": "a", "Е": "e", "І": "i", "О": "o", "Р": "p", "С": "c", "У": "y", "Х": "x", "К": "k", "М": "m", "Т": "t", "В": "b", "Н": "h",
    "ο": "o", "ι": "i", "ε": "e", "α": "a", "ρ": "p", "υ": "u", "κ": "k", "ν": "v", "Ι": "i", "Ο": "o", "Ε": "e", "Α": "a", "Ρ": "p", "Υ": "y", "Κ": "k",
    "‘": "'", "’": "'", "‚": "'", "‛": "'", "′": "'", "“": '"', "”": '"', "„": '"', "″": '"',
    "‐": "-", "‑": "-", "‒": "-", "–": "-", "—": "-", "―": "-", "−": "-", "﹘": "-", "﹣": "-", "－": "-",
})


def normalize(s):
    s = unicodedata.normalize("NFKC", s).translate(ZERO_WIDTH).translate(HOMOGLYPHS).lower()
    return re.sub(r"\s+", " ", s).strip()


def words_only(s):
    return re.sub(r"[^a-z0-9$%' ]+", " ", normalize(s)).replace("'", "").split()


def shingles(s, n=5):
    w = words_only(s)
    return {" ".join(w[i:i + n]) for i in range(len(w) - n + 1)}
