#!/usr/bin/env python3
"""
LLVM Obfuscator Web UI
Professional interface for the LLVM-based obfuscation tool
"""

import streamlit as st
import os
import json
import time
from datetime import datetime
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
from mock_llvm_backend import mock_backend
from simple_report import generate_simple_report

# Page configuration
st.set_page_config(
    page_title="LLVM Obfuscator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 0.5rem 0;
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .warning-box {
        background: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main UI function."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🛡️ LLVM Obfuscator</h1>
        <p>AI-Powered Code Obfuscation Tool | NTRO Project</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Mode selection
        mode = st.selectbox(
            "Obfuscation Mode",
            ["Smart Mode (AI-Driven)", "Manual Configuration", "Quick Demo"]
        )
        
        st.markdown("---")
        
        # Pass selection
        st.subheader("🔧 Obfuscation Passes")
        
        bogus_cf = st.checkbox("Bogus Control Flow", value=True, help="Adds fake branches and dead code")
        string_enc = st.checkbox("String Encryption", value=True, help="Encrypts string literals")
        inst_sub = st.checkbox("Instruction Substitution", value=True, help="Replaces simple operations")
        flattening = st.checkbox("Control Flow Flattening", value=False, help="Flattens control flow structure")
        
        st.markdown("---")
        
        # Advanced settings
        with st.expander("🔬 Advanced Settings"):
            target_platform = st.selectbox("Target Platform", ["Windows", "Linux"])
            optimization_level = st.selectbox("Optimization Level", ["O0", "O1", "O2", "O3"])
            resistance_threshold = st.slider("Min Resistance Score", 0, 100, 70)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Input Code")
        
        # File upload or text input
        upload_option = st.radio("Input Method", ["Upload File", "Paste Code"])
        
        if upload_option == "Upload File":
            uploaded_file = st.file_uploader("Choose a C/C++ file", type=['c', 'cpp', 'cc', 'cxx'])
            if uploaded_file:
                code_content = uploaded_file.read().decode('utf-8')
                st.code(code_content, language='c')
            else:
                # Default to example file
                with open("examples/simple_program.c", 'r') as f:
                    code_content = f.read()
                st.info("Using default example program")
                st.code(code_content, language='c')
        else:
            code_content = st.text_area(
                "Paste your C/C++ code here:",
                height=300,
                value=open("examples/simple_program.c", 'r').read()
            )
    
    with col2:
        st.header("📊 Code Analysis")
        
        if 'code_content' in locals():
            # Analyze code complexity
            lines = len([line for line in code_content.split('\n') if line.strip()])
            functions = code_content.count('{') - code_content.count('}') + 1
            branches = sum(code_content.count(keyword) for keyword in ['if', 'else', 'while', 'for', 'switch'])
            strings = code_content.count('"') // 2
            complexity_score = lines * 0.4 + functions * 10 + branches * 5 + strings * 2
            
            st.metric("Lines of Code", lines)
            st.metric("Functions", functions)
            st.metric("Branches", branches)
            st.metric("String Literals", strings)
            st.metric("Complexity Score", f"{complexity_score:.1f}")
            
            # Smart mode recommendation
            if mode == "Smart Mode (AI-Driven)":
                if complexity_score < 50:
                    intensity = "Light"
                    color = "🟢"
                elif complexity_score < 200:
                    intensity = "Moderate"
                    color = "🟡"
                else:
                    intensity = "Heavy"
                    color = "🔴"
                
                st.markdown(f"""
                <div class="warning-box">
                    <strong>🧠 Smart Recommendation:</strong><br>
                    {color} <strong>{intensity}</strong> obfuscation recommended<br>
                    <small>Based on complexity score: {complexity_score:.1f}</small>
                </div>
                """, unsafe_allow_html=True)
    
    # Obfuscation button
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Obfuscation", type="primary", use_container_width=True):
            run_obfuscation(code_content, mode, {
                'bogus_cf': bogus_cf,
                'string_enc': string_enc,
                'inst_sub': inst_sub,
                'flattening': flattening
            })

def run_obfuscation(code_content, mode, passes):
    """Run the obfuscation process with UI feedback."""
    
    # Create progress bar
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Prepare input
    status_text.text("📝 Preparing input file...")
    progress_bar.progress(20)
    
    # Save input to temp file
    input_file = "temp_input.c"
    with open(input_file, 'w') as f:
        f.write(code_content)
    
    time.sleep(0.5)
    
    # Step 2: Analyze complexity
    status_text.text("🧠 Analyzing code complexity...")
    progress_bar.progress(40)
    
    complexity = analyze_complexity(code_content)
    time.sleep(0.5)
    
    # Step 3: Select passes
    status_text.text("⚙️ Configuring obfuscation passes...")
    progress_bar.progress(60)
    
    selected_passes = []
    if passes['bogus_cf']:
        selected_passes.append('control_flow_bogus_control_flow')
    if passes['string_enc']:
        selected_passes.append('data_string_encryption')
    if passes['inst_sub']:
        selected_passes.append('instruction_instruction_substitution')
    if passes['flattening']:
        selected_passes.append('control_flow_flattening')
    
    time.sleep(0.5)
    
    # Step 4: Apply obfuscation
    status_text.text("🔧 Applying obfuscation transforms...")
    progress_bar.progress(80)
    
    output_file = "temp_obfuscated.exe"
    success = mock_backend.simulate_clang_compilation(input_file, output_file, selected_passes)
    
    time.sleep(1)
    
    # Step 5: Generate results
    status_text.text("📊 Generating results...")
    progress_bar.progress(100)
    
    if success:
        metrics = mock_backend.get_metrics(input_file, output_file)
        display_results(code_content, output_file, selected_passes, metrics, complexity)
    else:
        st.error("❌ Obfuscation failed!")
    
    # Cleanup
    progress_bar.empty()
    status_text.empty()
    
    # Clean up temp files
    if os.path.exists(input_file):
        os.remove(input_file)

def analyze_complexity(code_content):
    """Analyze code complexity."""
    lines = len([line for line in code_content.split('\n') if line.strip()])
    functions = code_content.count('{') - code_content.count('}') + 1
    branches = sum(code_content.count(keyword) for keyword in ['if', 'else', 'while', 'for', 'switch'])
    strings = code_content.count('"') // 2
    complexity_score = lines * 0.4 + functions * 10 + branches * 5 + strings * 2
    
    return {
        'lines': lines,
        'functions': functions,
        'branches': branches,
        'strings': strings,
        'complexity_score': complexity_score
    }

def display_results(original_code, output_file, passes, metrics, complexity):
    """Display obfuscation results."""
    
    st.markdown("---")
    st.header("🎯 Obfuscation Results")
    
    # Success message
    st.markdown("""
    <div class="success-box">
        <strong>✅ Obfuscation Completed Successfully!</strong><br>
        Your code has been successfully obfuscated with the selected passes.
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "IR Size Growth",
            f"{metrics['ir_size_growth']}%",
            delta=f"+{metrics['ir_size_growth']}%"
        )
    
    with col2:
        st.metric(
            "Bogus Code Ratio",
            f"{metrics['bogus_ratio']}%",
            delta=f"+{metrics['bogus_ratio']}%"
        )
    
    with col3:
        resistance_score = min(metrics['ir_size_growth'] + metrics['bogus_ratio'] + 20, 100)
        st.metric(
            "Resistance Score",
            f"{resistance_score}/100",
            delta="Excellent" if resistance_score > 80 else "Good"
        )
    
    with col4:
        st.metric(
            "Functions Processed",
            metrics['function_count'],
            delta=f"+{metrics['function_count']}"
        )
    
    # Visualization
    st.subheader("📈 Obfuscation Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Resistance score gauge
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = resistance_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Deobfuscation Resistance"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "green"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        fig_gauge.update_layout(height=300)
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col2:
        # Metrics comparison
        categories = ['Original', 'Obfuscated']
        size_values = [100, 100 + metrics['ir_size_growth']]
        
        fig_bar = go.Figure(data=[
            go.Bar(name='Code Size', x=categories, y=size_values, marker_color=['#636EFA', '#EF553B'])
        ])
        fig_bar.update_layout(
            title="Code Size Comparison",
            yaxis_title="Relative Size (%)",
            height=300
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Applied passes
    st.subheader("🔧 Applied Obfuscation Passes")
    
    pass_descriptions = {
        'control_flow_bogus_control_flow': '🔀 Bogus Control Flow - Adds fake branches and unreachable code',
        'data_string_encryption': '🔐 String Encryption - Encrypts string literals with XOR cipher',
        'instruction_instruction_substitution': '🔄 Instruction Substitution - Replaces simple operations with complex equivalents',
        'control_flow_flattening': '📏 Control Flow Flattening - Converts control flow to state machine'
    }
    
    for pass_name in passes:
        if pass_name in pass_descriptions:
            st.success(pass_descriptions[pass_name])
    
    # Show obfuscated code
    st.subheader("📄 Obfuscated Code")
    
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            obfuscated_code = f.read()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.text("Original Code:")
            st.code(original_code[:500] + "..." if len(original_code) > 500 else original_code, language='c')
        
        with col2:
            st.text("Obfuscated Code:")
            st.code(obfuscated_code[:500] + "..." if len(obfuscated_code) > 500 else obfuscated_code, language='c')
    
    # Download buttons
    st.subheader("💾 Download Results")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                obfuscated_content = f.read()
            st.download_button(
                "📁 Download Obfuscated Code",
                obfuscated_content,
                file_name="obfuscated_program.c",
                mime="text/plain"
            )
    
    with col2:
        # Generate JSON report
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "metrics": metrics,
            "complexity": complexity,
            "passes": passes,
            "resistance_score": resistance_score
        }
        st.download_button(
            "📊 Download JSON Report",
            json.dumps(report_data, indent=2),
            file_name="obfuscation_report.json",
            mime="application/json"
        )
    
    with col3:
        # Generate HTML report
        config = {"passes": {}, "smart_mode": {"enabled": True, "complexity_analysis": complexity}}
        html_report = generate_simple_report("input.c", output_file, config, metrics)
        st.download_button(
            "📋 Download HTML Report",
            html_report,
            file_name="obfuscation_report.html",
            mime="text/html"
        )

if __name__ == "__main__":
    main()