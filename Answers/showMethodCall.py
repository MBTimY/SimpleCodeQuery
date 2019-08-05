#coding=utf-8

import sys
sys.path.append("..")
from TYPES import TYPES
import Utils 
import json

Name : str = "showMethodCall"

Version : str = "1.0"

Describe : str = "得到某个提供的函数名字的所有调用表达式。Params: (methodCallName: str)"

def Report(conn: "Connection", methodCallName:str) -> str:
    output = []
    for methodInfo in Utils.getMethodsInfoByName(conn, methodCallName):
        methodExpr = json.loads(Utils.getCompleteExpr(conn, int(methodInfo["methodCallId"]), TYPES.METHODCALLEXPR))
        output.append({"output": methodExpr["output"], "fileName": methodExpr["fileName"], "lineNo": methodExpr["lineNo"]})
    
    return json.dumps(output)