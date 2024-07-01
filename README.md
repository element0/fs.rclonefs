# Access rclone from a pyfilesystem interface
I needed this.

__version__ = 0.3.1



## About

This gives you a `pyfilesystem` object with an `rclone` remote for a backend. So any backend you can use with rclone, you can use with pyfilesystem.

Internally it uses another project, `rclone-python` as middleware to `rclone`. If you don't need a `pyfilesystem` interface but you want to work with `rclone` via python, you should check out `rclone-python`.

### Usage

This assumes you've run the external program `rclone config` and configured a remote called `dropbox`.


    >>> from fs.rclonefs import RcloneFS
    >>> my_remote = RcloneFS('dropbox:')
    >>> my_remote.listdir('/')
    >>> my_remote.getinfo('/that_file_over_there.mp4')


### Status

Implemented:
- getinfo()
- listdir()
- isdir()

TBD:
- URI opener
- all other methods

## Dependencies

#### Automatically installed: rclone-python

This handy tool controls `rclone` from python. 

[pypi.org/project/rclone-python/](https://pypi.org/project/rclone-python/)

[github.com/Johannes11833/rclone_python](https://github.com/Johannes11833/rclone_python)

#### Manually installed: rclone v1.67.0

This _is_ rclone. Control a wide variety of cloud storage with this puppy.

[github.com/rclone/rclone](https://github.com/rclone/rclone)
[Install rclone on your own.](https://rclone.org/install/)

__version_used_by_this_project__ = _rclone-v1.67.0-linux-amd64_

#### Automatically installed: pyfilesystem 2.4.12

The Mac-Daddy of all file system abstractions -- besides rclone -- and besides FUSE. But _absolutely_ one of the number ones.

Installed automagically with fs-rclone if'n y'all don't already have it.


## Tools

Added a `makepy` tool in the tools directory which extracts the second cell from a jupyter notebook and saves a python file.

    >>> from makepy import makepy
    >>> makepy('rclonefs','opener')

It takes one or more filenames from the working directory -- without the .ipynb extension -- and exports the 2nd cell to a python file with the same base name.

(Not packaged with the pip distro. Find it in the git repo.)


## Changelog

0.3.1 Fixed `fs` namespace packaging.

0.3.0 Add `getinfo()`, `listdir()`, `isdir()`. Add `makepy` tool. Add `Devnotes.ipynb`.

0.2.0 Fix project name for pyfilesystem style. Add src RcloneFS.ipynb and opener.ipynb.

0.1.2 Update README

0.1.0 Add dependencies to `pyproject.toml`. Add `SoftBOM` (software bill of materials). Delete test code.

0.0.1 fix bug in example::add_one

0.0.0 configure package files
