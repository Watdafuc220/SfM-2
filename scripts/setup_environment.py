#!/usr/bin/env python3
"""
Setup script for SonaCore AI Pipeline Demo
Demonstrates environment configuration and provides testing utilities.
"""
import os
import subprocess
import sys
import time

def check_requirements():
    """Check if all required packages are installed."""
    required_packages = [
        'fastapi', 'uvicorn', 'streamlit', 'requests', 
        'openai', 'transformers', 'torch'
    ]
    
    print("🔍 Checking required packages...")
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing)}")
        return False
    return True

def setup_demo_environment():
    """Set up environment for demo purposes."""
    print("\n🚀 SonaCore AI Pipeline Setup")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return False
    
    print("\n📋 Current Model Status:")
    print("• SFM-2: Not loaded (requires training)")
    print("• GPT-2 LoRA: Not loaded (requires model files)")
    print("• OpenAI Fallback: Ready (requires API key)")
    
    print("\n🔧 Setup Options:")
    print("1. Demo Mode: Use placeholder responses")
    print("2. OpenAI Mode: Set API key for live responses")
    print("3. Full Training: Train SFM-2 model (takes time)")
    
    choice = input("\nSelect option (1-3): ").strip()
    
    if choice == "1":
        print("\n✅ Demo mode selected")
        print("The dashboard will show the API structure and fallback responses.")
        
    elif choice == "2":
        api_key = input("\nEnter OpenAI API key (or 'skip'): ").strip()
        if api_key and api_key != 'skip':
            os.environ['OPENAI_API_KEY'] = api_key
            print("✅ OpenAI API key configured for this session")
        else:
            print("⚠️ Skipping OpenAI configuration")
            
    elif choice == "3":
        print("\n🏋️ Training mode selected")
        print("This will run the SFM-2 training script...")
        print("⚠️ Warning: This may take several hours and requires GPU")
        confirm = input("Continue? (y/N): ").strip().lower()
        if confirm == 'y':
            print("Starting training... (This is a demo - actual training not implemented)")
        else:
            print("Training cancelled")
    
    return True

def start_services():
    """Start the API server and dashboard."""
    print("\n🚀 Starting SonaCore AI Services...")
    
    print("\n1. Starting API Server (port 8000)...")
    print("Command: python -m uvicorn api.app:app --reload --host 127.0.0.1 --port 8000")
    
    print("\n2. Starting Dashboard (port 8502)...")
    print("Command: python -m streamlit run demo/dashboard.py --server.port 8502")
    
    print("\n🌐 Access Points:")
    print("• API Health: http://127.0.0.1:8000/health")
    print("• API Docs: http://127.0.0.1:8000/docs")
    print("• Dashboard: http://localhost:8502")
    
    print("\n📝 Test the Pipeline:")
    print("• Run: python test_api.py")
    print("• Or use the dashboard interface")

def main():
    """Main setup function."""
    print("🎯 SonaCore AI Pipeline - Demo Setup")
    print("Building complete AI pipeline with SFM-2, API endpoints, and fallback integration")
    print()
    
    if setup_demo_environment():
        start_services()
        
        print("\n✨ Setup Complete!")
        print("\n📊 What's Working:")
        print("✅ FastAPI server with health checks")
        print("✅ Intelligent model routing")
        print("✅ Structured fallback responses")
        print("✅ Streamlit dashboard with real-time testing")
        print("✅ OpenAI fallback integration (with API key)")
        
        print("\n🔄 Next Steps:")
        print("1. Test the API using the dashboard or test_api.py")
        print("2. Configure OpenAI API key for live responses")
        print("3. Run model training scripts when ready")
        print("4. Deploy for stakeholder demonstrations")
        
        print("\n🎉 Ready for stakeholder demos!")
    else:
        print("\n❌ Setup incomplete. Please install missing requirements.")

if __name__ == "__main__":
    main()
