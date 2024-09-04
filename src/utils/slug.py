from slugify import slugify


def add_slug(data):

    for item in data:
        if item.get("category"):
            item["category-slug"] = slugify(item.get("category"))
        if item.get("module"):
            item["module-slug"] = slugify(item.get("module"))
        if item.get("title"):
            item["slug"] = slugify(item.get("title"))

    return data
