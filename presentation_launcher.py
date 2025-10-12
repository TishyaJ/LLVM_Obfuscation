#!/usr/bin/env python3
"""
NTRO Project Presentation Launcher
Comprehensive presentation combining LLVM theory and practical demo
"""

import streamlit as st
import subprocess
import sys
import os

# Page configuration
st.set_page_config(
    page_title="NTRO Project: LLVM Obfuscator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .presentation-card {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        margin: 1rem 0;
        text-align: center;
    }
    .demo-button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 8px;
        border: none;
        font-size: 1.2em;
        cursor: pointer;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main presentation launcher."""
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎓 NTRO Project Presentation</h1>
        <h2>Application Software to Obfuscate Object Files Using LLVM</h2>
        <p>Comprehensive Technical Demonstration</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Presentation options
    st.header("📋 Presentation Components")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="presentation-card">
            <h3>🏗️ Technical Architecture</h3>
            <p>Deep dive into LLVM concepts, IR system, and pass architecture</p>
            <ul style="text-align: left;">
                <li>LLVM compilation pipeline</li>
                <li>Intermediate representation (IR)</li>
                <li>Pass system architecture</li>
                <li>Obfuscation algorithms</li>
                <li>Smart mode implementation</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🚀 Launch Technical Presentation", type="primary", use_container_width=True):
            launch_technical_presentation()
    
    with col2:
        st.markdown("""
        <div class="presentation-card">
            <h3>🎯 Live Demo Interface</h3>
            <p>Interactive demonstration of the obfuscation tool</p>
            <ul style="text-align: left;">
                <li>Code input and analysis</li>
                <li>Smart obfuscation mode</li>
                <li>Real-time metrics</li>
                <li>Visual reports</li>
                <li>Download results</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🎮 Launch Interactive Demo", type="primary", use_container_width=True):
            launch_demo_interface()
    
    # Presentation flow guide
    st.markdown("---")
    st.header("📖 Recommended Presentation Flow")
    
    flow_steps = [
        {
            "step": "1. Introduction",
            "content": "Project overview and problem statement",
            "duration": "2 minutes"
        },
        {
            "step": "2. LLVM Foundation", 
            "content": "Technical architecture and LLVM concepts",
            "duration": "5 minutes"
        },
        {
            "step": "3. Implementation Details",
            "content": "Pass algorithms and smart mode",
            "duration": "4 minutes"
        },
        {
            "step": "4. Live Demonstration",
            "content": "Interactive obfuscation demo",
            "duration": "3 minutes"
        },
        {
            "step": "5. Results & Innovation",
            "content": "Metrics, achievements, and future work",
            "duration": "1 minute"
        }
    ]
    
    for i, step in enumerate(flow_steps):
        col1, col2, col3 = st.columns([1, 3, 1])
        
        with col1:
            st.markdown(f"**{step['step']}**")
        
        with col2:
            st.markdown(f"{step['content']}")
        
        with col3:
            st.markdown(f"*{step['duration']}*")
    
    # Quick access tools
    st.markdown("---")
    st.header("🛠️ Quick Access Tools")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📊 Generate Sample Report", use_container_width=True):
            generate_sample_report()
    
    with col2:
        if st.button("🔍 Show Code Examples", use_container_width=True):
            show_code_examples()
    
    with col3:
        if st.button("📈 Display Metrics", use_container_width=True):
            display_sample_metrics()
    
    with col4:
        if st.button("💾 Download Resources", use_container_width=True):
            show_download_resources()
    
    # Project summary
    st.markdown("---")
    st.header("📋 Project Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Key Features
        - **AI-Driven Obfuscation**: Smart mode with complexity analysis
        - **LLVM Integration**: Production-grade compiler infrastructure
        - **Visual Analytics**: Real-time metrics and reporting
        - **Cross-Platform**: Windows and Linux support
        - **Modular Design**: Extensible pass architecture
        """)
    
    with col2:
        st.markdown("""
        ### 🏆 Innovation Points
        - First student project with resistance scoring
        - Quantifiable security metrics
        - Automated pass selection algorithm
        - Professional-grade architecture
        - Research-ready framework
        """)

def launch_technical_presentation():
    """Launch the technical presentation."""
    st.success("🚀 Launching Technical Architecture Presentation...")
    st.info("Opening in new browser tab: http://localhost:8502")
    
    try:
        # Launch technical presentation on different port
        subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'llvm_presentation.py',
            '--server.port', '8502',
            '--server.headless', 'false'
        ])
        st.success("✅ Technical presentation launched successfully!")
    except Exception as e:
        st.error(f"❌ Error launching presentation: {e}")

def launch_demo_interface():
    """Launch the demo interface."""
    st.success("🎮 Launching Interactive Demo Interface...")
    st.info("Opening in new browser tab: http://localhost:8503")
    
    try:
        # Launch demo interface on different port
        subprocess.Popen([
            sys.executable, '-m', 'streamlit', 'run', 'obfuscator_ui.py',
            '--server.port', '8503',
            '--server.headless', 'false'
        ])
        st.success("✅ Demo interface launched successfully!")
    except Exception as e:
        st.error(f"❌ Error launching demo: {e}")

def generate_sample_report():
    """Generate and display sample report."""
    st.success("📊 Generating Sample Obfuscation Report...")
    
    # Run the demo to generate report
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, 'demo_complete.py'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            st.success("✅ Sample report generated!")
            
            # Show report content
            if os.path.exists("demo_output/demo_report.html"):
                st.markdown("**HTML Report Generated:**")
                st.code("demo_output/demo_report.html")
            
            if os.path.exists("demo_output/demo_report.json"):
                st.markdown("**JSON Report Generated:**")
                with open("demo_output/demo_report.json", 'r') as f:
                    st.json(f.read())
        else:
            st.error("❌ Failed to generate report")
    except Exception as e:
        st.error(f"❌ Error: {e}")

def show_code_examples():
    """Show code examples."""
    st.success("🔍 Displaying Code Examples...")
    
    tab1, tab2, tab3 = st.tabs(["Original Code", "Obfuscated Code", "LLVM Pass"])
    
    with tab1:
        st.markdown("**Original C Code:**")
        st.code("""
#include <stdio.h>

int compute(int x) {
    int result = 0;
    for (int i = 0; i < x; i++) {
        result += i * 2;
    }
    return result;
}

int main() {
    printf("Result: %d\\n", compute(10));
    return 0;
}
        """, language='c')
    
    with tab2:
        st.markdown("**After Obfuscation:**")
        if os.path.exists("demo_output/demo_obfuscated.exe"):
            with open("demo_output/demo_obfuscated.exe", 'r') as f:
                st.code(f.read(), language='c')
        else:
            st.code("""
// Obfuscated version with encrypted strings and bogus control flow
#include <stdio.h>

int compute(int x) {
    int result = 0;
    for (int i = 0; i < x; i++) {
        // BOGUS: if (0 == 0) goto fake_block;
        result += i * 2;
    }
    return result;
}

int main() {
    printf("[ENCRYPTED]Result: %d\\n"[ENCRYPTED], compute(10));
    return 0;
}
            """, language='c')
    
    with tab3:
        st.markdown("**LLVM Pass Implementation:**")
        st.code("""
bool BogusControlFlowPass::runOnFunction(Function &F) {
    bool modified = false;
    
    for (auto &BB : F) {
        if (shouldAddBogusControlFlow(BB)) {
            // Create bogus basic block
            BasicBlock *bogusBB = createBogusBlock(F, BB);
            
            // Insert fake branch
            insertFakeBranch(BB, bogusBB);
            
            modified = true;
        }
    }
    
    return modified;
}
        """, language='cpp')

def display_sample_metrics():
    """Display sample metrics."""
    st.success("📈 Displaying Sample Obfuscation Metrics...")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("IR Size Growth", "77%", delta="+77%")
    with col2:
        st.metric("Bogus Code Ratio", "45%", delta="+45%")
    with col3:
        st.metric("Resistance Score", "100/100", delta="Excellent")
    with col4:
        st.metric("Processing Time", "2.3s", delta="-0.7s")
    
    # Show metrics chart
    import plotly.graph_objects as go
    
    categories = ['Code Size', 'Complexity', 'Analysis Time', 'Reverse Difficulty']
    original = [100, 100, 100, 100]
    obfuscated = [177, 245, 320, 400]
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Original', x=categories, y=original, marker_color='lightblue'))
    fig.add_trace(go.Bar(name='Obfuscated', x=categories, y=obfuscated, marker_color='lightcoral'))
    
    fig.update_layout(
        title='Obfuscation Impact Comparison',
        yaxis_title='Relative Scale (%)',
        barmode='group',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

def show_download_resources():
    """Show downloadable resources."""
    st.success("💾 Available Download Resources...")
    
    resources = [
        {"name": "Project Source Code", "file": "llvm-obfuscator.zip", "desc": "Complete source code with documentation"},
        {"name": "Technical Report", "file": "technical_report.pdf", "desc": "Detailed technical documentation"},
        {"name": "Sample Obfuscated Code", "file": "demo_output/demo_obfuscated.exe", "desc": "Example obfuscated program"},
        {"name": "Metrics Report (JSON)", "file": "demo_output/demo_report.json", "desc": "Detailed obfuscation metrics"},
        {"name": "Visual Report (HTML)", "file": "demo_output/demo_report.html", "desc": "Interactive visual dashboard"}
    ]
    
    for resource in resources:
        col1, col2, col3 = st.columns([2, 3, 1])
        
        with col1:
            st.markdown(f"**{resource['name']}**")
        
        with col2:
            st.markdown(resource['desc'])
        
        with col3:
            if os.path.exists(resource['file']):
                with open(resource['file'], 'rb') as f:
                    st.download_button(
                        "📥 Download",
                        f.read(),
                        file_name=os.path.basename(resource['file']),
                        key=resource['name']
                    )
            else:
                st.markdown("*Not available*")

if __name__ == "__main__":
    main()