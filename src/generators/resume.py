from config import settings
from utils.file import get_all_files_from_path, write_file
from utils.format import beautify_html
from utils.markdown import parse_markdown_files_and_convert_to_html


def write_resume(resume):
    data = {
        "page_title": "Bruno Giarrizzo - CV",
        "resume": resume
    }
    template_name = "resume/main.j2"
    filename = "cv/index.html"

    write_file(data, template_name, filename)


def generate_resume_head(dataset: list, data: dict):
    for head in dataset:
        if head.get("tags"):
            for tag in head.get("tags"):
                if tag not in data.get("resume").get("tags"):
                    data.get("resume").get("tags").append(tag)

    data["head"] = dataset[0].get("body")

    return data


def generate_resume_experience(
    dataset: list,
    data: dict,
):
    for experience in dataset:
        if experience.get("tags"):
            for tag in experience.get("tags"):
                if tag not in data.get("resume"):
                    data.get("resume").get("tags").append(tag)

    data["experiences"] = dataset

    return data


def generate_resume_education(dataset: list, data: dict):
    for education in dataset:
        if education.get("tags"):
            for tag in education.get("tags"):
                if tag not in data.get("resume").get("tags"):
                    data.get("resume").get("tags").append(tag)

    data["educations"] = dataset

    return data


def prepare_resume_data(resume_path):
    head_files = get_all_files_from_path(f"{resume_path}/head")
    experiences_files = get_all_files_from_path(f"{resume_path}/experiences")
    educations_files = get_all_files_from_path(f"{resume_path}/educations")

    head = parse_markdown_files_and_convert_to_html(head_files)
    experiences = parse_markdown_files_and_convert_to_html(experiences_files)
    educations = parse_markdown_files_and_convert_to_html(educations_files)

    return head, experiences, educations


def generate_resume(resume_path):
    print("Generating resume ...")

    head, experiences, educations = prepare_resume_data(resume_path)

    resume = {
        "resume": {
            "tags": [],
        }
    }

    print("Generating header ...")
    resume |= generate_resume_head(dataset=head, data=resume)

    print("Generating education part ...")
    resume |= generate_resume_education(dataset=educations, data=resume)

    print("Generating experience part ...")
    resume |= generate_resume_experience(dataset=experiences, data=resume)

    write_resume(resume)
