import pandas as pd 
import re
import os 

# Project folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

clean_jobs_path = os.path.join(BASE_DIR, "data", "clean_jobs.csv")
skill_taxonomy_path = os.path.join(BASE_DIR, "data", "skill_taxonomy.csv")

df = pd.read_csv("data/clean_jobs.csv")
skill_taxonomy = pd.read_csv("data/skill_taxonomy.csv")

print("Jobs:", df.shape)
print("skills:", skill_taxonomy.shape)
print(skill_taxonomy.head())
# create the skill list
skills = skill_taxonomy["skill"].dropna().tolist()
print(skills)
# create the extractor
def extract_skills(text):
    found = []

    if pd.isna(text):
        return found

    text = str(text).lower()

    for _, row in skill_taxonomy.iterrows():

        skill = str(row["skill"]).strip()
        aliases = str(row["aliases"]).split(",")

        # Main skill + aliases
        terms = [skill] + [alias.strip() for alias in aliases]

        for term in terms:

            if not term or term == "nan":
                continue

            # Word boundary matching
            pattern = r"\b" + re.escape(term.lower()) + r"\b"

            if re.search(pattern, text):
                found.append(skill)
                break

    return list(dict.fromkeys(found))
text = df["clean_description"].iloc[0]
print(text)
result = extract_skills(text)
print("Extracted skills:")
print(result)
# test_df = df.head(1000).copy()
df["extracted_skills"] = df["clean_description"].apply(extract_skills)
print(df[["clean_description", "extracted_skills"]].head(10))
for col in df.columns:
    if "skill" in col.lower():
        print(col)
print(df["extracted_skills"].head().to_string())
# count how many skills each job 
df["skill_count"] = df["extracted_skills"].apply(len)
print(df["skill_count"].describe())
# find jobs where no skills found 
no_skill_jobs = df[
    df["skill_count"] == 0
]

print("Jobs with no extracted skills:",
      len(no_skill_jobs))
# Count most common extracted skills
from collections import Counter

all_skills = []

for skill_list in df["extracted_skills"]:
    all_skills.extend(skill_list)

skill_counts = Counter(all_skills)

skill_counts_df = pd.DataFrame(
    skill_counts.items(),
    columns=["skill", "job_count"]
)

skill_counts_df = skill_counts_df.sort_values(
    "job_count",
    ascending=False
)

print(skill_counts_df.head(20))
  

# visualization
import matplotlib.pyplot as plt

top_skills = skill_counts_df.head(10)

plt.figure(figsize=(10, 6))

plt.bar(
    top_skills["skill"],
    top_skills["job_count"]
)

plt.title("Top 10 Extracted Skills")
plt.xlabel("Skill")
plt.ylabel("Number of Jobs")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()