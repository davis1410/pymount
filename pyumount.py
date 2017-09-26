#!/usr/bin/python

import os
import sys
import argparse
import json

# unmount the directories
def unmount_directories(local_mount_dir, directories):

    directories_unmounted = 0

    for directory in directories:
        # check if this directory is a mount point, and if not, skip it
        if not os.path.ismount("%s/%s" % (local_mount_dir, directory)):
            continue
        else:
            os.system("umount %s/%s" % (local_mount_dir, directory))
            print 'unmounting directory: "%s"' % directory
            directories_unmounted += 1

    if directories_unmounted == 0:
        print "No directories currently mounted"
    else:
        dirs_to_unmount = []
        for directory in directories:
            if os.path.ismount("%s/%s" % (local_mount_dir, directory)):
                print '"%s" directory did not unmount properly. Removing directory aborted.'
            else:
                dirs_to_unmount.append(directory)
        
        for directory in dirs_to_unmount:
            os.system("rm -rf %s/%s" % (local_mount_dir, directory))

# get configuration
def get_config(config_file):
    with open(config_file) as f:
        data = json.load(f)
    return data


# parse the args input by the user
parser = argparse.ArgumentParser(description='Unmount directories on local filesystem.')
parser.add_argument("-d", "--directories", nargs='*', help="list of directories to unmount")

# get args
args = parser.parse_args()

config_dir, script_file = os.path.split(os.path.abspath(__file__))
config_file = "%s/pymount_config.json" % config_dir
config = get_config(config_file)

local_mount_dir = config["local_mount_dir"]

if args.directories:
    unmount_directories(local_mount_dir, args.directories)
else:
    if not os.path.ismount(local_mount_dir):
        print "Directory not mounted"
    else:
        os.system("umount %s" % local_mount_dir)
