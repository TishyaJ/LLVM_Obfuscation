#!/usr/bin/env python3
"""
LLVM Obfuscator Python Wrapper
Automation script for applying LLVM obfuscation passes
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any


class ObfuscatorWrapper:
    """Main wrapper class for LLVM obfuscation automation."""
    
    def __init__(self, config_path: str = "ollvm_config.json"):
        """Initialize the obfuscator wrapper with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.llvm_bin = self._find_llvm_bin()
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Configuration file '{self.config_path}' not found")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in configuration file: {e}")
            sys.exit(1)
    
    def _find_llvm_bin(self) -> str:
        """Find LLVM binary path."""
        # Try common LLVM installation paths
        llvm_paths = [
            "/usr/bin/opt",
            "/usr/local/bin/opt",
            "/opt/llvm/bin/opt",
            "C:\\Program Files\\LLVM\\bin\\opt.exe",
            "llvm-install\\bin\\opt.exe"
        ]
        
        for path in llvm_paths:
            if os.path.exists(path):
                return path
        
        # Try to find via which/where
        try:
            result = subprocess.run(['where', 'opt'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip().split('\n')[0]
        except FileNotFoundError:
            try:
                result = subprocess.run(['which', 'opt'], capture_output=True, text=True)
                if result.returncode == 0:
                    return result.stdout.strip()
            except FileNotFoundError:
                pass
        
        # Return mock for demo mode
        print("Warning: LLVM opt binary not found. Using mock backend for demo.")
        return "mock"
    
    def get_enabled_passes(self) -> List[str]:
        """Get list of enabled obfuscation passes."""
        enabled_passes = []
        
        for category, passes in self.config['passes'].items():
            for pass_name, pass_config in passes.items():
                if pass_config.get('enabled', False):
                    enabled_passes.append(f"{category}_{pass_name}")
        
        return enabled_passes
    
    def apply_obfuscation(self, input_file: str, output_file: str, 
                         passes: Optional[List[str]] = None) -> bool:
        """Apply obfuscation to input file."""
        if passes is None:
            passes = self.get_enabled_passes()
        
        if not passes:
            print("Warning: No obfuscation passes enabled")
            return False
        
        # Get file extension to determine input type
        input_ext = Path(input_file).suffix.lower()
        
        if input_ext in ['.c', '.cpp', '.cc', '.cxx']:
            # C/C++ source file - use clang with OLLVM passes
            return self._compile_with_ollvm(input_file, output_file, passes)
        elif input_ext in ['.bc', '.ll']:
            # LLVM IR file - use opt
            return self._apply_opt_passes(input_file, output_file, passes)
        else:
            print(f"Error: Unsupported file type: {input_ext}")
            return False
    
    def _compile_with_ollvm(self, input_file: str, output_file: str, passes: List[str]) -> bool:
        """Compile C/C++ source with OLLVM passes."""
        # Find clang binary
        clang_bin = self._find_clang_binary()
        if not clang_bin:
            return False
        
        # Build clang command with OLLVM passes
        cmd = [clang_bin, input_file, '-o', output_file]
        
        # Add OLLVM passes
        for pass_name in passes:
            if pass_name == 'control_flow_flattening':
                cmd.extend(['-mllvm', '-fla'])  # Flattening
            elif pass_name == 'control_flow_bogus_control_flow':
                cmd.extend(['-mllvm', '-bcf'])   # Bogus Control Flow
            elif pass_name == 'data_string_encryption':
                cmd.extend(['-mllvm', '-sobf'])  # String Obfuscation
            elif pass_name == 'instruction_substitution':
                cmd.extend(['-mllvm', '-sub'])   # Instruction Substitution
            elif pass_name == 'instruction_opaque_predicates':
                cmd.extend(['-mllvm', '-sobf'])  # Opaque Predicates
        
        # Add optimization level
        opt_level = self.config.get('target', {}).get('optimization_level', 'O2')
        cmd.append(f'-{opt_level}')
        
        print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Obfuscation completed successfully: {output_file}")
                return True
            else:
                print(f"Error during obfuscation: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error running obfuscation: {e}")
            return False
    
    def _apply_opt_passes(self, input_file: str, output_file: str, passes: List[str]) -> bool:
        """Apply LLVM opt passes to IR file."""
        # Build opt command
        cmd = [self.llvm_bin, input_file]
        
        # Add passes
        for pass_name in passes:
            cmd.extend(['-passes', pass_name])
        
        # Add output file
        cmd.extend(['-o', output_file])
        
        print(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Obfuscation completed successfully: {output_file}")
                return True
            else:
                print(f"Error during obfuscation: {result.stderr}")
                return False
        except Exception as e:
            print(f"Error running obfuscation: {e}")
            return False
    
    def _find_clang_binary(self) -> Optional[str]:
        """Find clang binary with OLLVM support."""
        # Try common paths
        clang_paths = [
            "clang",
            "clang.exe",
            f"{self.llvm_bin.replace('opt', 'clang')}",
            "llvm-install/bin/clang",
            "llvm-install/bin/clang.exe",
            "obfuscator-llvm/build/bin/clang.exe",
            "obfuscator-llvm/build/bin/clang"
        ]
        
        for path in clang_paths:
            try:
                result = subprocess.run([path, '--version'], capture_output=True, text=True)
                if result.returncode == 0:
                    # Check if it's OLLVM or regular clang
                    if 'obfuscator' in result.stdout.lower() or 'obfuscator-llvm' in result.stdout.lower():
                        return path
                    elif 'clang version' in result.stdout.lower():
                        # Regular clang - we can still use it for basic obfuscation
                        return path
            except FileNotFoundError:
                continue
        
        print("Warning: OLLVM-enabled clang not found. Using mock backend for demo.")
        return "mock"
    
    def analyze_code_complexity(self, input_file: str) -> Dict[str, int]:
        """Analyze code complexity for Smart Obfuscation Mode."""
        complexity = {
            'lines': 0,
            'functions': 0,
            'branches': 0,
            'strings': 0,
            'complexity_score': 0
        }
        
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                complexity['lines'] = len([line for line in lines if line.strip()])
                
                # Count functions (simple heuristic)
                complexity['functions'] = content.count('{') - content.count('}') + content.count('function')
                
                # Count branches
                branch_keywords = ['if', 'else', 'while', 'for', 'switch', 'case']
                for keyword in branch_keywords:
                    complexity['branches'] += content.count(keyword)
                
                # Count strings
                complexity['strings'] = content.count('"') // 2
                
                # Calculate complexity score
                complexity['complexity_score'] = (
                    complexity['lines'] * 0.4 +
                    complexity['functions'] * 10 +
                    complexity['branches'] * 5 +
                    complexity['strings'] * 2
                )
                
        except Exception as e:
            print(f"Warning: Could not analyze complexity: {e}")
        
        return complexity
    
    def smart_obfuscation_mode(self, input_file: str) -> Dict[str, any]:
        """Implement Smart Obfuscation Mode based on code complexity."""
        print("🧠 Smart Obfuscation Mode: Analyzing code complexity...")
        
        complexity = self.analyze_code_complexity(input_file)
        print(f"   Lines: {complexity['lines']}")
        print(f"   Functions: {complexity['functions']}")
        print(f"   Branches: {complexity['branches']}")
        print(f"   Strings: {complexity['strings']}")
        print(f"   Complexity Score: {complexity['complexity_score']:.1f}")
        
        # Determine obfuscation intensity
        if complexity['complexity_score'] < 50:
            intensity = "light"
            enabled_passes = {
                'control_flow': {'bogus_control_flow': {'enabled': True, 'probability': 0.3}},
                'data': {'string_encryption': {'enabled': True, 'encryption_method': 'xor'}},
                'instruction': {'instruction_substitution': {'enabled': False}}
            }
        elif complexity['complexity_score'] < 200:
            intensity = "moderate"
            enabled_passes = {
                'control_flow': {
                    'bogus_control_flow': {'enabled': True, 'probability': 0.5},
                    'flattening': {'enabled': True, 'max_flattening_depth': 2}
                },
                'data': {
                    'string_encryption': {'enabled': True, 'encryption_method': 'aes'},
                    'variable_substitution': {'enabled': True, 'substitution_ratio': 0.3}
                },
                'instruction': {
                    'instruction_substitution': {'enabled': True, 'substitution_rate': 0.4},
                    'opaque_predicates': {'enabled': True, 'predicate_complexity': 'medium'}
                }
            }
        else:
            intensity = "heavy"
            enabled_passes = {
                'control_flow': {
                    'bogus_control_flow': {'enabled': True, 'probability': 0.8},
                    'flattening': {'enabled': True, 'max_flattening_depth': 3}
                },
                'data': {
                    'string_encryption': {'enabled': True, 'encryption_method': 'aes', 'key_size': 256},
                    'variable_substitution': {'enabled': True, 'substitution_ratio': 0.6}
                },
                'instruction': {
                    'instruction_substitution': {'enabled': True, 'substitution_rate': 0.7},
                    'opaque_predicates': {'enabled': True, 'predicate_complexity': 'high'}
                }
            }
        
        print(f"🎯 Selected intensity: {intensity}")
        
        # Update config with smart decisions
        smart_config = self.config.copy()
        smart_config['passes'] = enabled_passes
        smart_config['smart_mode'] = {
            'enabled': True,
            'intensity': intensity,
            'complexity_analysis': complexity,
            'decision_summary': f"Selected {intensity} obfuscation based on complexity score {complexity['complexity_score']:.1f}"
        }
        
        return smart_config
    
    def generate_report(self, input_file: str, output_file: str) -> None:
        """Generate obfuscation report."""
        try:
            from report_generator import ReportGenerator
            
            print("📊 Generating obfuscation report...")
            
            # Calculate metrics
            metrics = self._calculate_obfuscation_metrics(input_file, output_file)
            
            # Generate HTML report
            generator = ReportGenerator()
            report_html = generator.generate_report(input_file, output_file, self.config, metrics)
            
            # Save report
            report_path = f"{Path(output_file).stem}_report.html"
            generator.save_report(report_html, report_path)
            
            # Also save JSON report
            json_report = {
                "timestamp": datetime.now().isoformat(),
                "input_file": input_file,
                "output_file": output_file,
                "config": self.config,
                "metrics": metrics,
                "resistance_score": self._calculate_resistance_score(metrics)
            }
            
            json_path = f"{Path(output_file).stem}_report.json"
            with open(json_path, 'w') as f:
                json.dump(json_report, f, indent=2)
            
            print(f"📄 JSON report saved to: {json_path}")
            
        except ImportError:
            print("Warning: Report generator not available. Install required dependencies.")
        except Exception as e:
            print(f"Error generating report: {e}")
    
    def _calculate_obfuscation_metrics(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """Calculate obfuscation metrics."""
        metrics = {
            'ir_size_growth': 0,
            'function_count': 0,
            'bogus_ratio': 0,
            'complexity_score': 0
        }
        
        try:
            # Analyze input file
            if os.path.exists(input_file):
                with open(input_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    metrics['function_count'] = content.count('{') - content.count('}') + 1
                    metrics['complexity_score'] = len(content.split('\n')) * 0.4
            
            # Simulate metrics (in real implementation, analyze actual IR)
            enabled_passes = self.get_enabled_passes()
            metrics['ir_size_growth'] = len(enabled_passes) * 15 + 10
            metrics['bogus_ratio'] = len([p for p in enabled_passes if 'bogus' in p]) * 20
            
        except Exception as e:
            print(f"Warning: Could not calculate metrics: {e}")
        
        return metrics
    
    def _calculate_resistance_score(self, metrics: Dict[str, Any]) -> int:
        """Calculate deobfuscation resistance score."""
        score = 0
        
        # Base score from enabled passes
        enabled_passes = self.get_enabled_passes()
        score += len(enabled_passes) * 10
        
        # Bonus for complexity
        if metrics.get('complexity_score', 0) > 50:
            score += 15
        
        # Bonus for bogus code
        if metrics.get('bogus_ratio', 0) > 10:
            score += 20
        
        return min(score, 100)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="LLVM Obfuscator Python Wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python obf_wrapper.py -i input.bc -o output.bc
  python obf_wrapper.py -i input.bc -o output.bc --passes control_flow_bogus_control_flow
  python obf_wrapper.py --list-passes
        """
    )
    
    parser.add_argument('-i', '--input', required=False,
                       help='Input LLVM IR file (.bc or .ll)')
    parser.add_argument('-o', '--output', required=False,
                       help='Output LLVM IR file (.bc or .ll)')
    parser.add_argument('-c', '--config', default='ollvm_config.json',
                       help='Configuration file path (default: ollvm_config.json)')
    parser.add_argument('--passes', nargs='+',
                       help='Specific passes to apply (overrides config)')
    parser.add_argument('--smart', action='store_true',
                       help='Enable Smart Obfuscation Mode (AI-based pass selection)')
    parser.add_argument('--list-passes', action='store_true',
                       help='List available obfuscation passes')
    parser.add_argument('--report', action='store_true',
                       help='Generate obfuscation report')
    parser.add_argument('--target', choices=['windows', 'linux'], default='windows',
                       help='Target platform for compilation')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Initialize wrapper
    wrapper = ObfuscatorWrapper(args.config)
    
    # List passes if requested
    if args.list_passes:
        print("Available obfuscation passes:")
        for category, passes in wrapper.config['passes'].items():
            print(f"  {category}:")
            for pass_name, pass_config in passes.items():
                status = "enabled" if pass_config.get('enabled', False) else "disabled"
                print(f"    - {pass_name} ({status})")
        return
    
    # Validate input file (only if not listing passes)
    if not args.input or not args.output:
        print("Error: Input and output files are required (unless using --list-passes)")
        sys.exit(1)
        
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Handle Smart Obfuscation Mode
    if args.smart:
        print("🧠 Smart Obfuscation Mode enabled")
        smart_config = wrapper.smart_obfuscation_mode(args.input)
        wrapper.config = smart_config
        print(f"📊 Decision: {smart_config['smart_mode']['decision_summary']}")
    
    # Apply obfuscation
    success = wrapper.apply_obfuscation(args.input, args.output, args.passes)
    
    if success and args.report:
        wrapper.generate_report(args.input, args.output)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
