import sqlite3
import click
import os
from Answer import Answer
import re
from cmd import Cmd
from TYPES import TYPES

class CmdShell(Cmd):
    prompt = '>>>'
    intro = "JavaCode advanced querying ..."

    def __init__(self, answer: Answer):
        super(CmdShell,self).__init__()
        self.gAnswer = answer

    def do_show(self, line):
        "Show all of supported answers\nUsage:\tshow"
        answers = self.gAnswer.getAnswers()
        click.echo (click.style("There is answer name list: \n", fg='green'))
        for answer in answers:
            click.echo (click.style("{0:<22} --> {1}".format(answer["name"], answer["describe"]), fg="green"))

    def do_use(self, answerName, *parameters):
        "Use a specify answer with name and parameters:\nUsage:\tuse [AnswerName] [Parameters]"
        click.echo(click.style(self.gAnswer.Answer(answerName, *parameters), fg="green"))
        pass
    
    def do_types(self, line):
        "Show supported types"
        types = TYPES.getTypes()
        output = "The supported types is fllowing:"
        for _type in types:
            output = output + "\n" + _type
        click.echo(click.style(output, fg="green"))
    
    def do_q(self, line):
        "Exit the shell"
        exit(0)
    
    def parseline(self, line):
        cmd, args, line = super(CmdShell, self).parseline(line)
        if (args != None and " " in args):
            args = [arg for arg in args.split(" ") if arg != ""]
        else:
            args = [args]
        return cmd,args,line
            
    def onecmd(self, line):
        """Interpret the argument as though it had been typed in response
        to the prompt.

        This may be overridden, but should not normally need to be;
        see the precmd() and postcmd() methods for useful execution hooks.
        The return value is a flag indicating whether interpretation of
        commands by the interpreter should stop.

        """
        cmd, arg, line = self.parseline(line)
        if not line:
            return self.emptyline()
        if cmd is None:
            return self.default(line)
        self.lastcmd = line
        if line == 'EOF' :
            self.lastcmd = ''
        if cmd == '':
            return self.default(line)
        else:
            try:
                func = getattr(self, 'do_' + cmd)
            except AttributeError:
                return self.default(line)
            return func(*arg)


@click.command()
@click.argument('dbfile', type=str)
@click.option("--cmd", help="Command Name", type=str, required=False)
def main(dbfile, cmd):
    if (not os.path.exists(dbfile) or not dbfile.endswith(".db")):
        raise FileExistsError

    conn = sqlite3.connect(dbfile)
    gAnswer = Answer(conn)
    gAnswer.Loads()

    import sys
    if cmd:
        CmdShell(gAnswer).onecmd(cmd)
    else:
        CmdShell(gAnswer).cmdloop()

    # COMMANDS = [
    #     {"command":"(show|s)", "cb":gAnswer.Show, "isParam": True},
    #     {"command":"(use|u) ([ \"\w]*)", "cb":gAnswer.Answer, "isParam": True}
    # ]

    # while True:
    #     command = click.prompt(">", type=str, prompt_suffix=">>")
    #     if command.lower() == "q" or command.lower() == "quit":
    #         exit(0)
    #     else:
    #         for c in COMMANDS:
    #             m = re.match(c["command"], command)
    #             if (not m):
    #                 continue
    #             params = []
    #             if len(m.groups()) > 1:
    #                 params = m.groups()[1].split(" ")
    #             try:
    #                 print(c["cb"](*params))
    #             except Exception as e:
    #                 print("Maybe your input is error, pls check inputed parameters ...")
    
if __name__ == "__main__":
    main()