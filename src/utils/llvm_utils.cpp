/**
 * @file llvm_utils.cpp
 * @brief LLVM Utility Functions
 * 
 * Common utility functions for LLVM pass development
 * and obfuscation operations.
 */

#include "llvm/IR/Function.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/Utils/BasicBlockUtils.h"

using namespace llvm;

namespace obfuscator {

/**
 * @brief Check if a function is suitable for obfuscation
 * @param F Function to check
 * @return true if function should be obfuscated
 */
bool shouldObfuscateFunction(const Function &F) {
    // Skip functions that shouldn't be obfuscated
    if (F.isDeclaration() || F.isIntrinsic()) {
        return false;
    }
    
    // Skip functions with specific attributes
    if (F.hasFnAttribute(Attribute::NoInline) || 
        F.hasFnAttribute(Attribute::AlwaysInline)) {
        return false;
    }
    
    // TODO: Add more criteria for obfuscation suitability
    return true;
}

/**
 * @brief Get a random number generator seed
 * @return Random seed value
 */
uint64_t getRandomSeed() {
    // TODO: Implement proper random seed generation
    return 0x12345678;
}

/**
 * @brief Create a new basic block with a given name
 * @param F Function to add block to
 * @param name Name for the new block
 * @return Pointer to the new basic block
 */
BasicBlock* createBasicBlock(Function &F, const std::string &name) {
    return BasicBlock::Create(F.getContext(), name, &F);
}

/**
 * @brief Insert a no-op instruction
 * @param builder IRBuilder for instruction insertion
 * @return Pointer to the inserted instruction
 */
Instruction* insertNoOp(IRBuilder<> &builder) {
    // TODO: Implement proper no-op insertion
    // For now, return a simple add with zero
    Value *zero = builder.getInt32(0);
    return builder.CreateAdd(zero, zero);
}

/**
 * @brief Check if an instruction is safe to replace
 * @param inst Instruction to check
 * @return true if instruction can be safely replaced
 */
bool isSafeToReplace(const Instruction &inst) {
    // Skip certain types of instructions
    if (isa<PHINode>(inst) || isa<LandingPadInst>(inst)) {
        return false;
    }
    
    // TODO: Add more safety checks
    return true;
}

} // namespace obfuscator
