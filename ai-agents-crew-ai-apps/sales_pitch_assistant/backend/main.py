#!/usr/bin/env python
import sys
import json
import warnings
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from sales_meeting_preparation.crew import SalesMeetingPreparation

warnings.filterwarnings("ignore", category=SyntaxWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def run():
    """
    Run the crew with a target person and company.
    Can accept command line arguments or use defaults.
    """
    # Check for command line arguments
    if len(sys.argv) >= 3:
        person = sys.argv[1]
        company = sys.argv[2]
    else:
        # Default values for testing
        person = 'Marc Benioff'
        company = 'Salesforce'
    
    inputs = {
        'person': person,
        'company': company
    }
    
    try:
        result = SalesMeetingPreparation().crew().kickoff(inputs=inputs)
        
        # Try to extract final output from known CrewAI formats
        final_output = None
        if hasattr(result, "final_output"):
            final_output = result.final_output
        elif hasattr(result, "output"):
            final_output = result.output
        elif isinstance(result, str):
            final_output = result
        else:
            final_output = str(result)
        
        if final_output:
            print("\n=== Sales Meeting Preparation Report ===\n")
            print(final_output)
            
            # Create outputs directory if it doesn't exist
            Path("outputs").mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            filename = f"sales_meeting_prep_{inputs['company'].lower().replace(' ', '_')}_{timestamp}.md"
            filepath = f"outputs/{filename}"
            
            # Save to file
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(final_output)
            
            print(f"\nReport saved to {filepath}")
            
            # Return JSON response for API integration
            response = {
                "success": True,
                "report": final_output,
                "filename": filename,
                "filepath": filepath,
                "person": person,
                "company": company,
                "timestamp": timestamp
            }
            
            return json.dumps(response, indent=2)
        else:
            error_response = {
                "success": False,
                "error": "No output content returned.",
                "person": person,
                "company": company
            }
            print("No output content returned.")
            return json.dumps(error_response, indent=2)
            
    except Exception as e:
        error_response = {
            "success": False,
            "error": str(e),
            "person": person,
            "company": company
        }
        print(f"An error occurred while running the crew: {e}")
        return json.dumps(error_response, indent=2)

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "person": "Training Exec",
        "company": "Training Co."
    }
    try:
        SalesMeetingPreparation().crew().train(
            n_iterations=int(sys.argv[1]),
            filename=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        SalesMeetingPreparation().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and return the results.
    """
    inputs = {
        "person": "Test Person",
        "company": "Test Company"
    }
    try:
        SalesMeetingPreparation().crew().test(
            n_iterations=int(sys.argv[1]),
            openai_model_name=sys.argv[2],
            inputs=inputs
        )
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")

if __name__ == "__main__":
    # Check for command line mode
    if len(sys.argv) > 1 and sys.argv[1] in ['train', 'replay', 'test']:
        if sys.argv[1] == 'train':
            train()
        elif sys.argv[1] == 'replay':
            replay()
        elif sys.argv[1] == 'test':
            test()
    else:
        # Run mode (default)
        result = run()
        print(result)