#!/usr/bin/env python

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
import uuid
import json

from crewai.flow import Flow, start, listen
from src.sdr_assistant_flow.crews.analyze_customer_profile_crew import AnalyzeCustomerProfileCrew
from src.sdr_assistant_flow.crews.draft_cold_email_crew import DraftColdEmailCrew
from src.sdr_assistant_flow.lead_types import (
    LeadReadinessResult, 
    LeadInput, 
    GeneratedEmail,
    LeadStatus,
    CampaignMetrics
)
from src.sdr_assistant_flow.utils.logger import get_logger
from src.sdr_assistant_flow.utils.database import DatabaseManager

logger = get_logger(__name__)

# === Define the Flow State ===
class SDRFlowState(BaseModel):
    """State management for the SDR Assistant Flow"""
    session_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    leads: List[LeadInput] = Field(default_factory=list)
    analyzed_leads: List[LeadReadinessResult] = Field(default_factory=list)
    generated_emails: List[GeneratedEmail] = Field(default_factory=list)
    campaign_metrics: CampaignMetrics = Field(default_factory=CampaignMetrics)
    processing_status: Dict[str, LeadStatus] = Field(default_factory=dict)
    errors: List[Dict[str, Any]] = Field(default_factory=list)
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None

# === Define the Flow ===
class SDRAssistantFlow(Flow[SDRFlowState]):
    """
    Main SDR Assistant Flow that orchestrates lead analysis and email generation.
    
    This flow manages the complete process:
    1. Load and validate leads
    2. Analyze each lead for readiness and fit
    3. Generate personalized cold emails
    4. Track metrics and performance
    """

    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()

    @start()
    def initialize_session(self):
        """Initialize a new SDR session with default sample data"""
        logger.info(f"Starting new SDR session: {self.state.session_id}")
        
        # Load sample leads (in production, this would come from CRM/API)
        sample_leads = [
            LeadInput(
                name="Mark Benioff",
                job_title="CEO",
                company="Salesforce",
                email="mark@salesforce.com",
                linkedin_url="https://linkedin.com/in/benioff",
                company_website="https://salesforce.com",
                use_case="Exploring GenAI strategy for executive-level productivity",
                source="conference_networking"
            ),
            LeadInput(
                name="Satya Nadella",
                job_title="CEO",
                company="Microsoft",
                email="satya@microsoft.com",
                linkedin_url="https://linkedin.com/in/satyanadella",
                company_website="https://microsoft.com",
                use_case="AI integration across enterprise products",
                source="industry_research"
            ),
            LeadInput(
                name="Jensen Huang",
                job_title="CEO",
                company="NVIDIA",
                email="jensen@nvidia.com",
                linkedin_url="https://linkedin.com/in/jenhsunhuang",
                company_website="https://nvidia.com",
                use_case="Enterprise AI acceleration and GPU optimization with DFN AI Services",
                source="partner_referral"
            )
        ]
        
        self.state.leads = sample_leads
        self.state.campaign_metrics.total_leads = len(sample_leads)
        
        # Initialize processing status
        for lead in sample_leads:
            lead_id = f"{lead.name}_{lead.company}".replace(" ", "_").lower()
            self.state.processing_status[lead_id] = LeadStatus.NEW
        
        logger.info(f"Initialized session with {len(sample_leads)} leads")

    @listen(initialize_session)
    def analyze_leads(self):
        """Analyze each lead for readiness and qualification"""
        logger.info("Starting lead analysis phase...")
        
        results = []
        
        for i, lead in enumerate(self.state.leads):
            lead_id = f"{lead.name}_{lead.company}".replace(" ", "_").lower()
            
            try:
                logger.info(f"Analyzing lead {i+1}/{len(self.state.leads)}: {lead.name} at {lead.company}")
                
                # Update status
                self.state.processing_status[lead_id] = LeadStatus.ANALYZING
                
                # Prepare lead data for analysis
                lead_data = {
                    "name": lead.name,
                    "job_title": lead.job_title,
                    "company": lead.company,
                    "email": lead.email,
                    "linkedin_url": lead.linkedin_url,
                    "company_website": lead.company_website,
                    "use_case": lead.use_case,
                    "source": lead.source,
                    "notes": lead.notes
                }
                
                # Run the analysis crew
                analysis_result = AnalyzeCustomerProfileCrew().crew().kickoff(
                    inputs={"lead_data": lead_data}
                )
                
                # Store the structured result
                if hasattr(analysis_result, 'pydantic') and analysis_result.pydantic:
                    results.append(analysis_result.pydantic)
                    self.state.processing_status[lead_id] = LeadStatus.ANALYZED
                    logger.info(f"Successfully analyzed {lead.name} - Score: {analysis_result.pydantic.readiness_score.score}")
                else:
                    # Handle case where pydantic output is not available
                    logger.warning(f"No structured output for {lead.name}, creating default result")
                    self.state.errors.append({
                        "lead": lead.name,
                        "error": "No structured analysis output",
                        "timestamp": datetime.now().isoformat()
                    })
                
            except Exception as e:
                logger.error(f"Error analyzing lead {lead.name}: {str(e)}")
                self.state.errors.append({
                    "lead": lead.name,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                continue
        
        self.state.analyzed_leads = results
        logger.info(f"Analysis complete: {len(results)} leads successfully analyzed")

    @listen(analyze_leads)
    def generate_emails(self):
        """Generate personalized cold emails for analyzed leads"""
        logger.info("Starting email generation phase...")
        
        emails = []
        
        for i, lead_analysis in enumerate(self.state.analyzed_leads):
            try:
                lead_name = lead_analysis.personal_info.name
                logger.info(f"Generating email {i+1}/{len(self.state.analyzed_leads)}: {lead_name}")
                
                # Update status
                lead_id = f"{lead_name}_{lead_analysis.company_info.company_name}".replace(" ", "_").lower()
                self.state.processing_status[lead_id] = LeadStatus.EMAIL_DRAFTED
                
                # Prepare data for email generation
                lead_dict = lead_analysis.model_dump()
                
                # Run the email drafting crew
                email_result = DraftColdEmailCrew().crew().kickoff(inputs={
                    "personal_info": lead_dict["personal_info"],
                    "company_info": lead_dict["company_info"],
                    "engagement_fit": lead_dict["engagement_fit"]
                })
                
                # Store the generated email
                if hasattr(email_result, 'pydantic') and email_result.pydantic:
                    emails.append(email_result.pydantic)
                    logger.info(f"Successfully generated email for {lead_name}")
                elif hasattr(email_result, 'raw'):
                    # Fallback to raw output if pydantic not available
                    generated_email = GeneratedEmail(
                        subject=f"AI Strategy Discussion for {lead_analysis.company_info.company_name}",
                        body=email_result.raw,
                        personalization_score=0.8,
                        key_talking_points=["AI ROI", "GenAI Services"],
                        call_to_action="Schedule a brief call to discuss your AI strategy",
                        estimated_read_time=30
                    )
                    emails.append(generated_email)
                    logger.info(f"Generated email from raw output for {lead_name}")
                
            except Exception as e:
                logger.error(f"Error generating email for lead {i}: {str(e)}")
                self.state.errors.append({
                    "lead": f"Lead {i}",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })
                continue
        
        self.state.generated_emails = emails
        self.state.campaign_metrics.emails_sent = len(emails)
        logger.info(f"Email generation complete: {len(emails)} emails generated")

    @listen(generate_emails)
    def finalize_campaign(self):
        """Finalize the campaign and prepare summary"""
        logger.info("Finalizing SDR campaign...")
        
        self.state.end_time = datetime.now()
        
        # Calculate campaign metrics
        total_time = (self.state.end_time - self.state.start_time).total_seconds()
        successful_analyses = len(self.state.analyzed_leads)
        successful_emails = len(self.state.generated_emails)
        
        # Update campaign metrics
        self.state.campaign_metrics.total_leads = len(self.state.leads)
        self.state.campaign_metrics.emails_sent = successful_emails
        
        if successful_analyses > 0:
            avg_score = sum(lead.readiness_score.score for lead in self.state.analyzed_leads) / successful_analyses
            self.state.campaign_metrics.average_score = round(avg_score, 2)
        
        # Calculate conversion rate (analysis success rate)
        if len(self.state.leads) > 0:
            self.state.campaign_metrics.conversion_rate = round(successful_emails / len(self.state.leads), 3)
        
        # Save results to database (optional)
        try:
            self.db_manager.save_campaign_results(self.state)
        except Exception as e:
            logger.warning(f"Could not save to database: {str(e)}")
        
        # Print campaign summary
        self._print_campaign_summary(total_time)
        
        logger.info(f"Campaign completed in {total_time:.2f} seconds")

    def _print_campaign_summary(self, total_time: float):
        """Print a formatted campaign summary"""
        print("\n" + "="*80)
        print("🎯 SDR CAMPAIGN SUMMARY")
        print("="*80)
        print(f"Session ID: {self.state.session_id}")
        print(f"Processing Time: {total_time:.2f} seconds")
        print(f"Total Leads: {len(self.state.leads)}")
        print(f"Successfully Analyzed: {len(self.state.analyzed_leads)}")
        print(f"Emails Generated: {len(self.state.generated_emails)}")
        print(f"Success Rate: {self.state.campaign_metrics.conversion_rate:.1%}")
        
        if self.state.analyzed_leads:
            print(f"Average Lead Score: {self.state.campaign_metrics.average_score}/100")
        
        if self.state.errors:
            print(f"Errors Encountered: {len(self.state.errors)}")
        
        print("\n📧 GENERATED EMAILS:")
        print("-" * 40)
        
        for i, email in enumerate(self.state.generated_emails):
            lead_name = self.state.analyzed_leads[i].personal_info.name if i < len(self.state.analyzed_leads) else f"Lead {i+1}"
            print(f"\n{i+1}. Email for {lead_name}")
            print(f"Subject: {email.subject}")
            print(f"Personalization Score: {email.personalization_score:.1%}")
            print(f"Read Time: ~{email.estimated_read_time}s")
            print("Body Preview:")
            print(email.body[:200] + "..." if len(email.body) > 200 else email.body)
            print("-" * 40)
        
        if self.state.errors:
            print("\n⚠️  ERRORS:")
            for error in self.state.errors:
                print(f"• {error['lead']}: {error['error']}")
        
        print("="*80)

    def get_campaign_results(self) -> Dict[str, Any]:
        """Get campaign results as a dictionary for API responses"""
        return {
            "session_id": self.state.session_id,
            "status": "completed" if self.state.end_time else "processing",
            "metrics": self.state.campaign_metrics.model_dump(),
            "leads_analyzed": len(self.state.analyzed_leads),
            "emails_generated": len(self.state.generated_emails),
            "processing_time": (
                (self.state.end_time - self.state.start_time).total_seconds() 
                if self.state.end_time else None
            ),
            "errors": self.state.errors,
            "leads": [lead.model_dump() for lead in self.state.leads],
            "results": [lead.model_dump() for lead in self.state.analyzed_leads],
            "emails": [email.model_dump() for email in self.state.generated_emails]
        }

# === Entry Point Functions ===
def kickoff_flow(leads: Optional[List[LeadInput]] = None) -> SDRAssistantFlow:
    """
    Start the SDR Assistant Flow with optional custom leads
    
    Args:
        leads: Optional list of leads to process. If None, uses sample data.
    
    Returns:
        The flow instance with results
    """
    flow = SDRAssistantFlow()
    
    # Override with custom leads if provided
    if leads:
        flow.state.leads = leads
        flow.state.campaign_metrics.total_leads = len(leads)
        
        # Initialize processing status for custom leads
        flow.state.processing_status = {}
        for lead in leads:
            lead_id = f"{lead.name}_{lead.company}".replace(" ", "_").lower()
            flow.state.processing_status[lead_id] = "pending"
    
    return flow