from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base


class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_filename = Column(String(255))
    job_description = Column(Text)
    ats_score = Column(Integer)
    matched_skills = Column(Text)
    missing_skills = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    