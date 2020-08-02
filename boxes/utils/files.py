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
    def birth_time(self):
        return self._statinfo.st_birthtime

    @property
    def content(self):
        with open(self._file_path, 'rb') as fp:
            return fp.read()

    @property
    def hash(self):
        m = hashlib.sha256(self.content)
        return m.digest()

    @property
    def data(self):
        d = datetime.fromtimestamp(self.birth_time).isoformat()
        return {
            "file_path": self._file_path,
            "size": self.size,
            "birth_time": self.birth_time,
            "hash": self.hash,
            "name": self.basename,
            'dateiso': d[:10],
            'time': d[11:],
        }
