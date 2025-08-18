#!/usr/bin/env python3
"""
Script to create all 60 boilerplates with tailored content for each project.
"""

import os
import json
from pathlib import Path

# Project configurations with tailored content
PROJECTS = {
    "ai-powered-medical-diagnosis-assistant": {
        "title": "AI-Powered Medical Diagnosis Assistant",
        "description": "Medical diagnosis system with AI-powered symptom analysis",
        "models": ["User", "Patient", "Diagnosis"],
        "endpoints": ["/diagnosis/analyze", "/patients/", "/patients/{id}/diagnosis"],
        "ai_features": ["symptom analysis", "diagnosis recommendations"],
        "special_configs": ["HIPAA compliance", "medical knowledge base"]
    },
    "ai-content-localizer": {
        "title": "AI Content Localizer",
        "description": "AI-powered content localization and translation system",
        "models": ["User", "Content", "Translation", "Locale"],
        "endpoints": ["/localize/translate", "/content/", "/translations/", "/locales/"],
        "ai_features": ["content translation", "cultural adaptation"],
        "special_configs": ["translation memory", "cultural context"]
    },
    "ai-driven-music-composition-tool": {
        "title": "AI-Driven Music Composition Tool",
        "description": "AI-powered music composition and arrangement system",
        "models": ["User", "Composition", "Track", "Instrument"],
        "endpoints": ["/music/compose", "/compositions/", "/tracks/", "/instruments/"],
        "ai_features": ["music generation", "arrangement suggestions"],
        "special_configs": ["music theory", "instrument libraries"]
    },
    "ai-email-campaign-writer": {
        "title": "AI Email Campaign Writer",
        "description": "AI-powered email campaign creation and optimization",
        "models": ["User", "Campaign", "Email", "Template"],
        "endpoints": ["/email/generate", "/campaigns/", "/emails/", "/templates/"],
        "ai_features": ["email generation", "campaign optimization"],
        "special_configs": ["email templates", "conversion tracking"]
    },
    "ai-meeting-notes---action-items": {
        "title": "AI Meeting Notes & Action Items",
        "description": "AI-powered meeting transcription and action item extraction",
        "models": ["User", "Meeting", "Note", "ActionItem"],
        "endpoints": ["/meeting/transcribe", "/meetings/", "/notes/", "/action-items/"],
        "ai_features": ["meeting transcription", "action extraction"],
        "special_configs": ["voice recognition", "task management"]
    },
    "ai-powered-code-review---refactoring-assistant": {
        "title": "AI-Powered Code Review & Refactoring Assistant",
        "description": "Code review and refactoring system with AI-powered suggestions",
        "models": ["User", "Project", "Review", "Suggestion"],
        "endpoints": ["/review/analyze", "/projects/", "/reviews/", "/suggestions/"],
        "ai_features": ["code analysis", "refactoring suggestions"],
        "special_configs": ["code parsing", "quality metrics"]
    },
    "ai-powered-financial-analysis---trading-bot": {
        "title": "AI-Powered Financial Analysis & Trading Bot",
        "description": "Financial analysis and trading system with AI-powered decisions",
        "models": ["User", "Portfolio", "Trade", "Analysis"],
        "endpoints": ["/trading/analyze", "/portfolios/", "/trades/", "/analysis/"],
        "ai_features": ["market analysis", "trading decisions"],
        "special_configs": ["market data", "risk management"]
    },
    "ai-powered-legal-document-analysis---contract-negotiation": {
        "title": "AI-Powered Legal Document Analysis & Contract Negotiation",
        "description": "Legal document analysis system with AI-powered contract review",
        "models": ["User", "Document", "Contract", "Analysis"],
        "endpoints": ["/analysis/review", "/documents/", "/contracts/", "/analyses/"],
        "ai_features": ["document analysis", "contract review"],
        "special_configs": ["legal compliance", "risk assessment"]
    },
    "ai-powered-resume-and-cover-letter-tailor": {
        "title": "AI-Powered Resume & Cover Letter Tailor",
        "description": "Resume and cover letter tailoring with AI-powered optimization",
        "models": ["User", "Resume", "CoverLetter", "Optimization"],
        "endpoints": ["/tailor/optimize", "/resumes/", "/cover-letters/", "/optimizations/"],
        "ai_features": ["content optimization", "job matching"],
        "special_configs": ["job descriptions", "industry templates"]
    },
    "ai-powered-resume-parser---job-matcher": {
        "title": "AI-Powered Resume Parser & Job Matcher",
        "description": "Resume parsing and job matching system with AI-powered analysis",
        "models": ["User", "Resume", "Job", "Match"],
        "endpoints": ["/parse/resume", "/resumes/", "/jobs/", "/matches/"],
        "ai_features": ["resume parsing", "job matching"],
        "special_configs": ["skill extraction", "matching algorithms"]
    },
    "auto-blog-post-series-creator": {
        "title": "Auto Blog Post Series Creator",
        "description": "AI-powered blog post series creation and content planning",
        "models": ["User", "Series", "Post", "Topic"],
        "endpoints": ["/blog/create-series", "/series/", "/posts/", "/topics/"],
        "ai_features": ["content planning", "series generation"],
        "special_configs": ["content calendar", "seo optimization"]
    },
    "automated-market-research-and-report-generation-team": {
        "title": "Automated Market Research & Report Generation Team",
        "description": "Automated market research system with AI-powered report generation",
        "models": ["User", "Research", "Report", "Market"],
        "endpoints": ["/research/conduct", "/researches/", "/reports/", "/markets/"],
        "ai_features": ["market analysis", "report generation"],
        "special_configs": ["data sources", "report templates"]
    },
    "automated-research-department": {
        "title": "Automated Research Department",
        "description": "Automated research system with AI-powered data analysis",
        "models": ["User", "Research", "Data", "Analysis"],
        "endpoints": ["/research/analyze", "/researches/", "/data/", "/analyses/"],
        "ai_features": ["data analysis", "research automation"],
        "special_configs": ["research protocols", "data validation"]
    },
    "automated-software-development-team": {
        "title": "Automated Software Development Team",
        "description": "Automated software development system with AI-powered collaboration",
        "models": ["User", "Project", "Code", "Collaboration"],
        "endpoints": ["/development/collaborate", "/projects/", "/code/", "/collaborations/"],
        "ai_features": ["code generation", "team coordination"],
        "special_configs": ["version control", "code review"]
    },
    "autonomous-data-science-pipeline": {
        "title": "Autonomous Data Science Pipeline",
        "description": "Autonomous data science pipeline with AI-powered analysis",
        "models": ["User", "Pipeline", "Dataset", "Model"],
        "endpoints": ["/pipeline/run", "/pipelines/", "/datasets/", "/models/"],
        "ai_features": ["data analysis", "model training"],
        "special_configs": ["mlops", "model monitoring"]
    },
    "autonomous-financial-trading---portfolio-management": {
        "title": "Autonomous Financial Trading & Portfolio Management",
        "description": "Autonomous financial trading system with portfolio management",
        "models": ["User", "Portfolio", "Trade", "Strategy"],
        "endpoints": ["/trading/execute", "/portfolios/", "/trades/", "/strategies/"],
        "ai_features": ["trading execution", "portfolio optimization"],
        "special_configs": ["risk management", "market data"]
    },
    "autonomous-learning-and-research-assistant": {
        "title": "Autonomous Learning & Research Assistant",
        "description": "Autonomous learning system with AI-powered research assistance",
        "models": ["User", "Learning", "Research", "Progress"],
        "endpoints": ["/learning/assist", "/learnings/", "/researches/", "/progress/"],
        "ai_features": ["learning assistance", "research automation"],
        "special_configs": ["learning paths", "knowledge base"]
    },
    "autonomous-research---report-generation-system": {
        "title": "Autonomous Research & Report Generation System",
        "description": "Autonomous research system with AI-powered report generation",
        "models": ["User", "Research", "Report", "Generation"],
        "endpoints": ["/research/conduct", "/researches/", "/reports/", "/generations/"],
        "ai_features": ["research automation", "report generation"],
        "special_configs": ["data sources", "report templates"]
    },
    "b2b-sales-prospecting-ai": {
        "title": "B2B Sales Prospecting AI",
        "description": "B2B sales prospecting system with AI-powered lead generation",
        "models": ["User", "Prospect", "Lead", "Campaign"],
        "endpoints": ["/prospect/generate", "/prospects/", "/leads/", "/campaigns/"],
        "ai_features": ["lead generation", "prospect scoring"],
        "special_configs": ["crm integration", "lead nurturing"]
    },
    "conference-planning-crew": {
        "title": "Conference Planning Crew",
        "description": "Conference planning system with AI-powered event management",
        "models": ["User", "Conference", "Event", "Schedule"],
        "endpoints": ["/conference/plan", "/conferences/", "/events/", "/schedules/"],
        "ai_features": ["event planning", "schedule optimization"],
        "special_configs": ["venue management", "attendee tracking"]
    },
    "creative-content-generation-and-marketing-team": {
        "title": "Creative Content Generation & Marketing Team",
        "description": "Creative content generation system with marketing optimization",
        "models": ["User", "Content", "Campaign", "Creative"],
        "endpoints": ["/content/generate", "/contents/", "/campaigns/", "/creatives/"],
        "ai_features": ["content generation", "marketing optimization"],
        "special_configs": ["brand guidelines", "campaign tracking"]
    },
    "creative-content-generator-for-social-media": {
        "title": "Creative Content Generator for Social Media",
        "description": "Social media content generation system with AI-powered creativity",
        "models": ["User", "Content", "Platform", "Creative"],
        "endpoints": ["/social/generate", "/contents/", "/platforms/", "/creatives/"],
        "ai_features": ["content generation", "platform optimization"],
        "special_configs": ["social media api", "engagement metrics"]
    },
    "customer-support-chatbot-with-hallucination-correction": {
        "title": "Customer Support Chatbot with Hallucination Correction",
        "description": "Customer support chatbot with AI-powered hallucination detection",
        "models": ["User", "Customer", "Conversation", "Correction"],
        "endpoints": ["/chat/support", "/customers/", "/conversations/", "/corrections/"],
        "ai_features": ["chatbot responses", "hallucination detection"],
        "special_configs": ["knowledge base", "fact checking"]
    },
    "cybersecurity-threat-analysis-team": {
        "title": "Cybersecurity Threat Analysis Team",
        "description": "Cybersecurity threat analysis system with AI-powered detection",
        "models": ["User", "Threat", "Analysis", "Alert"],
        "endpoints": ["/security/analyze", "/threats/", "/analyses/", "/alerts/"],
        "ai_features": ["threat detection", "risk assessment"],
        "special_configs": ["security protocols", "threat intelligence"]
    },
    "dynamic-video-storyboard-creator": {
        "title": "Dynamic Video Storyboard Creator",
        "description": "Dynamic video storyboard creation with AI-powered visualization",
        "models": ["User", "Storyboard", "Scene", "Visual"],
        "endpoints": ["/video/storyboard", "/storyboards/", "/scenes/", "/visuals/"],
        "ai_features": ["storyboard generation", "visual creation"],
        "special_configs": ["video templates", "animation tools"]
    },
    "e-commerce-customer-service-and-fraud-detection": {
        "title": "E-commerce Customer Service & Fraud Detection",
        "description": "E-commerce system with customer service and fraud detection",
        "models": ["User", "Customer", "Order", "Fraud"],
        "endpoints": ["/ecommerce/service", "/customers/", "/orders/", "/fraud/"],
        "ai_features": ["customer service", "fraud detection"],
        "special_configs": ["payment processing", "fraud prevention"]
    },
    "e-commerce-launch-crew": {
        "title": "E-commerce Launch Crew",
        "description": "E-commerce launch system with AI-powered optimization",
        "models": ["User", "Store", "Product", "Launch"],
        "endpoints": ["/ecommerce/launch", "/stores/", "/products/", "/launches/"],
        "ai_features": ["launch optimization", "market analysis"],
        "special_configs": ["store setup", "marketing automation"]
    },
    "financial-portfolio-management-system": {
        "title": "Financial Portfolio Management System",
        "description": "Financial portfolio management system with AI-powered optimization",
        "models": ["User", "Portfolio", "Asset", "Strategy"],
        "endpoints": ["/portfolio/manage", "/portfolios/", "/assets/", "/strategies/"],
        "ai_features": ["portfolio optimization", "risk management"],
        "special_configs": ["market data", "investment tracking"]
    },
    "intelligent-customer-support-chatbot": {
        "title": "Intelligent Customer Support Chatbot",
        "description": "Intelligent customer support chatbot with AI-powered responses",
        "models": ["User", "Customer", "Conversation", "Response"],
        "endpoints": ["/chat/support", "/customers/", "/conversations/", "/responses/"],
        "ai_features": ["response generation", "intent recognition"],
        "special_configs": ["conversation history", "knowledge base"]
    },
    "intelligent-document-processing---knowledge-base": {
        "title": "Intelligent Document Processing & Knowledge Base",
        "description": "Document processing system with knowledge base management",
        "models": ["User", "Document", "Knowledge", "Processing"],
        "endpoints": ["/document/process", "/documents/", "/knowledge/", "/processing/"],
        "ai_features": ["document processing", "knowledge extraction"],
        "special_configs": ["ocr technology", "search indexing"]
    },
    "intelligent-healthcare-diagnosis---treatment-planning": {
        "title": "Intelligent Healthcare Diagnosis & Treatment Planning",
        "description": "Healthcare diagnosis system with treatment planning",
        "models": ["User", "Patient", "Diagnosis", "Treatment"],
        "endpoints": ["/healthcare/diagnose", "/patients/", "/diagnoses/", "/treatments/"],
        "ai_features": ["diagnosis assistance", "treatment planning"],
        "special_configs": ["medical knowledge", "treatment protocols"]
    },
    "intelligent-smart-city-management-system": {
        "title": "Intelligent Smart City Management System",
        "description": "Smart city management system with AI-powered urban optimization",
        "models": ["User", "City", "Service", "Optimization"],
        "endpoints": ["/city/optimize", "/cities/", "/services/", "/optimizations/"],
        "ai_features": ["urban optimization", "service planning"],
        "special_configs": ["city infrastructure", "public services"]
    },
    "intelligent-supply-chain-optimization-system": {
        "title": "Intelligent Supply Chain Optimization System",
        "description": "Supply chain optimization system with AI-powered planning",
        "models": ["User", "SupplyChain", "Inventory", "Optimization"],
        "endpoints": ["/supply-chain/optimize", "/supply-chains/", "/inventory/", "/optimizations/"],
        "ai_features": ["inventory optimization", "demand forecasting"],
        "special_configs": ["supplier management", "demand planning"]
    },
    "learning-path-generator": {
        "title": "Learning Path Generator",
        "description": "Learning path generation system with AI-powered personalization",
        "models": ["User", "Learning", "Path", "Progress"],
        "endpoints": ["/learning/generate-path", "/learnings/", "/paths/", "/progress/"],
        "ai_features": ["path generation", "progress tracking"],
        "special_configs": ["learning objectives", "skill assessment"]
    },
    "local-retrieval-augmented-generation--rag--system": {
        "title": "Local Retrieval Augmented Generation (RAG) System",
        "description": "Local RAG system with AI-powered document retrieval",
        "models": ["User", "Document", "Query", "Response"],
        "endpoints": ["/rag/query", "/documents/", "/queries/", "/responses/"],
        "ai_features": ["document retrieval", "response generation"],
        "special_configs": ["vector database", "embedding models"]
    },
    "multi-agent-content-creation---marketing-system": {
        "title": "Multi-Agent Content Creation & Marketing System",
        "description": "Multi-agent content creation system with marketing optimization",
        "models": ["User", "Agent", "Content", "Campaign"],
        "endpoints": ["/agent/create", "/agents/", "/contents/", "/campaigns/"],
        "ai_features": ["content creation", "agent coordination"],
        "special_configs": ["agent roles", "workflow management"]
    },
    "multilingual-customer-support-reply-generator": {
        "title": "Multilingual Customer Support Reply Generator",
        "description": "Multilingual customer support system with AI-powered responses",
        "models": ["User", "Customer", "Language", "Response"],
        "endpoints": ["/support/reply", "/customers/", "/languages/", "/responses/"],
        "ai_features": ["multilingual responses", "intent recognition"],
        "special_configs": ["language detection", "translation services"]
    },
    "multimodal-ai-medical-assistant": {
        "title": "Multimodal AI Medical Assistant",
        "description": "Multimodal medical assistant with AI-powered diagnosis",
        "models": ["User", "Patient", "Image", "Diagnosis"],
        "endpoints": ["/medical/assist", "/patients/", "/images/", "/diagnoses/"],
        "ai_features": ["image analysis", "diagnosis assistance"],
        "special_configs": ["medical imaging", "diagnostic protocols"]
    },
    "personal-ai-powered-codebase-documentation-tool": {
        "title": "Personal AI-Powered Codebase Documentation Tool",
        "description": "Codebase documentation tool with AI-powered generation",
        "models": ["User", "Codebase", "Documentation", "Generation"],
        "endpoints": ["/docs/generate", "/codebases/", "/documentations/", "/generations/"],
        "ai_features": ["documentation generation", "code analysis"],
        "special_configs": ["code parsing", "documentation templates"]
    },
    "personal-brain-agent-system": {
        "title": "Personal Brain Agent System",
        "description": "Personal brain agent system with AI-powered knowledge management",
        "models": ["User", "Knowledge", "Memory", "Agent"],
        "endpoints": ["/brain/process", "/knowledge/", "/memories/", "/agents/"],
        "ai_features": ["knowledge processing", "memory management"],
        "special_configs": ["knowledge graph", "memory retrieval"]
    },
    "personalized-career-coach-agent-system": {
        "title": "Personalized Career Coach Agent System",
        "description": "Personalized career coaching system with AI-powered guidance",
        "models": ["User", "Career", "Goal", "Coach"],
        "endpoints": ["/career/coach", "/careers/", "/goals/", "/coaches/"],
        "ai_features": ["career guidance", "goal tracking"],
        "special_configs": ["career paths", "skill assessment"]
    },
    "podcast-to-blog-post-converter": {
        "title": "Podcast to Blog Post Converter",
        "description": "Podcast to blog post conversion system with AI-powered transcription",
        "models": ["User", "Podcast", "Transcription", "Blog"],
        "endpoints": ["/podcast/convert", "/podcasts/", "/transcriptions/", "/blogs/"],
        "ai_features": ["audio transcription", "content conversion"],
        "special_configs": ["audio processing", "seo optimization"]
    },
    "real-estate-investment-finder": {
        "title": "Real Estate Investment Finder",
        "description": "Real estate investment finding system with AI-powered analysis",
        "models": ["User", "Property", "Investment", "Analysis"],
        "endpoints": ["/real-estate/find", "/properties/", "/investments/", "/analyses/"],
        "ai_features": ["property analysis", "investment recommendations"],
        "special_configs": ["market data", "investment criteria"]
    },
    "real-time-ai-content-moderation-system": {
        "title": "Real-Time AI Content Moderation System",
        "description": "Real-time content moderation system with AI-powered filtering",
        "models": ["User", "Content", "Moderation", "Violation"],
        "endpoints": ["/moderation/analyze", "/contents/", "/moderations/", "/violations/"],
        "ai_features": ["content filtering", "violation detection"],
        "special_configs": ["content policies", "moderation rules"]
    },
    "real-time-ai-powered-text-to-3d-model-generator": {
        "title": "Real-Time AI-Powered Text to 3D Model Generator",
        "description": "Text to 3D model generation system with AI-powered creation",
        "models": ["User", "Model", "Generation", "Text"],
        "endpoints": ["/3d/generate", "/models/", "/generations/", "/texts/"],
        "ai_features": ["3d generation", "text processing"],
        "special_configs": ["3d rendering", "model formats"]
    },
    "realistic-synthetic-data-generator": {
        "title": "Realistic Synthetic Data Generator",
        "description": "Synthetic data generation system with AI-powered realism",
        "models": ["User", "Dataset", "Generation", "Schema"],
        "endpoints": ["/synthetic/generate", "/datasets/", "/generations/", "/schemas/"],
        "ai_features": ["data generation", "realism enhancement"],
        "special_configs": ["data privacy", "generation rules"]
    },
    "recruitment-flow-ai": {
        "title": "Recruitment Flow AI",
        "description": "Recruitment flow system with AI-powered candidate management",
        "models": ["User", "Candidate", "Position", "Flow"],
        "endpoints": ["/recruitment/manage", "/candidates/", "/positions/", "/flows/"],
        "ai_features": ["candidate matching", "flow optimization"],
        "special_configs": ["recruitment pipeline", "candidate scoring"]
    },
    "resume---cover-letter-personalizer": {
        "title": "Resume & Cover Letter Personalizer",
        "description": "Resume and cover letter personalization system",
        "models": ["User", "Resume", "CoverLetter", "Personalization"],
        "endpoints": ["/personalize/resume", "/resumes/", "/cover-letters/", "/personalizations/"],
        "ai_features": ["content personalization", "job matching"],
        "special_configs": ["job descriptions", "industry templates"]
    },
    "ai-powered-agricultural-optimization-system": {
        "title": "AI-Powered Agricultural Optimization System",
        "description": "Agricultural optimization system with AI-powered crop management",
        "models": ["User", "Farm", "Crop", "SensorData"],
        "endpoints": ["/optimization/analyze", "/farms/", "/farms/{id}/crops", "/sensor-data/"],
        "ai_features": ["crop optimization", "irrigation scheduling"],
        "special_configs": ["weather API", "soil data integration"]
    },
    "ai-powered-autonomous-vehicle-simulation": {
        "title": "AI-Powered Autonomous Vehicle Simulation",
        "description": "Autonomous vehicle simulation system with AI-powered decision making",
        "models": ["User", "Vehicle", "Simulation", "SensorData"],
        "endpoints": ["/simulation/run", "/vehicles/", "/simulations/", "/sensor-data/"],
        "ai_features": ["decision making", "safety analysis"],
        "special_configs": ["CARLA simulator", "safety thresholds"]
    },
    "ai-powered-blockchain-smart-contract-analyzer": {
        "title": "AI-Powered Blockchain Smart Contract Analyzer",
        "description": "Smart contract analysis system with AI-powered security and vulnerability detection",
        "models": ["User", "Contract", "Analysis", "Vulnerability"],
        "endpoints": ["/analysis/analyze", "/contracts/", "/contracts/{id}/analysis", "/vulnerabilities/"],
        "ai_features": ["security analysis", "vulnerability detection"],
        "special_configs": ["blockchain integration", "security scoring"]
    },
    "ai-powered-code-review-refactoring-assistant": {
        "title": "AI-Powered Code Review & Refactoring Assistant",
        "description": "Code review and refactoring system with AI-powered suggestions",
        "models": ["User", "Project", "Review", "Suggestion"],
        "endpoints": ["/review/analyze", "/projects/", "/projects/{id}/reviews", "/suggestions/"],
        "ai_features": ["code analysis", "refactoring suggestions"],
        "special_configs": ["code parsing", "quality metrics"]
    },
    "ai-powered-construction-management-system": {
        "title": "AI-Powered Construction Management System",
        "description": "Construction project management with AI-powered optimization",
        "models": ["User", "Project", "Task", "Resource"],
        "endpoints": ["/optimization/analyze", "/projects/", "/projects/{id}/tasks", "/resources/"],
        "ai_features": ["project optimization", "resource allocation"],
        "special_configs": ["project scheduling", "cost estimation"]
    },
    "ai-powered-content-moderation-system": {
        "title": "AI-Powered Content Moderation System",
        "description": "Content moderation system with AI-powered filtering",
        "models": ["User", "Content", "Moderation", "Violation"],
        "endpoints": ["/moderation/analyze", "/content/", "/content/{id}/moderate", "/violations/"],
        "ai_features": ["content filtering", "violation detection"],
        "special_configs": ["content policies", "moderation rules"]
    },
    "ai-powered-creative-writing-assistant": {
        "title": "AI-Powered Creative Writing Assistant",
        "description": "Creative writing assistant with AI-powered content generation",
        "models": ["User", "Project", "Content", "Suggestion"],
        "endpoints": ["/writing/generate", "/projects/", "/projects/{id}/content", "/suggestions/"],
        "ai_features": ["content generation", "writing suggestions"],
        "special_configs": ["writing styles", "content templates"]
    },
    "ai-powered-customer-support-chatbot": {
        "title": "AI-Powered Customer Support Chatbot",
        "description": "Customer support chatbot with AI-powered responses",
        "models": ["User", "Customer", "Conversation", "Response"],
        "endpoints": ["/chat/respond", "/customers/", "/conversations/", "/responses/"],
        "ai_features": ["response generation", "intent recognition"],
        "special_configs": ["conversation history", "knowledge base"]
    },
    "ai-powered-education-analytics-platform": {
        "title": "AI-Powered Education Analytics Platform",
        "description": "Education analytics platform with AI-powered insights",
        "models": ["User", "Student", "Course", "Analytics"],
        "endpoints": ["/analytics/analyze", "/students/", "/courses/", "/analytics/"],
        "ai_features": ["performance analysis", "learning insights"],
        "special_configs": ["learning metrics", "progress tracking"]
    },
    "ai-powered-energy-management-system": {
        "title": "AI-Powered Energy Management System",
        "description": "Energy management system with AI-powered optimization",
        "models": ["User", "Facility", "Device", "Consumption"],
        "endpoints": ["/optimization/analyze", "/facilities/", "/devices/", "/consumption/"],
        "ai_features": ["energy optimization", "consumption prediction"],
        "special_configs": ["energy monitoring", "efficiency metrics"]
    },
    "ai-powered-financial-analysis-trading-bot": {
        "title": "AI-Powered Financial Analysis & Trading Bot",
        "description": "Financial analysis and trading system with AI-powered decisions",
        "models": ["User", "Portfolio", "Trade", "Analysis"],
        "endpoints": ["/trading/analyze", "/portfolios/", "/trades/", "/analysis/"],
        "ai_features": ["market analysis", "trading decisions"],
        "special_configs": ["market data", "risk management"]
    },
    "ai-powered-game-development-assistant": {
        "title": "AI-Powered Game Development Assistant",
        "description": "Game development assistant with AI-powered content generation",
        "models": ["User", "Game", "Asset", "Generation"],
        "endpoints": ["/generation/create", "/games/", "/assets/", "/generations/"],
        "ai_features": ["asset generation", "game mechanics"],
        "special_configs": ["game engines", "asset libraries"]
    },
    "ai-powered-hospitality-management-system": {
        "title": "AI-Powered Hospitality Management System",
        "description": "Hospitality management system with AI-powered optimization",
        "models": ["User", "Property", "Booking", "Service"],
        "endpoints": ["/optimization/analyze", "/properties/", "/bookings/", "/services/"],
        "ai_features": ["booking optimization", "service recommendations"],
        "special_configs": ["property management", "guest services"]
    },
    "ai-powered-human-resources-management-system": {
        "title": "AI-Powered Human Resources Management System",
        "description": "HR management system with AI-powered recruitment and analytics",
        "models": ["User", "Employee", "Position", "Recruitment"],
        "endpoints": ["/recruitment/analyze", "/employees/", "/positions/", "/recruitments/"],
        "ai_features": ["candidate matching", "performance analysis"],
        "special_configs": ["recruitment pipeline", "employee analytics"]
    },
    "ai-powered-insurance-risk-assessment-system": {
        "title": "AI-Powered Insurance Risk Assessment System",
        "description": "Insurance risk assessment system with AI-powered analysis",
        "models": ["User", "Policy", "Claim", "Risk"],
        "endpoints": ["/risk/assess", "/policies/", "/claims/", "/risks/"],
        "ai_features": ["risk assessment", "claim analysis"],
        "special_configs": ["risk models", "fraud detection"]
    },
    "ai-powered-language-learning-platform": {
        "title": "AI-Powered Language Learning Platform",
        "description": "Language learning platform with AI-powered tutoring",
        "models": ["User", "Student", "Lesson", "Progress"],
        "endpoints": ["/learning/analyze", "/students/", "/lessons/", "/progress/"],
        "ai_features": ["personalized learning", "progress tracking"],
        "special_configs": ["language models", "learning paths"]
    },
    "ai-powered-legal-document-analysis-contract-negotiation": {
        "title": "AI-Powered Legal Document Analysis & Contract Negotiation",
        "description": "Legal document analysis system with AI-powered contract review",
        "models": ["User", "Document", "Contract", "Analysis"],
        "endpoints": ["/analysis/review", "/documents/", "/contracts/", "/analyses/"],
        "ai_features": ["document analysis", "contract review"],
        "special_configs": ["legal compliance", "risk assessment"]
    },
    "ai-powered-logistics-optimization-system": {
        "title": "AI-Powered Logistics Optimization System",
        "description": "Logistics optimization system with AI-powered routing",
        "models": ["User", "Shipment", "Route", "Optimization"],
        "endpoints": ["/optimization/route", "/shipments/", "/routes/", "/optimizations/"],
        "ai_features": ["route optimization", "delivery prediction"],
        "special_configs": ["transportation modes", "real-time tracking"]
    },
    "ai-powered-manufacturing-optimization-system": {
        "title": "AI-Powered Manufacturing Optimization System",
        "description": "Manufacturing optimization system with AI-powered production planning",
        "models": ["User", "Factory", "Production", "Optimization"],
        "endpoints": ["/optimization/produce", "/factories/", "/productions/", "/optimizations/"],
        "ai_features": ["production optimization", "quality control"],
        "special_configs": ["production planning", "quality metrics"]
    },
    "ai-powered-marketing-automation-platform": {
        "title": "AI-Powered Marketing Automation Platform",
        "description": "Marketing automation platform with AI-powered campaign optimization",
        "models": ["User", "Campaign", "Audience", "Performance"],
        "endpoints": ["/automation/optimize", "/campaigns/", "/audiences/", "/performance/"],
        "ai_features": ["campaign optimization", "audience targeting"],
        "special_configs": ["marketing channels", "conversion tracking"]
    },
    "ai-powered-music-composition-tool": {
        "title": "AI-Powered Music Composition Tool",
        "description": "Music composition tool with AI-powered generation",
        "models": ["User", "Composition", "Track", "Generation"],
        "endpoints": ["/composition/generate", "/compositions/", "/tracks/", "/generations/"],
        "ai_features": ["music generation", "composition assistance"],
        "special_configs": ["music theory", "instrument libraries"]
    },
    "ai-powered-personal-fitness-coach": {
        "title": "AI-Powered Personal Fitness Coach",
        "description": "Personal fitness coach with AI-powered workout planning",
        "models": ["User", "Client", "Workout", "Progress"],
        "endpoints": ["/coaching/plan", "/clients/", "/workouts/", "/progress/"],
        "ai_features": ["workout planning", "progress tracking"],
        "special_configs": ["fitness goals", "exercise library"]
    },
    "ai-powered-project-management-platform": {
        "title": "AI-Powered Project Management Platform",
        "description": "Project management platform with AI-powered task optimization",
        "models": ["User", "Project", "Task", "Timeline"],
        "endpoints": ["/management/optimize", "/projects/", "/tasks/", "/timelines/"],
        "ai_features": ["task optimization", "timeline prediction"],
        "special_configs": ["project templates", "resource allocation"]
    },
    "ai-powered-real-estate-investment-analyzer": {
        "title": "AI-Powered Real Estate Investment Analyzer",
        "description": "Real estate investment analyzer with AI-powered market analysis",
        "models": ["User", "Property", "Market", "Analysis"],
        "endpoints": ["/investment/analyze", "/properties/", "/markets/", "/analyses/"],
        "ai_features": ["market analysis", "investment recommendations"],
        "special_configs": ["market data", "investment criteria"]
    },
    "ai-powered-resume-cover-letter-tailor": {
        "title": "AI-Powered Resume & Cover Letter Tailor",
        "description": "Resume and cover letter tailoring with AI-powered optimization",
        "models": ["User", "Resume", "CoverLetter", "Optimization"],
        "endpoints": ["/tailor/optimize", "/resumes/", "/cover-letters/", "/optimizations/"],
        "ai_features": ["content optimization", "job matching"],
        "special_configs": ["job descriptions", "industry templates"]
    },
    "ai-powered-smart-city-management-system": {
        "title": "AI-Powered Smart City Management System",
        "description": "Smart city management system with AI-powered urban optimization",
        "models": ["User", "City", "Service", "Optimization"],
        "endpoints": ["/city/optimize", "/cities/", "/services/", "/optimizations/"],
        "ai_features": ["urban optimization", "service planning"],
        "special_configs": ["city infrastructure", "public services"]
    },
    "ai-powered-supply-chain-optimization-system": {
        "title": "AI-Powered Supply Chain Optimization System",
        "description": "Supply chain optimization system with AI-powered planning",
        "models": ["User", "SupplyChain", "Inventory", "Optimization"],
        "endpoints": ["/supply-chain/optimize", "/supply-chains/", "/inventory/", "/optimizations/"],
        "ai_features": ["inventory optimization", "demand forecasting"],
        "special_configs": ["supplier management", "demand planning"]
    },
    "ai-powered-synthetic-data-generator": {
        "title": "AI-Powered Synthetic Data Generator",
        "description": "Synthetic data generator with AI-powered data creation",
        "models": ["User", "Dataset", "Generation", "Schema"],
        "endpoints": ["/generation/create", "/datasets/", "/generations/", "/schemas/"],
        "ai_features": ["data generation", "schema creation"],
        "special_configs": ["data privacy", "generation rules"]
    },
    "ai-powered-video-content-generator": {
        "title": "AI-Powered Video Content Generator",
        "description": "Video content generator with AI-powered creation",
        "models": ["User", "Video", "Asset", "Generation"],
        "endpoints": ["/video/generate", "/videos/", "/assets/", "/generations/"],
        "ai_features": ["video generation", "content creation"],
        "special_configs": ["video templates", "asset libraries"]
    },
    "ai-powered-voice-based-meeting-assistant-note-taker": {
        "title": "AI-Powered Voice-Based Meeting Assistant & Note Taker",
        "description": "Voice-based meeting assistant with AI-powered transcription and summarization",
        "models": ["User", "Meeting", "Transcription", "Summary"],
        "endpoints": ["/meeting/transcribe", "/meetings/", "/transcriptions/", "/summaries/"],
        "ai_features": ["voice transcription", "meeting summarization"],
        "special_configs": ["voice recognition", "meeting analytics"]
    },
    "ai-powered-voice-controlled-smart-home-manager": {
        "title": "AI-Powered Voice-Controlled Smart Home Manager",
        "description": "Voice-controlled smart home manager with AI-powered automation",
        "models": ["User", "Device", "Automation", "VoiceCommand"],
        "endpoints": ["/voice/command", "/devices/", "/automations/", "/commands/"],
        "ai_features": ["voice recognition", "home automation"],
        "special_configs": ["device integration", "voice processing"]
    },
    "intelligent-ecommerce-management-system": {
        "title": "Intelligent E-commerce Management System",
        "description": "E-commerce management system with AI-powered optimization",
        "models": ["User", "Product", "Order", "Analytics"],
        "endpoints": ["/ecommerce/optimize", "/products/", "/orders/", "/analytics/"],
        "ai_features": ["product recommendations", "inventory optimization"],
        "special_configs": ["payment processing", "inventory management"]
    },
    "multi-agent-cybersecurity-defense-system": {
        "title": "Multi-Agent Cybersecurity Defense System",
        "description": "Cybersecurity defense system with multi-agent AI protection",
        "models": ["User", "Threat", "Agent", "Defense"],
        "endpoints": ["/defense/protect", "/threats/", "/agents/", "/defenses/"],
        "ai_features": ["threat detection", "automated response"],
        "special_configs": ["security protocols", "threat intelligence"]
    },
    "multi-agent-software-development-team": {
        "title": "Multi-Agent Software Development Team",
        "description": "Multi-agent software development system with AI-powered collaboration",
        "models": ["User", "Project", "Agent", "Collaboration"],
        "endpoints": ["/development/collaborate", "/projects/", "/agents/", "/collaborations/"],
        "ai_features": ["code collaboration", "project coordination"],
        "special_configs": ["version control", "team coordination"]
    },
    "autonomous-research-report-generation-system": {
        "title": "Autonomous Research & Report Generation System",
        "description": "Autonomous research system with AI-powered report generation",
        "models": ["User", "Research", "Report", "Generation"],
        "endpoints": ["/research/conduct", "/researches/", "/reports/", "/generations/"],
        "ai_features": ["research automation", "report generation"],
        "special_configs": ["data sources", "report templates"]
    }
}

def create_boilerplate_files(project_name, config):
    """Create all boilerplate files for a project"""
    base_path = Path(f"backend/templates/boilerplates/backend/{project_name}")
    app_path = base_path / "app"
    
    # Create directories
    app_path.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    (app_path / "__init__.py").touch()
    
    # Create main.py
    create_main_py(app_path, config)
    
    # Create models.py
    create_models_py(app_path, config)
    
    # Create schemas.py
    create_schemas_py(app_path, config)
    
    # Create database.py
    create_database_py(app_path, project_name)
    
    # Create auth.py
    create_auth_py(app_path)
    
    # Create config.py
    create_config_py(app_path, config)
    
    # Create README.md
    create_readme_md(base_path, config)
    
    # Create env.example
    create_env_example(base_path, project_name, config)

def create_main_py(app_path, config):
    """Create main.py file"""
    content = f'''from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
from dotenv import load_dotenv

# Import project-specific modules
from .database import get_db
from .models import Base, User, {", ".join(config["models"][1:])}
from .schemas import {", ".join([f"{model}Create" for model in config["models"][1:]])}
from .auth import get_current_user
from .config import settings

load_dotenv()

app = FastAPI(
    title="{config["title"]}",
    description="{config["description"]}",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Basic Pydantic models for API
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AnalysisResult(BaseModel):
    analysis_id: int
    results: List[Dict[str, Any]]
    recommendations: List[str]
    confidence_score: float

# Root endpoint
@app.get("/")
async def root():
    return {{"message": "{config["title"]} API"}}

# Authentication endpoint
@app.post("/auth/login", response_model=LoginResponse)
async def login(request: LoginRequest):
    """Authenticate user"""
    # TODO: Implement authentication logic
    pass

# Core AI endpoints
@app.post("/ai/analyze", response_model=AnalysisResult)
async def analyze_data(
    current_user = Depends(get_current_user)
):
    """Analyze data with AI-powered insights"""
    # TODO: Implement AI analysis logic
    pass

# Health check
@app.get("/health")
async def health_check():
    return {{"status": "healthy", "service": "{config["title"].lower().replace(" ", "-")}"}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
    
    with open(app_path / "main.py", "w", encoding="utf-8") as f:
        f.write(content)

def create_models_py(app_path, config):
    """Create models.py file"""
    models_content = '''from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(50), default="user")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
'''
    
    # Add project-specific models
    for model in config["models"][1:]:
        models_content += f'''

class {model}(Base):
    """{model} model"""
    __tablename__ = "{model.lower()}s"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    data = Column(JSON, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
'''
    
    with open(app_path / "models.py", "w", encoding="utf-8") as f:
        f.write(models_content)

def create_schemas_py(app_path, config):
    """Create schemas.py file"""
    schemas_content = '''from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

# Base schemas
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: str = Field(..., regex=r"^[^@]+@[^@]+\\.[^@]+$")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="user")

class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
'''
    
    # Add project-specific schemas
    for model in config["models"][1:]:
        schemas_content += f'''

class {model}Base(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

class {model}Create({model}Base):
    pass

class {model}Response({model}Base):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        from_attributes = True
'''
    
    schemas_content += '''

# AI-specific schemas
class AnalysisResult(BaseModel):
    analysis_id: int = Field(..., description="ID of the analysis")
    results: List[Dict[str, Any]] = Field(..., description="Analysis results")
    recommendations: List[str] = Field(..., description="AI recommendations")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="AI confidence score")
'''
    
    with open(app_path / "schemas.py", "w", encoding="utf-8") as f:
        f.write(schemas_content)

def create_database_py(app_path, project_name):
    """Create database.py file"""
    db_name = project_name.replace("-", "_")
    content = f'''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://user:password@localhost/{db_name}_db"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database with tables"""
    from .models import Base
    Base.metadata.create_all(bind=engine)
'''
    
    with open(app_path / "database.py", "w", encoding="utf-8") as f:
        f.write(content)

def create_auth_py(app_path):
    """Create auth.py file"""
    content = '''from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

from .database import get_db
from .models import User

load_dotenv()

# Security configuration
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token security
security = HTTPBearer()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> Optional[str]:
    """Verify and decode a JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get the current authenticated user from JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        token = credentials.credentials
        username = verify_token(token)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user
'''
    
    with open(app_path / "auth.py", "w", encoding="utf-8") as f:
        f.write(content)

def create_config_py(app_path, config):
    """Create config.py file"""
    content = f'''from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # Application
    APP_NAME: str = "{config["title"]}"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALGORITHM: str = "HS256"
    
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/{config["title"].lower().replace(" ", "_").replace("-", "_")}_db"
    )
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001"
    ]
    
    # AI Services
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4")
    
    # AI Model Configuration
    AI_CONFIDENCE_THRESHOLD: float = float(os.getenv("AI_CONFIDENCE_THRESHOLD", "0.7"))
    AI_RESPONSE_TIMEOUT: int = int(os.getenv("AI_RESPONSE_TIMEOUT", "30"))

# Create settings instance
settings = Settings()
'''
    
    with open(app_path / "config.py", "w", encoding="utf-8") as f:
        f.write(content)

def create_readme_md(base_path, config):
    """Create README.md file"""
    content = f'''# {config["title"]}

A FastAPI backend boilerplate for {config["description"].lower()}.

## Features

- **AI-Powered Analysis**: Basic structure for OpenAI integration
- **Data Management**: Core data models for {", ".join(config["models"][1:]).lower()}
- **JWT Authentication**: Basic security setup
- **{config["special_configs"][0].title()}**: Foundation for {config["special_configs"][0].lower()}

## Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL
- OpenAI API key

### Installation

1. **Install dependencies**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**
```bash
cp env.example .env
```

Edit `.env` with your configuration:
```env
SECRET_KEY=your-secret-key
OPENAI_API_KEY=your-openai-api-key
DATABASE_URL=postgresql://user:password@localhost/{config["title"].lower().replace(" ", "_").replace("-", "_")}_db
```

3. **Initialize database**
```bash
python -c "from app.database import init_db; init_db()"
```

4. **Run the application**
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
app/
├── __init__.py
├── main.py              # FastAPI application with endpoints
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas with validation
├── database.py          # Database configuration
├── auth.py              # JWT authentication
└── config.py            # Application settings
```

## API Endpoints

- `POST /auth/login` - Authenticate user
- `POST /ai/analyze` - Analyze data with AI
- `GET /health` - Health check

## Next Steps

This is a boilerplate. Implement the TODO sections in each endpoint to add:

- Business logic for data management
- AI integration for analysis
- Database operations
- Error handling
- Additional security features

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | JWT secret key | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Yes |
| `DATABASE_URL` | Database connection | Yes |
| `DEBUG` | Debug mode | No |
'''
    
    with open(base_path / "README.md", "w", encoding="utf-8") as f:
        f.write(content)

def create_env_example(base_path, project_name, config):
    """Create env.example file"""
    db_name = project_name.replace("-", "_")
    content = f'''# Application Settings
SECRET_KEY=your-secret-key-change-in-production
DEBUG=false

# Database
DATABASE_URL=postgresql://user:password@localhost/{db_name}_db

# AI Services
OPENAI_API_KEY=your-openai-api-key
OPENAI_MODEL=gpt-4

# Security
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Configuration
AI_CONFIDENCE_THRESHOLD=0.7
AI_RESPONSE_TIMEOUT=30
'''
    
    with open(base_path / "env.example", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    """Main function to create all boilerplates"""
    print("Creating boilerplates for all projects...")
    
    for project_name, config in PROJECTS.items():
        print(f"Creating boilerplate for: {project_name}")
        try:
            create_boilerplate_files(project_name, config)
            print(f"✓ Created boilerplate for: {project_name}")
        except Exception as e:
            print(f"✗ Error creating boilerplate for {project_name}: {e}")
    
    print("\nBoilerplate creation completed!")

if __name__ == "__main__":
    main()
