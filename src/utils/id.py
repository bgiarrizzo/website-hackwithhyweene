from hashlib import md5


def add_id(data):
    if data.get("slug") and data.get("publish_date"):
        encoded_string = f"{data.get('publish_date')}-{data.get('slug')}".encode()
        data["id"] = md5(encoded_string).hexdigest()[:6]
    return data
