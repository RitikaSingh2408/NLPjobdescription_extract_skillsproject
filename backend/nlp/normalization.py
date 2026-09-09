import re


MANUAL_NORMALIZATION = {
    "python3": "Python",
    "python 3": "Python",
    "python programming": "Python",

    "powerbi": "Power BI",
    "power bi": "Power BI",
    "power-bi": "Power BI",

    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",

    "reactjs": "React",
    "react.js": "React",

    "nodejs": "Node.js",
    "node.js": "Node.js",

    "javascript": "JavaScript",
    "js": "JavaScript",

    "typescript": "TypeScript",
    "ts": "TypeScript",
}


def clean_skill(skill):

    skill = str(skill).lower().strip()

    skill = re.sub(
        r"[^a-z0-9+#.\- ]+",
        "",
        skill
    )

    skill = re.sub(
        r"\s+",
        " ",
        skill
    )

    return skill


def normalize_skill(skill):

    cleaned = clean_skill(skill)

    if cleaned in MANUAL_NORMALIZATION:
        return MANUAL_NORMALIZATION[cleaned]

    return skill.strip()


def normalize_results(results):

    normalized = {}

    for item in results:

        skill = normalize_skill(
            item["skill"]
        )

        category = item["category"]

        normalized[skill] = category

    return [
        {
            "skill": skill,
            "category": category
        }
        for skill, category in normalized.items()
    ]