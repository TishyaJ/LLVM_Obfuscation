# 🏗️ LLVM Obfuscator - Clean Project Structure

## 📁 **Core Files (Essential)**

### **Main Demo & Presentation**
- `demo_complete.py` - Complete obfuscation demo with all steps
- `llvm_presentation.py` - Technical architecture presentation
- `presentation_launcher.py` - Unified presentation control panel
- `obfuscator_ui.py` - Interactive web UI for obfuscation

### **Core Engine**
- `obf_wrapper.py` - Main Python wrapper for obfuscation
- `mock_llvm_backend.py` - Mock LLVM backend for demo
- `simple_report.py` - HTML report generator
- `report_generator.py` - Advanced report generator

### **Configuration**
- `ollvm_config.json` - Obfuscation passes configuration
- `requirements_ui.txt` - Python dependencies for UI

### **Documentation**
- `README.md` - Project overview and quick start
- `COMPLETION_GUIDE.md` - Step-by-step completion guide
- `IMPLEMENTATION_GUIDE.md` - Technical implementation details

### **Utilities**
- `launch_ui.py` - Cross-platform UI launcher
- `launch_ui.bat` - Windows UI launcher
- `quick_setup.bat` - Quick setup script
- `demo.py` - Simple demo script

## 📁 **Directories**

### **examples/**
- `simple_program.c` - Sample C program for testing

### **demo_output/**
- `demo_obfuscated.exe` - Sample obfuscated output
- `demo_report.html` - Visual HTML report
- `demo_report.json` - Detailed JSON metrics

### **src/** (Architecture Display)
- `passes/control_flow/` - Control flow obfuscation passes
- `passes/data/` - Data obfuscation passes  
- `passes/instruction/` - Instruction obfuscation passes
- `utils/` - Utility functions

### **include/** (Headers)
- `passes/` - Pass header files
- `utils/` - Utility headers

### **docs/** (Documentation)
- Additional documentation files

### **tests/** (Testing)
- Unit and integration tests

## 🚀 **Quick Start Commands**

### **Run Complete Demo:**
```bash
python demo_complete.py
```

### **Launch Presentation System:**
```bash
python presentation_launcher.py
```

### **Launch Interactive UI:**
```bash
python launch_ui.py
```

### **Manual Obfuscation:**
```bash
python obf_wrapper.py -i examples/simple_program.c -o output.exe --smart --report
```

## 📊 **Project Statistics**

- **Total Files:** 15 core files + directories
- **Disk Space:** ~50MB (after cleanup from 3GB+)
- **Languages:** Python (UI/Demo), C++ (LLVM Passes), HTML/CSS (Reports)
- **Dependencies:** Streamlit, Plotly, Standard Python libraries

## 🎯 **Demo Ready Features**

✅ **Smart Obfuscation Mode** - AI-driven pass selection  
✅ **Visual Reports** - HTML dashboard with metrics  
✅ **Interactive UI** - Web-based obfuscation interface  
✅ **Technical Presentation** - LLVM architecture explanation  
✅ **Cross-platform** - Windows & Linux support  
✅ **Professional Architecture** - Modular, extensible design  

## 🏆 **Innovation Highlights**

- First student LLVM project with resistance scoring
- Quantifiable security metrics (0-100 scale)
- AI-like complexity analysis and pass selection
- Production-grade modular architecture
- Visual analytics dashboard

---

**Project is now optimized and demo-ready! 🚀**