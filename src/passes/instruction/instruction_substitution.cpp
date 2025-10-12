/**
 * @file instruction_substitution.cpp
 * @brief Instruction Substitution Obfuscation Pass
 * 
 * This pass substitutes simple instructions with more complex
 * equivalent sequences to make analysis more difficult.
 */

#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

/**
 * @class InstructionSubstitutionPass
 * @brief LLVM pass for instruction substitution
 */
class InstructionSubstitutionPass : public FunctionPass {
public:
    static char ID; // Pass identification
    
    InstructionSubstitutionPass() : FunctionPass(ID) {}
    
    /**
     * @brief Main pass execution
     * @param F Function to transform
     * @return true if function was modified
     */
    bool runOnFunction(Function &F) override {
        errs() << "InstructionSubstitutionPass: Processing function " << F.getName() << "\n";
        
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
    
private:
    /**
     * @brief Check if an instruction should be substituted
     * @param I Instruction to check
     * @return true if instruction should be substituted
     */
    bool shouldSubstitute(Instruction *I) {
        // Substitute simple arithmetic operations
        return isa<AddInst>(I) || isa<SubInst>(I) || isa<MulInst>(I) || isa<DivInst>(I);
    }
    
    /**
     * @brief Substitute an instruction with equivalent sequence
     * @param I Instruction to substitute
     * @param BB Basic block containing the instruction
     */
    void substituteInstruction(Instruction *I, BasicBlock &BB) {
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
        else if (auto *mul = dyn_cast<MulInst>(I)) {
            // Substitute: a * b = (a << 1) + a (for b = 3)
            // This is a simplified example
            IRBuilder<> builder(I);
            Value *shifted = builder.CreateShl(mul->getOperand(0), builder.getInt32(1));
            Value *result = builder.CreateAdd(shifted, mul->getOperand(0));
            I->replaceAllUsesWith(result);
            I->eraseFromParent();
        }
    }
    
    /**
     * @brief Get pass name
     */
    StringRef getPassName() const override {
        return "InstructionSubstitution";
    }
};

} // anonymous namespace

char InstructionSubstitutionPass::ID = 0;

// Register the pass
static RegisterPass<InstructionSubstitutionPass> X("instruction-substitution", 
                                                  "Substitute instructions with complex sequences",
                                                  false, false);
