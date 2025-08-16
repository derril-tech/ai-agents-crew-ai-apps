import json
import os

# Load prompt engineering system from JSON file
def load_prompt_engineering_system():
    """Load prompt engineering system from JSON file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    system_file = os.path.join(current_dir, 'prompt_engineering_system.json')
    
    with open(system_file, 'r') as f:
        return json.load(f)

# Export the prompt engineering system
PROMPT_ENGINEERING_SYSTEM = load_prompt_engineering_system()

def get_claude_optimization_techniques() -> dict:
    """Get Claude-specific optimization techniques"""
    return PROMPT_ENGINEERING_SYSTEM['claude_specific_techniques']

def get_prompt_archetype(archetype_name: str) -> dict:
    """Get prompt engineering archetype"""
    archetypes = PROMPT_ENGINEERING_SYSTEM['prompt_engineering_archetypes']
    return archetypes.get(archetype_name, archetypes['research_to_brief'])

def get_optimization_strategy(strategy_name: str) -> dict:
    """Get prompt optimization strategy"""
    strategies = PROMPT_ENGINEERING_SYSTEM['prompt_optimization_strategies']
    return strategies.get(strategy_name, strategies['for_research_conversion'])

def get_quality_checks() -> dict:
    """Get quality assurance checks"""
    return PROMPT_ENGINEERING_SYSTEM['quality_assurance']

def generate_claude_optimized_prompt(
    project_name: str,
    project_brief: str,
    market_research: dict,
    prompt_type: str = "code_generation"
) -> str:
    """Generate a Claude-optimized prompt based on project information"""
    
    archetype = get_prompt_archetype(prompt_type)
    strategy = get_optimization_strategy(f"for_{prompt_type}")
    techniques = get_claude_optimization_techniques()
    
    # Build the optimized prompt
    prompt = f"""
{archetype['prompt_template']['context_setting']}

{archetype['prompt_template']['background'].format(project_name=project_name)}

## PROJECT CONTEXT
**Project Name:** {project_name}
**Project Brief:** {project_brief}

## MARKET RESEARCH CONTEXT
- **Target Audience:** {market_research.get('target_audience', 'Not specified')}
- **Key Features:** {market_research.get('key_features', 'Not specified')}
- **Technical Requirements:** {market_research.get('technical_requirements', 'Not specified')}
- **Market Opportunities:** {market_research.get('market_opportunities', 'Not specified')}

## TASK BREAKDOWN
{chr(10).join([f"{i+1}. {task}" for i, task in enumerate(archetype['prompt_template']['task_breakdown'])])}

## CLAUDE OPTIMIZATION TECHNIQUES
Based on Claude's strengths and preferences:

### Context-Heavy Approach
{chr(10).join([f"- {technique}" for technique in techniques['context_heavy_approach']['techniques']])}

### Hierarchical Structure
{chr(10).join([f"- {technique}" for technique in techniques['hierarchical_structure']['techniques']])}

### Example-Driven Approach
{chr(10).join([f"- {technique}" for technique in techniques['example_driven_approach']['techniques']])}

### Constraint-Based Instructions
{chr(10).join([f"- {technique}" for technique in techniques['constraint_based_instructions']['techniques']])}

### Step-by-Step Breakdown
{chr(10).join([f"- {technique}" for technique in techniques['step_by_step_breakdown']['techniques']])}

## FORMAT REQUIREMENTS
{chr(10).join([f"- **{key.title()}:** {value}" for key, value in archetype['prompt_template']['format_requirements'].items()])}

## SUCCESS CRITERIA
{chr(10).join([f"- {criterion}" for criterion in archetype['prompt_template']['success_criteria']])}

## OPTIMIZATION STRATEGY
**Strategy:** {strategy['strategy']}
**Approach:**
{chr(10).join([f"- {approach}" for approach in strategy['approach']])}
**Claude Optimization:** {strategy['claude_optimization']}

## QUALITY ASSURANCE CHECKLIST
Before proceeding, ensure:
{chr(10).join([f"- {check}" for check in get_quality_checks()['prompt_quality_checks']])}

## CLAUDE OPTIMIZATION CHECKLIST
Verify the prompt:
{chr(10).join([f"- {check}" for check in get_quality_checks()['claude_optimization_checks']])}

Remember: Claude works best with comprehensive context, clear structure, relevant examples, explicit constraints, and step-by-step instructions. Leverage Claude's strengths in reasoning, pattern recognition, and code generation while avoiding its tendency toward verbosity through clear constraints.
"""
    
    return prompt

def generate_research_to_brief_prompt(project_name: str, market_research: dict) -> str:
    """Generate optimized prompt for converting research to brief"""
    return generate_claude_optimized_prompt(
        project_name=project_name,
        project_brief="To be created from research",
        market_research=market_research,
        prompt_type="research_to_brief"
    )

def generate_brief_to_prompt_conversion(project_name: str, project_brief: str) -> str:
    """Generate optimized prompt for converting brief to Claude prompt"""
    return generate_claude_optimized_prompt(
        project_name=project_name,
        project_brief=project_brief,
        market_research={},  # Brief already contains this info
        prompt_type="brief_to_prompt"
    )

def generate_code_generation_prompt(
    project_name: str, 
    project_brief: str, 
    architecture_type: str = "layered_mvc",
    tech_stack: str = "FastAPI + React + PostgreSQL"
) -> str:
    """Generate optimized prompt for code generation"""
    
    archetype = get_prompt_archetype("code_generation")
    techniques = get_claude_optimization_techniques()
    
    prompt = f"""
{archetype['prompt_template']['context_setting']}

{archetype['prompt_template']['background'].format(
    project_name=project_name,
    architecture_type=architecture_type,
    tech_stack=tech_stack
)}

## PROJECT SPECIFICATIONS
**Project Name:** {project_name}
**Architecture Type:** {architecture_type}
**Tech Stack:** {tech_stack}

## PROJECT BRIEF
{project_brief}

## TASK BREAKDOWN
{chr(10).join([f"{i+1}. {task}" for i, task in enumerate(archetype['prompt_template']['task_breakdown'])])}

## CLAUDE OPTIMIZATION FOR CODE GENERATION

### Context-Heavy Approach
{chr(10).join([f"- {technique}" for technique in techniques['context_heavy_approach']['techniques']])}

### Pattern Recognition
- Provide code patterns and templates
- Include architectural examples
- Show integration patterns
- Reference similar implementations

### Constraint-Based Instructions
- Set explicit file format requirements
- Specify code style and conventions
- Define performance expectations
- Set security and quality standards

### Step-by-Step Implementation
- Break down into backend, frontend, integration, deployment
- Provide clear success criteria for each step
- Include intermediate checkpoints
- Specify dependencies between components

## FORMAT REQUIREMENTS
{chr(10).join([f"- **{key.title()}:** {value}" for key, value in archetype['prompt_template']['format_requirements'].items()])}

## SUCCESS CRITERIA
{chr(10).join([f"- {criterion}" for criterion in archetype['prompt_template']['success_criteria']])}

## OUTPUT QUALITY INDICATORS
{chr(10).join([f"- {indicator}" for indicator in get_quality_checks()['output_quality_indicators']])}

Remember: Claude excels at code generation when given comprehensive context, clear patterns, explicit constraints, and step-by-step instructions. Leverage Claude's strengths in understanding software architecture and maintaining consistency across large codebases.
"""
    
    return prompt

def generate_validation_prompt(
    project_name: str,
    architecture_type: str = "layered_mvc",
    tech_stack: str = "FastAPI + React + PostgreSQL"
) -> str:
    """Generate optimized prompt for validation and verification"""
    
    archetype = get_prompt_archetype("validation_and_verification")
    techniques = get_claude_optimization_techniques()
    
    prompt = f"""
{archetype['prompt_template']['context_setting']}

{archetype['prompt_template']['background'].format(
    project_name=project_name,
    architecture_type=architecture_type,
    tech_stack=tech_stack
)}

## VALIDATION CONTEXT
**Project Name:** {project_name}
**Architecture Type:** {architecture_type}
**Tech Stack:** {tech_stack}

## TASK BREAKDOWN
{chr(10).join([f"{i+1}. {task}" for i, task in enumerate(archetype['prompt_template']['task_breakdown'])])}

## CLAUDE OPTIMIZATION FOR VALIDATION

### Analytical Approach
- Use systematic validation methodology
- Apply checklists and criteria
- Provide detailed analysis
- Include specific findings

### Comprehensive Coverage
- Review all code aspects
- Check architecture compliance
- Validate integration points
- Verify deployment setup

### Actionable Recommendations
- Make all findings actionable
- Provide specific improvements
- Include implementation guidance
- Set priority levels

## FORMAT REQUIREMENTS
{chr(10).join([f"- **{key.title()}:** {value}" for key, value in archetype['prompt_template']['format_requirements'].items()])}

## SUCCESS CRITERIA
{chr(10).join([f"- {criterion}" for criterion in archetype['prompt_template']['success_criteria']])}

## VALIDATION CHECKLIST
- [ ] Code structure and architecture review
- [ ] Implementation against requirements
- [ ] Security and best practices check
- [ ] Integration and deployment verification
- [ ] Comprehensive validation report

Remember: Claude excels at analytical tasks when given clear criteria, systematic approaches, and specific areas to focus on. Leverage Claude's strengths in reasoning and analysis for thorough validation.
"""
    
    return prompt
