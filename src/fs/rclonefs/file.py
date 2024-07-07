import io
import os
import subprocess
from fs.tempfs import TempFS
from fs.errors import ResourceNotFound

class RcloneFile(io.IOBase):
    def __init__(self, parentfs, path, mode):
        self.parentfs = parentfs
        self.rclone = parentfs.rclone
        self.path = path
        self.mode = mode
        self.temp_fs = parentfs.temp_fs
        self.temp_path = f"{os.path.basename(path)}"
        self.position = 0
        if self.parentfs.exists(path):
            self.parentfs.download(path,self.temp_fs.syspath(self.temp_path))
        self.file = self.temp_fs.openbin(self.temp_path, mode)
                           
    def read(self, size=-1):
        return self.file.read(size)

    def write(self, data):
        return self.file.write(data)

    def seek(self, offset, whence=io.SEEK_SET):
        return self.file.seek(offset, whence)

    def tell(self):
        return self.file.tell()

    def close(self):
        self.flush()
        if self.file:
            if 'w' in self.mode or '+' in self.mode:
                print('w in self.mode')
                self.parentfs.upload(self.path, self.file)
            self.file.close()
            self.temp_fs.remove(self.temp_path)
            
