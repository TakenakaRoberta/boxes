import os


class FileInfo:

    def __init__(self, file_info):
        self._file_path = file_path
        self._statinfo = os.stat(file_path)

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


