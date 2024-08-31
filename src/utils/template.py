from os import makedirs, path

from jinja2 import Environment, FileSystemLoader

from config import settings


def write_page(filename, content):
    makedirs(path.dirname(f"{settings.BUILD_PATH}/{filename}"), exist_ok=True)

    with open(f"{settings.BUILD_PATH}/{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)


def render_template(template_name, data):
    env = Environment(loader=FileSystemLoader(settings.TEMPLATE_PATH))
    template = env.get_template(template_name)
    return template.render(data)


def prepare_template_data(datalist):
    data = {
        "site": {
            "url": settings.BASE_URL,
            "short_url": settings.SHORT_URL,
            "description": settings.DESCRIPTION,
            "language": settings.LANGUAGE,
            "name": settings.NAME,
            "author": settings.AUTHOR,
            "keywords": settings.KEYWORDS,
        }
    }

    for item in datalist:
        data = data | item

    return data
