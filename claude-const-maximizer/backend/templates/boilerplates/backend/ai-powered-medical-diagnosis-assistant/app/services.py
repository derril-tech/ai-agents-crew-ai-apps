from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from typing import List, Optional, Dict, Any
import openai
import time
import logging
from datetime import datetime, timedelta
import json
import re

from .models import (
    User, Patient, Diagnosis, Symptom, MedicalRecord, 
    MedicalKnowledge, AIDiagnosisLog
)
from .schemas import (
    PatientCreate, DiagnosisCreate, MedicalRecordCreate,
    DiagnosisRecommendation, SymptomAnalysisRequest
)
from .auth import get_password_hash, verify_password
from .config import settings

logger = logging.getLogger(__name__)

class MedicalDiagnosisService:
    """Service for AI-powered medical diagnosis"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.medical_prompt_template = self._load_medical_prompt()
    
    def _load_medical_prompt(self) -> str:
        """Load the medical diagnosis prompt template"""
        return """
        You are an advanced AI medical diagnosis assistant. Your role is to analyze patient symptoms and provide evidence-based diagnostic recommendations.

        PATIENT INFORMATION:
        Age: {age}
        Gender: {gender}
        Symptoms: {symptoms}
        Medical History: {medical_history}
        Current Medications: {medications}

        TASK: Analyze the symptoms and provide:
        1. Possible medical conditions (with ICD-10 codes if applicable)
        2. Confidence score (0.0-1.0)
        3. Recommended diagnostic tests
        4. Urgency level (low/medium/high/emergency)
        5. Next steps for the healthcare provider
        6. Differential diagnoses to consider
        7. Risk factors
        8. Treatment suggestions

        IMPORTANT GUIDELINES:
        - Always prioritize patient safety
        - Consider age and gender-specific factors
        - Account for medical history and medications
        - Provide evidence-based recommendations
        - Include both common and serious conditions
        - Suggest appropriate diagnostic tests
        - Consider drug interactions and contraindications

        RESPONSE FORMAT (JSON):
        {{
            "possible_conditions": [
                {{
                    "condition": "condition_name",
                    "icd_code": "ICD-10_code",
                    "probability": 0.0-1.0,
                    "severity": "mild/moderate/severe/critical"
                }}
            ],
            "confidence_score": 0.0-1.0,
            "recommended_tests": ["test1", "test2"],
            "urgency_level": "low/medium/high/emergency",
            "next_steps": ["step1", "step2"],
            "differential_diagnoses": ["condition1", "condition2"],
            "risk_factors": ["factor1", "factor2"],
            "treatment_suggestions": ["suggestion1", "suggestion2"]
        }}
        """
    
    async def analyze_symptoms(
        self,
        symptoms: List[str],
        age: int,
        gender: str,
        medical_history: Optional[List[str]] = None,
        medications: Optional[List[str]] = None
    ) -> DiagnosisRecommendation:
        """Analyze symptoms using AI and return diagnosis recommendations"""
        
        start_time = time.time()
        
        try:
            # Prepare the prompt
            prompt = self.medical_prompt_template.format(
                age=age,
                gender=gender,
                symptoms=", ".join(symptoms),
                medical_history=", ".join(medical_history or []),
                medications=", ".join(medications or [])
            )
            
            # Call OpenAI API
            response = await self._call_openai_api(prompt)
            
            # Parse the response
            diagnosis_data = self._parse_ai_response(response)
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            # Create diagnosis recommendation
            recommendation = DiagnosisRecommendation(
                possible_conditions=diagnosis_data.get("possible_conditions", []),
                confidence_score=diagnosis_data.get("confidence_score", 0.0),
                recommended_tests=diagnosis_data.get("recommended_tests", []),
                urgency_level=diagnosis_data.get("urgency_level", "medium"),
                next_steps=diagnosis_data.get("next_steps", []),
                differential_diagnoses=diagnosis_data.get("differential_diagnoses", []),
                risk_factors=diagnosis_data.get("risk_factors", []),
                treatment_suggestions=diagnosis_data.get("treatment_suggestions", [])
            )
            
            logger.info(f"AI diagnosis completed in {processing_time:.2f}s with confidence {recommendation.confidence_score}")
            
            return recommendation
            
        except Exception as e:
            logger.error(f"AI diagnosis failed: {str(e)}")
            # Return a safe fallback response
            return DiagnosisRecommendation(
                possible_conditions=[],
                confidence_score=0.0,
                recommended_tests=["Consult with a healthcare provider"],
                urgency_level="medium",
                next_steps=["Schedule an appointment with a doctor"],
                differential_diagnoses=[],
                risk_factors=[],
                treatment_suggestions=[]
            )
    
    async def _call_openai_api(self, prompt: str) -> str:
        """Make API call to OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a medical AI assistant. Provide responses in valid JSON format only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,  # Low temperature for consistent medical advice
                max_tokens=2000,
                timeout=settings.AI_RESPONSE_TIMEOUT
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API call failed: {str(e)}")
            raise
    
    def _parse_ai_response(self, response: str) -> Dict[str, Any]:
        """Parse the AI response and extract structured data"""
        try:
            # Clean the response and extract JSON
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                logger.warning("No JSON found in AI response")
                return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response as JSON: {str(e)}")
            return {}
    
    def create_diagnosis(
        self,
        db: Session,
        patient_id: int,
        diagnosis_data: DiagnosisCreate,
        doctor_id: int
    ) -> Diagnosis:
        """Create a new diagnosis record"""
        try:
            diagnosis = Diagnosis(
                patient_id=patient_id,
                doctor_id=doctor_id,
                diagnosis_name=diagnosis_data.diagnosis_name,
                diagnosis_code=diagnosis_data.diagnosis_code,
                severity=diagnosis_data.severity,
                symptoms_present=diagnosis_data.symptoms_present,
                differential_diagnoses=diagnosis_data.differential_diagnoses,
                recommended_tests=diagnosis_data.recommended_tests,
                treatment_plan=diagnosis_data.treatment_plan,
                follow_up_date=diagnosis_data.follow_up_date,
                notes=diagnosis_data.notes,
                confidence_score=diagnosis_data.confidence_score,
                is_ai_generated=diagnosis_data.is_ai_generated
            )
            
            db.add(diagnosis)
            db.commit()
            db.refresh(diagnosis)
            
            logger.info(f"Diagnosis created for patient {patient_id} by doctor {doctor_id}")
            return diagnosis
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create diagnosis: {str(e)}")
            raise
    
    def get_patient_diagnoses(self, db: Session, patient_id: int) -> List[Diagnosis]:
        """Get all diagnoses for a patient"""
        try:
            return db.query(Diagnosis).filter(Diagnosis.patient_id == patient_id).all()
        except Exception as e:
            logger.error(f"Failed to get patient diagnoses: {str(e)}")
            raise
    
    def log_ai_diagnosis(
        self,
        db: Session,
        patient_id: Optional[int],
        user_id: Optional[int],
        input_data: SymptomAnalysisRequest,
        ai_recommendations: DiagnosisRecommendation,
        processing_time: float
    ) -> AIDiagnosisLog:
        """Log AI diagnosis attempt for audit and improvement"""
        try:
            log_entry = AIDiagnosisLog(
                patient_id=patient_id,
                user_id=user_id,
                input_symptoms=input_data.symptoms,
                patient_age=input_data.age,
                patient_gender=input_data.gender,
                medical_history=input_data.medical_history,
                medications=input_data.medications,
                ai_recommendations=ai_recommendations.dict(),
                confidence_score=ai_recommendations.confidence_score,
                processing_time=processing_time
            )
            
            db.add(log_entry)
            db.commit()
            db.refresh(log_entry)
            
            return log_entry
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to log AI diagnosis: {str(e)}")
            raise

class PatientService:
    """Service for patient management"""
    
    def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        try:
            user = db.query(User).filter(User.username == username).first()
            if user and verify_password(password, user.hashed_password):
                return user
            return None
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return None
    
    def create_patient(self, db: Session, patient_data: PatientCreate, created_by_id: int) -> Patient:
        """Create a new patient record"""
        try:
            # Generate unique patient ID
            patient_id = self._generate_patient_id()
            
            patient = Patient(
                patient_id=patient_id,
                first_name=patient_data.first_name,
                last_name=patient_data.last_name,
                date_of_birth=patient_data.date_of_birth,
                gender=patient_data.gender,
                phone=patient_data.phone,
                email=patient_data.email,
                address=patient_data.address,
                emergency_contact=patient_data.emergency_contact,
                blood_type=patient_data.blood_type,
                allergies=patient_data.allergies,
                medical_history=patient_data.medical_history,
                current_medications=patient_data.current_medications,
                insurance_info=patient_data.insurance_info,
                created_by_id=created_by_id
            )
            
            db.add(patient)
            db.commit()
            db.refresh(patient)
            
            logger.info(f"Patient created: {patient_id}")
            return patient
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create patient: {str(e)}")
            raise
    
    def get_patients(self, db: Session, skip: int = 0, limit: int = 100) -> List[Patient]:
        """Get list of patients with pagination"""
        try:
            return db.query(Patient).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Failed to get patients: {str(e)}")
            raise
    
    def get_patient(self, db: Session, patient_id: int) -> Optional[Patient]:
        """Get a specific patient by ID"""
        try:
            return db.query(Patient).filter(Patient.id == patient_id).first()
        except Exception as e:
            logger.error(f"Failed to get patient {patient_id}: {str(e)}")
            raise
    
    def search_patients(
        self,
        db: Session,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Patient]:
        """Search patients by name or patient ID"""
        try:
            return db.query(Patient).filter(
                or_(
                    Patient.first_name.ilike(f"%{query}%"),
                    Patient.last_name.ilike(f"%{query}%"),
                    Patient.patient_id.ilike(f"%{query}%")
                )
            ).offset(skip).limit(limit).all()
        except Exception as e:
            logger.error(f"Failed to search patients: {str(e)}")
            raise
    
    def create_medical_record(
        self,
        db: Session,
        record_data: MedicalRecordCreate,
        created_by_id: int
    ) -> MedicalRecord:
        """Create a new medical record"""
        try:
            record = MedicalRecord(
                patient_id=record_data.patient_id,
                created_by_id=created_by_id,
                record_type=record_data.record_type,
                title=record_data.title,
                content=record_data.content,
                attachments=record_data.attachments,
                vital_signs=record_data.vital_signs,
                lab_results=record_data.lab_results,
                medications_prescribed=record_data.medications_prescribed,
                follow_up_required=record_data.follow_up_required,
                follow_up_date=record_data.follow_up_date
            )
            
            db.add(record)
            db.commit()
            db.refresh(record)
            
            logger.info(f"Medical record created for patient {record_data.patient_id}")
            return record
            
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to create medical record: {str(e)}")
            raise
    
    def _generate_patient_id(self) -> str:
        """Generate a unique patient ID"""
        import uuid
        return f"P{datetime.now().strftime('%Y%m')}{str(uuid.uuid4())[:8].upper()}"

class MedicalKnowledgeService:
    """Service for managing medical knowledge base"""
    
    def get_condition_info(self, db: Session, condition_name: str) -> Optional[MedicalKnowledge]:
        """Get information about a medical condition"""
        try:
            return db.query(MedicalKnowledge).filter(
                MedicalKnowledge.condition_name.ilike(f"%{condition_name}%")
            ).first()
        except Exception as e:
            logger.error(f"Failed to get condition info: {str(e)}")
            raise
    
    def search_conditions(self, db: Session, query: str) -> List[MedicalKnowledge]:
        """Search medical conditions"""
        try:
            return db.query(MedicalKnowledge).filter(
                MedicalKnowledge.condition_name.ilike(f"%{query}%")
            ).all()
        except Exception as e:
            logger.error(f"Failed to search conditions: {str(e)}")
            raise
    
    def add_condition(self, db: Session, condition_data: Dict[str, Any]) -> MedicalKnowledge:
        """Add a new medical condition to the knowledge base"""
        try:
            condition = MedicalKnowledge(**condition_data)
            db.add(condition)
            db.commit()
            db.refresh(condition)
            return condition
        except Exception as e:
            db.rollback()
            logger.error(f"Failed to add condition: {str(e)}")
            raise


