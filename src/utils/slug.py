from slugify import slugify as third_party_slugify


def slugify(text):
    return third_party_slugify(text)


def add_slug(data):
    if data.get("category"):
        data["category-slug"] = third_party_slugify(data.get("category"))
    if data.get("module_name"):
        data["module-slug"] = third_party_slugify(data.get("module_name"))
    if data.get("title"):
        data["slug"] = third_party_slugify(data.get("title"))

    return data
