/**
 * @file flattening.cpp
 * @brief Control Flow Flattening Pass
 * 
 * This pass flattens the control flow graph by using a state machine
 * to make the program flow harder to follow.
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
 * @class FlatteningPass
 * @brief LLVM pass for control flow flattening
 */
class FlatteningPass : public FunctionPass {
public:
    static char ID; // Pass identification
    
    FlatteningPass() : FunctionPass(ID) {}
    
    /**
     * @brief Main pass execution
     * @param F Function to transform
     * @return true if function was modified
     */
    bool runOnFunction(Function &F) override {
        errs() << "FlatteningPass: Processing function " << F.getName() << "\n";
        
        if (F.size() <= 1) return false;
        
        // Create state variable
        AllocaInst *stateVar = createStateVariable(F);
        
        // Create dispatcher block
        BasicBlock *dispatcher = createDispatcherBlock(F, stateVar);
        
        // Restructure basic blocks
        restructureBasicBlocks(F, dispatcher, stateVar);
        
        return true;
    }
    
private:
    /**
     * @brief Create state variable for control flow flattening
     * @param F Function to add state variable to
     * @return Pointer to the state variable
     */
    AllocaInst* createStateVariable(Function &F) {
        IRBuilder<> builder(&F.getEntryBlock());
        AllocaInst *stateVar = builder.CreateAlloca(builder.getInt32Ty());
        builder.CreateStore(builder.getInt32(0), stateVar);
        return stateVar;
    }
    
    /**
     * @brief Create dispatcher block for control flow flattening
     * @param F Function to add dispatcher to
     * @param stateVar State variable
     * @return Pointer to the dispatcher block
     */
    BasicBlock* createDispatcherBlock(Function &F, AllocaInst *stateVar) {
        BasicBlock *dispatcher = BasicBlock::Create(F.getContext(), "dispatcher", &F);
        
        IRBuilder<> builder(dispatcher);
        LoadInst *state = builder.CreateLoad(builder.getInt32Ty(), stateVar);
        
        // Create switch instruction
        SwitchInst *switchInst = builder.CreateSwitch(state, nullptr, F.size());
        
        return dispatcher;
    }
    
    /**
     * @brief Restructure basic blocks for control flow flattening
     * @param F Function to restructure
     * @param dispatcher Dispatcher block
     * @param stateVar State variable
     */
    void restructureBasicBlocks(Function &F, BasicBlock *dispatcher, AllocaInst *stateVar) {
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
    
    /**
     * @brief Get pass name
     */
    StringRef getPassName() const override {
        return "Flattening";
    }
};

} // anonymous namespace

char FlatteningPass::ID = 0;

// Register the pass
static RegisterPass<FlatteningPass> X("flattening", 
                                    "Flatten control flow using state machine",
                                    false, false);
