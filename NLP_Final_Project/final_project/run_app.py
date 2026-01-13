#!/usr/bin/env python3
"""
Simple launcher script for the MovieMate Streamlit app
"""

import subprocess
import sys
import os

def main():
    """Launch the Streamlit app"""
    
    print("🎬 Starting MovieMate - AI Movie Recommender...")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('IMDB Top 1000 Movies.csv'):
        print("❌ Error: IMDB Top 1000 Movies.csv not found in current directory")
        print("Please make sure you're running this from the correct directory")
        return
    
    if not os.path.exists('app.py'):
        print("❌ Error: app.py not found in current directory")
        return
    
    print("✅ Found required files")
    print("🚀 Launching Streamlit app...")
    print("📱 The app will open in your default web browser")
    print("🔗 If it doesn't open automatically, visit: http://localhost:8501")
    print("=" * 50)
    
    try:
        # Launch Streamlit
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error launching app: {e}")
        print("💡 Make sure Streamlit is installed: pip install streamlit")
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")

if __name__ == "__main__":
    main()
