class WebSite:
    def __init__(self, name, domain):
        self.name = name
        self.domain = domain

    def get_info(self):
        return f"Website Name: {self.name}, Domain: {self.domain}"
