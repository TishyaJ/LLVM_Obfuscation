/**
 * @file bogus_control_flow.cpp
 * @brief Bogus Control Flow Obfuscation Pass
 * 
 * This pass adds fake control flow to make reverse engineering more difficult.
 * It inserts bogus basic blocks and branches that never execute.
 */

#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"

using namespace llvm;

namespace {

/**
 * @class BogusControlFlowPass
 * @brief LLVM pass for adding bogus control flow
 */
class BogusControlFlowPass : public FunctionPass {
public:
    static char ID; // Pass identification
    
    BogusControlFlowPass() : FunctionPass(ID) {}
    
    /**
     * @brief Main pass execution
     * @param F Function to transform
     * @return true if function was modified
     */
    bool runOnFunction(Function &F) override {
        errs() << "BogusControlFlowPass: Processing function " << F.getName() << "\n";
        
        // Skip functions that shouldn't be obfuscated
        if (F.isDeclaration() || F.size() < 2) {
            return false;
        }
        
        bool modified = false;
        
        // Process each basic block
        for (auto &BB : F) {
            if (shouldAddBogusControlFlow(BB)) {
                addBogusControlFlow(BB, F);
                modified = true;
            }
        }
        
        return modified;
    }
    
private:
    /**
     * @brief Check if bogus control flow should be added to a basic block
     * @param BB Basic block to check
     * @return true if bogus control flow should be added
     */
    bool shouldAddBogusControlFlow(BasicBlock &BB) {
        // Don't add to entry block or blocks with less than 3 instructions
        if (BB.isEntryBlock() || BB.size() < 3) {
            return false;
        }
        
        // Random probability check (50% chance)
        return (rand() % 100) < 50;
    }
    
    /**
     * @brief Add bogus control flow to a basic block
     * @param BB Basic block to modify
     * @param F Function containing the block
     */
    void addBogusControlFlow(BasicBlock &BB, Function &F) {
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
    
    /**
     * @brief Get pass name
     */
    StringRef getPassName() const override {
        return "BogusControlFlow";
    }
};

} // anonymous namespace

char BogusControlFlowPass::ID = 0;

// Register the pass
static RegisterPass<BogusControlFlowPass> X("bogus-control-flow", 
                                          "Add bogus control flow to functions",
                                          false, false);
