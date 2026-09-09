ROLE_SKILLS = {

    "data analyst": [
        {"skill": "Python", "category": "Programming"},
        {"skill": "SQL", "category": "Database"},
        {"skill": "Excel", "category": "Data Analytics"},
        {"skill": "Power BI", "category": "Data Visualization"},
        {"skill": "Pandas", "category": "Data Analytics"},
        {"skill": "NumPy", "category": "Data Analytics"}
    ],

    "data analytics": [
        {"skill": "Python", "category": "Programming"},
        {"skill": "SQL", "category": "Database"},
        {"skill": "Excel", "category": "Data Analytics"},
        {"skill": "Power BI", "category": "Data Visualization"},
        {"skill": "Pandas", "category": "Data Analytics"},
        {"skill": "NumPy", "category": "Data Analytics"}
    ],

    "business analyst": [
        {"skill": "Excel", "category": "Data Analytics"},
        {"skill": "SQL", "category": "Database"},
        {"skill": "Power BI", "category": "Data Visualization"},
        {"skill": "Tableau", "category": "Data Visualization"}
    ],

    "data scientist": [
        {"skill": "Python", "category": "Programming"},
        {"skill": "SQL", "category": "Database"},
        {"skill": "Pandas", "category": "Data Analytics"},
        {"skill": "NumPy", "category": "Data Analytics"},
        {"skill": "Machine Learning", "category": "Machine Learning"},
        {"skill": "Scikit-learn", "category": "Machine Learning"}
    ],

    "python developer": [
        {"skill": "Python", "category": "Programming"},
        {"skill": "Django", "category": "Web Development"},
        {"skill": "Flask", "category": "Web Development"},
        {"skill": "SQL", "category": "Database"},
        {"skill": "Git", "category": "DevOps"}
    ],

    "java developer": [
        {"skill": "Java", "category": "Programming"},
        {"skill": "Spring Boot", "category": "Web Development"},
        {"skill": "Hibernate", "category": "Web Development"},
        {"skill": "SQL", "category": "Database"},
        {"skill": "Git", "category": "DevOps"}
    ],

    "frontend developer": [
        {"skill": "HTML", "category": "Web Development"},
        {"skill": "CSS", "category": "Web Development"},
        {"skill": "JavaScript", "category": "Programming"},
        {"skill": "React", "category": "Web Development"},
        {"skill": "Git", "category": "DevOps"}
    ],

    "react developer": [
        {"skill": "HTML", "category": "Web Development"},
        {"skill": "CSS", "category": "Web Development"},
        {"skill": "JavaScript", "category": "Programming"},
        {"skill": "React", "category": "Web Development"},
        {"skill": "Git", "category": "DevOps"}
    ]
}


def get_role_skills(job_title):

    if not job_title:
        return []

    text = job_title.lower().strip()

    # matched_skills = []

    for role, skills in ROLE_SKILLS.items():

        if role in text:
            # matched_skills.extend(skills)
            return skills

    # Remove duplicate skills
    # unique_skills = []
    # seen = set()

    # for item in matched_skills:

    #     skill_name = item["skill"]

    #     if skill_name not in seen:
    #         unique_skills.append(item)
    #         seen.add(skill_name)

    return []