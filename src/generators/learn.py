from collections import defaultdict

from utils.date import add_multiple_date_formats
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_files_and_convert_to_html
from utils.slug import add_slug


def create_path(*args):
    return "/".join(args)


def generate_module_page(page):
    template_name = "learn/page.j2"
    data = {
        "learn": page,
        "page_title": f"{page.get('title')} - {page.get('module')} - Apprendre",
    }
    filename = f"apprendre/{page.get('path')}/index.html"

    write_file(data, template_name, filename)


def generate_learning_module_pages(module_data):
    for module_page in module_data.get("pages"):
        generate_module_page(module_page)


def generate_module_table_of_contents(module_data):
    template_name = "learn/module_toc.j2"

    data = {
        "page_title": f"Table des matières - {module_data.get('name')} - Apprendre",
        "module": {
            "name": module_data.get("name"),
        },
        "pages": module_data.get("pages"),
    }

    filename = f"apprendre/{module_data.get('path')}/index.html"

    write_file(data, template_name, filename)


def prepare_learn_data(module_path):
    module_file_list = get_all_files_from_path(module_path)
    module_pages = parse_markdown_files_and_convert_to_html(module_file_list)

    module_pages = add_multiple_date_formats(module_pages)
    module_pages = add_slug(module_pages)

    categories = defaultdict(
        lambda: {"path": "", "slug": "", "modules": defaultdict(lambda: {"pages": []})}
    )

    for module_page in module_pages:
        if module_page.get("disabled"):
            continue
        
        category_id = module_page.get("category_id")
        category_name = module_page.get("category")
        category_slug = module_page.get("category-slug")

        module_id = module_page.get("module_id")
        module_name = module_page.get("module")
        module_slug = module_page.get("module-slug")
        module_description = module_page.get("module_description")

        # Mise à jour de la catégorie
        if not categories[category_name]["path"]:
            categories[category_name].update(
                {
                    "id": category_id,
                    "path": create_path(category_slug),
                    "slug": category_slug,
                }
            )

        # Mise à jour du module
        module = categories[category_name]["modules"][module_name]
        if not module.get("path"):
            module.update(
                {
                    "id": module_id,
                    "name": module_name,
                    "description": module_description,
                    "logo": module_page.get("module_logo"),
                    "path": create_path(category_slug, module_slug),
                    "slug": module_slug,
                }
            )

        page = {k: v for k, v in module_page.items()}
        page["path"] = create_path(category_slug, module_slug, module_page.get("slug"))

        module["pages"].append(page)

    # Conversion en liste de dictionnaires
    result = []
    for category_name, category_data in categories.items():
        category = {
            "id": category_data["id"],
            "name": category_name,
            "path": category_data["path"],
            "slug": category_data["slug"],
            "modules": list(category_data["modules"].values()),
        }
        result.append(category)

    return {"categories": result}


def generate_table_of_contents(table_of_contents):
    template_name = "learn/global_toc.j2"
    data = {
        "page_title": "Table des matières - Apprendre",
        "table_of_contents": table_of_contents.get("categories"),
    }
    filename = "apprendre/index.html"

    write_file(data, template_name, filename)


def generate_learning(learning_path):
    print("#", "-" * 80)
    print("Generating learning ...")

    learn_data = prepare_learn_data(learning_path)

    print("Generating global table of contents ...")
    generate_table_of_contents(learn_data)

    for category in learn_data.get("categories"):
        category_name = category.get("name")
        print(f"Generating category: {category_name} ...")

        for module in category.get("modules"):
            module_name = module.get("name")
            print(f"Generating module: {module_name} ...")

            generate_module_table_of_contents(module)

            generate_learning_module_pages(module)
