#!/usr/bin/env python3
"""
LLVM Obfuscator Launcher
Unified launcher for demo and production modes
"""

import subprocess
import sys
import os
import argparse

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="LLVM Obfuscator Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available Commands:
  setup          - Setup backend (demo/production)
  dashboard      - Launch web dashboard
  cli            - Command line interface
  demo           - Quick demo
  info           - Show system information
  
Examples:
  python launch_obfuscator.py setup
  python launch_obfuscator.py dashboard
  python launch_obfuscator.py cli -i input.c -o output.exe --smart
        """
    )
    
    parser.add_argument('command', 
                       choices=['setup', 'dashboard', 'cli', 'demo', 'info'],
                       help='Command to execute')
    
    # CLI arguments (passed through to enhanced wrapper)
    parser.add_argument('-i', '--input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    parser.add_argument('--smart', action='store_true', help='Smart mode')
    parser.add_argument('--real', action='store_true', help='Use real backend')
    parser.add_argument('--demo', action='store_true', help='Use demo backend')
    
    args, unknown = parser.parse_known_args()
    
    if args.command == 'setup':
        # Run backend setup
        subprocess.run([sys.executable, 'setup_backend.py'])
    
    elif args.command == 'dashboard':
        # Launch dashboard
        print("🚀 Launching LLVM Obfuscator Dashboard...")
        print("URL: http://localhost:8501")
        subprocess.run([sys.executable, 'launch_dashboard.py'])
    
    elif args.command == 'cli':
        # Run CLI interface
        if not args.input or not args.output:
            print("Error: CLI mode requires -i and -o arguments")
            sys.exit(1)
        
        cli_args = [sys.executable, 'enhanced_obf_wrapper.py']
        cli_args.extend(['-i', args.input, '-o', args.output])
        
        if args.smart:
            cli_args.append('--smart')
        if args.real:
            cli_args.append('--real')
        if args.demo:
            cli_args.append('--demo')
        
        # Add any unknown arguments
        cli_args.extend(unknown)
        
        subprocess.run(cli_args)
    
    elif args.command == 'demo':
        # Run quick demo
        print("🎬 Running Quick Demo...")
        subprocess.run([sys.executable, 'demo_complete.py'])
    
    elif args.command == 'info':
        # Show system information
        print("LLVM Obfuscator System Information")
        print("=" * 40)
        
        # Check Python version
        print(f"Python Version: {sys.version}")
        
        # Check available backends
        try:
            result = subprocess.run([
                sys.executable, 'enhanced_obf_wrapper.py', '--info', '--demo'
            ], capture_output=True, text=True)
            print("Demo Backend:", "Available" if result.returncode == 0 else "Not Available")
        except:
            print("Demo Backend: Not Available")
        
        try:
            result = subprocess.run([
                sys.executable, 'enhanced_obf_wrapper.py', '--info', '--real'
            ], capture_output=True, text=True)
            print("Production Backend:", "Available" if result.returncode == 0 else "Not Available")
        except:
            print("Production Backend: Not Available")
        
        # Check dependencies
        deps = ['streamlit', 'plotly', 'matplotlib']
        for dep in deps:
            try:
                __import__(dep)
                print(f"{dep}: Available")
            except ImportError:
                print(f"{dep}: Not Available")

if __name__ == "__main__":
    main()