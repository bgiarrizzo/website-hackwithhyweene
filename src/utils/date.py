from datetime import datetime, timedelta

class DateFormat:
    def __init__(self, date):
        # If date is None, use current date
        if date is None:
            self.original = datetime.now()
        elif isinstance(date, datetime):
            self.original = date
        elif isinstance(date, str):
            if date.lower() == "now":
                self.original = datetime.now()
            else:
                # Assume string is in valid ISO 8601 format
                self.original = datetime.fromisoformat(date)
        else:
            raise TypeError("date must be str, datetime, or None")

        self.rfc3339 = self.original.strftime("%Y-%m-%dT%H:%M:%SZ")
        self.condensed = self.original.strftime("%Y%m%d")
        self.short = self.original.strftime("%Y-%m-%d")
        self.medium = self.original.strftime("%d %b %Y")
        self.long = self.original.strftime("%d %B %Y")
        self.year = self.original.year
        self.month = self.original.strftime("%m-%B")

        self.tzinfo = self.original.tzinfo

    def replace(self, tzinfo):
        new_date = self.original.replace(tzinfo=tzinfo)
        return DateFormat(new_date)


def date_older_than_six_months(date):
    if not date:
        return False

    if date.tzinfo is None:
        date = date.replace(tzinfo=None)

    now = datetime.now(tz=date.tzinfo)
    return date.original < now - timedelta(days=180)
