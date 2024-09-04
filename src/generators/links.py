from slugify import slugify

from utils.date import add_multiple_date_formats
from utils.file import get_all_files_from_path, write_file
from utils.id import add_id
from utils.markdown import parse_markdown_files_and_convert_to_html
from utils.slug import add_slug


def generate_rss_feed(links: list):
    data = {"links": links}
    template_name = "links_feed_rss.j2"
    filename = "liens/feed.xml"

    write_file(data, template_name, filename)


def generate_link_page_list(links):
    data = {"all_links": links}
    template_name = "links_list.j2"
    filename = "liens/index.html"

    write_file(data, template_name, filename)


def prepare_link_data(links_path):
    link_files = get_all_files_from_path(links_path)
    links = parse_markdown_files_and_convert_to_html(link_files)

    links = add_multiple_date_formats(links)
    links = add_slug(links)
    links = add_id(links)

    return links


def generate_links(links_path):
    links = prepare_link_data(links_path)

    print("#", "-" * 80)
    print("Generating links ...")

    print("Generating RSS feed ...")
    generate_rss_feed(links)

    print("Generating link list ...")
    generate_link_page_list(links)

    return links
