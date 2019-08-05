#coding=utf-8

import sys
sys.path.append("..")
from TYPES import TYPES
import Utils 
import json

Name : str = "countMC"

Version : str = "1.0"

Describe : str = "用来查找某个函数调用的位置，描述这个函数总的调用次数！Params: (methodCallName: str)"

def Report(conn: "Connection", methodCallName:str) -> str:
    cursor = conn.cursor()
    c = cursor.execute('''
select group_concat(expr_id), E.precedent_id, M.args_num from EXPRS E, (
select E.id, M.args_num from EXPRS  E JOIN METHOD_CALL_EXPR  M on E.EXPR_ID = M.id where E.EXPR_TYPE="METHOD_CALL" 
)  M where E.precedent_id  = M.id and E.precedent_type = 8   GROUP BY PRECEDENT_ID
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
            if (packageinfo["fileName"] not in package_list):
                package_list.append(packageinfo["fileName"])
            founded_methodcallexpr.append({
                "methodCallId": item[1],
                "name": methodCallName,
                "argsNum": item[2]
            })
    
    output = []
    output.append("The \"{0}\" Method Call is occurs {1} times\nSpread in {2} files\n".format(methodCallName, len(founded_methodcallexpr), len(package_list)))
    output.append("\nName of files is following:")
    for fileName in package_list:
        output.append("\n" + fileName)
    return json.dumps({"occurs": len(founded_methodcallexpr), "package_list":package_list, "output":output})