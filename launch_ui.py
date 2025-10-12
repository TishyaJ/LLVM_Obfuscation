#!/usr/bin/env python3
"""
UI Launcher for LLVM Obfuscator
Cross-platform launcher script
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install required dependencies."""
    print("Installing UI dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements_ui.txt'])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    try:
        import streamlit
        import plotly
        return True
    except ImportError:
        return False

def main():
    """Main launcher function."""
    print("🚀 LLVM Obfuscator Web UI Launcher")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("📦 Installing required dependencies...")
        if not install_dependencies():
            print("❌ Failed to install dependencies. Please install manually:")
            print("   pip install streamlit plotly pandas")
            return 1
    
    print("🌐 Starting web interface...")
    print("📍 URL: http://localhost:8501")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'obfuscator_ui.py',
            '--server.port', '8501',
            '--server.headless', 'false'
        ])
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    except Exception as e:
        print(f"❌ Error launching UI: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())