"""
Pre-Code Validation System
Ensures all specifications are locked in before Claude starts coding
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ValidationStatus(Enum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    WARNING = "warning"

@dataclass
class ValidationResult:
    component: str
    status: ValidationStatus
    message: str
    details: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dictionary"""
        return {
            "component": self.component,
            "status": self.status.value,  # Convert enum to string
            "message": self.message,
            "details": self.details
        }

class PreCodeValidator:
    """Validates all project specifications before coding begins"""
    
    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.results: List[ValidationResult] = []
        
    def validate_project_brief(self) -> ValidationResult:
        """Validate project brief completeness"""
        brief_file = self.project_dir / "project_brief.md"
        
        if not brief_file.exists():
            return ValidationResult(
                component="Project Brief",
                status=ValidationStatus.FAILED,
                message="Project brief file not found",
                details={"file": str(brief_file)}
            )
        
        try:
            with open(brief_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for required sections
            required_sections = [
                "Project Overview",
                "Market Research Summary", 
                "Technical Requirements",
                "Core Features",
                "Integration Points",
                "Claude Coding Instructions"
            ]
            
            missing_sections = []
            for section in required_sections:
                if section not in content:
                    missing_sections.append(section)
            
            if missing_sections:
                return ValidationResult(
                    component="Project Brief",
                    status=ValidationStatus.FAILED,
                    message=f"Missing required sections: {', '.join(missing_sections)}",
                    details={"missing_sections": missing_sections}
                )
            
            # Check for placeholder values
            placeholders = ["[PROJECT_NAME]", "[CRUD/CHATBOT/RAG/DASHBOARD/ANALYTICS/GENERATOR]"]
            found_placeholders = []
            for placeholder in placeholders:
                if placeholder in content:
                    found_placeholders.append(placeholder)
            
            if found_placeholders:
                return ValidationResult(
                    component="Project Brief",
                    status=ValidationStatus.FAILED,
                    message=f"Found placeholder values: {', '.join(found_placeholders)}",
                    details={"placeholders": found_placeholders}
                )
            
            return ValidationResult(
                component="Project Brief",
                status=ValidationStatus.PASSED,
                message="Project brief is complete and ready"
            )
            
        except Exception as e:
            return ValidationResult(
                component="Project Brief",
                status=ValidationStatus.FAILED,
                message=f"Error reading project brief: {str(e)}"
            )
    
    def validate_prompt_template(self) -> ValidationResult:
        """Validate prompt template selection"""
        prompt_file = self.project_dir / "prompt_template.json"
        
        if not prompt_file.exists():
            return ValidationResult(
                component="Prompt Template",
                status=ValidationStatus.FAILED,
                message="Prompt template file not found"
            )
        
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                template = json.load(f)
            
            required_fields = ["app_type", "prompt_template", "key_features", "tech_stack"]
            missing_fields = []
            
            for field in required_fields:
                if field not in template:
                    missing_fields.append(field)
            
            if missing_fields:
                return ValidationResult(
                    component="Prompt Template",
                    status=ValidationStatus.FAILED,
                    message=f"Missing required fields: {', '.join(missing_fields)}",
                    details={"missing_fields": missing_fields}
                )
            
            # Validate app type
            valid_app_types = ["CRUD", "CHATBOT", "RAG", "DASHBOARD", "GENERATOR", "ANALYTICS"]
            if template["app_type"] not in valid_app_types:
                return ValidationResult(
                    component="Prompt Template",
                    status=ValidationStatus.FAILED,
                    message=f"Invalid app type: {template['app_type']}",
                    details={"valid_types": valid_app_types}
                )
            
            return ValidationResult(
                component="Prompt Template",
                status=ValidationStatus.PASSED,
                message=f"Prompt template for {template['app_type']} is ready"
            )
            
        except Exception as e:
            return ValidationResult(
                component="Prompt Template",
                status=ValidationStatus.FAILED,
                message=f"Error reading prompt template: {str(e)}"
            )
    
    def validate_boilerplate_selection(self) -> ValidationResult:
        """Validate boilerplate selection"""
        # In Phase 3, we don't use boilerplates - we generate code directly
        # This validation is not applicable for our approach
        return ValidationResult(
            component="Boilerplate Selection",
            status=ValidationStatus.PASSED,
            message="Boilerplate validation skipped - using direct code generation",
            details={"approach": "Phase 3 direct generation"}
        )
        
        try:
            with open(boilerplate_file, 'r', encoding='utf-8') as f:
                spec = json.load(f)
            
            required_fields = ["frontend_type", "backend_type", "database_type"]
            missing_fields = []
            
            for field in required_fields:
                if field not in spec:
                    missing_fields.append(field)
            
            if missing_fields:
                return ValidationResult(
                    component="Boilerplate Selection",
                    status=ValidationStatus.FAILED,
                    message=f"Missing required fields: {', '.join(missing_fields)}",
                    details={"missing_fields": missing_fields}
                )
            
            # Check if boilerplate files exist
            frontend_dir = Path("templates/boilerplates/frontend") / spec["frontend_type"].lower()
            backend_dir = Path("templates/boilerplates/backend") / spec["backend_type"].lower()
            
            missing_boilerplates = []
            if not frontend_dir.exists():
                missing_boilerplates.append(f"Frontend: {spec['frontend_type']}")
            if not backend_dir.exists():
                missing_boilerplates.append(f"Backend: {spec['backend_type']}")
            
            if missing_boilerplates:
                return ValidationResult(
                    component="Boilerplate Selection",
                    status=ValidationStatus.FAILED,
                    message=f"Missing boilerplate directories: {', '.join(missing_boilerplates)}",
                    details={"missing_boilerplates": missing_boilerplates}
                )
            
            return ValidationResult(
                component="Boilerplate Selection",
                status=ValidationStatus.PASSED,
                message=f"Boilerplates selected: {spec['frontend_type']} + {spec['backend_type']}"
            )
            
        except Exception as e:
            return ValidationResult(
                component="Boilerplate Selection",
                status=ValidationStatus.FAILED,
                message=f"Error reading boilerplate spec: {str(e)}"
            )
    
    def validate_api_integrations(self) -> ValidationResult:
        """Validate API integration specifications"""
        api_file = self.project_dir / "api_integrations.json"
        
        if not api_file.exists():
            return ValidationResult(
                component="API Integrations",
                status=ValidationStatus.WARNING,
                message="API integrations file not found - will use defaults"
            )
        
        try:
            with open(api_file, 'r', encoding='utf-8') as f:
                apis = json.load(f)
            
            # Validate required APIs are specified
            required_apis = []
            if "authentication" not in apis:
                required_apis.append("authentication")
            if "database" not in apis:
                required_apis.append("database")
            
            if required_apis:
                return ValidationResult(
                    component="API Integrations",
                    status=ValidationStatus.FAILED,
                    message=f"Missing required API specifications: {', '.join(required_apis)}",
                    details={"missing_apis": required_apis}
                )
            
            return ValidationResult(
                component="API Integrations",
                status=ValidationStatus.PASSED,
                message=f"API integrations configured: {len(apis)} services"
            )
            
        except Exception as e:
            return ValidationResult(
                component="API Integrations",
                status=ValidationStatus.FAILED,
                message=f"Error reading API integrations: {str(e)}"
            )
    
    def validate_environment_variables(self) -> ValidationResult:
        """Validate environment variable requirements"""
        env_file = self.project_dir / "env_requirements.json"
        
        if not env_file.exists():
            return ValidationResult(
                component="Environment Variables",
                status=ValidationStatus.WARNING,
                message="Environment requirements file not found - will use defaults"
            )
        
        try:
            with open(env_file, 'r', encoding='utf-8') as f:
                env_reqs = json.load(f)
            
            # Check if required env vars are documented
            required_vars = env_reqs.get("required", [])
            optional_vars = env_reqs.get("optional", [])
            
            if not required_vars:
                return ValidationResult(
                    component="Environment Variables",
                    status=ValidationStatus.WARNING,
                    message="No required environment variables specified"
                )
            
            return ValidationResult(
                component="Environment Variables",
                status=ValidationStatus.PASSED,
                message=f"Environment variables documented: {len(required_vars)} required, {len(optional_vars)} optional"
            )
            
        except Exception as e:
            return ValidationResult(
                component="Environment Variables",
                status=ValidationStatus.FAILED,
                message=f"Error reading environment requirements: {str(e)}"
            )
    
    def run_full_validation(self) -> Dict[str, Any]:
        """Run complete validation suite"""
        self.results = []
        
        # Run all validations
        self.results.append(self.validate_project_brief())
        self.results.append(self.validate_prompt_template())
        self.results.append(self.validate_boilerplate_selection())
        self.results.append(self.validate_api_integrations())
        self.results.append(self.validate_environment_variables())
        
        # Calculate overall status
        failed_count = sum(1 for r in self.results if r.status == ValidationStatus.FAILED)
        warning_count = sum(1 for r in self.results if r.status == ValidationStatus.WARNING)
        
        if failed_count > 0:
            overall_status = ValidationStatus.FAILED
        elif warning_count > 0:
            overall_status = ValidationStatus.WARNING
        else:
            overall_status = ValidationStatus.PASSED
        
        return {
            "overall_status": overall_status.value,
            "results": [r.to_dict() for r in self.results],
            "summary": {
                "total": len(self.results),
                "passed": sum(1 for r in self.results if r.status == ValidationStatus.PASSED),
                "failed": failed_count,
                "warnings": warning_count
            }
        }
    
    def generate_validation_report(self) -> str:
        """Generate human-readable validation report"""
        validation = self.run_full_validation()
        
        report = f"""
# Pre-Code Validation Report

## Overall Status: {validation['overall_status'].upper()}

## Summary
- Total Components: {validation['summary']['total']}
- ✅ Passed: {validation['summary']['passed']}
- ❌ Failed: {validation['summary']['failed']}
- ⚠️ Warnings: {validation['summary']['warnings']}

## Detailed Results
"""
        
        for result in validation['results']:
            status_icon = {
                'passed': '✅',
                'failed': '❌', 
                'warning': '⚠️',
                'pending': '⏳'
            }.get(result['status'], '❓')
            
            report += f"""
### {status_icon} {result['component']}
**Status:** {result['status'].upper()}
**Message:** {result['message']}
"""
            
            if result['details']:
                report += f"**Details:** {json.dumps(result['details'], indent=2)}\n"
        
        # Add recommendations
        if validation['overall_status'] == 'failed':
            report += """
## 🚨 CRITICAL ISSUES FOUND
**DO NOT PROCEED WITH CODING** until all failed validations are resolved.

### Required Actions:
1. Fix all failed validations above
2. Re-run validation
3. Ensure all specifications are complete
4. Get approval from coordinator
"""
        elif validation['overall_status'] == 'warning':
            report += """
## ⚠️ WARNINGS DETECTED
Proceed with caution. Some components may use default configurations.

### Recommendations:
1. Review warnings above
2. Consider addressing warnings for better customization
3. Ensure defaults are acceptable for your use case
"""
        else:
            report += """
## ✅ ALL SYSTEMS GO
All validations passed successfully. Ready to proceed with coding.

### Next Steps:
1. ✅ Validation complete
2. 🚀 Ready for Claude coding
3. 📋 Follow 5-prompt development plan
"""
        
        return report

def main():
    """Main validation function"""
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python pre_code_validator.py <project_directory>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    validator = PreCodeValidator(project_dir)
    
    # Generate and save report
    report = validator.generate_validation_report()
    
    report_file = Path(project_dir) / "validation_report.md"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"Validation report saved to: {report_file}")
    
    # Print summary to console
    validation = validator.run_full_validation()
    print(f"\nOverall Status: {validation['overall_status'].upper()}")
    
    if validation['overall_status'] == 'failed':
        print("❌ CRITICAL ISSUES FOUND - DO NOT PROCEED")
        sys.exit(1)
    elif validation['overall_status'] == 'warning':
        print("⚠️ WARNINGS DETECTED - Proceed with caution")
    else:
        print("✅ ALL SYSTEMS GO - Ready for coding")

if __name__ == "__main__":
    main()
