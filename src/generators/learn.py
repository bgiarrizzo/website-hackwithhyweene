from typing import Optional

from slugify import slugify

from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_file_and_convert_to_html
from utils.yaml import parse_yaml
from utils.date import DateFormat


class Learn:
    def __init__(self, modules: list):
        self.modules = modules

    def write_modules_list_file(self):
        data = {
            "page_title": "Table des matières - Apprendre",
            "table_of_contents": self.modules,
        }
        template_name = "learn/list.j2"
        filename = "apprendre/index.html"
        print("#", "-" * 70)
        print(f"Writing modules list : {filename}")
        write_file(data=data, template_name=template_name, filename=filename)

    def write_sitemap_xml_file(self):
        data = {
            "modules": self.modules,
        }
        template_name = "learn/sitemap.xml"
        filename = "apprendre/sitemap.xml"
        print("#", "-" * 70)
        print(f"Writing sitemap XML : {filename}")
        write_file(data=data, template_name=template_name, filename=filename)


class LearnModule:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.pages: list = []
        self._process_file()

    def _process_file(self):
        data = parse_yaml(self.file_path)
        self.id = data.get("id")
        self.name = data.get("name")
        self.slug = slugify(self.name)
        self.logo = data.get("logo")
        self.description = data.get("description")
        self.disabled = data.get("disabled", False)
        self.module_path = "/".join(self.file_path.split("/")[:-1])

    def write_table_of_contents_file(self):
        template_name = "learn/toc.j2"
        data = {
            "module": self,
        }
        filename = f"apprendre/{self.slug}/index.html"
        print("#", "-" * 70)
        print(f"Writing learning module table of contents: {filename}")
        write_file(data=data, template_name=template_name, filename=filename)
        print("#", "-" * 70)


class LearnModulePage:
    def __init__(self, file_path: str, module: LearnModule):
        self.file_path = file_path
        self.module = module
        self.id: Optional[int] = None
        self.title: Optional[str] = None
        self.slug: Optional[str] = None
        self.summary: Optional[str] = None
        self.publish_date: Optional[DateFormat] = None
        self.update_date: Optional[DateFormat] = None
        self.toc: Optional[str] = None
        self.body: Optional[str] = None
        self.prism_needed: bool = False
        self._process_file()

    def _process_file(self):
        data = parse_markdown_file_and_convert_to_html(self.file_path)
        self.id = data.get("id")
        self.title = data.get("title")
        self.slug = slugify(self.title) if self.title else None
        self.summary = data.get("summary", "")
        self.publish_date = DateFormat(date=data.get("publish_date", "now"))
        update_date = (
            data.get("update_date")
            if data.get("update_date")
            else data.get("publish_date", "now")
        )
        self.update_date = DateFormat(date=update_date)
        self.toc = data.get("toc_html", "")
        self.body = data.get("body", "")
        self.prism_needed = data.get("prism_needed", False)

    def write_module_page(self):
        template_name = "learn/page.j2"
        data = {
            "learn": self,
        }
        filename = f"apprendre/{self.module.slug}/{self.slug}/index.html"

        print(f"Writing learning module page: {filename}")
        write_file(data=data, template_name=template_name, filename=filename)


def process_learn_data(learning_path):
    modules = []

    for module_file in get_all_files_from_path(learning_path, extension=".yml"):
        modules_pages = []

        module = LearnModule(module_file)

        if module.disabled:
            continue

        module_page_list = get_all_files_from_path(module.module_path)

        for module_page_item in module_page_list:
            module_page = LearnModulePage(module_page_item, module)
            module_page.write_module_page()

            modules_pages.append(module_page)

        module.pages = modules_pages
        module.write_table_of_contents_file()

        modules.append(module)

    learn = Learn(modules)
    learn.write_modules_list_file()
    learn.write_sitemap_xml_file()
