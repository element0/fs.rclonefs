# Access rclone from a pyfilesystem interface
I needed this.

__version__ = 0.3.1



## About

This gives you a `pyfilesystem` object with an `rclone` remote for a backend. So any backend you can use with rclone, you can use with pyfilesystem. (You need to configure rclone separately.)


### Usage

This assumes you've run the external program `rclone config` and configured a remote called `dropbox:`.

    >>> from fs.rclonefs import RcloneFS
    >>> my_remote = RcloneFS('dropbox:')
    >>> my_remote.listdir('/')
    >>> my_remote.getinfo('/that file over there.mp4')
    >>> my_remote.remove('/that file over there.mp4')
    >>> my_remote.getinfo('/some folder', namespaces=['details'])

Use the 'storage' namespace to report directory sizes.

    >>> my_remote.getinfo('/gigantor', namespaces=['storage'])

The `removetree()` method uses rclone's `purge` command -- which should make quick work of directories and their contents -- really quick work if the rclone backend supports the command (Dropbox does). (The pyfilesystem default does a path walk and removes every item individually which causes a storm of API calls to the backend and takes forever to complete with large trees, leaving rclone running for several minutes and keeping you hanging.) 

### USE AT YOUR OWN RISK

Things might not work as expected. Like any other household product, you should test it on a small out-of-the-way piece of material first before dumping it all over everything.

### Status

Implemented:
- getinfo()
- listdir()
- remove()
- removedir()
- removetree()

TBD:
- URI opener
- all other methods

## Dependencies

#### Automatically installed: pyfilesystem 2.4.12

The Mac-Daddy of all file system abstractions -- along side rclone -- and FUSE. But _absolutely_ number one of the number ones.

Installed automagically with fs-rclone if'n y'all don't already have it.

#### You need to install: rclone v1.67.0

Control a wide variety of cloud storage with this puppy.

[github.com/rclone/rclone](https://github.com/rclone/rclone)
[Install rclone on your own.](https://rclone.org/install/)

__version_used_by_this_project__ = _rclone-v1.67.0-linux-amd64_


## Tools

The `Rclone` object class controls `rclone` on your system.

    >>>from fs.rclonefs import Rclone
    >>>rclone = Rclone()
    >>>rclone.list_files('myremote:')


A `makepy` tool in the tools directory extracts the second cell from a jupyter notebook and saves it as a python file.

    >>> from makepy import makepy
    >>> makepy('rclonefs','opener')

It takes one or more filenames from the working directory (without the .ipynb extension) and exports the 2nd cell of each to python files with the same base names.

(`makepy` is not packaged with the pip distro. Find it in the git repo.)


## Changelog

0.4.0 Add `remove()`, `removedir()`, `removetree()`. Add `Rclone` class. Add `storage` namespace for getinfo(). Fix datetime format in getinfo.

0.3.1 Fixed `fs` namespace packaging.

0.3.0 Add `getinfo()`, `listdir()`, `isdir()`. Add `makepy` tool. Add `Devnotes.ipynb`.

0.2.0 Fix project name for pyfilesystem style. Add src RcloneFS.ipynb and opener.ipynb.

0.1.2 Update README

0.1.0 Add dependencies to `pyproject.toml`. Add `SoftBOM` (software bill of materials). Delete test code.

0.0.1 fix bug in example::add_one

0.0.0 configure package files
