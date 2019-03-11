import os
import tempfile

from django.core.files import File


def get_tempfile(suffix, file=None):
    """
    Windowsではdelete=Falseを指定したtempfileは権限エラーでアクセスできない
    https://stackoverflow.com/questions/23212435/permission-denied-to-write-to-my-temporary-file
    :param str suffix:
    :param File file:
    :return:
    :rtype str
    """
    delete_option = not os.name == 'nt'

    temp_file = tempfile.NamedTemporaryFile(suffix=suffix, delete=delete_option)
    temp_file_path = temp_file.name

    if file is not None:
        with open(temp_file_path, 'wb+') as f:
            for chunk in file.chunks():
                f.write(chunk)

    return temp_file_path
