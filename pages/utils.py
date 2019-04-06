from markdown import markdown


def markdownify(content):
    return markdown(content, tab_length=2)
