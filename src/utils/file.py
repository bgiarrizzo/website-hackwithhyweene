from os import path, walk

from utils.html import beautify
from utils.template import prepare_template_data, render_template, write_page


def get_all_files_from_path(target_path, extension=".md") -> list:
    file_list = []
    for root, _, files in walk(target_path):
        for file in sorted(files):
            if file.endswith(extension):
                file_list.append(path.join(root, file))
    return file_list


def write_file(data, template_name, filename, filetype="html5"):
    template_data = prepare_template_data([data])

    final_content = render_template(template_name, template_data)

    beautified_content = beautify(rendered_page=final_content, type=filetype)
    write_page(filename=filename, content=beautified_content)
