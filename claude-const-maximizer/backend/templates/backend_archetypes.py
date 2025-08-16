import json
import os

# Load backend archetypes from JSON file
def load_backend_archetypes():
    """Load backend archetypes from JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    archetypes_file = os.path.join(current_dir, 'backend_archetypes.json')
    
    with open(archetypes_file, 'r') as f:
        return json.load(f)

# Export the backend system
BACKEND_ARCHETYPES = load_backend_archetypes()

def get_backend_archetype(project_type: str) -> dict:
    """Get backend archetype for a specific project type"""
    archetypes = BACKEND_ARCHETYPES['backend_archetypes']
    
    # Map project types to archetypes
    type_mapping = {
        'CRUD': 'professional_saas',
        'DASHBOARD': 'professional_saas', 
        'ANALYTICS': 'professional_saas',
        'GENERATOR': 'ai_ml_backend',
        'MEDIA_CONTENT': 'ai_ml_backend',
        'CREATIVE_AI': 'ai_ml_backend',
        'RAG': 'rag_knowledge_backend',
        'KNOWLEDGE_BASE': 'rag_knowledge_backend',
        'DOCUMENT_AI': 'rag_knowledge_backend',
        'CHATBOT': 'real_time_backend',
        'CONVERSATIONAL_AI': 'real_time_backend',
        'CUSTOMER_SUPPORT': 'real_time_backend',
        'FINANCE_TRADING': 'financial_backend',
        'CRYPTO_ANALYTICS': 'financial_backend',
        'PORTFOLIO_MANAGER': 'financial_backend',
        'HEALTHCARE_DEMO': 'healthcare_backend',
        'MEDICAL_ANALYTICS': 'healthcare_backend',
        'PATIENT_PORTAL': 'healthcare_backend',
        'LEGAL_DOCUMENT': 'legal_backend',
        'CONTRACT_ANALYSIS': 'legal_backend',
        'COMPLIANCE_TOOL': 'legal_backend',
        'GAMING_AI': 'gaming_backend',
        'ENTERTAINMENT_PLATFORM': 'gaming_backend',
        'VIRTUAL_REALITY': 'gaming_backend',
        'EDUCATIONAL_AI': 'educational_backend',
        'LEARNING_PLATFORM': 'educational_backend',
        'TUTORING_SYSTEM': 'educational_backend',
        'RESEARCH_AI': 'research_backend',
        'DATA_ANALYTICS': 'research_backend',
        'SCIENTIFIC_TOOLS': 'research_backend'
    }
    
    archetype_key = type_mapping.get(project_type, 'professional_saas')
    return archetypes.get(archetype_key, archetypes['professional_saas'])

def get_backend_pattern_info(pattern_name: str) -> dict:
    """Get backend pattern information"""
    patterns = BACKEND_ARCHETYPES['backend_patterns']
    return patterns.get(pattern_name, patterns['layered_mvc'])

def get_database_pattern_info(database_name: str) -> dict:
    """Get database pattern information"""
    databases = BACKEND_ARCHETYPES['database_patterns']
    return databases.get(database_name, databases['postgresql'])

def get_auth_pattern_info(auth_name: str) -> dict:
    """Get authentication pattern information"""
    auth_patterns = BACKEND_ARCHETYPES['authentication_patterns']
    return auth_patterns.get(auth_name, auth_patterns['jwt'])

def get_deployment_pattern_info(deployment_name: str) -> dict:
    """Get deployment pattern information"""
    deployment_patterns = BACKEND_ARCHETYPES['deployment_patterns']
    return deployment_patterns.get(deployment_name, deployment_patterns['docker'])

def generate_backend_instructions(project_type: str) -> str:
    """Generate comprehensive backend instructions for a project type"""
    archetype = get_backend_archetype(project_type)
    pattern = get_backend_pattern_info(archetype['architecture'])
    database = get_database_pattern_info(archetype['database'])
    auth = get_auth_pattern_info('jwt')  # Default to JWT
    deployment = get_deployment_pattern_info('docker')  # Default to Docker
    
    instructions = f"""
    BACKEND ARCHETYPE: {archetype['name']}
    DESCRIPTION: {archetype['description']}
    
    FRAMEWORK: {archetype['framework'].upper()}
    DATABASE: {database['name']}
    ARCHITECTURE: {pattern['description']}
    
    ARCHITECTURE PATTERN:
    - Description: {pattern['description']}
    - Layers: {', '.join(pattern['layers'])}
    - Benefits: {', '.join(pattern['benefits'])}
    - Best For: {', '.join(pattern['best_for'])}
    
    DATABASE PATTERN:
    - Name: {database['name']}
    - Description: {database['description']}
    - Installation: {database['installation']}
    - Features: {', '.join(database['features'])}
    - Best For: {', '.join(database['best_for'])}
    
    DESIGN PATTERNS:
    {', '.join(archetype['patterns'])}
    
    CORE FEATURES:
    {', '.join(archetype['features'])}
    
    INTEGRATIONS:
    {', '.join(archetype['integrations'])}
    
    AUTHENTICATION:
    - Name: {auth['name']}
    - Description: {auth['description']}
    - Implementation: {auth['implementation']}
    - Features: {', '.join(auth['features'])}
    - Best For: {', '.join(auth['best_for'])}
    
    DEPLOYMENT:
    - Container: {archetype['deployment']['container']}
    - Platform: {archetype['deployment']['platform']}
    - Database: {archetype['deployment']['database']}
    - Additional Services: {', '.join([f"{k}: {v}" for k, v in archetype['deployment'].items() if k not in ['container', 'platform', 'database']])}
    
    BACKEND PRINCIPLES:
    1. Implement the specified architecture pattern with all required layers
    2. Use the recommended database with proper configuration
    3. Implement authentication and authorization according to the pattern
    4. Add all core features with proper error handling and validation
    5. Integrate with specified third-party services and APIs
    6. Implement proper logging, monitoring, and error tracking
    7. Use async/await patterns where appropriate for performance
    8. Include comprehensive API documentation with OpenAPI/Swagger
    9. Implement proper security measures (rate limiting, CORS, etc.)
    10. Prepare deployment configuration for the specified platform
    11. Include database migrations and seed data
    12. Add comprehensive testing (unit, integration, API tests)
    """
    
    return instructions
