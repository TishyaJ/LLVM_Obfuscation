#!/usr/bin/env python3
"""
Mock LLVM Backend for Demo
Simulates LLVM obfuscation without requiring full LLVM installation
"""

import os
import random

class MockLLVMBackend:
    """Mock LLVM backend that simulates obfuscation for demo purposes."""
    
    def __init__(self):
        self.version = "16.0.6 (mock)"
        self.passes_applied = []
    
    def simulate_clang_compilation(self, input_file, output_file, passes):
        """Simulate clang compilation with obfuscation passes."""
        print(f"[MOCK] Compiling {input_file} -> {output_file}")
        print(f"[MOCK] Applying passes: {', '.join(passes)}")
        
        # Read input file
        with open(input_file, 'r') as f:
            original_code = f.read()
        
        # Simulate obfuscated output
        obfuscated_code = self._simulate_obfuscation(original_code, passes)
        
        # Create output directory if needed
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        # Create mock executable
        with open(output_file, 'w') as f:
            f.write(f"// Obfuscated version of {input_file}\n")
            f.write(f"// Applied passes: {', '.join(passes)}\n")
            f.write(obfuscated_code)
        
        self.passes_applied = passes
        return True
    
    def _simulate_obfuscation(self, code, passes):
        """Simulate code obfuscation."""
        lines = code.split('\n')
        obfuscated_lines = []
        
        for line in lines:
            # Simulate bogus control flow
            if 'control_flow_bogus_control_flow' in passes and 'if' in line:
                obfuscated_lines.append(line)
                obfuscated_lines.append("    // BOGUS: if (0 == 0) goto fake_block;")
            
            # Simulate string encryption
            elif 'data_string_encryption' in passes and '"' in line:
                encrypted_line = line.replace('"', '"[ENCRYPTED]')
                obfuscated_lines.append(encrypted_line)
            
            # Simulate instruction substitution
            elif 'instruction_instruction_substitution' in passes and '+' in line:
                substituted_line = line.replace('+', '- (-')
                if substituted_line != line:
                    substituted_line += ')'
                obfuscated_lines.append(substituted_line)
            
            else:
                obfuscated_lines.append(line)
        
        return '\n'.join(obfuscated_lines)
    
    def get_metrics(self, original_file, obfuscated_file):
        """Generate realistic obfuscation metrics."""
        base_growth = random.randint(25, 40)
        base_bogus = random.randint(15, 25)
        
        metrics = {
            'ir_size_growth': base_growth,
            'function_count': random.randint(2, 6),
            'bogus_ratio': base_bogus,
            'complexity_score': random.randint(45, 95),
            'processing_time': random.uniform(1.2, 3.8),
            'memory_usage': random.randint(45, 120),
            'optimization_level': 'O2'
        }
        
        # Adjust based on applied passes
        if 'control_flow_bogus_control_flow' in self.passes_applied:
            metrics['ir_size_growth'] += random.randint(15, 25)
            metrics['bogus_ratio'] += random.randint(10, 20)
        
        if 'data_string_encryption' in self.passes_applied:
            metrics['ir_size_growth'] += random.randint(8, 15)
            metrics['complexity_score'] += random.randint(10, 20)
        
        if 'instruction_instruction_substitution' in self.passes_applied:
            metrics['ir_size_growth'] += random.randint(12, 18)
            metrics['complexity_score'] += random.randint(8, 15)
        
        if 'control_flow_flattening' in self.passes_applied:
            metrics['ir_size_growth'] += random.randint(20, 35)
            metrics['bogus_ratio'] += random.randint(15, 25)
        
        # Ensure realistic bounds
        metrics['ir_size_growth'] = min(metrics['ir_size_growth'], 150)
        metrics['bogus_ratio'] = min(metrics['bogus_ratio'], 60)
        
        return metrics

# Create global mock backend instance
mock_backend = MockLLVMBackend()