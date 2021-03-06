#!/usr/bin/python

import os
import sys
import argparse
import json

# creates directories to mount to if they don't exist
def create_dirs(directories):
    for directory in directories:
        # handle nested directories
        dir_name = directory.split('/')[-1]
        dir_path = "%s/%s" % (local_mount_dir, dir_name)

        # Check if directory exists, and if not, create it
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print 'directory created: "%s"' % dir_name

        else:
            print 'mounting existing directory: "%s"' % directory

            
# mounts the directories
def mount_directories(ssh_host, local_mount_dir, directories):
    opts = "auto_cache,defer_permissions,follow_symlinks,reconnect,noappledouble"

    if directories:
        for directory in directories:
            # handle nested directories
            dir_name = directory.split('/')[-1]
            # Create connection to server
            os.system( "sshfs %s/%s %s/%s -o %s,volname=%s" % (ssh_host, directory, local_mount_dir, dir_name, opts, dir_name) )
    else:
        os.system( "sshfs %s %s -o %s" % (ssh_host, local_mount_dir, opts) )


# generate config file
def generate_config(config_file):
    ssh_host = raw_input("Please enter an ssh host (e.g. user@server:/path/to/remote/dir): ")
    local_mount_dir = raw_input("Please enter a local directory path to mount remote directories to (e.g. /Users/username/Development): ")
    if not os.path.exists(local_mount_dir):
        create_local_mount_dir = raw_input("The local directory you entered does not exist. Create directory? (y/n) ")
        if create_local_mount_dir == 'y':
            os.system("mkdir %s" % local_mount_dir)
    
    config_data = {
        "ssh_host": ssh_host,
        "local_mount_dir": local_mount_dir
    }

    os.system( "touch %s" % config_file )
    with open(config_file, 'w') as f:
        data = json.dumps(config_data, f, sort_keys=True, indent=4, ensure_ascii=False)
        f.write(data)


# get configuration
def get_config(config_file):
    with open(config_file) as f:
        data = json.load(f)
    return data


# parse the args input by the user
parser = argparse.ArgumentParser(description='Mount directories from remote server to local filesystem.')
parser.add_argument("-d", "--directories", nargs='*', help="sub-directories inside main directory to mount")
parser.add_argument("-gc", "--generate-config", action='store_true', help="generates config file containing the remote server path and the local directory path to mount remote directories to")

# get args
args = parser.parse_args()

config_dir, script_file = os.path.split(os.path.abspath(__file__))
config_file = "%s/pymount_config.json" % config_dir

if args.generate_config:
    generate_config(config_file)

elif os.path.exists(config_file):
    config = get_config(config_file)

    ssh_host = config["ssh_host"]
    local_mount_dir = config["local_mount_dir"]

    directories = args.directories

    if directories:
        # create directories if they don't exist
        create_dirs(directories)
        
    # mount the directories
    mount_directories(ssh_host, local_mount_dir, directories)

else:
    print "Config file not found. Please run 'pymount --generate-config' to generate a config file"