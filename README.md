# Rclone Wrapper for Pyfilesystem
__version__ = 0.1.0

I needed this.

## About

This wraps `rclone-python` in a `pyfilesystem` interface. If you don't need a `pyfilesystem` interface you don't need `fs_rclone`. So if that's the case you should use `rclone-python` or `rclone` directly.

## Dependencies

    pip install fs_rclone

...installs `rclone-python` automatically.

You [install rclone](https://rclone.org/install/) on your own.


#### rclone-python

This dep controls `rclone` from python. 

    [https://pypi.org/project/rclone-python/](https://pypi.org/project/rclone-python/)

    [https://github.com/Johannes11833/rclone_python](https://github.com/Johannes11833/rclone_python)

#### Rclone v1.67.0

This dep _is_ rclone. Control a wide variety of cloud storage with this puppy.

    [https://github.com/rclone/rclone](https://github.com/rclone/rclone)

__reference_distribution__ = _rclone-v1.67.0-linux-amd64_

[Installation](https://rclone.org/install/)


#### pyfilesystem 2.4.12

The Mac-Daddy of all file system abstractions -- besides rclone -- and besides FUSE. But _absolutely_ one of the number ones.

`pyfilesystem` and `rclone` need to have a baby. Which is `fs_rclone` IMHO.


## Changelog

0.1.0 Add dependencies to `pyproject.toml`. Add `SoftBOM` (software bill of materials). Delete test code.

0.0.1 fix bug in example::add_one

0.0.0 configure package files

