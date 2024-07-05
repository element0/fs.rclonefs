# Access rclone from a pyfilesystem interface
I needed this.

__version__ = 0.4.0



## About

This gives you a `pyfilesystem` object with an `rclone` remote for a backend. So any backend you can use with rclone, you can use with pyfilesystem.

If you don't need a `pyfilesystem` interface but you want to work with `rclone` via python, you can use the `rclone` class that comes with this package and your should also check out the (unrelated) `rclone-python` project.

(BTW: I've used Anthropic's Claude to co-write this. I highly recommend it.)

There's work to be done making sure the `Info` object's raw formatting matches pyfilesystem.

One MINOR regression with this current commit. You can't use a colon in the remote name when you init.

WARNING: Only the listdir() and getinfo() methods have been tested. Use at your own risk!

### Usage

This assumes you've run the external program `rclone config` and configured a remote called `dropbox`.

    >>> from fs.rclonefs import RcloneFS
    >>> my_remote = RcloneFS('dropbox')
    >>> my_remote.listdir('/')
    >>> my_remote.getinfo('/that_file_over_there.mp4')


### Status

Implemented:
- getinfo()
- listdir()
- isdir()
- makedir()
- remove()
- removedir()
- upload()
- download()

TBD:
- URI opener
- openbin() and related

## Dependencies

#### Automatically installed: pyfilesystem 2.4.12

The Mac-Daddy of all file system abstractions -- along side rclone -- and FUSE. But _absolutely_ number one of the number ones.

Installed automagically with fs-rclone if'n y'all don't already have it.

#### Must be installed separately: rclone v1.67.0

This _is_ rclone. Control a wide variety of cloud storage with this puppy.

[github.com/rclone/rclone](https://github.com/rclone/rclone)
[Install rclone on your own.](https://rclone.org/install/)

__version_used_by_this_project__ = _rclone-v1.67.0-linux-amd64_

<strong>Note:</strong> You might be tempted to use another version. Please use 1.67. I've confirmed that refresh tokens with Dropbox work better in 1.67. (I experienced a problem with 1.50 in which refresh tokens weren't being created during the interactive Oauth flow with Dropbox.)




## Tools

There's a `makepy` tool in the tools directory which extracts the second cell from a jupyter notebook and saves a python file.

    >>> from makepy import makepy
    >>> makepy('rclonefs','opener')

It takes one or more filenames from the working directory -- without the .ipynb extension -- and exports the 2nd cell to a python file with the same base name.

(Not packaged with the pip distro. Find it in the git repo.)


## Changelog

0.4.0 Replaced `rclone_python` dependency with custom class.

0.3.1 Fixed `fs` namespace packaging.

0.3.0 Add `getinfo()`, `listdir()`, `isdir()`. Add `makepy` tool. Add `Devnotes.ipynb`.

0.2.0 Fix project name for pyfilesystem style. Add src RcloneFS.ipynb and opener.ipynb.

0.1.2 Update README

0.1.0 Add dependencies to `pyproject.toml`. Add `SoftBOM` (software bill of materials). Delete test code.

0.0.1 fix bug in example::add_one

0.0.0 configure package files
