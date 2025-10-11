from datetime import datetime

class DateFormat:
    def __init__(self, date):
        # Si la date est None, on prend la date actuelle
        if date is None:
            self.original = datetime.now()
        elif isinstance(date, datetime):
            self.original = date
        elif isinstance(date, str):
            if date.lower() == "now":
                self.original = datetime.now()
            else:
                # Suppose la chaîne est en format ISO 8601 valide
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
