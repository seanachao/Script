import gdb
class BPC(gdb.Command):
    def __init__(self) -> None:
        super().__init__("bm",gdb.COMMAND_USER)

    def invoke(self,args,from_tty):
        argv = gdb.string_to_argv(args)
        if len(argv) != 2:
                raise gdb.GdbError("输入参数不对!bpc *0x0000 comment")
        gdb.execute('b ' + argv[0])
        with open("break.txt",'a') as f:
            f.write(argv[0]+":"+argv[1]+"\n")
class DEL(gdb.Command):
    def __init__(self) -> None:
         super().__init__("bcm", gdb.COMMAND_USER)
    def invoke(self,args,from_tty):
        with open("break.txt","w") as f:
            f.write("")
        gdb.execute("bc")
class INFOC(gdb.Command):
    def __init__(self):
        super().__init__("infoc",gdb.COMMAND_USER)
    def invoke(self,args,from_tty):
        with open("break.txt","r") as f:
            data = f.read()
        print(data)
DEL()
BPC()
INFOC()
