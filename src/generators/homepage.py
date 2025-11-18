from generators.factory import Factory
from utils.file import write_file


class Homepage(Factory):
    def __init__(self):
        pass

    def write_homepage(self):
        data = {}
        template_name = "homepage.j2"
        filename = "index.html"
        print(f"Writing homepage: {filename}")
        write_file(data=data, template_name=template_name, filename=filename)


def build_homepage():
    print("#", "-" * 80)
    print("Generating homepage ...")

    homepage = Homepage()
    homepage.write_homepage()
