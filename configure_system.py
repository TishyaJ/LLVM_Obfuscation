#!/usr/bin/env python3
"""
LLVM Obfuscator Backend Setup
Choose between demo mode and production mode
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("LLVM OBFUSCATOR BACKEND SETUP")
    print("Choose your obfuscation backend")
    print("=" * 60)
    print()

def check_polaris_status():
    """Check if Polaris is available and built."""
    polaris_path = Path("Polaris-Obfuscator")
    
    if not polaris_path.exists():
        return "not_cloned", "Polaris-Obfuscator not found"
    
    build_path = polaris_path / "build"
    clang_path = build_path / "bin" / "clang"
    
    if not build_path.exists():
        return "not_built", "Polaris not built"
    
    if not clang_path.exists():
        return "not_built", "Clang binary not found"
    
    return "ready", "Polaris ready for production use"

def setup_demo_mode():
    """Set up demo mode."""
    print("🎭 Setting up Demo Mode...")
    print()
    print("Demo mode uses a mock LLVM backend that simulates obfuscation")
    print("Perfect for presentations and demonstrations")
    print()
    
    # Test demo mode
    try:
        result = subprocess.run([
            sys.executable, "enhanced_obf_wrapper.py", "--info", "--demo"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✅ Demo mode ready!")
            print()
            print("Test commands:")
            print("  python enhanced_obf_wrapper.py -i examples/simple_program.c -o demo.exe --demo --smart")
            print("  python launch_dashboard.py")
            return True
        else:
            print("❌ Demo mode setup failed")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def setup_production_mode():
    """Set up production mode."""
    print("🔧 Setting up Production Mode...")
    print()
    print("Production mode uses real LLVM obfuscation with Polaris-Obfuscator")
    print("Provides actual code obfuscation with real metrics")
    print()
    
    status, message = check_polaris_status()
    print(f"Polaris Status: {message}")
    
    if status == "ready":
        print("✅ Production mode ready!")
        print()
        print("Test commands:")
        print("  python enhanced_obf_wrapper.py -i examples/simple_program.c -o prod.exe --real --smart")
        return True
    
    elif status == "not_built":
        print("🔨 Building Polaris-Obfuscator...")
        print("⚠️  This will take 30-60 minutes and requires 5GB+ disk space")
        
        confirm = input("Continue with build? (y/N): ").lower().strip()
        if confirm != 'y':
            print("❌ Build cancelled")
            return False
        
        try:
            result = subprocess.run([
                sys.executable, "enhanced_obf_wrapper.py", "--build-polaris"
            ], timeout=3600)  # 1 hour timeout
            
            if result.returncode == 0:
                print("✅ Production mode ready!")
                return True
            else:
                print("❌ Build failed")
                return False
        except subprocess.TimeoutExpired:
            print("❌ Build timed out (>1 hour)")
            return False
        except Exception as e:
            print(f"❌ Build error: {e}")
            return False
    
    else:  # not_cloned
        print("❌ Polaris-Obfuscator not found")
        print("The repository should have been cloned already")
        return False

def main():
    """Main setup function."""
    print_banner()
    
    print("Available modes:")
    print()
    print("1. Demo Mode (Recommended for presentations)")
    print("   - Fast setup, no build required")
    print("   - Mock obfuscation with realistic metrics")
    print("   - Perfect for demonstrations and testing UI")
    print()
    print("2. Production Mode (For real obfuscation)")
    print("   - Requires building Polaris-Obfuscator (30-60 min)")
    print("   - Real LLVM obfuscation with actual transformations")
    print("   - 5GB+ disk space required")
    print()
    print("3. Both Modes")
    print("   - Set up both demo and production backends")
    print("   - Switch between modes in the dashboard")
    print()
    
    while True:
        choice = input("Choose mode (1/2/3/q to quit): ").strip()
        
        if choice == 'q':
            print("Setup cancelled")
            return
        
        elif choice == '1':
            print()
            success = setup_demo_mode()
            break
        
        elif choice == '2':
            print()
            success = setup_production_mode()
            break
        
        elif choice == '3':
            print()
            print("Setting up both modes...")
            demo_success = setup_demo_mode()
            print()
            prod_success = setup_production_mode()
            success = demo_success and prod_success
            break
        
        else:
            print("Invalid choice. Please enter 1, 2, 3, or q")
    
    print()
    print("=" * 60)
    if success:
        print("✅ SETUP COMPLETED SUCCESSFULLY!")
        print()
        print("Next steps:")
        print("1. Launch dashboard: python launch_dashboard.py")
        print("2. Or use CLI: python enhanced_obf_wrapper.py --help")
        print("3. For presentations: Use demo mode")
        print("4. For real obfuscation: Use production mode")
    else:
        print("❌ SETUP FAILED")
        print()
        print("Troubleshooting:")
        print("1. Check system requirements (Python 3.10+, CMake, Ninja)")
        print("2. Ensure sufficient disk space (5GB+ for production)")
        print("3. Check network connection for cloning repositories")
    print("=" * 60)

if __name__ == "__main__":
    main()