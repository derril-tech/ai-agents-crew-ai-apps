#!/usr/bin/env python
"""
SDR Assistant Flow - Main Entry Point

This file provides the main entry points for running the SDR Assistant Flow.
It supports both command-line execution and programmatic usage.
"""

import sys
import os
from pathlib import Path
from typing import List, Optional
import argparse
import json

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.sdr_assistant_flow.flows.sdr_flow import SDRAssistantFlow, kickoff_flow, plot_flow
from src.sdr_assistant_flow.lead_types import LeadInput
from src.sdr_assistant_flow.utils.config import load_config
from src.sdr_assistant_flow.utils.logger import get_logger

logger = get_logger(__name__)

def load_leads_from_file(file_path: str) -> List[LeadInput]:
    """Load leads from a JSON or CSV file"""
    try:
        with open(file_path, 'r') as f:
            if file_path.endswith('.json'):
                data = json.load(f)
                return [LeadInput(**lead) for lead in data]
            elif file_path.endswith('.csv'):
                import pandas as pd
                df = pd.read_csv(file_path)
                return [LeadInput(**row.to_dict()) for _, row in df.iterrows()]
            else:
                raise ValueError("File must be JSON or CSV format")
    except Exception as e:
        logger.error(f"Error loading leads from {file_path}: {str(e)}")
        raise

def kickoff(leads_file: Optional[str] = None, output_file: Optional[str] = None):
    """
    Main function to run the SDR Assistant Flow
    
    Args:
        leads_file: Optional path to file containing leads data
        output_file: Optional path to save results
    """
    logger.info("Starting SDR Assistant Flow...")
    
    # Load configuration
    config = load_config()
    
    # Load leads if file provided
    leads = None
    if leads_file:
        logger.info(f"Loading leads from: {leads_file}")
        leads = load_leads_from_file(leads_file)
        logger.info(f"Loaded {len(leads)} leads from file")
    
    # Run the flow
    flow = kickoff_flow(leads)
    
    # Get results
    results = flow.get_campaign_results()
    
    # Save results if output file specified
    if output_file:
        logger.info(f"Saving results to: {output_file}")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info("Results saved successfully")
    
    return results

def plot():
    """Generate a visual plot of the flow"""
    logger.info("Generating flow plot...")
    plot_flow()

def main():
    """Command-line interface for the SDR Assistant"""
    parser = argparse.ArgumentParser(description="SDR Assistant Flow - AI-powered lead analysis and email generation")
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Run command
    run_parser = subparsers.add_parser('run', help='Run the SDR flow')
    run_parser.add_argument('--leads-file', '-l', help='Path to leads file (JSON or CSV)')
    run_parser.add_argument('--output-file', '-o', help='Path to save results')
    
    # Plot command
    plot_parser = subparsers.add_parser('plot', help='Generate flow visualization')
    
    # API command
    api_parser = subparsers.add_parser('api', help='Start the API server')
    api_parser.add_argument('--host', default='0.0.0.0', help='API host')
    api_parser.add_argument('--port', type=int, default=8000, help='API port')
    api_parser.add_argument('--reload', action='store_true', help='Enable auto-reload')
    
    args = parser.parse_args()
    
    if args.command == 'run':
        results = kickoff(args.leads_file, args.output_file)
        print(f"\n✅ Campaign completed successfully!")
        print(f"📊 Results: {results['leads_analyzed']} leads analyzed, {results['emails_generated']} emails generated")
        
    elif args.command == 'plot':
        plot()
        
    elif args.command == 'api':
        logger.info(f"Starting API server on {args.host}:{args.port}")
        import uvicorn
        from src.sdr_assistant_flow.api.app import app
        uvicorn.run(
            "src.sdr_assistant_flow.api.app:app",
            host=args.host,
            port=args.port,
            reload=args.reload,
            log_level="info"
        )
        
    else:
        # Default behavior - run the flow
        results = kickoff()
        print(f"\n✅ Campaign completed successfully!")
        print(f"📊 Results: {results['leads_analyzed']} leads analyzed, {results['emails_generated']} emails generated")

if __name__ == "__main__":
    main()