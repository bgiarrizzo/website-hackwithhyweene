from slugify import slugify


def add_slug(data):

    for item in data:
        if item.get("title"):
            item["slug"] = slugify(item.get("title"))

    return data
