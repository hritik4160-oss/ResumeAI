from fastapi import FastAPI, UploadFile, File, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pypdf import PdfReader
from io import BytesIO
from google import genai
from dotenv import load_dotenv
import os
import re
import json

from database import engine, get_db
from models import Base, ResumeAnalysis

load_dotenv()

app = FastAPI(title="ResumeAI Gemini Analyzer")

Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://resume-ai-xi-two.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SKILLS = [
    "python", "java", "javascript", "typescript",
    "react", "node.js", "fastapi", "django",
    "html", "css", "tailwind", "sql",
    "mysql", "postgresql", "mongodb",
    "machine learning", "deep learning",
    "artificial intelligence", "data analysis",
    "pandas", "numpy", "tensorflow",
    "pytorch", "git", "github",
    "docker", "aws", "rest api",
    "communication", "problem solving",
    "teamwork", "leadership"
]


def extract_skills(text):
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return found


def get_gemini_recommendations(
    resume_text,
    job_description,
    matched_skills,
    missing_skills
):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return [
            "Gemini API key was not found. Check your backend .env file."
        ]

    client = genai.Client(api_key=api_key)

    prompt = f"""
You are a professional resume improvement assistant.

Analyze the resume against the job description.

RESUME TEXT:
{resume_text[:5000]}

JOB DESCRIPTION:
{job_description[:3000]}

MATCHED SKILLS:
{", ".join(matched_skills)}

MISSING SKILLS:
{", ".join(missing_skills)}

Provide 5 practical, personalized recommendations.

Focus on:
1. Improving resume bullet points.
2. Highlighting relevant projects.
3. Demonstrating skills with genuine examples.
4. Improving resume structure.
5. Making the resume more relevant to the job.

Do not invent qualifications, experience, projects, or achievements.
Do not recommend claiming skills the candidate does not have.

Return recommendations as a numbered list.
Keep the language clear and concise.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        if response.text:
            return [
                line.strip()
                for line in response.text.split("\n")
                if line.strip()
            ]

        return ["Gemini returned an empty response."]

    except Exception as error:
        print("Gemini error:", str(error))
        return [
            "Gemini recommendations are temporarily unavailable.",
            "Please check your API key, model access, and internet connection."
        ]

    finally:
        client.close()


@app.get("/")
def home():
    return {
        "message": "ResumeAI Gemini Backend is running!"
    }


@app.post("/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...),
    db: Session = Depends(get_db)
):
    try:
        if not resume.filename.lower().endswith(".pdf"):
            return {
                "success": False,
                "error": "Please upload a PDF resume."
            }

        if not job_description.strip():
            return {
                "success": False,
                "error": "Job description cannot be empty."
            }

        content = await resume.read()
        pdf = PdfReader(BytesIO(content))

        resume_text = ""

        for page in pdf.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():
            return {
                "success": False,
                "error": "Unable to extract text from PDF."
            }

        resume_skills = extract_skills(resume_text)
        required_skills = extract_skills(job_description)

        matched_skills = [
            skill for skill in required_skills
            if skill in resume_skills
        ]

        missing_skills = [
            skill for skill in required_skills
            if skill not in resume_skills
        ]

        if required_skills:
            score = round(
                len(matched_skills) / len(required_skills) * 100
            )
        else:
            score = 0

        suggestions = []

        if missing_skills:
            suggestions.append(
                "Consider learning and demonstrating these relevant skills: "
                + ", ".join(missing_skills)
            )

        if len(resume_text) < 500:
            suggestions.append(
                "Your resume contains limited information. "
                "Consider adding education, projects, and experience."
            )

        if "project" not in resume_text.lower():
            suggestions.append(
                "Consider adding a Projects section."
            )

        if "experience" not in resume_text.lower():
            suggestions.append(
                "Consider including relevant experience or practical training."
            )

        if "skills" not in resume_text.lower():
            suggestions.append(
                "Add a clearly organized Skills section."
            )

        if not suggestions:
            suggestions.append(
                "Continue tailoring your achievements to the target role."
            )

        # Generate real AI recommendations using Gemini
        ai_recommendations = get_gemini_recommendations(
            resume_text,
            job_description,
            matched_skills,
            missing_skills
        )

        # Save analysis to SQLite
        analysis = ResumeAnalysis(
            resume_filename=resume.filename,
            job_description=job_description,
            ats_score=score,
            matched_skills=json.dumps(matched_skills),
            missing_skills=json.dumps(missing_skills)
        )

        db.add(analysis)
        db.commit()
        db.refresh(analysis)

        return {
            "success": True,
            "analysis_id": analysis.id,
            "ats_score": score,
            "resume_skills": resume_skills,
            "required_skills": required_skills,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "total_matched": len(matched_skills),
            "total_required": len(required_skills),
            "suggestions": suggestions,
            "ai_recommendations": ai_recommendations,
            "resume_text": resume_text[:1500],
            "message": "Gemini-powered resume analysis completed and saved!"
        }

    except Exception as error:
        db.rollback()

        return {
            "success": False,
            "error": str(error)
        }


@app.get("/history")
def get_history(db: Session = Depends(get_db)):
    analyses = (
        db.query(ResumeAnalysis)
        .order_by(ResumeAnalysis.id.desc())
        .all()
    )

    return [
        {
            "id": item.id,
            "resume_filename": item.resume_filename,
            "ats_score": item.ats_score,
            "matched_skills": json.loads(
                item.matched_skills or "[]"
            ),
            "missing_skills": json.loads(
                item.missing_skills or "[]"
            ),
            "created_at": (
                item.created_at.isoformat()
                if item.created_at else None
            )
        }
        for item in analyses
    ]
