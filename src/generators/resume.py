from typing import List
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_file_and_convert_to_html


class Resume:
    def __init__(
        self,
        head: "ResumeHead",
        experiences: List["ResumeExperience"],
        educations: List["ResumeEducation"],
        skills: List["ResumeSkill"],
    ):
        self.head = head
        self.experiences = experiences
        self.educations = educations
        self.skills = skills

        self.tags: List[str] = [
            tag for experience in experiences for tag in experience.tags
        ]

    def write_resume_file(self):
        data = {
            "page_title": "Bruno Giarrizzo - CV",
            "resume": self,
        }
        template_name = "resume/main.j2"
        filename = "cv/index.html"
        print("#", "-" * 70)
        print(f"Writing resume : {filename}")
        write_file(data=data, template_name=template_name, filename=filename)


class ResumeHead:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._process_file(file_path)

    def _process_file(self, file_path: str):
        data = parse_markdown_file_and_convert_to_html(file_path)
        self.body = data.get("body")


class ResumeSkill:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._process_file(file_path)

    def _process_file(self, file_path: str):
        data = parse_markdown_file_and_convert_to_html(file_path)
        self.body = data.get("body")


class ResumeExperience:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._process_file(file_path)

    def _process_file(self, file_path: str):
        data = parse_markdown_file_and_convert_to_html(file_path)
        self.id = data.get("id")
        self.title = data.get("title")
        self.company = data.get("company")
        self.company_url = data.get("company_url")
        self.location = data.get("location", "")
        self.start_date = data.get("start_date")
        self.end_date = data.get("end_date")
        self.contract_type = data.get("contract_type")
        self.tags = data.get("tags", [])
        self.body = data.get("body")


class ResumeEducation:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._process_file(file_path)

    def _process_file(self, file_path: str):
        data = parse_markdown_file_and_convert_to_html(file_path)
        self.id = data.get("id")
        self.title = data.get("title")
        self.school = data.get("school")
        self.location = data.get("location", "")
        self.start_date = data.get("start_date")
        self.end_date = data.get("end_date")
        self.formation_type = data.get("formation_type")
        self.status = data.get("status")
        self.body = data.get("body")


def process_resume_data(resume_path):
    experiences = []
    educations = []
    skills = []
    head = ResumeHead(f"{resume_path}/head/head.md")

    experience_files = get_all_files_from_path(f"{resume_path}/experiences")
    for experience_file in experience_files:
        experience = ResumeExperience(experience_file)
        experiences.append(experience)

    education_files = get_all_files_from_path(f"{resume_path}/educations")
    for education_file in education_files:
        education = ResumeEducation(education_file)
        educations.append(education)

    skill_files = get_all_files_from_path(f"{resume_path}/skills")
    for skill_file in skill_files:
        skill = ResumeSkill(skill_file)
        skills.append(skill)

    resume = Resume(
        head=head,
        experiences=experiences,
        educations=educations,
        skills=[],  # skills
    )

    resume.write_resume_file()
