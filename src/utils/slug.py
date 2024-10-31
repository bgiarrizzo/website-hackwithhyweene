from slugify import slugify


def add_slug(data):
    if data.get("category"):
        data["category-slug"] = slugify(data.get("category"))
    if data.get("module"):
        data["module-slug"] = slugify(data.get("module"))
    if data.get("title"):
        data["slug"] = slugify(data.get("title"))

    return data
