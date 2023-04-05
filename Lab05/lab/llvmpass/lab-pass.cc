/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Support/Error.h"
#include "llvm/TableGen/DirectiveEmitter.h"

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



bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";
  
  LLVMContext &ctx = M.getContext();
  FunctionCallee printfCallee = printfPrototype(M);
  
  GlobalVariable *depthVar = M.getGlobalVariable("depthVar");
  depthVar = new GlobalVariable(M, Type::getInt32Ty(ctx), false, GlobalValue::LinkageTypes::CommonLinkage, nullptr, "depthVar");
  depthVar->setInitializer(ConstantInt::get(Type::getInt32Ty(ctx), 0));
  
  for (auto &F : M) {
    if (F.empty()) {
      continue;
    }  
    
    Constant *space = getI8StrVal(M, " ", "space");
    Constant *one = Constant::getIntegerValue(Type::getInt32Ty(ctx), APInt(32, 1));
    
    BasicBlock &Bstart = F.front();
    BasicBlock &Bend = F.back();
    Instruction &ret = *(++Bend.rend());
    BasicBlock *Bret = Bend.splitBasicBlock(&ret, "ret");

    BasicBlock *Bdepth = BasicBlock::Create(ctx, "depth", &F, &Bstart);
    BasicBlock *Bspace = BasicBlock::Create(ctx, "space", &F, &Bstart);
    BasicBlock *Bshow = BasicBlock::Create(ctx, "show", &F, &Bstart);
    
    GlobalVariable *depth = M.getNamedGlobal("depthVar");

    
    IRBuilder<> BuilderDepth(Bdepth);
    if(F.getName() != "main"){
      Value *depth_load = BuilderDepth.CreateLoad(depth->getValueType(), depth);
      Value *depth_load_add = BuilderDepth.CreateAdd(depth_load, one);
      BuilderDepth.CreateStore(depth_load_add, depth);
    }
    

    Value *cnt = BuilderDepth.CreateAlloca(Type::getInt32Ty(ctx));
    BuilderDepth.CreateStore(ConstantInt::get(Type::getInt32Ty(ctx), 0), cnt);

    Value *noSpace = BuilderDepth.CreateICmpEQ(BuilderDepth.CreateLoad(Type::getInt32Ty(ctx), depth), Constant::getIntegerValue(Type::getInt32Ty(ctx), APInt(32, 0)));
    BuilderDepth.CreateCondBr(noSpace, Bshow, Bspace);


    
    IRBuilder<> BuilderSpace(Bspace);
    BuilderSpace.CreateCall(printfCallee, {space});
    Value *cntPlus = BuilderSpace.CreateAdd(BuilderSpace.CreateLoad(Type::getInt32Ty(ctx), cnt), one);
    BuilderSpace.CreateStore(cntPlus, cnt);
    Value *eq = BuilderSpace.CreateICmpEQ(BuilderSpace.CreateLoad(depth->getValueType(), depth), BuilderSpace.CreateLoad(Type::getInt32Ty(ctx), cnt));
    BuilderSpace.CreateCondBr(eq, Bshow, Bspace);


    IRBuilder<> BuilderShow(Bshow);
    Value *funcName = BuilderShow.CreateGlobalStringPtr(F.getName().str());
    Value *funcPtr = BuilderShow.CreatePointerCast(&F, Type::getInt8PtrTy(ctx));
    Constant *formatString = ConstantDataArray::getString(ctx, "%s: %p\n");
    GlobalVariable *formatStringVar = new GlobalVariable(M, formatString->getType(), true, GlobalValue::InternalLinkage, formatString, "formatString");
    
    std::vector<Value *> printfArgs = {formatStringVar, funcName, funcPtr};
    BuilderShow.CreateCall(printfCallee, printfArgs);
    BuilderShow.CreateBr(&Bstart);

    BasicBlock &Bfinal = F.back(); 
    Instruction &final_ret = *(++Bfinal.rend());
    IRBuilder<> BuilderSub(&final_ret);
    Value *depth_laod_2 = BuilderSub.CreateLoad(depth->getValueType(), depth);
    Value *depth_laod_sub = BuilderSub.CreateSub(depth_laod_2, one);
    BuilderSub.CreateStore(depth_laod_sub, depth);
    
    // dumpIR(F);
    
  }

  return true;
}
static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);
