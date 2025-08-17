"""
Resume Parser Service for AI-Powered Resume Parser & Job Matcher
Handles resume parsing, skill extraction, and AI analysis
"""

import asyncio
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime
import aiofiles
import os
from pathlib import Path

# AI and NLP imports
import spacy
from transformers import pipeline
import openai
from anthropic import Anthropic

# Document processing
import PyPDF2
from docx import Document
import pdfplumber

# Data processing
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

# Local imports
from app.models.resume import (
    Resume, ResumeCreate, ResumeUpdate, ResumeResponse, 
    ResumeStatus, Skill, SkillLevel, Experience, Education,
    Project, Certification, ResumeAnalysis
)
from app.config.settings import Settings
from app.utils.file_handler import FileHandler
from app.utils.text_processor import TextProcessor

logger = logging.getLogger(__name__)

class ResumeParserService:
    """Service for parsing and analyzing resumes"""
    
    def __init__(self):
        """Initialize the resume parser service"""
        self.settings = Settings()
        
        # Initialize AI clients
        self.openai_client = openai.OpenAI(api_key=self.settings.OPENAI_API_KEY)
        self.anthropic_client = Anthropic(api_key=self.settings.ANTHROPIC_API_KEY)
        
        # Initialize NLP models
        self.nlp = spacy.load("en_core_web_sm")
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.ner_pipeline = pipeline("ner")
        
        # Initialize utilities
        self.file_handler = FileHandler()
        self.text_processor = TextProcessor()
        
        # Load skill databases
        self.skill_database = self._load_skill_database()
        self.industry_keywords = self._load_industry_keywords()
    
    def _load_skill_database(self) -> Dict[str, List[str]]:
        """Load skill database from file or API"""
        # This would typically load from a database or API
        return {
            "programming": [
                "Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust",
                "TypeScript", "PHP", "Ruby", "Swift", "Kotlin", "Scala"
            ],
            "frameworks": [
                "React", "Angular", "Vue.js", "Django", "Flask", "FastAPI",
                "Spring", "Express.js", "Laravel", "Ruby on Rails"
            ],
            "databases": [
                "PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch",
                "Cassandra", "DynamoDB", "SQLite"
            ],
            "cloud": [
                "AWS", "Azure", "Google Cloud", "Docker", "Kubernetes",
                "Terraform", "Jenkins", "GitLab CI/CD"
            ],
            "soft_skills": [
                "Leadership", "Communication", "Problem Solving", "Teamwork",
                "Time Management", "Adaptability", "Creativity", "Critical Thinking"
            ]
        }
    
    def _load_industry_keywords(self) -> Dict[str, List[str]]:
        """Load industry-specific keywords"""
        return {
            "technology": ["software", "development", "programming", "coding", "tech"],
            "finance": ["banking", "investment", "financial", "trading", "risk"],
            "healthcare": ["medical", "healthcare", "patient", "clinical", "pharmaceutical"],
            "marketing": ["marketing", "advertising", "brand", "campaign", "social media"],
            "sales": ["sales", "business development", "account management", "revenue"]
        }
    
    async def parse_resume_async(self, file, user_id: int) -> Resume:
        """Parse resume asynchronously"""
        try:
            logger.info(f"Starting resume parsing for user {user_id}")
            start_time = datetime.utcnow()
            
            # Save file
            file_path = await self.file_handler.save_uploaded_file(file, user_id)
            
            # Extract text based on file type
            raw_text = await self._extract_text(file_path, file.filename)
            
            # Create initial resume record
            resume_data = ResumeCreate(
                filename=file.filename,
                file_path=file_path,
                file_size=file.size,
                file_type=file.filename.split('.')[-1].lower()
            )
            
            # Parse structured data
            parsed_data = await self._parse_structured_data(raw_text)
            
            # Extract skills
            skills = await self._extract_skills(raw_text)
            
            # AI analysis
            ai_analysis = await self._perform_ai_analysis(raw_text, skills)
            
            # Calculate processing time
            processing_time = (datetime.utcnow() - start_time).total_seconds()
            
            # Create complete resume object
            resume = Resume(
                user_id=user_id,
                filename=resume_data.filename,
                file_path=resume_data.file_path,
                file_size=resume_data.file_size,
                file_type=resume_data.file_type,
                raw_text=raw_text,
                **parsed_data,
                skills=skills,
                **ai_analysis,
                status=ResumeStatus.COMPLETED,
                processing_time=processing_time
            )
            
            # Save to database (this would be implemented)
            # await self._save_resume(resume)
            
            logger.info(f"Resume parsing completed for user {user_id} in {processing_time:.2f}s")
            return resume
            
        except Exception as e:
            logger.error(f"Resume parsing failed for user {user_id}: {e}")
            # Create error resume record
            error_resume = Resume(
                user_id=user_id,
                filename=file.filename,
                file_path="",
                file_size=file.size,
                file_type=file.filename.split('.')[-1].lower(),
                raw_text="",
                name="",
                email="",
                summary="",
                status=ResumeStatus.FAILED,
                error_message=str(e)
            )
            # await self._save_resume(error_resume)
            raise
    
    async def _extract_text(self, file_path: str, filename: str) -> str:
        """Extract text from different file formats"""
        file_extension = filename.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return await self._extract_pdf_text(file_path)
        elif file_extension in ['docx', 'doc']:
            return await self._extract_docx_text(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")
    
    async def _extract_pdf_text(self, file_path: str) -> str:
        """Extract text from PDF file"""
        try:
            text = ""
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"PDF text extraction failed: {e}")
            raise
    
    async def _extract_docx_text(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        try:
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            logger.error(f"DOCX text extraction failed: {e}")
            raise
    
    async def _parse_structured_data(self, raw_text: str) -> Dict[str, Any]:
        """Parse structured data from raw text"""
        # Use AI to extract structured information
        prompt = f"""
        Extract the following information from this resume text:
        - Name
        - Email
        - Phone number
        - Location
        - LinkedIn URL
        - GitHub URL
        - Portfolio URL
        - Professional summary
        - Work experience (company, position, dates, description)
        - Education (institution, degree, field, dates)
        - Projects (name, description, technologies, URL)
        - Certifications (name, issuer, dates)
        
        Resume text:
        {raw_text}
        
        Return the information in JSON format.
        """
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            # Parse JSON response and extract data
            # This is a simplified version - in practice, you'd parse the JSON
            parsed_data = self._parse_ai_response(response.choices[0].message.content)
            return parsed_data
            
        except Exception as e:
            logger.error(f"AI parsing failed: {e}")
            # Fallback to basic parsing
            return self._basic_parsing(raw_text)
    
    def _parse_ai_response(self, ai_response: str) -> Dict[str, Any]:
        """Parse AI response into structured data"""
        # This would parse the JSON response from AI
        # For now, return basic structure
        return {
            "name": "Extracted Name",
            "email": "extracted@email.com",
            "phone": None,
            "location": None,
            "linkedin": None,
            "github": None,
            "portfolio": None,
            "summary": "Professional summary extracted from resume",
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": []
        }
    
    def _basic_parsing(self, raw_text: str) -> Dict[str, Any]:
        """Basic parsing when AI fails"""
        # Implement basic regex-based parsing
        return {
            "name": "Basic Name Extraction",
            "email": "basic@email.com",
            "phone": None,
            "location": None,
            "linkedin": None,
            "github": None,
            "portfolio": None,
            "summary": "Basic summary extraction",
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": []
        }
    
    async def _extract_skills(self, raw_text: str) -> List[Skill]:
        """Extract skills from resume text"""
        skills = []
        
        # Use spaCy for NER and skill extraction
        doc = self.nlp(raw_text.lower())
        
        # Extract skills from skill database
        for category, skill_list in self.skill_database.items():
            for skill in skill_list:
                if skill.lower() in raw_text.lower():
                    # Determine skill level based on context
                    level = self._determine_skill_level(raw_text, skill)
                    confidence = self._calculate_skill_confidence(raw_text, skill)
                    
                    skills.append(Skill(
                        name=skill,
                        level=level,
                        category=category,
                        confidence_score=confidence
                    ))
        
        # Use AI for additional skill extraction
        ai_skills = await self._extract_ai_skills(raw_text)
        skills.extend(ai_skills)
        
        return skills
    
    def _determine_skill_level(self, text: str, skill: str) -> SkillLevel:
        """Determine skill proficiency level"""
        text_lower = text.lower()
        skill_lower = skill.lower()
        
        # Look for level indicators
        if any(word in text_lower for word in ["expert", "master", "advanced"]):
            return SkillLevel.EXPERT
        elif any(word in text_lower for word in ["proficient", "experienced", "intermediate"]):
            return SkillLevel.INTERMEDIATE
        elif any(word in text_lower for word in ["beginner", "basic", "learning"]):
            return SkillLevel.BEGINNER
        else:
            return SkillLevel.INTERMEDIATE
    
    def _calculate_skill_confidence(self, text: str, skill: str) -> float:
        """Calculate confidence score for skill extraction"""
        # Simple frequency-based confidence
        skill_count = text.lower().count(skill.lower())
        return min(skill_count * 0.3, 1.0)
    
    async def _extract_ai_skills(self, raw_text: str) -> List[Skill]:
        """Extract skills using AI"""
        prompt = f"""
        Extract technical and soft skills from this resume text.
        For each skill, provide:
        - Skill name
        - Proficiency level (beginner, intermediate, advanced, expert)
        - Category (programming, frameworks, databases, cloud, soft_skills, etc.)
        
        Resume text:
        {raw_text}
        
        Return as JSON array of skill objects.
        """
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1
            )
            
            # Parse AI response and convert to Skill objects
            # This is simplified - you'd parse the JSON response
            return []
            
        except Exception as e:
            logger.error(f"AI skill extraction failed: {e}")
            return []
    
    async def _perform_ai_analysis(self, raw_text: str, skills: List[Skill]) -> Dict[str, Any]:
        """Perform AI-powered analysis of resume"""
        try:
            # Resume scoring
            score = await self._calculate_resume_score(raw_text, skills)
            
            # Generate feedback
            feedback = await self._generate_resume_feedback(raw_text, skills)
            
            # Extract keywords
            keywords = await self._extract_keywords(raw_text)
            
            # Detect industry
            industry = await self._detect_industry(raw_text, skills)
            
            # Determine seniority level
            seniority = await self._determine_seniority_level(raw_text, skills)
            
            return {
                "ai_score": score,
                "ai_feedback": feedback,
                "keywords": keywords,
                "industry": industry,
                "seniority_level": seniority
            }
            
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            return {
                "ai_score": None,
                "ai_feedback": [],
                "keywords": [],
                "industry": None,
                "seniority_level": None
            }
    
    async def _calculate_resume_score(self, raw_text: str, skills: List[Skill]) -> float:
        """Calculate AI-powered resume score"""
        # This would use AI to score the resume
        # For now, return a basic score
        return 75.0
    
    async def _generate_resume_feedback(self, raw_text: str, skills: List[Skill]) -> List[str]:
        """Generate AI-powered resume feedback"""
        prompt = f"""
        Analyze this resume and provide 3-5 specific suggestions for improvement.
        Focus on:
        - Content quality
        - Formatting
        - Skill presentation
        - Impact and achievements
        
        Resume text:
        {raw_text}
        
        Return suggestions as a list.
        """
        
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # Parse response into list of suggestions
            return ["Sample feedback 1", "Sample feedback 2", "Sample feedback 3"]
            
        except Exception as e:
            logger.error(f"Feedback generation failed: {e}")
            return []
    
    async def _extract_keywords(self, raw_text: str) -> List[str]:
        """Extract keywords from resume"""
        # Use TF-IDF to extract important keywords
        vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform([raw_text])
            feature_names = vectorizer.get_feature_names_out()
            return feature_names.tolist()
        except:
            return []
    
    async def _detect_industry(self, raw_text: str, skills: List[Skill]) -> Optional[str]:
        """Detect industry from resume content"""
        text_lower = raw_text.lower()
        
        for industry, keywords in self.industry_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return industry
        
        return None
    
    async def _determine_seniority_level(self, raw_text: str, skills: List[Skill]) -> Optional[str]:
        """Determine seniority level"""
        # Analyze experience and skills to determine level
        if "senior" in raw_text.lower() or "lead" in raw_text.lower():
            return "senior"
        elif "junior" in raw_text.lower() or "entry" in raw_text.lower():
            return "junior"
        else:
            return "mid-level"
    
    async def get_user_resumes(self, user_id: int) -> List[ResumeResponse]:
        """Get all resumes for a user"""
        # This would query the database
        # For now, return empty list
        return []
    
    async def get_resume(self, resume_id: int, user_id: int) -> Optional[ResumeResponse]:
        """Get a specific resume by ID"""
        # This would query the database
        # For now, return None
        return None
    
    async def extract_skills(self, resume_id: int, user_id: int) -> List[str]:
        """Extract skills from a specific resume"""
        # This would get the resume and extract skills
        # For now, return empty list
        return []
