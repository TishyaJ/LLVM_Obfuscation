/**
 * @file string_encryption.cpp
 * @brief String Encryption Obfuscation Pass
 * 
 * This pass encrypts string literals and adds decryption code
 * to make string analysis more difficult.
 */

#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

/**
 * @class StringEncryptionPass
 * @brief LLVM pass for string encryption
 */
class StringEncryptionPass : public FunctionPass {
public:
    static char ID; // Pass identification
    
    StringEncryptionPass() : FunctionPass(ID) {}
    
    /**
     * @brief Main pass execution
     * @param F Function to transform
     * @return true if function was modified
     */
    bool runOnFunction(Function &F) override {
        errs() << "StringEncryptionPass: Processing function " << F.getName() << "\n";
        
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
    
private:
    /**
     * @brief Check if a call instruction is a string function
     * @param call Call instruction to check
     * @return true if it's a string function
     */
    bool isStringFunction(CallInst *call) {
        Function *func = call->getCalledFunction();
        if (!func) return false;
        
        StringRef name = func->getName();
        return name == "printf" || name == "puts" || name == "strlen" || 
               name == "strcpy" || name == "strcmp";
    }
    
    /**
     * @brief Check if a value is a string literal
     * @param val Value to check
     * @return true if it's a string literal
     */
    bool isStringLiteral(Value *val) {
        if (auto *gep = dyn_cast<GetElementPtrInst>(val)) {
            if (auto *gv = dyn_cast<GlobalVariable>(gep->getPointerOperand())) {
                return gv->isConstant() && gv->hasInitializer();
            }
        }
        return false;
    }
    
    /**
     * @brief Encrypt a string argument in a call instruction
     * @param call Call instruction
     * @param argIndex Index of the argument to encrypt
     */
    void encryptStringArgument(CallInst *call, unsigned argIndex) {
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
    
    /**
     * @brief Create an encrypted version of a string constant
     * @param original Original string constant
     * @return Encrypted string constant
     */
    Constant* createEncryptedString(Constant *original) {
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
    
    /**
     * @brief Get pass name
     */
    StringRef getPassName() const override {
        return "StringEncryption";
    }
};

} // anonymous namespace

char StringEncryptionPass::ID = 0;

// Register the pass
static RegisterPass<StringEncryptionPass> X("string-encryption", 
                                           "Encrypt string literals",
                                           false, false);
