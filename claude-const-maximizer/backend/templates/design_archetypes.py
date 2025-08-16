import json
import os

# Load design archetypes from JSON file
def load_design_archetypes():
    """Load design archetypes from JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    archetypes_file = os.path.join(current_dir, 'design_archetypes.json')
    
    with open(archetypes_file, 'r') as f:
        return json.load(f)

# Export the design system
DESIGN_ARCHETYPES = load_design_archetypes()

def get_design_archetype(project_type: str) -> dict:
    """Get design archetype for a specific project type"""
    archetypes = DESIGN_ARCHETYPES['design_archetypes']
    
    # Map project types to archetypes
    type_mapping = {
        'CRUD': 'professional_saas',
        'DASHBOARD': 'professional_saas', 
        'ANALYTICS': 'professional_saas',
        'GENERATOR': 'creative_tool',
        'MEDIA_CONTENT': 'creative_tool',
        'CREATIVE_AI': 'creative_tool',
        'FINANCE_TRADING': 'finance_trading',
        'CRYPTO_ANALYTICS': 'finance_trading',
        'PORTFOLIO_MANAGER': 'finance_trading',
        'HEALTHCARE_DEMO': 'healthcare_demo',
        'MEDICAL_ANALYTICS': 'healthcare_demo',
        'PATIENT_PORTAL': 'healthcare_demo',
        'LEGAL_DOCUMENT': 'legal_document',
        'CONTRACT_ANALYSIS': 'legal_document',
        'COMPLIANCE_TOOL': 'legal_document',
        'GAMING_AI': 'gaming_entertainment',
        'ENTERTAINMENT_PLATFORM': 'gaming_entertainment',
        'VIRTUAL_REALITY': 'gaming_entertainment',
        'EDUCATIONAL_AI': 'educational_learning',
        'LEARNING_PLATFORM': 'educational_learning',
        'TUTORING_SYSTEM': 'educational_learning',
        'RESEARCH_AI': 'research_analytics',
        'DATA_ANALYTICS': 'research_analytics',
        'SCIENTIFIC_TOOLS': 'research_analytics',
        'CHATBOT': 'chatbot_conversational',
        'CONVERSATIONAL_AI': 'chatbot_conversational',
        'CUSTOMER_SUPPORT': 'chatbot_conversational',
        'RAG': 'rag_knowledge',
        'KNOWLEDGE_BASE': 'rag_knowledge',
        'DOCUMENT_AI': 'rag_knowledge'
    }
    
    archetype_key = type_mapping.get(project_type, 'professional_saas')
    return archetypes.get(archetype_key, archetypes['professional_saas'])

def get_css_library_info(library_name: str) -> dict:
    """Get CSS library information"""
    libraries = DESIGN_ARCHETYPES['css_libraries']
    return libraries.get(library_name, libraries['tailwind'])

def get_layout_pattern_info(pattern_name: str) -> dict:
    """Get layout pattern information"""
    patterns = DESIGN_ARCHETYPES['layout_patterns']
    return patterns.get(pattern_name, patterns['dashboard_grid'])

def generate_design_instructions(project_type: str) -> str:
    """Generate comprehensive design instructions for a project type"""
    archetype = get_design_archetype(project_type)
    css_lib = get_css_library_info(archetype['css_library'])
    layout = get_layout_pattern_info(archetype['layout_style'])
    
    instructions = f"""
    DESIGN ARCHETYPE: {archetype['name']}
    DESCRIPTION: {archetype['description']}
    
    CSS LIBRARY: {css_lib['name']}
    INSTALLATION: {css_lib['installation']}
    BEST FOR: {', '.join(css_lib['best_for'])}
    
    COLOR SCHEME:
    - Primary: {archetype['color_scheme']['primary']}
    - Secondary: {archetype['color_scheme']['secondary']}
    - Accent: {archetype['color_scheme']['accent']}
    - Success: {archetype['color_scheme']['success']}
    - Warning: {archetype['color_scheme']['warning']}
    - Error: {archetype['color_scheme']['error']}
    - Background: {archetype['color_scheme']['background']}
    - Surface: {archetype['color_scheme']['surface']}
    - Text Primary: {archetype['color_scheme']['text_primary']}
    - Text Secondary: {archetype['color_scheme']['text_secondary']}
    
    TYPOGRAPHY:
    - Heading Font: {archetype['typography']['heading_font']}
    - Body Font: {archetype['typography']['body_font']}
    - Font Weights: {', '.join(map(str, archetype['typography']['font_weights']))}
    
    LAYOUT STYLE: {layout['description']}
    LAYOUT COMPONENTS: {', '.join(layout['components'])}
    RESPONSIVE: {layout['responsive']}
    
    COMPONENT STYLES:
    - Cards: {archetype['components']['cards']}
    - Buttons: {archetype['components']['buttons']}
    - Forms: {archetype['components']['forms']}
    - Tables: {archetype['components']['tables']}
    
    ANIMATIONS: {archetype['animations']}
    
    DESIGN PRINCIPLES:
    1. Use the specified color scheme consistently throughout the application
    2. Apply the typography system with proper font weights and hierarchy
    3. Implement the layout pattern with all required components
    4. Style components according to the archetype specifications
    5. Add appropriate animations that match the design mood
    6. Ensure responsive design for all screen sizes
    7. Maintain accessibility standards
    8. Create a cohesive visual identity that matches the project type
    """
    
    return instructions
