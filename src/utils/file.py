from os import path, walk

from utils.format import beautify_html, beautify_xml
from utils.template import prepare_template_data, render_template, write_page


def get_all_files_from_path(target_path) -> list:
    file_list = []
    for root, dirs, files in walk(target_path):
        for file in sorted(files):
            if file.endswith(".md"):
                file_list.append(path.join(root, file))
    return file_list


def render_and_beautify_html(rendered_page, beautify=True):
    if beautify:
        return beautify_html(rendered_page)
    return rendered_page

def write_file(data, template_name, filename):
    page_template = render_template(template_name, prepare_template_data([data]))

    content = {"content": page_template}

    template_data = prepare_template_data([data, content])

    if "blog_feed_rss" in template_name:
        rendered_page = render_template("blog_feed_rss.j2", template_data)
        content = beautify_xml(rendered_page)
    elif "links_feed_rss" in template_name:
        rendered_page = render_template("links_feed_rss.j2", template_data)
        content = beautify_xml(rendered_page)
    else:
        rendered_page = render_template("main.j2", template_data)
        content = render_and_beautify_html(rendered_page)

    write_page(filename=filename, content=content)
