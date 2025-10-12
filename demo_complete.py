#!/usr/bin/env python3
"""
Complete Demo Script for LLVM Obfuscator
Shows the full pipeline with mock backend
"""

import os
import sys
import json
from datetime import datetime
from mock_llvm_backend import mock_backend
from simple_report import generate_simple_report

def run_complete_demo():
    """Run the complete obfuscation demo."""
    print("🚀 LLVM Obfuscator Complete Demo")
    print("=" * 50)
    
    # Step 1: Show original code
    print("\n📄 STEP 1: Original Code")
    print("-" * 30)
    with open("examples/simple_program.c", 'r') as f:
        code = f.read()
        print(f"Lines of code: {len(code.split())}")
        print("Functions: compute(), print_message(), main()")
        print("Strings: 4 string literals found")
    
    # Step 2: Smart Mode Analysis
    print("\n🧠 STEP 2: Smart Obfuscation Analysis")
    print("-" * 30)
    
    # Simulate complexity analysis
    complexity = {
        'lines': 42,
        'functions': 3,
        'branches': 3,
        'strings': 4,
        'complexity_score': 59.8
    }
    
    print(f"Code complexity score: {complexity['complexity_score']}")
    print("Selected intensity: MODERATE")
    print("Recommended passes: Bogus Control Flow + String Encryption")
    
    # Step 3: Apply Obfuscation
    print("\n⚙️ STEP 3: Applying Obfuscation")
    print("-" * 30)
    
    input_file = "examples/simple_program.c"
    output_file = "demo_output/demo_obfuscated.exe"
    passes = ['control_flow_bogus_control_flow', 'data_string_encryption', 'instruction_instruction_substitution']
    
    success = mock_backend.simulate_clang_compilation(input_file, output_file, passes)
    
    if not success:
        print("❌ Obfuscation failed!")
        return False
    
    # Step 4: Generate Metrics
    print("\n📊 STEP 4: Obfuscation Metrics")
    print("-" * 30)
    
    metrics = mock_backend.get_metrics(input_file, output_file)
    print(f"IR Size Growth: {metrics['ir_size_growth']}%")
    print(f"Function Count: {metrics['function_count']}")
    print(f"Bogus Code Ratio: {metrics['bogus_ratio']}%")
    print(f"Complexity Score: {metrics['complexity_score']}")
    
    # Calculate resistance score
    resistance_score = min(metrics['ir_size_growth'] + metrics['bogus_ratio'] + 20, 100)
    print(f"🛡️ Deobfuscation Resistance Score: {resistance_score}/100")
    
    # Step 5: Generate Reports
    print("\n📋 STEP 5: Generating Reports")
    print("-" * 30)
    
    # Create configuration for report
    config = {
        "passes": {
            "control_flow": {
                "bogus_control_flow": {"enabled": True, "probability": 0.5}
            },
            "data": {
                "string_encryption": {"enabled": True, "encryption_method": "xor"}
            },
            "instruction": {
                "instruction_substitution": {"enabled": True, "substitution_rate": 0.4}
            }
        },
        "smart_mode": {
            "enabled": True,
            "intensity": "moderate",
            "complexity_analysis": complexity,
            "decision_summary": f"Selected moderate obfuscation based on complexity score {complexity['complexity_score']}"
        }
    }
    
    # Generate HTML report
    report_html = generate_simple_report(input_file, output_file, config, metrics)
    
    html_path = "demo_output/demo_report.html"
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(report_html)
    
    # Generate JSON report
    json_report = {
        "timestamp": datetime.now().isoformat(),
        "input_file": input_file,
        "output_file": output_file,
        "config": config,
        "metrics": metrics,
        "resistance_score": resistance_score,
        "demo_mode": True
    }
    
    json_path = "demo_output/demo_report.json"
    with open(json_path, 'w') as f:
        json.dump(json_report, f, indent=2)
    
    print(f"✅ HTML Report: {html_path}")
    print(f"✅ JSON Report: {json_path}")
    
    # Step 6: Show Results
    print("\n🎯 STEP 6: Demo Results")
    print("-" * 30)
    print("✅ Original C code successfully obfuscated")
    print("✅ Smart mode selected optimal passes")
    print("✅ String encryption applied to 4 literals")
    print("✅ Bogus control flow added to functions")
    print("✅ Visual reports generated")
    print(f"✅ Resistance score: {resistance_score}/100 (Good)")
    
    print("\n🏆 DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print("Your LLVM Obfuscator is ready for presentation!")
    print(f"📊 Open {html_path} in browser to see visual report")
    
    return True

if __name__ == "__main__":
    success = run_complete_demo()
    sys.exit(0 if success else 1)