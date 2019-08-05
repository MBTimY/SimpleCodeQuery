#coding=utf-8

Name : str = "Example"

Version : str = "1.0"

Describe : str = "这只是一个例子，传入的参数会当成一个数组输出到Console"

def Report(conn, *args):
    print(args)
    print("This is a example ...")