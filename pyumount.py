#!/usr/bin/python

import os
import sys
import argparse
import json

# unmount the directories
def unmount_directories(local_mount_dir, directories):

    directories_unmounted = 0

    for directory in directories:
        dir_path = "%s/%s" % (local_mount_dir, directory)
        # check if this directory is a mount point, and if not, skip it
        if not os.path.ismount(dir_path):
            continue
        else:
            os.system("umount %s" % dir_path)
            if not os.path.ismount(dir_path):
                print '"%s" directory unmounted' % directory
                os.system("rm -r %s" % dir_path)
                directories_unmounted += 1
            else:
                print 'error unmounting "%s" directory' % directory
                break

    if directories_unmounted == 0:
        print "No directories currently mounted"

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
