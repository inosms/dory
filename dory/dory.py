import argparse
from dory import backup
from dory import util

def parse_arguments():
    parser = argparse.ArgumentParser(description="simple file backup tool using rsync")
    parser.add_argument("source",type=str, help="source path for backup, will be backed up in destination")
    parser.add_argument("destination",type=str, help="destination path for backup")
    args = parser.parse_args()

    SRC = args.source
    DEST = args.destination

    # make sure that the destination directory ends with a "/"
    if not DEST.endswith("/"):
        DEST = DEST + "/"

    backup.start(SRC,DEST)

def main():
    util.check_for("rsync")
    util.check_for("ssh")
    parse_arguments()
