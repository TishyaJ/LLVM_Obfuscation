/**
 * @file llvm_utils.h
 * @brief LLVM Utility Functions Header
 * 
 * Common utility functions for LLVM pass development
 * and obfuscation operations.
 */

#ifndef LLVM_UTILS_H
#define LLVM_UTILS_H

#include "llvm/IR/Function.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/IRBuilder.h"

namespace obfuscator {

/**
 * @brief Check if a function is suitable for obfuscation
 * @param F Function to check
 * @return true if function should be obfuscated
 */
bool shouldObfuscateFunction(const llvm::Function &F);

/**
 * @brief Get a random number generator seed
 * @return Random seed value
 */
uint64_t getRandomSeed();

/**
 * @brief Create a new basic block with a given name
 * @param F Function to add block to
 * @param name Name for the new block
 * @return Pointer to the new basic block
 */
llvm::BasicBlock* createBasicBlock(llvm::Function &F, const std::string &name);

/**
 * @brief Insert a no-op instruction
 * @param builder IRBuilder for instruction insertion
 * @return Pointer to the inserted instruction
 */
llvm::Instruction* insertNoOp(llvm::IRBuilder<> &builder);

/**
 * @brief Check if an instruction is safe to replace
 * @param inst Instruction to check
 * @return true if instruction can be safely replaced
 */
bool isSafeToReplace(const llvm::Instruction &inst);

} // namespace obfuscator

#endif // LLVM_UTILS_H
