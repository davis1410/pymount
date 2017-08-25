# Pymount
Helper command line program for OSX to mount remote directories to a local filesystem

## Install
1. Install [Node.js](https://nodejs.org/en/)
2. Install [FUSE (SSHFS)](https://osxfuse.github.io/)
3. Install Pymount via npm:

        $ npm install -g git+https://github.com/davis1410/pymount.git
4. Run generate config to create the configuration file:

        $ pymount --generate-config

    or:

        $ pymount -gc
## Usage

#### Mount
* To mount the default directory set in the config file, simply run the `pymount` command:

        $ pymount

* To mount subdirectories within the default directory, use the `--directories` flag:

        $ pymount --directories foo bar

    or:

        $ pymount -d foo bar

#### Unmount
* To unmount the default directory, run the `pyumount` command:

        $ pyumount

* To unmount subdirectories, use the `--directories` flag with the `pyumount` command:

        $ pyumount --directories foo bar

    or:

        $ pyumount -d foo bar


