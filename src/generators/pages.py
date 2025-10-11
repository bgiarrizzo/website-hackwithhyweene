from typing import Optional

from slugify import slugify

from config import settings
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_file_and_convert_to_html


class Page:
    def __init__(
        self,
        file_path: str,
    ):
        self.file_path = file_path
        self.title: Optional[str] = None
        self.body: Optional[str] = None
        self.permalink: Optional[str] = None
        self.slug: Optional[str] = None
        self.summary: Optional[str] = None
        self.cover: Optional[str] = None
        self._process_file(file_path)

    def _process_file(self, file_path: str):
        data = parse_markdown_file_and_convert_to_html(file_path)
        self.title = data.get("title")
        self.body = data.get("body", "")
        self.permalink = data.get("permalink", "")
        self.slug = slugify(self.title) if self.title else None
        self.summary = data.get("summary", "")
        self.cover = data.get("cover", "")

    def write_page(self):
        template_name = "page/main.j2"
        data = {"page_title": self.title, "page": self}
        filename = f"{self.permalink}/index.html"

        if self.permalink == "":
            filename = "index.html"
            print(f"Writing page with empty permalink: {self.title}")
        else:
            print(f"Writing page: {self.slug} ...")

        write_file(data=data, template_name=template_name, filename=filename)


def process_pages_data(pages_path, website_data=None):
    print("#", "-" * 80)
    print("Generating pages ...")

    page_files = get_all_files_from_path(pages_path)

    for page_file in page_files:
        page = Page(file_path=page_file)
        page.write_page()
