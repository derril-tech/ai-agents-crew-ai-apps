"""
Prompt Engineer Agent
Responsible for Step 2 of Phase 3: Converting project brief into Claude-optimized prompts
"""

import asyncio
from typing import Dict, Any, List
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from templates.prompt_engineering_system import (
    generate_claude_optimized_prompt,
    generate_research_to_brief_prompt,
    generate_brief_to_prompt_conversion,
    generate_code_generation_prompt,
    generate_validation_prompt,
    get_claude_optimization_techniques,
    get_quality_checks
)

load_dotenv()

class PromptEngineer:
    """Prompt Engineer agent for optimizing prompts specifically for Claude"""
    
    # DEBUG MODE: Set to True for faster testing with minimal iterations
    DEBUG_MODE = True  # Set to False for full prompt engineering
    
    def __init__(self):
        # Check for required API keys - try multiple options
        openai_api_key = os.getenv("OPENAI_API_KEY")
        google_api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        huggingface_api_key = os.getenv("HUGGINGFACE_API_KEY")
        deep_ai_api_key = os.getenv("DEEP_AI_API_KEY")
        mistral_api_key = os.getenv("MISTRAL_API_KEY")
        
        # Initialize LLMs with proper error handling
        self.primary_llm = None
        self.backup_llms = []
        
        # Primary LLM (DeepSeek - cost-effective for prompt engineering)
        if openai_api_key:
            try:
                self.primary_llm = ChatOpenAI(
                    model="deepseek-chat",
                    temperature=0.1,  # Lower temperature for consistent prompt engineering
                    openai_api_key=openai_api_key,
                    base_url="https://api.deepseek.com/v1"
                )
                print("  [OK] DeepSeek primary LLM configured for Prompt Engineer")
            except Exception as e:
                print(f"  [WARN] Failed to configure DeepSeek: {e}")
        else:
            print("  [WARN] OPENAI_API_KEY not found - DeepSeek not available")
        
        # Add Gemini if API key is available
        if google_api_key:
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                gemini_llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-pro",  # Updated model name
                    temperature=0.1,
                    google_api_key=google_api_key
                )
                self.backup_llms.append(gemini_llm)
                print("  [OK] Gemini Pro backup LLM configured for Prompt Engineer")
            except Exception as e:
                print(f"  [WARN] Failed to configure Gemini Pro for Prompt Engineer: {e}")
        else:
            print("  [WARN] GOOGLE_API_KEY/GEMINI_API_KEY not found - Gemini Pro not available")
        
        # Add Hugging Face if API key is available
        if huggingface_api_key:
            try:
                from langchain_huggingface import ChatHuggingFace
                huggingface_llm = ChatHuggingFace(
                    model="mistralai/Mistral-7B-Instruct-v0.2",
                    temperature=0.1,
                    huggingfacehub_api_token=huggingface_api_key,
                    task="text-generation"  # Added required field
                )
                self.backup_llms.append(huggingface_llm)
                print("  [OK] Hugging Face LLM configured for Prompt Engineer")
            except Exception as e:
                print(f"  [WARN] Failed to configure Hugging Face: {e}")
        else:
            print("  [WARN] HUGGINGFACE_API_KEY not found - Hugging Face not available")
        
        # Add Mistral if API key is available
        if mistral_api_key:
            try:
                from langchain_community.chat_models import ChatOpenAI
                mistral_llm = ChatOpenAI(
                    model="mistral-large-latest",
                    temperature=0.1,
                    openai_api_key=mistral_api_key,
                    base_url="https://api.mistral.ai/v1"
                )
                self.backup_llms.append(mistral_llm)
                print("  [OK] Mistral LLM configured for Prompt Engineer")
            except Exception as e:
                print(f"  [WARN] Failed to configure Mistral: {e}")
        else:
            print("  [WARN] MISTRAL_API_KEY not found - Mistral not available")
        
        # Add GPT-3.5 as backup if OpenAI key is available
        if openai_api_key:
            try:
                gpt_llm = ChatOpenAI(
                    model="gpt-3.5-turbo",
                    temperature=0.1,
                    openai_api_key=openai_api_key
                )
                self.backup_llms.append(gpt_llm)
                print("  [OK] GPT-3.5 Turbo backup LLM configured for Prompt Engineer")
            except Exception as e:
                print(f"  [WARN] Failed to configure GPT-3.5 Turbo: {e}")
        
        # Check if we have any working LLMs
        if not self.primary_llm and not self.backup_llms:
            print("  [ERROR] No LLMs available! Please set one of: OPENAI_API_KEY, GEMINI_API_KEY, HUGGINGFACE_API_KEY, MISTRAL_API_KEY")
            raise ValueError("No LLMs available for Prompt Engineer")
        
        # Set primary LLM to first available backup if primary failed
        if not self.primary_llm and self.backup_llms:
            self.primary_llm = self.backup_llms[0]
            self.backup_llms = self.backup_llms[1:]
            print("  [OK] Using backup LLM as primary")
        
        print(f"  [OK] Prompt Engineer: {len(self.backup_llms) + 1} LLM(s) configured")
        
        self.current_llm_index = 0
    
    async def create_claude_optimized_prompt(
        self, 
        project_name: str, 
        project_brief: str, 
        market_research: Dict[str, Any],
        prompt_type: str = "code_generation"
    ) -> str:
        """Create a Claude-optimized prompt using the comprehensive prompt engineering system"""
        
        print(f"[GOAL] Creating Claude-optimized prompt for {project_name} ({prompt_type})")
        
        # Generate the optimized prompt using our system
        optimized_prompt = generate_claude_optimized_prompt(
            project_name=project_name,
            project_brief=project_brief,
            market_research=market_research,
            prompt_type=prompt_type
        )
        
        # Further enhance the prompt using LLM
        enhanced_prompt = await self._enhance_prompt_with_llm(
            optimized_prompt, project_name, prompt_type
        )
        
        return enhanced_prompt
    
    async def _enhance_prompt_with_llm(
        self, 
        base_prompt: str, 
        project_name: str, 
        prompt_type: str
    ) -> str:
        """Enhance the base prompt using LLM for additional optimization"""
        
        enhancement_prompt = f"""
You are an expert prompt engineer specializing in Claude optimization. Your task is to enhance the provided prompt to make it even more effective for Claude.

## PROJECT CONTEXT
**Project Name:** {project_name}
**Prompt Type:** {prompt_type}

## BASE PROMPT
{base_prompt}

## ENHANCEMENT TASK
Analyze the base prompt and enhance it by:

1. **Claude-Specific Optimizations:**
   - Ensure all Claude strengths are leveraged
   - Add any missing context or background
   - Include more specific examples if needed
   - Strengthen constraints to avoid verbosity

2. **Quality Improvements:**
   - Make instructions even more specific and actionable
   - Add any missing success criteria
   - Improve structure and organization
   - Ensure all requirements are clearly communicated

3. **Technical Enhancements:**
   - Add relevant code patterns and examples
   - Include architectural considerations
   - Specify integration requirements
   - Add deployment considerations

## ENHANCEMENT GUIDELINES
- Maintain the existing structure and format
- Add value without making it overly verbose
- Focus on Claude's specific strengths and preferences
- Ensure all quality checks are addressed
- Make the prompt production-ready

## OUTPUT FORMAT
Return the enhanced prompt with all improvements integrated. Maintain the same structure but with enhanced content that addresses all the above considerations.

Remember: The goal is to create the most effective prompt possible for Claude, leveraging all known optimization techniques and Claude-specific best practices.
"""
        
        try:
            # Try primary LLM first
            print(f"  [PROCESS] Enhancing prompt with DeepSeek...")
            response = await self.primary_llm.agenerate([
                [HumanMessage(content=enhancement_prompt)]
            ])
            
            if response.generations and response.generations[0]:
                enhanced_content = response.generations[0][0].text
                if not self._is_fallback_response(enhanced_content):
                    print(f"  [OK] Prompt enhanced successfully with DeepSeek")
                    return enhanced_content
            
        except Exception as e:
            print(f"  [WARN] DeepSeek enhancement failed: {e}")
        
        # Try backup LLMs
        for i, backup_llm in enumerate(self.backup_llms):
            try:
                llm_name = "Gemini Pro" if i == 0 else "GPT-3.5 Turbo"
                print(f"  [PROCESS] Trying {llm_name} for prompt enhancement...")
                
                response = await backup_llm.agenerate([
                    [HumanMessage(content=enhancement_prompt)]
                ])
                
                if response.generations and response.generations[0]:
                    enhanced_content = response.generations[0][0].text
                    if not self._is_fallback_response(enhanced_content):
                        print(f"  [OK] Prompt enhanced successfully with {llm_name}")
                        return enhanced_content
                        
            except Exception as e:
                print(f"  [WARN] {llm_name} enhancement failed: {e}")
            
            # In debug mode, limit to first backup LLM only
            if self.DEBUG_MODE:
                print("  [CONFIG] DEBUG_MODE: Limiting to first backup LLM only")
                break
        
        # Return base prompt if all LLMs fail
        print(f"  [WARN] All LLMs failed, using base prompt")
        return base_prompt
    
    def _is_fallback_response(self, content: str) -> bool:
        """Check if the response is a fallback/error response"""
        fallback_indicators = [
            "I apologize",
            "I'm sorry",
            "I cannot",
            "I'm unable",
            "fallback",
            "error",
            "failed"
        ]
        
        content_lower = content.lower()
        return any(indicator in content_lower for indicator in fallback_indicators)
    
    async def create_research_to_brief_prompt(
        self, 
        project_name: str, 
        market_research: Dict[str, Any]
    ) -> str:
        """Create optimized prompt for converting research to brief"""
        return await self.create_claude_optimized_prompt(
            project_name=project_name,
            project_brief="To be created from research",
            market_research=market_research,
            prompt_type="research_to_brief"
        )
    
    async def create_brief_to_prompt_conversion(
        self, 
        project_name: str, 
        project_brief: str
    ) -> str:
        """Create optimized prompt for converting brief to Claude prompt"""
        return await self.create_claude_optimized_prompt(
            project_name=project_name,
            project_brief=project_brief,
            market_research={},  # Brief already contains this info
            prompt_type="brief_to_prompt"
        )
    
    async def create_code_generation_prompt(
        self, 
        project_name: str, 
        project_brief: str, 
        architecture_type: str = "layered_mvc",
        tech_stack: str = "FastAPI + React + PostgreSQL"
    ) -> str:
        """Create optimized prompt for code generation"""
        return await self.create_claude_optimized_prompt(
            project_name=project_name,
            project_brief=project_brief,
            market_research={},  # Brief contains this info
            prompt_type="code_generation"
        )
    
    async def create_validation_prompt(
        self, 
        project_name: str,
        architecture_type: str = "layered_mvc",
        tech_stack: str = "FastAPI + React + PostgreSQL"
    ) -> str:
        """Create optimized prompt for validation and verification"""
        return await self.create_claude_optimized_prompt(
            project_name=project_name,
            project_brief="Validation of generated code",
            market_research={},
            prompt_type="validation_and_verification"
        )
    
    def get_prompt_quality_score(self, prompt: str) -> Dict[str, Any]:
        """Analyze prompt quality and provide score"""
        quality_checks = get_quality_checks()
        claude_techniques = get_claude_optimization_techniques()
        
        # Analyze prompt against quality criteria
        quality_score = 0
        total_criteria = 0
        passed_criteria = []
        failed_criteria = []
        
        # Check prompt quality criteria
        for check in quality_checks['prompt_quality_checks']:
            total_criteria += 1
            if self._check_criterion(prompt, check):
                quality_score += 1
                passed_criteria.append(check)
            else:
                failed_criteria.append(check)
        
        # Check Claude optimization criteria
        for check in quality_checks['claude_optimization_checks']:
            total_criteria += 1
            if self._check_criterion(prompt, check):
                quality_score += 1
                passed_criteria.append(check)
            else:
                failed_criteria.append(check)
        
        quality_percentage = (quality_score / total_criteria) * 100 if total_criteria > 0 else 0
        
        return {
            "quality_score": quality_score,
            "total_criteria": total_criteria,
            "quality_percentage": quality_percentage,
            "passed_criteria": passed_criteria,
            "failed_criteria": failed_criteria,
            "grade": self._get_grade(quality_percentage)
        }
    
    def _check_criterion(self, prompt: str, criterion: str) -> bool:
        """Check if a specific criterion is met in the prompt"""
        prompt_lower = prompt.lower()
        
        # Simple keyword-based checking (can be enhanced with more sophisticated analysis)
        if "context" in criterion.lower() and ("context" in prompt_lower or "background" in prompt_lower):
            return True
        elif "instructions" in criterion.lower() and ("task" in prompt_lower or "instruction" in prompt_lower):
            return True
        elif "examples" in criterion.lower() and ("example" in prompt_lower or "template" in prompt_lower):
            return True
        elif "constraints" in criterion.lower() and ("constraint" in prompt_lower or "requirement" in prompt_lower):
            return True
        elif "criteria" in criterion.lower() and ("criteria" in prompt_lower or "success" in prompt_lower):
            return True
        elif "structure" in criterion.lower() and ("structure" in prompt_lower or "format" in prompt_lower):
            return True
        elif "requirements" in criterion.lower() and ("requirement" in prompt_lower or "specification" in prompt_lower):
            return True
        elif "language" in criterion.lower() and len(prompt) > 100:  # Basic length check
            return True
        
        return False
    
    def _get_grade(self, percentage: float) -> str:
        """Convert percentage to letter grade"""
        if percentage >= 90:
            return "A+"
        elif percentage >= 85:
            return "A"
        elif percentage >= 80:
            return "A-"
        elif percentage >= 75:
            return "B+"
        elif percentage >= 70:
            return "B"
        elif percentage >= 65:
            return "B-"
        elif percentage >= 60:
            return "C+"
        elif percentage >= 55:
            return "C"
        elif percentage >= 50:
            return "C-"
        else:
            return "F"
