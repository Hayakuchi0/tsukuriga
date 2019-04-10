import markdown


def markdownify(content):
    return markdown.Markdown(
        tab_length=2,
        extensions=[
            'toc',
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
