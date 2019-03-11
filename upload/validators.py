# https://gist.github.com/jrosebr1/2140738

import os
import mimetypes

from moviepy.editor import VideoFileClip

from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

from .utils import get_tempfile


class FileValidator:
    """
    Validator for files, checking the size, extension and mimetype.

    Initialization parameters:
        allowed_extensions: iterable with allowed file extensions
            ie. ('txt', 'doc')
        allowd_mimetypes: iterable with allowed mimetypes
            ie. ('image/png', )
        min_size: minimum number of bytes allowed
            ie. 100
        max_size: maximum number of bytes allowed
            ie. 24*1024*1024 for 24 MB

    Usage example::

        MyModel(models.Model):
            myfile = FileField(validators=[FileValidator(max_size=24*1024*1024), ...])

    """

    extension_message = "'%(extension)s'は許可されていない拡張子です。 許可されている拡張子: '%(allowed_extensions)s.'"
    mime_message = "'%(mimetype)s'は許可されていないファイル形式です。 許可されているファイル形式: %(allowed_mimetypes)s."
    min_size_message = 'ファイルサイズが小さすぎます(%(size)s). 最小サイズは%(allowed_size)sです。'
    max_size_message = 'ファイルサイズが大きすぎます(%(size)s), 最大サイズは%(allowed_size)sです。'

    def __init__(self, *args, **kwargs):
        self.allowed_extensions = kwargs.pop('allowed_extensions', None)
        self.allowed_mimetypes = kwargs.pop('allowed_mimetypes', None)
        self.min_size = kwargs.pop('min_size', 0)
        self.max_size = kwargs.pop('max_size', None)

    def __call__(self, value):
        """
        Check the extension, content type and file size.
        """

        # Check the extension
        ext = os.path.splitext(value.name)[1][1:].lower()
        if self.allowed_extensions and ext not in self.allowed_extensions:
            message = self.extension_message % {
                'extension': ext,
                'allowed_extensions': ', '.join(self.allowed_extensions)
            }

            raise ValidationError(message)

        # Check the content type
        mimetype = mimetypes.guess_type(value.name)[0]
        if self.allowed_mimetypes and mimetype not in self.allowed_mimetypes:
            message = self.mime_message % {
                'mimetype': mimetype,
                'allowed_mimetypes': ', '.join(self.allowed_mimetypes)
            }

            raise ValidationError(message)

        # Check the file size
        filesize = len(value)
        if self.max_size and filesize > self.max_size:
            message = self.max_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.max_size)
            }

            raise ValidationError(message)

        elif filesize < self.min_size:
            message = self.min_size_message % {
                'size': filesizeformat(filesize),
                'allowed_size': filesizeformat(self.min_size)
            }

            raise ValidationError(message)


def video_file_validator(file):
    temp_file_path = get_tempfile('.mp4', file)

    try:
        clip = VideoFileClip(temp_file_path)
        clip.close()
    except:
        raise ValidationError('ファイル形式が不正です。動画ファイルとして読み込むことが出来ませんでした')
