def add_multiple_date_formats(data):
    publish_update_keys = ["publish_date", "update_date"]

    for item in data:
        for key in publish_update_keys:
            if item.get(key):
                item[f"{key}_condensed"] = item.get(key).strftime("%Y%m%d")
                item[f"{key}_short"] = item.get(key).strftime("%d-%b-%Y")
                item[f"{key}_medium"] = item.get(key).strftime("%d %b %Y")
                item[f"{key}_long"] = item.get(key).strftime("%A, %d %B %Y")
                item[f"{key}_full"] = item.get(key).strftime("%A, %d %B %Y %I:%M %p")

                item[f"{key}_year"] = item.get(key).year
                item[f"{key}_month"] = item.get(key).strftime("%B")
                item[f"{key}_month_short"] = item.get(key).strftime("%m")
                item[f"{key}_day"] = item.get(key).day

                item[f"{key}_iso"] = item.get(key).isoformat()
                item[f"{key}_rfc"] = item.get(key).strftime("%a, %d %b %Y %H:%M:%S %z")

    return data
