#!/usr/bin/env python3
"""
HTML Report Generator for LLVM Obfuscator
Generates visual dashboard reports with metrics and charts
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

class ReportGenerator:
    """Generate HTML reports for obfuscation results."""
    
    def __init__(self):
        self.template = self._get_html_template()
    
    def _get_html_template(self) -> str:
        """Get HTML template for the report."""
        return r"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LLVM Obfuscation Report</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 2.5em;
        }
        .header p {
            margin: 10px 0 0 0;
            opacity: 0.9;
        }
        .content {
            padding: 30px;
        }
        .section {
            margin-bottom: 30px;
        }
        .section h2 {
            color: #333;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .metric-card {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
        }
        .metric-value {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        .metric-label {
            color: #666;
            margin-top: 5px;
        }
        .passes-table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .passes-table th,
        .passes-table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        .passes-table th {
            background-color: #667eea;
            color: white;
        }
        .passes-table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .status-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8em;
            font-weight: bold;
        }
        .status-enabled {
            background-color: #d4edda;
            color: #155724;
        }
        .status-disabled {
            background-color: #f8d7da;
            color: #721c24;
        }
        .resistance-score {
            background: linear-gradient(90deg, #ff6b6b, #ffd93d, #6bcf7f);
            height: 20px;
            border-radius: 10px;
            position: relative;
            margin: 10px 0;
        }
        .resistance-score::after {
            content: attr(data-score);
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            font-weight: bold;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
        }
        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #666;
            border-top: 1px solid #e9ecef;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>LLVM Obfuscation Report</h1>
            <p>Generated on {timestamp}</p>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>Obfuscation Metrics</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{ir_size_growth}%</div>
                        <div class="metric-label">IR Size Growth</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{function_count}</div>
                        <div class="metric-label">Functions Obfuscated</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{bogus_ratio}%</div>
                        <div class="metric-label">Bogus Code Ratio</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{resistance_score}</div>
                        <div class="metric-label">Resistance Score</div>
                    </div>
                </div>
            </div>
            
            <div class="section">
                <h2>Applied Passes</h2>
                <table class="passes-table">
                    <thead>
                        <tr>
                            <th>Pass Name</th>
                            <th>Category</th>
                            <th>Status</th>
                            <th>Parameters</th>
                        </tr>
                    </thead>
                    <tbody>
                        {passes_rows}
                    </tbody>
                </table>
            </div>
            
            <div class="section">
                <h2>Deobfuscation Resistance</h2>
                <div class="resistance-score" data-score="{resistance_score}/100" style="width: {resistance_score}%"></div>
                <p>This score indicates the difficulty level for reverse engineers to deobfuscate the code.</p>
            </div>
            
            {smart_mode_section}
        </div>
        
        <div class="footer">
            <p>Generated by LLVM Obfuscator | NTRO Project</p>
        </div>
    </div>
</body>
</html>
        """
    
    def generate_report(self, input_file: str, output_file: str, 
                       config: Dict[str, Any], metrics: Dict[str, Any] = None) -> str:
        """Generate HTML report."""
        if metrics is None:
            metrics = self._calculate_default_metrics(input_file, output_file)
        
        # Calculate resistance score
        resistance_score = self._calculate_resistance_score(config, metrics)
        
        # Generate passes table rows
        passes_rows = self._generate_passes_table(config)
        
        # Generate smart mode section if applicable
        smart_mode_section = self._generate_smart_mode_section(config)
        
        # Fill template
        report_html = self.template.format(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            ir_size_growth=metrics.get('ir_size_growth', 0),
            function_count=metrics.get('function_count', 0),
            bogus_ratio=metrics.get('bogus_ratio', 0),
            resistance_score=resistance_score,
            passes_rows=passes_rows,
            smart_mode_section=smart_mode_section
        )
        
        return report_html
    
    def _calculate_default_metrics(self, input_file: str, output_file: str) -> Dict[str, Any]:
        """Calculate default metrics if not provided."""
        metrics = {
            'ir_size_growth': 25,  # Placeholder
            'function_count': 1,
            'bogus_ratio': 15,
            'complexity_score': 0
        }
        
        # Try to analyze files if they exist
        if os.path.exists(input_file):
            with open(input_file, 'r') as f:
                content = f.read()
                metrics['function_count'] = content.count('{') - content.count('}') + 1
        
        return metrics
    
    def _calculate_resistance_score(self, config: Dict[str, Any], metrics: Dict[str, Any]) -> int:
        """Calculate deobfuscation resistance score (0-100)."""
        score = 0
        
        # Base score from enabled passes
        passes = config.get('passes', {})
        for category, category_passes in passes.items():
            for pass_name, pass_config in category_passes.items():
                if pass_config.get('enabled', False):
                    if category == 'control_flow':
                        score += 20
                    elif category == 'data':
                        score += 15
                    elif category == 'instruction':
                        score += 10
        
        # Bonus for smart mode
        if config.get('smart_mode', {}).get('enabled', False):
            score += 10
        
        # Bonus for high complexity
        complexity = metrics.get('complexity_score', 0)
        if complexity > 100:
            score += 15
        elif complexity > 50:
            score += 10
        
        return min(score, 100)
    
    def _generate_passes_table(self, config: Dict[str, Any]) -> str:
        """Generate HTML table rows for passes."""
        rows = []
        passes = config.get('passes', {})
        
        for category, category_passes in passes.items():
            for pass_name, pass_config in category_passes.items():
                status = "enabled" if pass_config.get('enabled', False) else "disabled"
                status_class = "status-enabled" if status == "enabled" else "status-disabled"
                
                # Format parameters
                params = []
                for key, value in pass_config.items():
                    if key != 'enabled':
                        params.append(f"{key}: {value}")
                params_str = ", ".join(params) if params else "default"
                
                row = f"""
                <tr>
                    <td>{pass_name.replace('_', ' ').title()}</td>
                    <td>{category.replace('_', ' ').title()}</td>
                    <td><span class="status-badge {status_class}">{status}</span></td>
                    <td>{params_str}</td>
                </tr>
                """
                rows.append(row)
        
        return "".join(rows)
    
    def _generate_smart_mode_section(self, config: Dict[str, Any]) -> str:
        """Generate smart mode section if applicable."""
        smart_mode = config.get('smart_mode', {})
        if not smart_mode.get('enabled', False):
            return ""
        
        complexity = smart_mode.get('complexity_analysis', {})
        intensity = smart_mode.get('intensity', 'unknown')
        
        return f"""
        <div class="section">
            <h2> Smart Obfuscation Mode</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{intensity.title()}</div>
                    <div class="metric-label">Selected Intensity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{complexity.get('lines', 0)}</div>
                    <div class="metric-label">Code Lines</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{complexity.get('functions', 0)}</div>
                    <div class="metric-label">Functions</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{complexity.get('complexity_score', 0):.1f}</div>
                    <div class="metric-label">Complexity Score</div>
                </div>
            </div>
            <p><strong>Decision:</strong> {smart_mode.get('decision_summary', 'N/A')}</p>
        </div>
        """
    
    def save_report(self, report_html: str, output_path: str) -> None:
        """Save HTML report to file."""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_html)
        print(f"HTML report saved to: {output_path}")


def main():
    """Test the report generator."""
    generator = ReportGenerator()
    
    # Sample configuration
    config = {
        "passes": {
            "control_flow": {
                "bogus_control_flow": {"enabled": True, "probability": 0.5},
                "flattening": {"enabled": True, "max_flattening_depth": 2}
            },
            "data": {
                "string_encryption": {"enabled": True, "encryption_method": "aes"}
            }
        },
        "smart_mode": {
            "enabled": True,
            "intensity": "moderate",
            "complexity_analysis": {
                "lines": 45,
                "functions": 3,
                "complexity_score": 75.5
            },
            "decision_summary": "Selected moderate obfuscation based on complexity score 75.5"
        }
    }
    
    # Generate and save report
    report_html = generator.generate_report("input.c", "output.c", config)
    generator.save_report(report_html, "report.html")
    print("Report generation completed!")


if __name__ == "__main__":
    main()
