import requests

from .utils import load_credentials, get_container_and_filename


class ObjectStorageApi:
    def __init__(self):
        self.tenant_id, self.token_id = load_credentials()
        self.endpoint = f'https://object-storage.tyo1.conoha.io/v1/nc_{self.tenant_id}'

    def _request(self, method, name, **kwargs):
        headers = {
            'Accept': 'application/json',
            'X-Auth-Token': self.token_id,
            'X-Container-Read': '.r:*',
        }
        url = f'{self.endpoint}/{name}'
        return requests.request(method, url, headers=headers, **kwargs)

    def get(self, name):
        return self._request('get', name)

    def post(self, name):
        return self._request('post', name)

    def put(self, name, f=None):
        return self._request('put', name, data=f)

    def create(self, name, f=None):
        container, filename = get_container_and_filename(name)
        if not self.exists(container):
            self.put(container)
            self.post(container)
        return self.put(name, f)

    def delete(self, name):
        return self._request('delete', name)

    def get_dir_info(self, name):
        """
        nameに対応するファイルが存在するコンテナの情報か、空白なら全コンテナを返す
        """
        if name == '':
            return self.get('').json()

        container, filename = get_container_and_filename(name)
        return self.get(container).json()

    def get_path_info(self, name):
        """
        nameに対応するファイルもしくはコンテナの情報を返す
        """
        container, filename = get_container_and_filename(name)

        if filename:
            response = self.get(container)
            target = filename
        else:
            response = self.get('')
            target = container

        try:
            response_json = response.json()
        except:
            return None

        for obj in response_json:
            if obj['name'] == target:
                return obj

    def exists(self, name):
        return self.get_path_info(name) is not None

    def info(self, name, k):
        return self.get_path_info(name)[k]
