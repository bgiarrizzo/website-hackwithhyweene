def add_multiple_date_formats(data):
    date_keys = ["publish_date", "update_date"]

    for key in date_keys:
        if data.get(key):
            data[f"{key}_condensed"] = data.get(key).strftime("%Y%m%d")
            data[f"{key}_short"] = data.get(key).strftime("%d-%b-%Y")
            data[f"{key}_medium"] = data.get(key).strftime("%d %b %Y")
            data[f"{key}_long"] = data.get(key).strftime("%A, %d %B %Y")
            data[f"{key}_full"] = data.get(key).strftime("%A, %d %B %Y %I:%M %p")

            data[f"{key}_year"] = data.get(key).year
            data[f"{key}_month"] = data.get(key).strftime("%m-%B")
            data[f"{key}_month_short"] = data.get(key).strftime("%m")
            data[f"{key}_day"] = data.get(key).day

            data[f"{key}_iso"] = data.get(key).isoformat()
            data[f"{key}_rfc"] = data.get(key).strftime("%a, %d %b %Y %H:%M:%S %z")

    return data
