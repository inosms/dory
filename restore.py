#http://pymotw.com/2/cmd/
import cmd
import backup
import os
import util
from termcolor import colored

class RestorationConsole(cmd.Cmd):
    """Restorarion Console class"""

    def __init__(self,source,destination):
            cmd.Cmd.__init__(self)
            self.source = source
            self.destination = destination
            self.current_dir = ""
            self.set_prompt()

    def set_prompt(self):
        if self.current_dir == "":
            self.prompt = "(dory) "
        else:
            self.prompt = "(dory: " + self.current_dir + ") "

    def help_diff(self):
        print("lists difference for [path]\n"
                +  "Lists difference between the given path")
        print(colored("in backup and source","green"))
        print(colored("in backup and not in source","red"))
        print(colored("not in backup but in source","yellow"))

    def do_diff(self, arg1="."):
        print("TODO")
        # TODO
        # for line in util.run_command("rsync -nhi {} '{}' '{}'".format(backup.RSYNC_OPTIONS,os.path.abspath(self.destination+"backup")+"/",os.path.abspath(self.source))):
            # https://stackoverflow.com/questions/17615414/how-to-convert-binary-string-to-normal-string-in-python3
            # print(util.remove_end_newline(line.decode("ascii")))

    def do_cd(self, path="."):
        print("TODO")

    def do_exit(self,line):
        """exits the console"""
        return True

    def preloop(self):
        print("Welcome to the restoration console for {} using backup from {}".format(colored(self.source,"green"),colored(self.destination,"green")))

    def postloop(self):
        print("bye")

def start(source,destination):
    RestorationConsole(source,destination).cmdloop()
