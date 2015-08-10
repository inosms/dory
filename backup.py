import os
import sys
import time
import shutil
import util
from termcolor import colored

RSYNC_OPTIONS = "--numeric-ids --delete -az --rsh=ssh"

def get_rsync_command(source,destination):
    return "rsync -Ph {} '{}' '{}'".format(RSYNC_OPTIONS,source,destination)

def create_new_backup_folder_local(destination,backup_name):
    print(colored("looking for last backup as base ...","green"))

    # https://stackoverflow.com/questions/973473/getting-a-list-of-all-subdirectories-in-the-current-directory
    # list all folders in destination
    folders = [dir for dir in os.listdir(destination) if os.path.isdir(os.path.join(destination,dir))]

    # sort folders by date
    folders.sort()

    # only if there was one folder copy
    if folders:
        print("using last backup: {}".format(folders[-1]))
        # https://stackoverflow.com/questions/10778229/recursively-creating-hardlinks-using-python
        shutil.copytree(os.path.join(destination,folders[-1]), os.path.join(destination,backup_name), copy_function=os.link)
    else:
        print("no last backup found")

def create_new_backup_folder_ssh(destination,backup_name):
    print(colored("looking for last backup as base ...","green"))

    # https://stackoverflow.com/questions/14352290/listing-only-directory-using-ls-in-bash
    folders = []
    for line in util.run_command("ssh {} ls -1 -d {}*/"\
        .format(\
            get_remote_login(destination),\
            get_remote_path(destination))):
        if not "No such file or directory" in line.decode("ascii"):
            folders.append(util.remove_end_newline(line.decode("ascii")))

    # sort folders by date
    folders.sort()

    # only if there was one folder copy
    if folders:
        print("using last backup: {}".format(folders[-1]))
        os.system("ssh {} cp -al {} {}"\
            .format(\
                get_remote_login(destination),\
                os.path.join(get_remote_path(destination),folders[-1]),\
                os.path.join(get_remote_path(destination),backup_name)))
    else:
        print("no last backup found")


def is_remote(path):
    return '@' in path

def get_remote_login(destination):
    return destination.split(':')[0]

def get_remote_path(destination):
    return destination.split(':')[-1]

def start(source,destination):
    today = time.strftime("%Y_%m_%d_%H_%M_%S")
    logfile = destination + today + ".log"

    if is_remote(destination):
        print(colored("remote destination paths not supported yet","red"))
        create_new_backup_folder_ssh(destination,today)
        print("logging into " + get_remote_login(destination) + " into " + get_remote_path(destination))
        # https://unix.stackexchange.com/questions/34273/can-i-pipe-stdout-on-one-server-to-stdin-on-another-server
        os.system( (get_rsync_command(source,os.path.join(destination,today)) + "| ssh {} tee -a {}").format(get_remote_login(destination), os.path.join(get_remote_path(destination),today+".log")) )
    else:
        create_new_backup_folder_local(destination,today)
        print(colored("starting backup ...","green"))
        os.system( (get_rsync_command(source,os.path.join(destination,today)) + "| tee -a {}").format(logfile) )
        print(colored("backup finished!","green"))
