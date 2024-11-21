from collections import defaultdict

from utils.date import add_multiple_date_formats
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_file_and_convert_to_html
from utils.slug import add_slug, slugify
from utils.yaml import parse_yaml


def generate_module_page(module_slug, page):
    template_name = "learn/page.j2"
    data = {
        "learn": page,
    }
    filename = f"apprendre/{module_slug}/{page.get('slug')}/index.html"

    write_file(data, template_name, filename)


def generate_learning_module_pages(module_data):
    for module_page in module_data.get("module_pages"):
        module_page["module"] = {
            "name": module_data.get("module_name"),
            "slug": module_data.get("module_slug"),
        }
        print(f"Generating module page: {module_page.get('title')} ...")
        generate_module_page(module_data.get("module_slug"), module_page)


def generate_module_table_of_contents(module_data):
    template_name = "learn/module_toc.j2"

    data = {
        "module": {
            "name": module_data.get("module_name"),
            "slug": module_data.get("module_slug"),
            "description": module_data.get("module_description"),
        },
        "pages": module_data.get("module_pages"),
    }

    filename = f"apprendre/{module_data.get('module_slug')}/index.html"

    write_file(data, template_name, filename)


def generate_table_of_contents(table_of_contents):
    template_name = "learn/global_toc.j2"
    data = {
        "page_title": "Table des matières - Apprendre",
        "table_of_contents": table_of_contents,
    }
    filename = "apprendre/index.html"

    write_file(data, template_name, filename)


def prepare_learn_data(learning_path):
    modules = []

    for module_file in get_all_files_from_path(learning_path, extension=".yml"):
        module = parse_yaml(module_file)

        if module.get("disabled"):
            continue

        module["module_slug"] = slugify(module["module_name"])
        module["module_path"] = "/".join(module_file.split("/")[:-1])
        module["module_pages"] = []

        module_page_list = get_all_files_from_path(module["module_path"])

        for module_page in module_page_list:
            module_page = parse_markdown_file_and_convert_to_html(module_page)
            module_page = add_multiple_date_formats(module_page)
            module_page = add_slug(module_page)

            module["module_pages"].append(module_page)

        modules.append(module)

    return modules


def build_learning(learning_path):
    print("#", "-" * 80)
    print("Generating learning ...")

    modules = prepare_learn_data(learning_path)

    print("Generating global table of contents ...")
    generate_table_of_contents(modules)

    for module in modules:
        module_name = module.get("module_name")
        print("#", "-" * 40)
        print(f"Generating module: {module_name} ...")

        generate_module_table_of_contents(module)

        generate_learning_module_pages(module)
