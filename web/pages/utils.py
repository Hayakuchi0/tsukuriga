import markdown
import re
from markdown.extensions.toc import TocExtension


def slugify(value, separator):
    return re.sub(r'\s', separator, value).strip().lower()


def markdownify(content):
    return markdown.Markdown(
        tab_length=2,
        extensions=[
            TocExtension(slugify=slugify),
            'pymdownx.magiclink',
            'pymdownx.tilde',
        ],
        extension_configs={
            'pymdownx.magiclink': {
                'hide_protocol': True,
                'social_url_shorthand': True,
                'repo_url_shortener': True,
                'repo_url_shorthand': True,
                'user': 'Compeito',
                'repo': 'tsukuriga'
            },
        }
    ).convert(content)
