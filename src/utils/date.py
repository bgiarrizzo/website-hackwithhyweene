def add_multiple_date_formats(data):

    for item in data:
        if item.get("publish_date"):
            item["publish_date_condensed"] = item.get("publish_date").strftime("%Y%m%d")
            item["publish_date_short"] = item.get("publish_date").strftime("%d-%b-%Y")
            item["publish_date_medium"] = item.get("publish_date").strftime("%d %b %Y")
            item["publish_date_long"] = item.get("publish_date").strftime(
                "%A, %d %B %Y"
            )
            item["publish_date_full"] = item.get("publish_date").strftime(
                "%A, %d %B %Y %I:%M %p"
            )

            item["publish_date_year"] = item.get("publish_date").year
            item["publish_date_month"] = item.get("publish_date").strftime("%B")
            item["publish_date_month_short"] = item.get("publish_date").strftime("%m")
            item["publish_date_day"] = item.get("publish_date").day

            item["publish_date_iso"] = item.get("publish_date").isoformat()
            item["publish_date_rfc"] = item.get("publish_date").strftime(
                "%a, %d %b %Y %H:%M:%S %z"
            )

    return data
