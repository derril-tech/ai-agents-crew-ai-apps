#!/usr/bin/env python
"""
SDR Assistant Application Runner

This script provides a unified entry point for running different components
of the SDR Assistant application.
"""

import sys
import argparse
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def run_flow():
    """Run the SDR flow with sample data"""
    try:
        from src.sdr_assistant_flow.main import kickoff
        print("🤖 Starting SDR Assistant Flow...")
        results = kickoff()
        print("✅ Flow completed successfully!")
        return results
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running flow: {e}")
        sys.exit(1)

def run_api(host="0.0.0.0", port=8000, reload=True):
    """Run the FastAPI server"""
    try:
        import uvicorn
        
        print(f"🌐 Starting API server on {host}:{port}")
        print(f"📚 API Documentation: http://{host}:{port}/docs")
        
        uvicorn.run(
            "src.sdr_assistant_flow.api.app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Install with: pip install uvicorn")
        sys.exit(1)
    except OSError as e:
        print(f"❌ Network error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting API server: {e}")
        sys.exit(1)

def plot_flow():
    """Generate flow visualization"""
    try:
        from src.sdr_assistant_flow.main import plot
        print("📊 Generating flow visualization...")
        plot()
        print("✅ Flow plot generated!")
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure plotting dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error generating plot: {e}")
        sys.exit(1)

def test_setup():
    """Test the application setup"""
    try:
        print("🧪 Testing SDR Assistant setup...")
        
        # Test imports
        print("  ✓ Testing imports...")
        from src.sdr_assistant_flow.utils.config import load_config
        
        # Test configuration
        print("  ✓ Testing configuration...")
        config = load_config()
        
        # Test API keys
        print("  ✓ Testing API keys...")
        if not config.openai_api_key or config.openai_api_key.startswith('your-'):
            print("  ⚠️  OpenAI API key not configured")
        else:
            print("  ✓ OpenAI API key configured")
            
        if not config.serper_api_key or config.serper_api_key.startswith('your-'):
            print("  ⚠️  Serper API key not configured")
        else:
            print("  ✓ Serper API key configured")
        
        # Test CrewAI
        print("  ✓ Testing CrewAI...")
        import crewai
        print(f"  ✓ CrewAI version: {crewai.__version__}")
        
        print("\n✅ Setup test completed successfully!")
        print("\n🚀 You're ready to run the SDR Assistant!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\n🔧 Please install missing dependencies.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        print("\n🔧 Please check your installation and configuration.")
        sys.exit(1)

def run_sample_analysis():
    """Run a sample lead analysis"""
    try:
        from src.sdr_assistant_flow.lead_types import LeadInput
        from src.sdr_assistant_flow.flows.sdr_flow import kickoff_flow
        
        print("🎯 Running sample lead analysis...")
        
        # Create a sample lead
        sample_lead = LeadInput(
            name="Sample User",
            job_title="Chief Technology Officer",
            company="Tech Innovations Inc",
            email="cto@techinnovations.com",
            linkedin_url="https://linkedin.com/in/sample-user",
            company_website="https://techinnovations.com",
            use_case="Looking to implement AI across engineering teams",
            source="demo"
        )
        
        # Run analysis
        flow = kickoff_flow([sample_lead])
        results = flow.get_campaign_results()
        
        print("✅ Sample analysis completed!")
        print(f"📊 Results: {results['leads_analyzed']} leads analyzed, {results['emails_generated']} emails generated")
        
        return results
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all modules are properly implemented")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running sample analysis: {e}")
        sys.exit(1)

def show_help():
    """Show available commands"""
    print("""
🤖 SDR Assistant - Available Commands

Usage: python run.py [command] [options]

Commands:
  flow          Run the SDR flow with sample data
  api           Start the FastAPI server
  plot          Generate flow visualization
  test          Test the application setup
  sample        Run sample lead analysis
  help          Show this help message

API Options:
  --host        API host (default: 0.0.0.0)
  --port        API port (default: 8000)
  --no-reload   Disable auto-reload

Examples:
  python run.py flow                    # Run flow with sample data
  python run.py api                     # Start API server
  python run.py api --port 8080         # Start API on port 8080
  python run.py test                    # Test setup
  python run.py sample                  # Run sample analysis

For more information, visit: https://github.com/aiaccellera/sdr-assistant-flow
    """)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="SDR Assistant - AI-powered Sales Development Representative",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        'command',
        nargs='?',
        default='help',
        choices=['flow', 'api', 'plot', 'test', 'sample', 'help'],
        help='Command to run'
    )
    
    # API specific arguments
    parser.add_argument('--host', default='0.0.0.0', help='API host')
    parser.add_argument('--port', type=int, default=8000, help='API port')
    parser.add_argument('--no-reload', action='store_true', help='Disable auto-reload')
    
    args = parser.parse_args()
    
    # Print banner
    print("🤖 SDR Assistant Flow")
    print("=" * 50)
    
    if args.command == 'flow':
        run_flow()
    elif args.command == 'api':
        run_api(args.host, args.port, not args.no_reload)
    elif args.command == 'plot':
        plot_flow()
    elif args.command == 'test':
        test_setup()
    elif args.command == 'sample':
        run_sample_analysis()
    else:
        show_help()

if __name__ == "__main__":
    main()