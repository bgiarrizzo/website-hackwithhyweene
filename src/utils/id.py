from hashlib import md5


def add_id(data):
    for item in data:
        if item.get("slug") and item.get("publish_date"):
            encoded_string = f"{item.get('publish_date')}-{item.get('slug')}".encode()
            item["id"] = md5(encoded_string).hexdigest()[:6]
    return data
