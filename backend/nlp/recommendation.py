RECOMMENDATIONS = {

    "Python": [
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Jupyter"
    ],

    "SQL": [
        "MySQL",
        "PostgreSQL",
        "SQL Server"
    ],

    "Excel": [
        "Power BI",
        "Tableau",
        "Pandas"
    ],

    "Power BI": [
        "DAX",
        "Power Query",
        "Excel"
    ],

    "Machine Learning": [
        "Scikit-learn",
        "NumPy",
        "Pandas",
        "Jupyter"
    ],

    "Data Analysis": [
        "Pandas",
        "NumPy",
        "Matplotlib",
        "Power BI"
    ],

    "React": [
        "Vite",
        "Redux",
        "Tailwind CSS"
    ],

    "JavaScript": [
        "React",
        "Node.js",
        "Vite"
    ],

    "Java": [
        "Spring Boot",
        "Maven",
        "Hibernate"
    ],

    "AWS": [
        "Docker",
        "Terraform",
        "CloudFormation"
    ],

    "Docker": [
        "Kubernetes",
        "Jenkins",
        "GitHub Actions"
    ],

    "Git": [
        "GitHub",
        "GitLab",
        "GitHub Actions"
    ]
}


def recommend_technologies(skills):
    recommendations = []

    for skill in skills:

        skill_name = skill.get("skill")

        if skill_name in RECOMMENDATIONS:

            recommendations.extend(
                RECOMMENDATIONS[skill_name]
            )

    # Remove duplicates
    recommendations = list(
        dict.fromkeys(recommendations)
    )

    return recommendations[:8]