#!/usr/bin/env python3
"""
🌍 Smart Place Recommender - Startup Script
Simple script to run the Flask application with helpful messages
"""

import os
import sys
import subprocess
import webbrowser
import time

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'requests', 'pandas', 'numpy', 'sentence_transformers']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install them using:")
        print("   pip install -r requirements.txt")
        return False
    
    print("✅ All required packages are installed!")
    return True

def check_api_key():
    """Check if Google API key is configured"""
    try:
        with open('app.py', 'r') as f:
            content = f.read()
            if 'AIzaSyDzbgxX9OR4-ds2SgMOAGWlhZYRZf9pZIM' in content:
                print("⚠️  Warning: Using default API key. Consider using your own Google Places API key.")
                print("   Get one from: https://console.cloud.google.com/")
            else:
                print("✅ Google API key is configured!")
    except FileNotFoundError:
        print("❌ app.py not found!")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🌍 Smart Place Recommender")
    print("=" * 40)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check API key
    check_api_key()
    
    print("\n🚀 Starting the application...")
    print("📍 The website will open automatically in your browser")
    print("🔗 Or visit: http://localhost:5000")
    print("\n⏹️  Press Ctrl+C to stop the application")
    print("-" * 40)
    
    try:
        # Start the Flask app
        from app import app
        
        # Open browser after a short delay
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:5000')
        
        import threading
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # Run the app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error starting application: {e}")
        print("💡 Make sure you're in the correct directory and all files are present")

if __name__ == "__main__":
    main()

