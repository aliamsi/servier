# Exemple de SCHEMA où chaque colonne a un nom et un type attendu
from typing import List

DATA_TABLE_NAMES: List[str] = ["drugs", "clinical_trials", "pubmed"]

PUBLICATION_TABLE_NAMES: List[str] = ["clinical_trials", "pubmed"]

SCHEMA = {
    "drugs": {"atccode": str, "drug": str},
    "clinical_trials": {
        "id": str,
        "scientific_title": str,
        "date": str,
        "journal": str,
    },
    "pubmed": {"id": int, "title": str, "date": str, "journal": str},
    "search_column": {
        "drugs": "drug",
        "clinical_trials": "scientific_title",
        "pubmed": "title",
    },
}
