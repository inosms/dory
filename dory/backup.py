import os
import sys
import time
import shutil
from dory import util
from dory.util import get_remote_login
from dory.util import get_remote_path
import re
from termcolor import colored

RSYNC_OPTIONS = "--numeric-ids --delete -az --rsh=ssh"
def get_rsync_command(source,destination):
    return "rsync -Ph {} '{}' '{}'".format(RSYNC_OPTIONS,source,destination)

def create_base_backup(destination,backup_name,is_remote):
    """creates a base backup folder, which is just a
    hardlinked copy of the previous backup, when existing
    """
    print(colored("looking for last backup as base ...","green"))

    folders = util.backup_folder_list(destination)

    # only if there was one folder copy
    if folders:
        # last backup is the last element in the sorted list
        last_backup = folders[-1]

        if last_backup == backup_name or last_backup+".part" == backup_name:
            print(colored("backup with current timestamp already exists\n\
                            are you trying, to backup more than one time per second?","red"))
            sys.exit(1)

        print("using last backup: {}".format(last_backup))

        if util.is_remote(destination):
            os.system("ssh {} cp -al {} {}"\
                .format(\
                    get_remote_login(destination),\
                    os.path.join(get_remote_path(destination),last_backup),\
                    os.path.join(get_remote_path(destination),backup_name)))
        else:
            # https://stackoverflow.com/questions/10778229/recursively-creating-hardlinks-using-python
            shutil.copytree(
                os.path.join(destination,last_backup),
                os.path.join(destination,backup_name),
                copy_function=os.link)
    else:
        print("no last backup found")


def start(source,destination):
    today = time.strftime("%Y_%m_%d_%H%M%S")
    logfile = destination + today + ".log"

    backupfolder_partial = today+".part"
    backupfolder_full = today

    if util.is_remote(destination):
        create_base_backup(destination,backupfolder_partial,is_remote=True)

        print(colored("starting backup ...","green"))
        rsync_command = get_rsync_command(source,os.path.join(destination,backupfolder_partial))
        # https://unix.stackexchange.com/questions/34273/can-i-pipe-stdout-on-one-server-to-stdin-on-another-server
        result = os.system("{} | ssh {} tee -a {}"
                    .format(
                        rsync_command,
                        get_remote_login(destination),
                        os.path.join(get_remote_path(destination),today+".log")))

        if result != 0:
            print(colored("backup failed; rsync returned {}".format(result),"red"))
            sys.exit(1)
        else:
            # rename the partial folder name to the full name at the end
            os.system("ssh {} mv '{}' '{}'"
                .format(
                    get_remote_login(destination),
                    os.path.join(get_remote_path(destination),backupfolder_partial),
                    os.path.join(get_remote_path(destination),backupfolder_full)
                ))
    else:
        create_base_backup(destination,backupfolder_partial,is_remote=False)

        print(colored("starting backup ...","green"))
        rsync_command = get_rsync_command(source,os.path.join(destination,backupfolder_partial))
        result = os.system("{} | tee -a {}".format(rsync_command,logfile) )

        if result != 0:
            print(colored("backup failed; rsync returned {}".format(result),"red"))
            sys.exit(1)
        else:
            # rename the partial folder name to the full name at the end
            os.rename(os.path.abspath(os.path.join(destination,backupfolder_partial)),
                os.path.abspath(os.path.join(destination,backupfolder_full)))


    print(colored("backup finished!","green"))
