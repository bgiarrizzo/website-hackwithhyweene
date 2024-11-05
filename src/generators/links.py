from slugify import slugify

from utils.date import add_multiple_date_formats
from utils.file import get_all_files_from_path, write_file
from utils.id import add_id
from utils.markdown import parse_markdown_file_and_convert_to_html
from utils.slug import add_slug


def generate_rss_feed(links: list):
    data = {"links": links}
    template_name = "links/feed_rss.j2"
    filename = "liens/feed.xml"

    write_file(data, template_name, filename)


def generate_link_page(link):
    data = {"page_title": link.get("title"), "link": link}
    template_name = "links/single.j2"
    filename = f"liens/{link.get('slug')}/index.html"

    write_file(data, template_name, filename)

def generate_link_page_list(links):
    data = {"page_title": "Liens", "all_links": links}
    template_name = "links/list.j2"
    filename = "liens/index.html"

    write_file(data, template_name, filename)


def prepare_link_data(link_file):
    link = parse_markdown_file_and_convert_to_html(link_file)
    link = add_multiple_date_formats(link)
    link = add_slug(link)
    link = add_id(link)

    return link


def build_links(links_path):
    links = []

    print("#", "-" * 80)
    print("Generating links ...")

    link_files = get_all_files_from_path(links_path)
    
    for link_file in link_files:
        link = prepare_link_data(link_file)
        generate_link_page(link)

        links.append(link)

    print("Generating RSS feed ...")
    generate_rss_feed(links)

    print("Generating link list ...")
    generate_link_page_list(links)

    return links
