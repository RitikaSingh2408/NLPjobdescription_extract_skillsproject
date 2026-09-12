import json
import re
from nlp.recommendation import recommend_technologies
from nlp.role_skills import get_role_skills
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Header
)

from fastapi.middleware.cors import CORSMiddleware

from database import (
    get_connection,
    init_db
)

from schemas import (
    RegisterRequest,
    LoginRequest,
    ExtractRequest,
    ExtractResponse
)

from auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token
)

from nlp.extractor import extract_skills

from nlp.normalization import normalize_results


app = FastAPI(
    title="Job Skill Extraction API",
    description="NLP based Job Skill Extraction System",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        # "http://localhost:5173",
        # "http://127.0.0.1:5173"
        "*"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


# --------------------------------------------------
# Database
# --------------------------------------------------

@app.on_event("startup")
def startup():

    init_db()


# --------------------------------------------------
# Root
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "message": "Job Skill Extraction API is running"
    }


# --------------------------------------------------
# Register
# --------------------------------------------------

@app.post("/auth/register")
def register(request: RegisterRequest):

    username = request.username.strip()
    email = request.email.strip().lower()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username is required"
        )

    if not re.match(
        r"^[^@\s]+@[^@\s]+\.[^@\s]+$",
        email
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid email address"
        )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM users WHERE email = ?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    password_hash = hash_password(
        request.password
    )

    cursor.execute(
        """
        INSERT INTO users
        (username, email, password_hash)
        VALUES (?, ?, ?)
        """,
        (
            username,
            email,
            password_hash
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Registration successful",
        "user": {
            "id": user_id,
            "username": username,
            "email": email
        }
    }


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.post("/auth/login")
def login(request: LoginRequest):

    email = request.email.strip().lower()

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, email, password_hash
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    user = cursor.fetchone()

    connection.close()

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        request.password,
        user["password_hash"]
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        user["id"],
        user["username"]
    )

    return {
        "message": "Login successful",

        "access_token": token,

        "token_type": "bearer",

        "user": {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
    }


# --------------------------------------------------
# Current User
# --------------------------------------------------

def get_current_user(
    authorization: str = Header(default="")
):

    if not authorization.startswith(
        "Bearer "
    ):

        raise HTTPException(
            status_code=401,
            detail="Authentication required"
        )

    token = authorization.split(
        " ",
        1
    )[1]

    payload = decode_access_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return payload


@app.get("/auth/me")
def get_me(
    current_user=Depends(get_current_user)
):

    user_id = int(
        current_user["sub"]
    )

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id, username, email
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    )

    user = cursor.fetchone()

    connection.close()

    if not user:

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": user["id"],
        "username": user["username"],
        "email": user["email"]
    }


# --------------------------------------------------
# Extract Skills
# --------------------------------------------------

@app.post(
    "/api/extract-skills",
    response_model=ExtractResponse
)
def extract_job_skills(
    data: ExtractRequest,
    current_user= Depends(get_current_user)

):

    text = data.job_description.strip()

    if not text:

        raise HTTPException(
            status_code=400,
            detail="Job description cannot be empty"
        )

    # --------------------------------
    # 1. EXISTING NLP EXTRACTION
    # --------------------------------

    extracted = extract_skills(text)

    # --------------------------------
    # 2. EXISTING NORMALIZATION
    # --------------------------------

    normalized = normalize_results(
        extracted
    )

    # --------------------------------
    # 3. ROLE-BASED SKILLS
    # --------------------------------
    # Only use role-based prediction
    # when no actual skills were detected.
    #
    # This keeps the original behavior
    # unchanged for normal job descriptions.

    '''if len(normalized) == 0:

        role_skills = get_role_skills(text)

        final_skills = role_skills'''
    role_skills = get_role_skills(text)

    if role_skills and len(normalized) <=1:
        final_skills = normalized + [
            skill
            for skill in role_skills
            if skill not in normalized
        ]
    else:

        # IMPORTANT:
        # If actual skills were found,
        # DO NOT add expected role skills.

        final_skills = normalized

    # --------------------------------
    # 4. TECHNOLOGY RECOMMENDATIONS
    # --------------------------------

    recommended = recommend_technologies(
        final_skills
    )

    # --------------------------------
    # 5. SAVE EXTRACTION HISTORY
    # --------------------------------

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO extraction_history
        (user_id, job_description, skills)
        VALUES (?, ?, ?)
        """,
        (
            int(current_user["sub"]),
            text,
            json.dumps(final_skills)
        )
    )

    connection.commit()
    connection.close()

    # --------------------------------
    # 5. API RESPONSE
    # --------------------------------

    return {
        "skills": final_skills,
        "total_skills": len(final_skills),
        "recommended_technologies": recommended
    }


# --------------------------------------------------
# History
# --------------------------------------------------

@app.get("/api/history")
def get_history(
    current_user=Depends(get_current_user)
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            job_description,
            skills,
            created_at
        FROM extraction_history
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        (int(current_user["sub"]),)
    )

    rows = cursor.fetchall()

    connection.close()

    history = []

    for row in rows:

        history.append({
            "id": row["id"],
            "job_description": row[
                "job_description"
            ],
            "skills": json.loads(
                row["skills"]
            ),
            "created_at": row[
                "created_at"
            ]
        })

    return {
        "history": history
    }