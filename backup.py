import os
import sys
import time
import shutil
import util
from termcolor import colored

RSYNC_OPTIONS = "--numeric-ids --delete -az --rsh=ssh"
def get_rsync_command(source,destination):
    return "rsync -Ph {} '{}' '{}'".format(RSYNC_OPTIONS,source,destination)

def create_base_backup(destination,backup_name,is_remote):
    """ creates a base bakcup folder, which is just a
    hardlinked copy of the previous backup, when existing """

    print(colored("looking for last backup as base ...","green"))

    folders = []

    if is_remote:
        # for remote: get list of folders per ssh
        for line in util.run_command("ssh {} ls -1 -d {}*/"\
            .format(\
                get_remote_login(destination),\
                get_remote_path(destination))):
            if not "No such file or directory" in line.decode("ascii"):
                folders.append(util.remove_end_newline(line.decode("ascii")))
    else:
        # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
        # list all folders in destination
        folders = [dir for dir in os.listdir(destination) if os.path.isdir(os.path.join(destination,dir))]

    # sort folders by date
    folders.sort()

    # only if there was one folder copy
    if folders:
        # last backup is the last element in the sorted list
        last_backup = folders[-1]

        if last_backup == backup_name:
            print(colored("backup with current timestamp already exists\n\
                            are you trying, to backup more than one time per second?","red"))
            sys.exit(1)

        print("using last backup: {}".format(last_backup))

        if is_remote:
            os.system("ssh {} cp -al {} {}"\
                .format(\
                    get_remote_login(destination),\
                    os.path.join(get_remote_path(destination),last_backup),\
                    os.path.join(get_remote_path(destination),backup_name)))
        else:
            # https://stackoverflow.com/questions/10778229/recursively-creating-hardlinks-using-python
            shutil.copytree(os.path.join(destination,last_backup), os.path.join(destination,backup_name), copy_function=os.link)
    else:
        print("no last backup found")

def is_remote(path):
    return '@' in path

def get_remote_login(destination):
    return destination.split(':')[0]

def get_remote_path(destination):
    return destination.split(':')[-1]

def start(source,destination):
    today = time.strftime("%Y_%m_%d_%H%M%S")
    logfile = destination + today + ".log"

    if is_remote(destination):
        create_base_backup(destination,today,is_remote=True)
        # https://unix.stackexchange.com/questions/34273/can-i-pipe-stdout-on-one-server-to-stdin-on-another-server
        os.system( (get_rsync_command(source,os.path.join(destination,today)) + "| ssh {} tee -a {}").format(get_remote_login(destination), os.path.join(get_remote_path(destination),today+".log")) )
    else:
        create_base_backup(destination,today,is_remote=False)
        print(colored("starting backup ...","green"))
        os.system( (get_rsync_command(source,os.path.join(destination,today)) + "| tee -a {}").format(logfile) )
        print(colored("backup finished!","green"))
