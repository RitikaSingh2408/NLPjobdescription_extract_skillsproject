import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

TAXONOMY_PATH = (
    BASE_DIR
    / "data-Notebook"
    / "Skill_taxonomy.csv"
)


def clean_text(text):
    text = str(text).lower()

    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


def load_taxonomy():

    if not TAXONOMY_PATH.exists():
        raise FileNotFoundError(
            f"Taxonomy file not found: {TAXONOMY_PATH}"
        )

    df = pd.read_csv(TAXONOMY_PATH)

    required_columns = {
        "skill",
        "category",
        "aliases"
    }

    missing = required_columns - set(df.columns)

    if missing:
        raise ValueError(
            f"Missing taxonomy columns: {missing}"
        )

    return df.fillna("")


def build_skill_dictionary():

    taxonomy = load_taxonomy()

    skill_dictionary = []

    for _, row in taxonomy.iterrows():

        canonical_skill = str(
            row["skill"]
        ).strip()

        category = str(
            row["category"]
        ).strip()

        aliases = str(
            row["aliases"]
        ).strip()

        terms = [canonical_skill]

        if aliases:
            terms.extend(
                alias.strip()
                for alias in aliases.split("|")
                if alias.strip()
            )

        for term in terms:

            if term:
                skill_dictionary.append({
                    "term": term,
                    "skill": canonical_skill,
                    "category": category
                })

    return skill_dictionary


SKILL_DICTIONARY = build_skill_dictionary()


def term_pattern(term):

    cleaned = clean_text(term)

    escaped = re.escape(cleaned)

    return re.compile(
        rf"(?<!\w){escaped}(?!\w)",
        re.IGNORECASE
    )


def extract_skills(job_description):

    text = clean_text(job_description)

    detected = {}

    # Longer terms first
    sorted_dictionary = sorted(
        SKILL_DICTIONARY,
        key=lambda x: len(x["term"]),
        reverse=True
    )

    for item in sorted_dictionary:

        term = item["term"]

        pattern = term_pattern(term)

        if pattern.search(text):

            skill = item["skill"]
            category = item["category"]

            detected[skill] = category

    results = []

    for skill, category in detected.items():

        results.append({
            "skill": skill,
            "category": category
        })

    results.sort(
        key=lambda x: x["skill"].lower()
    )

    return results