from fs.base import FS
from fs.info import Info
from fs.permissions import Permissions
from fs.enums import ResourceType
from fs.errors import DirectoryExists, ResourceNotFound
from fs.path import split, normpath
from datetime import datetime
import json
from typing import List, Union

from rclone import Rclone  # Assuming this is how you've imported the previous class

class RcloneFS(FS):
    def __init__(self, remote: str, rclone: Rclone = None):
        super().__init__()
        self.remote = remote
        self.rclone = rclone or Rclone()

    def _path(self, path: str) -> str:
        return f"{self.remote}:{normpath(path).lstrip('/')}"

    def getinfo(self, path: str, namespaces=None) -> Info:
        path = normpath(path)
        if path == '/':
            return self._root_info()
        
        parent_dir, name = split(path)
        try:
            parent_path = self._path(parent_dir)
            files = self.rclone.list_files(parent_path)
            for file_info in files:
                if file_info['Name'] == name:
                    return self._make_info(file_info)
            raise ResourceNotFound(path)
        except Exception as e:
            raise ResourceNotFound(path)

    def _root_info(self) -> Info:
        try:
            # Attempt to get remote info
            remote_info = self.rclone.get_remote_info(self.remote)
            
            raw_info = {
                "basic": {
                    "name": "",
                    "is_dir": True
                },
                "details": {
                    "type": ResourceType.directory,
                    "size": remote_info.get('total_space', 0),  # Total space if available
                    "used": remote_info.get('used_space', 0),  # Used space if available
                    "free": remote_info.get('free_space', 0),  # Free space if available
                }
            }
            
            if 'modified' in remote_info:
                raw_info['details']['modified'] = self._parse_time(remote_info['modified'])

            return Info(raw_info)
        except Exception:
            # If we can't get remote info, return minimal info
            return Info({
                "basic": {
                    "name": "",
                    "is_dir": True
                },
                "details": {
                    "type": ResourceType.directory,
                }
            })

    def _make_info(self, file_info: dict) -> Info:
        raw_info = {
            "basic": {
                "name": file_info['Name'],
                "is_dir": file_info['IsDir']
            },
            "details": {
                "type": ResourceType.directory if file_info['IsDir'] else ResourceType.file,
                "size": file_info['Size'],
                "modified": self._parse_time(file_info['ModTime'])
            }
        }
        if 'Mode' in file_info:
            raw_info['access'] = {
                "permissions": Permissions(mode=int(file_info['Mode'], 8)).dump()
            }
        return Info(raw_info)

    def _parse_time(self, time_str: str) -> datetime:
        formats = [
            "%Y-%m-%dT%H:%M:%SZ",  # Dropbox format
            "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO 8601 with microseconds
            "%Y-%m-%dT%H:%M:%S%z",  # ISO 8601 with timezone
        ]
        for fmt in formats:
            try:
                return datetime.strptime(time_str, fmt)
            except ValueError:
                continue
        raise ValueError(f"Time '{time_str}' doesn't match any known format")

    def listdir(self, path: str) -> List[str]:
        path = normpath(path)
        try:
            files = self.rclone.list_files(self._path(path))
            return [file['Name'] for file in files]
        except Exception as e:
            raise ResourceNotFound(path)

    def makedir(self, path: str, permissions=None, recreate=False):
        path = normpath(path)
        try:
            self.rclone.mkdir(self._path(path))
        except Exception as e:
            if not recreate:
                raise DirectoryExists(path)

    def openbin(self, path: str, mode="r", buffering=-1, **options):
        path = normpath(path)
        raise NotImplementedError("openbin is not implemented for RcloneFS")

    def remove(self, path: str):
        path = normpath(path)
        try:
            self.rclone.delete(self._path(path))
        except Exception as e:
            raise ResourceNotFound(path)

    def removedir(self, path: str):
        path = normpath(path)
        try:
            self.rclone.rmdir(self._path(path))
        except Exception as e:
            raise ResourceNotFound(path)

    def setinfo(self, path: str, info):
        path = normpath(path)
        # RClone doesn't provide a direct way to set file info
        # You might need to implement this differently based on your needs
        pass

    def upload(self, path: str, file):
        path = normpath(path)
        local_path = file.name
        self.rclone.copy(local_path, self._path(path))

    def download(self, path: str, file):
        path = normpath(path)
        local_path = file.name
        self.rclone.copy(self._path(path), local_path)