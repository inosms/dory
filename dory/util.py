import os
import re
from termcolor import colored
import sys
import shutil
import subprocess

def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)
    return iter(p.stdout.readline, b'')

def check_for(command):
    """check for commands if they are
    available on the system
    """
    if shutil.which(command) is None:
        print(colored("{} not available on system".format(command),"red"))
        sys.exit(1)

def remove_end_newline(text):
    if text:
        if text.endswith('\n'):
            return text[:-1]
        else:
            return text
    else:
        return ""

def is_remote(path):
    return '@' in path

def get_remote_login(destination):
    return destination.split(':')[0]

def get_remote_path(destination):
    return destination.split(':')[-1]


def backup_folder_list(path):
    """returns a list of directories in the given path,
    matching all folders, that are named like a backup folder.
    path can either be local or a remote ssh path.
    """
    folders = []

    if is_remote(path):
        # for remote: get list of folders per ssh
        for line in run_command("ssh {} ls -1 -d {}*/"
            .format(
                get_remote_login(path),
                get_remote_path(path))):
            if not "No such file or directory" in line.decode("ascii"):
                decoded_name = line.decode("ascii")
                # as we only want to use only the folder name and not the whole path
                only_folder_name = re.sub("^"+get_remote_path(path),"",decoded_name)
                folders.append(remove_end_newline(only_folder_name))
    else:
        # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
        # list all folders in destination
        folders = [dir for dir in os.listdir(path) if os.path.isdir(os.path.join(path,dir))]

    # filter out only folder matching a backup name
    folders = [dir for dir in folders if re.match(r"\d\d\d\d_\d\d_\d\d_\d\d\d\d\d\d(.part)?/?",dir) != None ]

    # sort folders by date
    folders.sort()

    return folders
