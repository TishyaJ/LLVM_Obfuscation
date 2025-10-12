/**
 * @file opaque_predicates.cpp
 * @brief Opaque Predicates Obfuscation Pass
 * 
 * This pass adds opaque predicates (always true/false conditions)
 * to make control flow analysis more difficult.
 */

#include "llvm/Pass.h"
#include "llvm/IR/Function.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Support/raw_ostream.h"

using namespace llvm;

namespace {

/**
 * @class OpaquePredicatesPass
 * @brief LLVM pass for opaque predicates
 */
class OpaquePredicatesPass : public FunctionPass {
public:
    static char ID; // Pass identification
    
    OpaquePredicatesPass() : FunctionPass(ID) {}
    
    /**
     * @brief Main pass execution
     * @param F Function to transform
     * @return true if function was modified
     */
    bool runOnFunction(Function &F) override {
        errs() << "OpaquePredicatesPass: Processing function " << F.getName() << "\n";
        
        bool modified = false;
        
        // Process each basic block
        for (auto &BB : F) {
            if (shouldAddOpaquePredicate(BB)) {
                addOpaquePredicate(BB, F);
                modified = true;
            }
        }
        
        return modified;
    }
    
private:
    /**
     * @brief Check if opaque predicate should be added to a basic block
     * @param BB Basic block to check
     * @return true if opaque predicate should be added
     */
    bool shouldAddOpaquePredicate(BasicBlock &BB) {
        // Don't add to entry block or blocks with less than 2 instructions
        if (BB.isEntryBlock() || BB.size() < 2) {
            return false;
        }
        
        // Random probability check (30% chance)
        return (rand() % 100) < 30;
    }
    
    /**
     * @brief Add opaque predicate to a basic block
     * @param BB Basic block to modify
     * @param F Function containing the block
     */
    void addOpaquePredicate(BasicBlock &BB, Function &F) {
        // Create fake basic block
        BasicBlock *fakeBB = BasicBlock::Create(F.getContext(), "fake_" + BB.getName(), &F);
        
        // Add fake instructions to fake block
        IRBuilder<> builder(fakeBB);
        Value *fake1 = builder.CreateAdd(builder.getInt32(0), builder.getInt32(0));
        Value *fake2 = builder.CreateMul(fake1, builder.getInt32(1));
        builder.CreateBr(&BB);
        
        // Create opaque predicate (always true)
        IRBuilder<> origBuilder(&BB);
        Value *x = origBuilder.getInt32(42);
        Value *y = origBuilder.getInt32(42);
        Value *condition = origBuilder.CreateICmpEQ(x, y); // Always true
        
        // Insert conditional branch
        origBuilder.CreateCondBr(condition, &BB, fakeBB);
    }
    
    /**
     * @brief Get pass name
     */
    StringRef getPassName() const override {
        return "OpaquePredicates";
    }
};

} // anonymous namespace

char OpaquePredicatesPass::ID = 0;

// Register the pass
static RegisterPass<OpaquePredicatesPass> X("opaque-predicates", 
                                           "Add opaque predicates to control flow",
                                           false, false);
