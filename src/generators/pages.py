from config import settings
from utils.date import add_multiple_date_formats
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_files_and_convert_to_html
from utils.slug import add_slug


def generate_page(page):
    template_name = "page/main.j2"
    data = {
        "page_title": page.get("title"),
        "page": page
    }
    filename = f"{page['permalink']}/index.html"

    write_file(data, template_name, filename)


def generate_pages(pages_path):
    page_file_list = get_all_files_from_path(pages_path)
    pages = parse_markdown_files_and_convert_to_html(page_file_list)

    pages = add_multiple_date_formats(pages)
    pages = add_slug(pages)

    print("#", "-" * 80)
    print("Generating pages ...")

    for page in pages:
        if len(page.get("permalink")) == 0:
            print(f"Generating page with empty permalink: {page.get('title')} ...")
        else:
            print(f"Generating page: {page['slug']} ...")

        generate_page(page=page)
