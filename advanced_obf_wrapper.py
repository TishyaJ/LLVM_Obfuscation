#!/usr/bin/env python3
"""
Enhanced LLVM Obfuscator Wrapper
Supports both mock backend (for demo) and real Polaris backend (for production)
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

class EnhancedObfuscatorWrapper:
    """Enhanced wrapper supporting multiple backends."""
    
    def __init__(self, config_path: str = "ollvm_config.json", use_real_backend: bool = False):
        self.config_path = config_path
        self.config = self._load_config()
        self.use_real_backend = use_real_backend
        
        # Initialize backends
        if use_real_backend:
            try:
                from llvm_backend_engine import AdvancedLLVMBackend
                self.backend = AdvancedLLVMBackend()
                self.backend_type = "Advanced-LLVM"
            except ImportError:
                print("⚠️ Polaris backend not available, falling back to mock")
                from mock_llvm_backend import mock_backend
                self.backend = mock_backend
                self.backend_type = "Mock"
        else:
            from mock_llvm_backend import mock_backend
            self.backend = mock_backend
            self.backend_type = "Mock"
    
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
    
    def get_enabled_passes(self) -> List[str]:
        """Get list of enabled obfuscation passes."""
        enabled_passes = []
        
        for category, passes in self.config['passes'].items():
            for pass_name, pass_config in passes.items():
                if pass_config.get('enabled', False):
                    enabled_passes.append(f"{category}_{pass_name}")
        
        return enabled_passes
    
    def apply_obfuscation(self, input_file: str, output_file: str, 
                         passes: Optional[List[str]] = None, config: Dict = None) -> bool:
        """Apply obfuscation to input file."""
        if passes is None:
            passes = self.get_enabled_passes()
        
        if not passes:
            print("Warning: No obfuscation passes enabled")
            return False
        
        print(f"🔧 Using {self.backend_type} backend")
        
        # Get file extension to determine input type
        input_ext = Path(input_file).suffix.lower()
        
        if input_ext in ['.c', '.cpp', '.cc', '.cxx']:
            return self._compile_with_backend(input_file, output_file, passes, config)
        else:
            print(f"Error: Unsupported file type: {input_ext}")
            return False
    
    def _compile_with_backend(self, input_file: str, output_file: str, 
                            passes: List[str], config: Dict = None) -> bool:
        """Compile with selected backend."""
        
        if self.backend_type == "Advanced-LLVM":
            # Use real LLVM backend
            success, metrics = self.backend.compile_with_obfuscation(
                input_file, output_file, passes, config
            )
            
            if success:
                print(f"✅ Real obfuscation completed: {output_file}")
                # Store metrics for reporting
                self._store_metrics(metrics)
                return True
            else:
                print("❌ Real obfuscation failed, falling back to mock")
                # Fallback to mock backend
                from mock_llvm_backend import mock_backend
                return mock_backend.simulate_clang_compilation(input_file, output_file, passes)
        
        else:
            # Use mock backend
            print("🎭 Using Mock Backend for Demo")
            return self.backend.simulate_clang_compilation(input_file, output_file, passes)
    
    def _store_metrics(self, metrics: Dict):
        """Store metrics for later use."""
        self._last_metrics = metrics
    
    def get_metrics(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """Get obfuscation metrics."""
        if hasattr(self, '_last_metrics'):
            return self._last_metrics
        else:
            return self.backend.get_metrics(input_file, output_file)
    
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
                
                # Count functions
                complexity['functions'] = max(1, content.count('{') - content.count('}') + 1)
                
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
                'control_flow': {
                    'bogus_control_flow': {'enabled': True, 'probability': 0.3}
                },
                'data': {
                    'string_encryption': {'enabled': True, 'encryption_method': 'xor'}
                },
                'instruction': {
                    'instruction_substitution': {'enabled': False}
                }
            }
        elif complexity['complexity_score'] < 200:
            intensity = "moderate"
            enabled_passes = {
                'control_flow': {
                    'bogus_control_flow': {'enabled': True, 'probability': 0.5},
                    'flattening': {'enabled': True, 'max_flattening_depth': 2}
                },
                'data': {
                    'string_encryption': {'enabled': True, 'encryption_method': 'xor'},
                    'variable_substitution': {'enabled': False}
                },
                'instruction': {
                    'instruction_substitution': {'enabled': True, 'substitution_rate': 0.4},
                    'opaque_predicates': {'enabled': False}
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
                    'string_encryption': {'enabled': True, 'encryption_method': 'xor', 'key_size': 256},
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
    
    def get_backend_info(self) -> Dict[str, str]:
        """Get backend information."""
        info = {
            'backend_type': self.backend_type,
            'status': 'Available'
        }
        
        if self.backend_type == "Polaris-LLVM":
            info.update(self.backend.get_version_info())
        else:
            info.update({
                'backend': 'Mock LLVM Backend',
                'llvm_version': '16.0.6 (simulated)',
                'status': 'Demo Mode'
            })
        
        return info

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Enhanced LLVM Obfuscator Wrapper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Demo mode (mock backend)
  python enhanced_obf_wrapper.py -i input.c -o output.exe --demo
  
  # Production mode (real Polaris backend)
  python enhanced_obf_wrapper.py -i input.c -o output.exe --real
  
  # Smart mode with real backend
  python enhanced_obf_wrapper.py -i input.c -o output.exe --real --smart
        """
    )
    
    parser.add_argument('-i', '--input', required=True,
                       help='Input C/C++ source file')
    parser.add_argument('-o', '--output', required=True,
                       help='Output executable file')
    parser.add_argument('-c', '--config', default='ollvm_config.json',
                       help='Configuration file path')
    parser.add_argument('--passes', nargs='+',
                       help='Specific passes to apply')
    parser.add_argument('--smart', action='store_true',
                       help='Enable Smart Obfuscation Mode')
    parser.add_argument('--real', action='store_true',
                       help='Use real Polaris backend (requires build)')
    parser.add_argument('--demo', action='store_true',
                       help='Use mock backend for demo')
    parser.add_argument('--build-polaris', action='store_true',
                       help='Build Polaris-Obfuscator backend')
    parser.add_argument('--info', action='store_true',
                       help='Show backend information')
    parser.add_argument('--target', choices=['windows', 'linux'], default='windows',
                       help='Target platform')
    
    args = parser.parse_args()
    
    # Determine backend type
    use_real_backend = args.real or args.build_polaris
    
    # Initialize wrapper
    wrapper = EnhancedObfuscatorWrapper(args.config, use_real_backend)
    
    # Handle special commands
    if args.build_polaris:
        print("🔨 Building Polaris-Obfuscator...")
        if wrapper.backend_type == "Polaris-LLVM":
            success = wrapper.backend.build_polaris()
            sys.exit(0 if success else 1)
        else:
            print("❌ Polaris backend not available")
            sys.exit(1)
    
    if args.info:
        info = wrapper.get_backend_info()
        print("Backend Information:")
        for key, value in info.items():
            print(f"  {key}: {value}")
        return
    
    # Validate input file
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found")
        sys.exit(1)
    
    # Handle Smart Obfuscation Mode
    config = {'target_platform': args.target.title()}
    
    if args.smart:
        print("🧠 Smart Obfuscation Mode enabled")
        smart_config = wrapper.smart_obfuscation_mode(args.input)
        wrapper.config = smart_config
        print(f"📊 Decision: {smart_config['smart_mode']['decision_summary']}")
    
    # Apply obfuscation
    start_time = time.time()
    success = wrapper.apply_obfuscation(args.input, args.output, args.passes, config)
    end_time = time.time()
    
    if success:
        print(f"✅ Obfuscation completed in {end_time - start_time:.2f} seconds")
        
        # Show metrics
        metrics = wrapper.get_metrics(args.input, args.output)
        print(f"📊 IR Size Growth: {metrics.get('ir_size_growth', 0)}%")
        print(f"📊 Bogus Code Ratio: {metrics.get('bogus_ratio', 0)}%")
        print(f"📊 Passes Applied: {metrics.get('passes_applied', len(args.passes or []))}")
    else:
        print("❌ Obfuscation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()