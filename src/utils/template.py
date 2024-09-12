from datetime import datetime, timedelta
from os import makedirs, path

from jinja2 import Environment, FileSystemLoader

from config import settings


def date_older_than_one_year(date):
    if not date:
        return False
    
    # Convertir les deux dates en naive datetime si elles ne le sont pas déjà
    if date.tzinfo:
        date = date.replace(tzinfo=None)
    
    now = datetime.now()
    
    # Comparer les dates
    return date < now - timedelta(days=180)


def write_page(filename, content):
    makedirs(path.dirname(f"{settings.BUILD_PATH}/{filename}"), exist_ok=True)

    with open(f"{settings.BUILD_PATH}/{filename}", mode="w", encoding="utf-8") as page:
        page.write(content)


def render_template(template_name, data):
    env = Environment(
        loader=FileSystemLoader(settings.TEMPLATE_PATH),
    )
    env.filters["is_outdated"] = date_older_than_one_year
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
