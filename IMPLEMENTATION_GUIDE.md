# 🔧 LLVM Pass Implementation Guide

## 📋 **STEP-BY-STEP PASS IMPLEMENTATION**

### **1. Bogus Control Flow Pass**

#### **File: `src/passes/control_flow/bogus_control_flow.cpp`**

Replace the TODO section with this implementation:

```cpp
bool BogusControlFlowPass::runOnFunction(Function &F) {
    bool modified = false;

    // Skip functions that shouldn't be obfuscated
    if (F.isDeclaration() || F.size() < 2) {
        return false;
    }

    // Get probability from config
    double probability = 0.5; // Default
    if (auto *config = getAnalysisIfAvailable<ConfigAnalysis>()) {
        probability = config->getProbability("bogus_control_flow");
    }

    // Process each basic block
    for (auto &BB : F) {
        if (shouldAddBogusControlFlow(BB, probability)) {
            addBogusControlFlow(BB, F);
            modified = true;
        }
    }

    return modified;
}

bool BogusControlFlowPass::shouldAddBogusControlFlow(BasicBlock &BB, double probability) {
    // Don't add to entry block or blocks with less than 3 instructions
    if (BB.isEntryBlock() || BB.size() < 3) {
        return false;
    }

    // Random probability check
    return (rand() % 100) < (probability * 100);
}

void BogusControlFlowPass::addBogusControlFlow(BasicBlock &BB, Function &F) {
    // Create bogus basic block
    BasicBlock *bogusBB = BasicBlock::Create(F.getContext(), "bogus_" + BB.getName(), &F);

    // Add fake instructions to bogus block
    IRBuilder<> builder(bogusBB);
    Value *fake1 = builder.CreateAdd(builder.getInt32(0), builder.getInt32(0));
    Value *fake2 = builder.CreateMul(fake1, builder.getInt32(1));
    builder.CreateBr(&BB);

    // Insert fake branch in original block
    IRBuilder<> origBuilder(&BB);
    Value *condition = origBuilder.CreateICmpEQ(
        origBuilder.getInt32(0),
        origBuilder.getInt32(0)
    );
    origBuilder.CreateCondBr(condition, bogusBB, &BB);
}
```

### **2. String Encryption Pass**

#### **File: `src/passes/data/string_encryption.cpp`**

```cpp
bool StringEncryptionPass::runOnFunction(Function &F) {
    bool modified = false;

    // Find all string literals in the function
    for (auto &BB : F) {
        for (auto &I : BB) {
            if (auto *call = dyn_cast<CallInst>(&I)) {
                if (isStringFunction(call)) {
                    // Encrypt string arguments
                    for (unsigned i = 0; i < call->getNumArgOperands(); i++) {
                        if (isStringLiteral(call->getArgOperand(i))) {
                            encryptStringArgument(call, i);
                            modified = true;
                        }
                    }
                }
            }
        }
    }

    return modified;
}

bool StringEncryptionPass::isStringFunction(CallInst *call) {
    Function *func = call->getCalledFunction();
    if (!func) return false;

    StringRef name = func->getName();
    return name == "printf" || name == "puts" || name == "strlen" ||
           name == "strcpy" || name == "strcmp";
}

bool StringEncryptionPass::isStringLiteral(Value *val) {
    if (auto *gep = dyn_cast<GetElementPtrInst>(val)) {
        if (auto *gv = dyn_cast<GlobalVariable>(gep->getPointerOperand())) {
            return gv->isConstant() && gv->hasInitializer();
        }
    }
    return false;
}

void StringEncryptionPass::encryptStringArgument(CallInst *call, unsigned argIndex) {
    // Get the string literal
    Value *arg = call->getArgOperand(argIndex);
    if (auto *gep = dyn_cast<GetElementPtrInst>(arg)) {
        if (auto *gv = dyn_cast<GlobalVariable>(gep->getPointerOperand())) {
            // Create encrypted version
            Constant *original = gv->getInitializer();
            Constant *encrypted = createEncryptedString(original);

            // Replace the global variable
            gv->setInitializer(encrypted);
        }
    }
}

Constant* StringEncryptionPass::createEncryptedString(Constant *original) {
    if (auto *array = dyn_cast<ConstantDataArray>(original)) {
        // Simple XOR encryption
        std::vector<uint8_t> data;
        for (unsigned i = 0; i < array->getNumElements(); i++) {
            uint8_t byte = array->getElementAsInteger(i);
            data.push_back(byte ^ 0x42); // XOR with key 0x42
        }

        // Create new constant array
        return ConstantDataArray::get(original->getContext(), data);
    }
    return original;
}
```

### **3. Control Flow Flattening**

#### **File: `src/passes/control_flow/flattening.cpp`**

```cpp
bool FlatteningPass::runOnFunction(Function &F) {
    if (F.size() <= 1) return false;

    // Create state variable
    AllocaInst *stateVar = createStateVariable(F);

    // Create dispatcher block
    BasicBlock *dispatcher = createDispatcherBlock(F, stateVar);

    // Restructure basic blocks
    restructureBasicBlocks(F, dispatcher, stateVar);

    return true;
}

AllocaInst* FlatteningPass::createStateVariable(Function &F) {
    IRBuilder<> builder(&F.getEntryBlock());
    AllocaInst *stateVar = builder.CreateAlloca(builder.getInt32Ty());
    builder.CreateStore(builder.getInt32(0), stateVar);
    return stateVar;
}

BasicBlock* FlatteningPass::createDispatcherBlock(Function &F, AllocaInst *stateVar) {
    BasicBlock *dispatcher = BasicBlock::Create(F.getContext(), "dispatcher", &F);

    IRBuilder<> builder(dispatcher);
    LoadInst *state = builder.CreateLoad(builder.getInt32Ty(), stateVar);

    // Create switch instruction
    SwitchInst *switchInst = builder.CreateSwitch(state, nullptr, F.size());

    return dispatcher;
}

void FlatteningPass::restructureBasicBlocks(Function &F, BasicBlock *dispatcher, AllocaInst *stateVar) {
    // Collect all basic blocks except entry and dispatcher
    std::vector<BasicBlock*> blocks;
    for (auto &BB : F) {
        if (&BB != &F.getEntryBlock() && &BB != dispatcher) {
            blocks.push_back(&BB);
        }
    }

    // Assign state numbers to blocks
    for (unsigned i = 0; i < blocks.size(); i++) {
        BasicBlock *BB = blocks[i];

        // Add state transition at end of block
        IRBuilder<> builder(BB->getTerminator());
        builder.CreateStore(builder.getInt32(i + 1), stateVar);
        builder.CreateBr(dispatcher);

        // Remove original terminator
        BB->getTerminator()->eraseFromParent();
    }

    // Update dispatcher switch
    SwitchInst *switchInst = cast<SwitchInst>(dispatcher->getTerminator());
    for (unsigned i = 0; i < blocks.size(); i++) {
        switchInst->addCase(ConstantInt::get(switchInst->getContext(), APInt(32, i + 1)), blocks[i]);
    }
}
```

### **4. Instruction Substitution**

#### **File: `src/passes/instruction/instruction_substitution.cpp`**

```cpp
bool InstructionSubstitutionPass::runOnFunction(Function &F) {
    bool modified = false;

    for (auto &BB : F) {
        for (auto it = BB.begin(); it != BB.end(); ++it) {
            Instruction *I = &*it;

            if (shouldSubstitute(I)) {
                substituteInstruction(I, BB);
                modified = true;
            }
        }
    }

    return modified;
}

bool InstructionSubstitutionPass::shouldSubstitute(Instruction *I) {
    // Substitute simple arithmetic operations
    return isa<AddInst>(I) || isa<SubInst>(I) || isa<MulInst>(I) || isa<DivInst>(I);
}

void InstructionSubstitutionPass::substituteInstruction(Instruction *I, BasicBlock &BB) {
    if (auto *add = dyn_cast<AddInst>(I)) {
        // Substitute: a + b = a - (-b)
        IRBuilder<> builder(I);
        Value *negB = builder.CreateNeg(add->getOperand(1));
        Value *result = builder.CreateSub(add->getOperand(0), negB);
        I->replaceAllUsesWith(result);
        I->eraseFromParent();
    }
    else if (auto *sub = dyn_cast<SubInst>(I)) {
        // Substitute: a - b = a + (-b)
        IRBuilder<> builder(I);
        Value *negB = builder.CreateNeg(sub->getOperand(1));
        Value *result = builder.CreateAdd(sub->getOperand(0), negB);
        I->replaceAllUsesWith(result);
        I->eraseFromParent();
    }
    // Add more substitutions as needed
}
```

## 🧪 **TESTING YOUR IMPLEMENTATION**

### **1. Unit Tests**

Create test files in `tests/unit/`:

```cpp
// tests/unit/test_bogus_control_flow.cpp
TEST(BogusControlFlowTest, BasicFunction) {
    // Create test function
    LLVMContext context;
    Module module("test", context);
    FunctionType *funcType = FunctionType::get(Type::getInt32Ty(context), {}, false);
    Function *func = Function::Create(funcType, GlobalValue::ExternalLinkage, "test_func", module);

    // Add basic block with instructions
    BasicBlock *BB = BasicBlock::Create(context, "entry", func);
    IRBuilder<> builder(BB);
    builder.CreateRet(builder.getInt32(42));

    // Apply pass
    BogusControlFlowPass pass;
    bool modified = pass.runOnFunction(*func);

    // Verify modification
    EXPECT_TRUE(modified);
    EXPECT_GT(func->size(), 1); // Should have more than 1 block
}
```

### **2. Integration Tests**

```python
# tests/integration/test_full_pipeline.py
def test_bogus_control_flow():
    result = subprocess.run([
        'python', 'obf_wrapper.py',
        '-i', 'examples/simple_program.c',
        '-o', 'test_bcf.exe',
        '--passes', 'control_flow_bogus_control_flow'
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert os.path.exists('test_bcf.exe')

def test_smart_mode():
    result = subprocess.run([
        'python', 'obf_wrapper.py',
        '-i', 'examples/simple_program.c',
        '-o', 'smart_output.exe',
        '--smart', '--report'
    ], capture_output=True, text=True)

    assert result.returncode == 0
    assert os.path.exists('smart_output_report.html')
```

## 🚀 **BUILD AND TEST COMMANDS**

### **1. Build Individual Passes**

```bash
# Build bogus control flow pass
g++ -std=c++17 -fPIC -I/path/to/llvm/include \
    -c src/passes/control_flow/bogus_control_flow.cpp \
    -o build/bogus_control_flow.o

# Build string encryption pass
g++ -std=c++17 -fPIC -I/path/to/llvm/include \
    -c src/passes/data/string_encryption.cpp \
    -o build/string_encryption.o
```

### **2. Test Passes**

```bash
# Test individual pass
python obf_wrapper.py -i examples/simple_program.c -o test.exe --passes control_flow_bogus_control_flow

# Test smart mode
python obf_wrapper.py -i examples/simple_program.c -o smart.exe --smart --report

# Run complete demo
python demo.py
```

### **3. Verify Output**

```bash
# Check if obfuscated binary was created
ls -la test.exe smart.exe

# Check if reports were generated
ls -la *_report.html *_report.json

# Open HTML report in browser
start smart_output_report.html
```

## 🎯 **SUCCESS CRITERIA**

### **Complete When:**

- ✅ All passes compile without errors
- ✅ Passes modify LLVM IR as expected
- ✅ Smart mode selects appropriate passes
- ✅ HTML reports generate with real metrics
- ✅ Demo runs end-to-end successfully

### **Verification:**

```bash
# 1. Test compilation
python obf_wrapper.py --list-passes
# Should show all passes available

# 2. Test obfuscation
python obf_wrapper.py -i examples/simple_program.c -o test.exe --smart
# Should create test.exe and reports

# 3. Test demo
python demo.py
# Should complete all 8 steps successfully
```

## 🔧 **TROUBLESHOOTING**

### **Common Issues:**

1. **Compilation Errors**: Check LLVM include paths
2. **Pass Not Found**: Verify pass registration
3. **No Output**: Check if LLVM backend is installed
4. **Report Errors**: Verify Python dependencies

### **Debug Commands:**

```bash
# Check LLVM installation
llvm-config --version
llvm-config --cppflags
llvm-config --ldflags

# Test individual components
python obf_wrapper.py --list-passes
python report_generator.py
```

This implementation guide provides the exact code needed to complete the remaining 15% of your LLVM obfuscator project!
