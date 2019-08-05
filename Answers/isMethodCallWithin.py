#coding=utf-8

import sys
sys.path.append("..")
from TYPES import TYPES
import Utils 
import json

Name : str = "isWithin"

Version : str = "1.0"

Describe : str = "用于检测某个函数调用否直接或者间接存在与另外一个表达式之中, 返回满足存在于给定表达式之中的函数调用。Params: (methodCallName: str, ParentType: str)"

def Report(conn: "Connection", methodCallName:str, parentType:str) -> str:
    parentType = parentType.upper()
    cursor = conn.cursor()
    c = cursor.execute('''
select group_concat(expr_id), e.precedent_id, M.args_num, M.line_no from EXPRS E, (
select E.id, M.args_num, E.line_no from EXPRS  E JOIN METHOD_CALL_EXPR  M on E.EXPR_ID = M.id where E.EXPR_TYPE="METHOD_CALL" 
)  M where e.precedent_id  = M.id and e.precedent_type = 8 GROUP BY PRECEDENT_ID
''')
    all_item = c.fetchall()
    founded_methodcallexpr = []
    package_list = []
    for item in all_item:
        sub_exprs = [expr_id for expr_id in item[0].split(",")]
        name_id = sub_exprs[item[2]]
        c = cursor.execute("SELECT count(id) from SIMPLE_NAME_EXPR where id = ? and name = ?", (name_id, methodCallName))
        if (c.fetchone()[0] == 1):
            packageinfo = Utils.getPackageInfo(conn, item[1], TYPES.METHODCALLEXPR)
            founded_methodcallexpr.append({
                "methodCallId": item[1],
                "name": methodCallName,
                "argsNum": item[2],
                "fileName": packageinfo["fileName"],
                "lineNo": item[3]
            })
    
    result = []
    for method_expr in founded_methodcallexpr:
        if (Utils.isMethodCallWithinParent(conn, method_expr["methodCallId"], TYPES.ofName(parentType))):
            result.append(method_expr)

    output = "The {0} Method Call is occurs {1} times, details is fllowing:\n".format(methodCallName, len(result))
    for r in result:
        output = output + json.dumps(r) + "\n"
    return json.dumps({"occurs": len(result), "method_call_list":result, "output":output})