import sys
import shutil
import argparse
import restore
import backup
from termcolor import colored

def parse_arguments():
    parser = argparse.ArgumentParser(description="simple file backup tool using rsync")
    parser.add_argument("source",type=str, help="source path for backup, will be backed up in destination")
    parser.add_argument("destination",type=str, help="destination path for backup")
    parser.add_argument("-r","--restore",action="store_true", help="with restore one connects the source to the backup to open the restoration console")
    args = parser.parse_args()

    SRC = args.source
    DEST = args.destination

    # make sure that the destination directory ends with a "/"
    if not DEST.endswith("/"):
        DEST = DEST + "/"

    if args.restore:
        restore.start(SRC,DEST)
    else:
        backup.start(SRC,DEST)

def check_rsync():
    if shutil.which("rsync") is None:
        print(colored("rsync not available on system","red"))
        sys.exit(0)

def main():
    check_rsync()
    parse_arguments()
