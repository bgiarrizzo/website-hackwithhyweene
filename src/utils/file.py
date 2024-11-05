from os import path, walk

from utils.html import beautify
from utils.template import prepare_template_data, render_template, write_page


def get_all_files_from_path(target_path, extension=".md") -> list:
    file_list = []
    for root, dirs, files in walk(target_path):
        for file in sorted(files):
            if file.endswith(extension):
                file_list.append(path.join(root, file))
    return file_list


def write_file(data, template_name, filename):
    page_template = render_template(template_name, prepare_template_data([data]))
    content = {"content": page_template}
    template_data = prepare_template_data([data, content])

    if "blog_feed_rss" in template_name:
        content = beautify(
            rendered_page=render_template("blog_feed_rss.j2", template_data), type="xml"
        )
    elif "links_feed_rss" in template_name:
        content = beautify(
            rendered_page=render_template("links_feed_rss.j2", template_data),
            type="xml",
        )
    else:
        content = beautify(
            rendered_page=render_template("main.j2", template_data), type="html5"
        )

    write_page(filename=filename, content=content)
