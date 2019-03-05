import io

from django.core.files import File
from django.core.files.storage import Storage

from .utils import is_container, clean_name
from .api import ObjectStorageApi


class ConohaObjectStorage(Storage):
    def __init__(self):
        self.api = ObjectStorageApi()

    def _open(self, name, mode='rb'):
        response = self.api.get(name)
        response.raise_for_status()
        return File(io.BytesIO(response.content))

    def _save(self, name, content):
        response = self.api.put(name, content)
        response.raise_for_status()
        return name

    def delete(self, name):
        self.api.delete(name)

    def exists(self, name):
        return self.api.exists(name)

    def listdir(self, path):
        """
        コンテナをディレクトリ、コンテナ以下は全てファイルとして扱う
        """
        data = self.api.get_dir_info(path)
        result = [obj['name'] for obj in data]
        if path == '':
            return result, []
        elif is_container(path):
            return [], result
        return [], []

    def size(self, name):
        return self.api.info(name, 'bytes')

    def url(self, name):
        return self.api.endpoint + '/' + name

    def get_modified_time(self, name):
        return self.api.info(name, 'last_modified')

    def generate_filename(self, filename):
        return clean_name(filename)
