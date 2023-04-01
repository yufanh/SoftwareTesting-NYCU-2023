/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
  * https://stackoverflow.com/questions/28168815/adding-a-function-call-in-my-ir-code-in-llvm
  * https://stackoverflow.com/questions/30234027/how-to-call-printf-in-llvm-through-the-module-builder-system
  * https://gite.lirmm.fr/grevy/llvm-tutorial/-/blob/master/src/exercise3bis/ReplaceFunction.cpp
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/Error.h"

#include <random>

using namespace llvm;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
  return true;
}

static void dumpIR(Function &F)
{
  for (auto &BB : F) {
    errs() << "BB: " << "\n";
    errs() << BB << "\n";
  }
}

static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}

static FunctionCallee printfPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx) },
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static FunctionCallee exitPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *exitType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt32Ty(ctx) },
    false);

  FunctionCallee exitCallee = M.getOrInsertFunction("exit", exitType);

  return exitCallee;
}

bool LabPass::runOnModule(Module &M) {

    M.dump();

  //   llvm::raw_ostream& out = llvm::outs();
  errs() << "runOnModule\n"; // 在 Module 運行之前，輸出一行訊息
  // outs() << "runOnModule\n";
  LLVMContext &ctx = M.getContext(); // 取得 Module 的 LLVM Context
  std::random_device randDev; // 宣告一個 random_device 物件，用來產生隨機數
  std::default_random_engine randEngine(randDev()); // 宣告一個 random_engine 物件，用來產生隨機數
  std::uniform_int_distribution<unsigned int> uniformDist(0, 0xffffffff); // 宣告一個 uniform_distribution 物件，用來產生 0 到 0xffffffff 之間的整數

  FunctionCallee exitCallee = exitPrototype(M); // 取得 exit 函式的 FunctionCallee
  FunctionCallee printfCallee = printfPrototype(M); // 取得 printf 函式的 FunctionCallee

  Constant *stackBofMsg = getI8StrVal(M, "!!!STACK BOF!!!\n", "stackBofMsg"); // 取得一個字串常數，用來在 stack-based buffer overflow 發生時輸出訊息

  for (auto &F : M) { // 遍歷每個函式
    if (F.empty()) { // 如果函式為空，則跳過
      continue;
    }
    dumpIR(F);
    errs() << F.getName() << "\n"; // 輸出函式名稱

    Constant *one = Constant::getIntegerValue(Type::getInt32Ty(ctx), APInt(32, 1)); // 創建一個整數常數，值為 1

    unsigned int canary = uniformDist(randEngine); // 產生一個隨機數，作為 canary 的值
    Constant *cCanary = Constant::getIntegerValue(Type::getInt32Ty(ctx), APInt(32, canary)); // 創建一個整數常數，值為 canary 的值

    BasicBlock &Bstart = F.front(); // 取得函式的第一個 Basic Block
    BasicBlock &Bend = F.back(); // 取得函式的最後一個 Basic Block

    // Split "ret" from original basic block
    Instruction &ret = *(++Bend.rend()); // 取得最後一個指令，即 "ret" 指令
    BasicBlock *Bret = Bend.splitBasicBlock(&ret, "ret"); // 把 "ret" 指令替換成一個新的 Basic Block，並將它命名為 "ret"

    // Create epilogue BB before ret BB
    BasicBlock *Bepi = BasicBlock::Create(ctx, "epi", &F, Bret); // 創建一個新的 Basic Block，並把它放在 "ret" 的前面，命名為 "epi"

    // Create BB handling stack-based buffer overflow after epilogue BB (before ret BB)
    BasicBlock *Bbof = BasicBlock::Create(ctx, "bof", &F, Bret);

    // Patch the instruction at end of of Bend BB, "br ret", to "br epi"
    Instruction &br = *(++Bend.rend());
    IRBuilder<> BuilderBr(&br);

    BuilderBr.CreateBr(Bepi);

    br.eraseFromParent();

    // Insert code at prologue
    Instruction &Istart = Bstart.front();
    IRBuilder<> BuilderStart(&Istart);

    AllocaInst *aCanary = BuilderStart.CreateAlloca(Type::getInt32Ty(ctx), 0, "canary");
    BuilderStart.CreateStore(cCanary, aCanary);

    // New basic block for handling stack-based buffer overflow
    IRBuilder<> BuilderBof(Bbof);

    BuilderBof.CreateCall(printfCallee, { stackBofMsg });
    BuilderBof.CreateCall(exitCallee, { one });
    BuilderBof.CreateBr(Bret);

    // Insert code at epilogue
    IRBuilder<> BuilderEnd(Bepi);

    Value *i0 = BuilderEnd.CreateLoad(Type::getInt32Ty(ctx), aCanary);
    Value *eq = BuilderEnd.CreateICmpEQ(i0, cCanary);
    BuilderEnd.CreateCondBr(eq, Bret, Bbof);

    // Dump IR
    dumpIR(F);
  }

  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);
