import uuid

import django
from django.core.files import File
from django.test import TestCase
import requests
from requests.exceptions import HTTPError

from conoha.storage.backend import ConohaObjectStorage

django.setup()


class ConohaObjectStorageTests(TestCase):

    def setUp(self):
        self.storage = ConohaObjectStorage()
        self.storage.api.put('__test')
        self.storage.api.post('__test')

    @staticmethod
    def _get_filename():
        return f'__test/{uuid.uuid4().hex}.txt'

    def test_save_and_delete(self):
        filename = self._get_filename()
        content = open('tests/test.txt')

        self.storage.save(filename, File(content.buffer))
        print('create: ' + filename)

        self.storage.delete(filename)
        print('delete: ' + filename)

        content.close()

    def test_save_to_not_found_directory(self):
        filename = f'not-found-directory/new.txt'
        content = open('tests/test.txt')
        self.assertRaises(
            HTTPError,
            lambda: self.storage._save(filename, File(content.buffer))
        )
        content.close()

    def test_url(self):
        filename = self._get_filename()
        content = open('tests/test.txt')

        self.storage._save(filename, File(content.buffer))
        url = self.storage.url(filename)
        print('url: ' + url)

        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

        self.storage.delete(filename)
        print('delete: ' + url)

        content.close()

    def test_size(self):
        filename = self._get_filename()
        content = open('tests/test.txt')

        self.storage._save(filename, File(content.buffer))
        print('create :' + filename)

        expect = 10
        actual = self.storage.size(filename)
        self.assertEqual(expect, actual)

        self.storage.delete(filename)
        print('delete :' + filename)

        content.close()
