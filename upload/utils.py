import os
import tempfile

import requests


def get_tempfile(suffix, file=None):
    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=False)
    temp_file_path = temp_file.name

    if file is not None:
        with open(temp_file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

    return temp_file_path


class RequestFile:
    def __init__(self, url, suffix=None):
        self.url = url
        if suffix is None:
            suffix = os.path.splitext(url)[-1]
        self.path = get_tempfile(suffix)

    def open(self, mode='rb'):
        return open(self.path, mode=mode)

    def _download_file(self, url):
        response = requests.get(url)
        with open(self.path, 'wb') as f:
            f.write(response.content)

    def download_file(self):
        self._download_file(self.url)
