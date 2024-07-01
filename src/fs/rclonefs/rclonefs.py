# fs.rclonefs
# rclonefs.py

# Let's get this party started.

from fs.base import FS
from fs.info import Info
from fs.errors import FSError
from fs.errors import CreateFailed
from fs.errors import ResourceNotFound
from fs.errors import DirectoryExpected
from fs.enums import ResourceType
from fs.path import basename
from fs.path import dirname
from fs.path import abspath
from fs.path import normpath
import json

# this is our rclone_handler
from rclone_python import rclone


def helper_type_from_mime_type(mime_type):
    """Turn mime type into ResourceType.
    (Map to files or directories.)
    These are just for starters...
    """
    if mime_type == 'inode/directory':
        return int(ResourceType.directory)
    elif mime_type == 'inode/file':
        return int(ResourceType.file)
    elif mime_type == 'application/octet-stream':
        return int(ResourceType.file)
    else:
        return int(ResourceType.unknown)

class RcloneFS(FS):
    """Provide a pyfilesystem interface for an rclone remote.
    """

    def __init__(self, rclone_remote_name, rclone_handler=rclone):
        """
        Arguments:
            self
            rclone_remote_name
            rclone_handler
        Raises:
            fs.errors.CreateFailed
        """
        
        self._rclone = rclone_handler
        self._remote_name = rclone_remote_name if rclone_remote_name.endswith(':') else rclone_remote_name + ':'
        if not self._rclone.is_installed:
            raise CreateFailed("Requires rclone. For installation see https://rclone.org/install/")
        if not self._rclone.check_remote_existing(rclone_remote_name):
            raise CreateFailed('Please use the name of an existing remote.')
        super().__init__()

    def getinfo(self, path, namespaces=None):
        # type: (Text, Optional[Collection[Text]]) -> Info
        """
        Arguments:
            path (str): 
            namespaces (list, optional): "basic" always included
        Returns:
            ~fs.info.Info: resource information object.

        Raises:
            fs.errors.ResourceNotFound: If ``path`` does not exist.
        
        """
        _abspath = abspath(normpath(path))
        _dirname = dirname(_abspath)
        _basename = basename(_abspath)
            
        with self._lock:
            
            if _abspath == '/':
                # it's fakeroot time.
                about = self._rclone.about(self._remote_name)
                raw_info = {
                    'basic': {
                        'name': '/',
                        'is_dir': True
                    },
                    'details': {
                        'accessed': None,
                        'created': None,
                        'metadata_changed': None,
                        'modified': None,
                        'size': about['used'],
                        'type': 1
                    },
                    'rclone.about': about
                }
                return Info(raw_info)

            try:
                _dir = self._rclone.ls(self._remote_name + _dirname)
                _e = [e for e in _dir if e["Name"] == _basename][0]
                _type = helper_type_from_mime_type(_e["MimeType"])
                raw_info = {
                    'basic': {
                        'name': _e["Name"],
                        'is_dir': _e["IsDir"]
                    },
                    'details': {
                        'accessed': None,
                        'created': None,
                        'metadata_changed': None,
                        'modified': _e['ModTime'],
                        'size': _e['Size'],
                        'type': _type
                    }
                }
            except Exception as e:
                raise e
            return Info(raw_info)

    # note: the default implementation
    #   of `isdir()` uses the results of
    #   get info.

    def listdir(self, path):
        # type: (Text) -> List[Text]
        """Get a list of the resource names in a directory.

        This method will return a list of the resources in a directory.
        Resources are defined in `~fs.enums.ResourceType`.

        Arguments:
            path (str): A path to a directory on the filesystem.
            
        Returns:
            list: list of names, relative to ``path``.
        
        Raises:
            fs.errors.DirectoryExpected: If ``path`` is not a directory.
            fs.errors.ResourceNotFound: If ``path`` does not exist.
    
        """
        
        _abspath = abspath(normpath(path))
        _dirname = dirname(_abspath)
        _basename = basename(_abspath)
        
        with self._lock:
            try:
                if self.isdir(_abspath):
                    res = self._rclone.ls(self._remote_name + _abspath)
                    return [ e['Name'] for e in res ]
                else:
                    raise DirectoryExpected(path)
            except Exception as e:
                if "directory not found" in str(e):
                    raise ResourceNotFound(path)
                else:
                    raise
                
    
    def makedir(self):
        pass

    def openbin(self):
        pass

    def remove(self):
        pass

    def removedir(self):
        pass

    def setinfo(self):
        pass