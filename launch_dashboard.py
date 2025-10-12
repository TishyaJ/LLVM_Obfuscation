#!/usr/bin/env python3
"""
Launch Production Dashboard
Simple launcher for the LLVM Obfuscator production interface
"""

import subprocess
import sys
import os

def main():
    """Launch the production dashboard."""
    print("LLVM Code Obfuscator - Production Dashboard")
    print("=" * 50)
    print("Starting dashboard...")
    print("URL: http://localhost:8501")
    print("Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Launch production dashboard
        subprocess.run([
            sys.executable, '-m', 'streamlit', 'run', 'production_dashboard.py',
            '--server.port', '8501',
            '--server.headless', 'false'
        ])
    except KeyboardInterrupt:
        print("\nShutting down dashboard...")
    except Exception as e:
        print(f"Error launching dashboard: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())