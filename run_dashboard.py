#!/usr/bin/env python3
"""
Simple script to run the Rynova AI Dashboard
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        sys.exit(1)

def run_streamlit():
    """Run the Streamlit dashboard"""
    print("Starting Rynova AI Dashboard...")
    print("🚀 Dashboard will open in your browser at: http://localhost:8501")
    print("📝 Press Ctrl+C to stop the dashboard")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped. Thank you for using Rynova AI!")
    except FileNotFoundError:
        print("❌ Streamlit not found. Installing...")
        install_requirements()
        run_streamlit()

if __name__ == "__main__":
    # Check if we're in the right directory
    if not os.path.exists("app.py"):
        print("❌ app.py not found. Please run this script from the dashboard directory.")
        sys.exit(1)
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found. Please ensure all files are present.")
        sys.exit(1)
    
    print("🤖 Rynova AI Dashboard Launcher")
    print("=" * 40)
    
    # Ask user if they want to install requirements
    choice = input("Install/update requirements? (y/n): ").lower().strip()
    if choice in ['y', 'yes']:
        install_requirements()
    
    # Run the dashboard
    run_streamlit()
