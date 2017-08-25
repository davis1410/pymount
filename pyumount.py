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
            print '"%s" directory unmounted' % directory

    if directories_unmounted == 0:
        print "No directories currently mounted"
    else:
        os.system("rm -rf %s/*" % local_mount_dir)

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



# def unmount_directories():
#     # Disconnect single directory
#     if umount_dirs:
#         print "single directory"

#         # Don't run umount if directory isn't mounted
#         if not os.path.ismount("%s/%s" % (local_mount_dir, umount_dir)):
#             print '"%s" directory is not mounted' % umount_dir

#         else:
#             os.system("umount %s/%s" % (local_mount_dir, umount_dir))
#             os.system("rm -r %s/%s" % (local_mount_dir, umount_dir))
#             print '"%s" directory unmounted' % umount_dir

#     # Disconnect all directories
#     else:

#         unmounted_dirs = 0

#         for unmount_dir in os.listdir(local_mount_dir):

#             # Check if this directory is the media directory. If so, check for mounted directories inside.
#             if unmount_dir == "media":
#                 for sub_unmount_dir in os.listdir("%s/media" % local_mount_dir):

#                     # Check if this directory is a mount point, and if not, skip it.
#                     if not os.path.ismount("%s/media/%s" % (local_mount_dir, sub_unmount_dir)):
#                         continue
#                     else:
#                         os.system("umount %s/media/%s" % (local_mount_dir, sub_unmount_dir))
#                         print '"media/%s" directory unmounted' % sub_unmount_dir
#                         unmounted_dirs += 1

#             # Check if this directory is a mount point, and if not, skip it.
#             elif not os.path.ismount("%s/%s" % (local_mount_dir, unmount_dir)):
#                 continue

#             else:
#                 os.system("umount %s/%s" % (local_mount_dir, unmount_dir))
#                 print '"%s" directory unmounted' % unmount_dir
#                 unmounted_dirs += 1

#         if unmounted_dirs == 0:
#             print 'No directories currently mounted'
#         else:
#             os.system("rm -rf %s/*" % local_mount_dir)

# unmount_directories()
