from generators.factory import Factory
from utils.file import write_file


class RobotsTxt(Factory):
    def __init__(self, url):
        self.url = url

    def write_robotstxt(self):
        data = {"url": self.url}
        template_name = "robots.txt.j2"
        filename = "robots.txt"
        print(f"Writing robots.txt: {filename}")
        write_file(data, template_name, filename)


def build_robots_txt(url):
    print("#", "-" * 80)
    print("Generating robots.txt ...")

    RobotsTxt(url=url).write_robotstxt()
