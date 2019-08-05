#coding:utf-8
from TYPES import TYPES
import sqlite3
from typing import Tuple
import json

def getCompleteExpr(conn: "Connection", index: int, expr_type: TYPES) -> str: 
    handles = {
        TYPES.METHODCALLEXPR:MethodCallExpr,
        TYPES.FIELDACCESS:FieldAccessExpr,
        TYPES.THIS:lambda x,y :json.dumps({"output":"This"}),
        TYPES.SIMPLENAME:SimpleNameExpr,
        TYPES.CAST:CastExpr,
        TYPES.REFERENCETYPE:ReferenceTypeExpr, 
        TYPES.WILDCARDTYPE:lambda x,y: json.dumps({"output":"?"}),
        TYPES.LITERAL:LiteralExpr,
        TYPES.OBJECTCREATION:ObjectCreationExpr
    }
    return handles[expr_type](conn, index)

def ObjectCreationExpr(conn: "Connection", index: int) -> str:
    methodInfo = json.loads(MethodCallExpr(conn, index))
    output = "new "  + methodInfo["output"]
    methodInfo["output"] = output
    return json.dumps(
        methodInfo
    )

def LiteralExpr(conn: "Connection", index: int) -> str:
    cursor = conn.cursor()
    c = cursor.execute("select expr_id from exprs where id = ?", (index,))
    literal_expr_id = c.fetchone()
    c = cursor.execute("select value, type from literal_expr where id = ?", (literal_expr_id[0],))
    pair_literal = c.fetchone()

    output = ""
    if (pair_literal[1] == "BOOL"):
        output = "TRUE" if pair_literal[0] == "1" else "FALSE"
    else:
       output = pair_literal[0]
    
    return json.dumps({
        "value" : pair_literal[0],
        "type" : pair_literal[1],
        "output" : output
    })



def ReferenceTypeExpr(conn: "Connection", index: int) -> str:
    cursor = conn.cursor()
    c = cursor.execute("select id, expr_type from exprs where precedent_id = ? and precedent_type = ? limit 1", (index, TYPES.REFERENCETYPE.value[1]))
    item = c.fetchone()
    ref_name = json.loads(getCompleteExpr(conn, item[0], TYPES.ofName(toStandardName(item[1]))))
    return json.dumps(
        {
            "name": ref_name["output"],
            "output": ref_name["output"]
        }
    )


def CastExpr(conn: "Connection", index: int) -> str:
    cursor = conn.cursor()
    c = cursor.execute("select id, expr_type from exprs where precedent_id = ? and precedent_type = ? ", (index, TYPES.CAST.value[1]))
    child_items = c.fetchall()
    childs = []

    if len(child_items) > 2:
        raise ValueError

    for child_item in child_items:
        childs.append(json.loads(getCompleteExpr(conn, child_item[0], TYPES.ofName(toStandardName(child_item[1])))))

    
    reference = childs.pop()
    token = childs.pop()

    output = ""
    output += "(" + reference["output"] + ")" + token["output"]
    return json.dumps({
        "token": token,
        "reference": reference,
        "output": output
    })


def getParent(cursor: "Connection", index: int, _type : TYPES) -> Tuple[int, TYPES]:
    c = cursor.execute("select precedent_id, precedent_type from "+ _type.value[0] +" where id = ?", (index,))
    precedent = c.fetchone()
    if precedent == None:
        return None, None
    precedent_type = TYPES.ofValue(precedent[1])
    return precedent[0], precedent_type

def getPackageInfo (conn: "Connection", index: int, expr_type: TYPES) -> Tuple[str,str]:
    #select precedent_id, precedent_type from exprs where id = index
    cursor = conn.cursor()

    precedent_id , precedent_type = getParent(cursor, index, expr_type)
    while True:
        if (precedent_type == TYPES.CU):
            c = cursor.execute("select name, package from "+ precedent_type.value[0] +" where id = ?", (precedent_id,)) 
            item = c.fetchone()
            return {"packageName": item[1], "fileName":item[0]}

        if precedent_id:
            precedent_id , precedent_type = getParent(cursor, precedent_id, precedent_type)
        else:
            break
    return None

def isMethodCallWithinParent(conn: "Connection", index: int, parent_expr_type: TYPES) -> bool:
    return isWithinParent(conn, index, TYPES.METHODCALLEXPR, parent_expr_type)

def isWithinParent(conn: "Connection", index: int, expr_type: TYPES, parent_expr_type: TYPES) -> bool:
    precedent_id, precedent_type = getParent(conn, index, expr_type)

    if (precedent_type == parent_expr_type):
        return True
    elif (precedent_type == TYPES.CU):
        return False
    else:
        return isWithinParent(conn, precedent_id, precedent_type, parent_expr_type)

def MethodCallExpr(conn: "Connection", index: int)  -> str:
    # select id from exprs where precedent_id = index and precedent_type = 8 
    # 通过nargs和查询到的结果集得到 MethodCallExpr 的 名称 和参数
    # 参数可能为Expression表达式，需要对表达式进行展开

    cursor = conn.cursor()
    methodInfo = getMethodInfoById(conn, index)    
    arguments_exprs = []
    for argument in methodInfo["argsIds"]:
        c = cursor.execute("select expr_type from exprs where id = ?", (argument,))
        argument_type = c.fetchone()[0]
        arguments_exprs.append(json.loads(getCompleteExpr(conn, argument, TYPES.ofName(toStandardName(argument_type)))))
        
    output = methodInfo["name"] + "("
    for argument_expr in arguments_exprs:
        output += argument_expr["output"] + ","

    if (output[-1] == ","):
        output = output[:-1]
    output += ")"

    return json.dumps({
        "methodCallId": methodInfo["methodCallId"],
        "name": methodInfo["name"],
        "argsNum": methodInfo["argsNum"],
        "fileName": methodInfo["fileName"],
        "lineNo": methodInfo["lineNo"],
        "arguments": arguments_exprs,
        "output": output
    })

def toStandardName(name: str) -> str:
    return name.replace("_", "").upper()


def FieldAccessExpr(conn: "Connection", index: int) -> str:
    cursor = conn.cursor()
    c = cursor.execute("select id, expr_type from exprs where precedent_id = ? and precedent_type = ?",(index, TYPES.FIELDACCESS.value[1]))
    tokens = c.fetchall()
    tokens_expr = []
    for token in tokens:
        tokens_expr.insert(0, json.loads(getCompleteExpr(conn, token[0], TYPES.ofName(toStandardName(token[1])))))
    
    
    return json.dumps({
        "tokens":tokens_expr,
        "output":".".join([expr["output"] for expr in tokens_expr])
    })


def SimpleNameExpr(conn: "Connection", index: int) -> str:
    cursor = conn.cursor()
    c = cursor.execute("select name from SIMPLE_NAME_EXPR S, EXPRS E where E.id = ? and S.id = e.EXPR_ID", (index,))
    name = c.fetchone()
    if (name):
        return json.dumps({"output": name[0]})
    return ""
    
def getMethodInfoById(conn: "Connection", index: int) -> dict:
    cursor = conn.cursor()
    c = cursor.execute('''
select group_concat(E.expr_id), E.precedent_id, M.args_num, E.line_no, group_concat(E.id), E.precedent_type from EXPRS E, (
select E.id, M.args_num from EXPRS E ,METHOD_CALL_EXPR M where E.id = ? and E.EXPR_TYPE in ("METHOD_CALL", "OBJECT_CREATION") and E.expr_id = M.id
)  M where E.precedent_id  = M.id and E.precedent_type in (8,12) GROUP BY PRECEDENT_ID
    ''', (index,))
    methodInfo = c.fetchone()
    founded_methodcallexprs = []
    sub_exprs = [expr_id for expr_id in methodInfo[4].split(",")]
    name_id = sub_exprs[methodInfo[2]]
    # c = cursor.execute("SELECT name from SIMPLE_NAME_EXPR where id = ?", (name_id,))
    # methodCallName = c.fetchone()[0]
    name_type = cursor.execute("select expr_type from exprs where id = ?", (name_id,)).fetchone()[0]
    methodCallName = json.loads(getCompleteExpr(conn, name_id, TYPES.ofName(toStandardName(name_type))))["output"]
    packageinfo = getPackageInfo(conn, methodInfo[1], TYPES.METHODCALLEXPR)
    return {
        "methodCallId": methodInfo[1],
        "name": methodCallName,
        "argsNum": methodInfo[2],
        "argsIds": [argId for index, argId in enumerate(methodInfo[4].split(",")) if index < methodInfo[2]],
        "fileName": packageinfo["fileName"],
        "lineNo": methodInfo[3]
        }


def getMethodsInfoByName(conn: "Connection", methodCallName: str) -> list:
    cursor = conn.cursor()
    c = cursor.execute('''
select group_concat(E.expr_id), E.precedent_id, M.args_num, E.line_no, group_concat(E.id) from EXPRS E, (
select E.id, M.args_num from EXPRS E JOIN METHOD_CALL_EXPR  M on E.EXPR_ID = M.id where E.EXPR_TYPE="METHOD_CALL" 
)  M where E.precedent_id  = M.id and E.precedent_type = 8 GROUP BY PRECEDENT_ID
''')
    all_item = c.fetchall()
    founded_methodcallexprs = []
    # package_list = []
    for item in all_item:
        sub_exprs = [expr_id for expr_id in item[0].split(",")]
        name_id = sub_exprs[item[2]]
        c = cursor.execute("SELECT count(id) from SIMPLE_NAME_EXPR where id = ? and name = ?", (name_id, methodCallName))
        if (c.fetchone()[0] == 1):
            packageinfo = getPackageInfo(conn, item[1], TYPES.METHODCALLEXPR)
            # if (packageinfo["fileName"] not in package_list):
            #     package_list.append(packageinfo["fileName"])
            founded_methodcallexprs.append({
                "methodCallId": item[1],
                "name": methodCallName,
                "argsNum": item[2],
                "argsIds": [argId for index, argId in enumerate(item[4].split(",")) if index < item[2]],
                "fileName": packageinfo["fileName"],
                "lineNo": item[3]
            })
    return founded_methodcallexprs
    