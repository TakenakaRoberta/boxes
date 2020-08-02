import os
import hashlib
from datetime import datetime


class FileInfo:

    def __init__(self, file_path):
        self._file_path = file_path
        self._statinfo = os.stat(file_path)

    @property
    def basename(self):
        return os.path.basename(self._file_path)

    @property
    def file_path(self):
        return self._file_path

    @property
    def statinfo(self):
        return self._statinfo

    @property
    def size(self):
        return self._statinfo.st_size

    @property
    def first_time(self):
        return sorted([self.birth_time, self.recent_access_time, self.modification_time, self.c_time])[0] 

    @property
    def birth_time(self):
        try:
            return self._statinfo.st_birthtime
        except AttributeError:
            return self._statinfo.st_ctime

    @property
    def recent_access_time(self):
        return self._statinfo.st_atime

    @property
    def modification_time(self):
        return self._statinfo.st_mtime

    @property
    def c_time(self):
        return self._statinfo.st_ctime

    @property
    def content(self):
        try:
            with open(self._file_path, 'rb') as fp:
                c = fp.read()
        except Exception as e:
            return b''
        else:
            return c

    @property
    def hash(self):
        m = hashlib.sha256(self.content)
        return m.digest()
