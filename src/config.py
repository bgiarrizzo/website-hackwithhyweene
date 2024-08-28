import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SHORT_URL: str = "hack-with-hyweene.com"
    CNAME: str = f"www.{SHORT_URL}"
    BASE_URL: str = f"https://{CNAME}"

    BUILD_PATH: str = "docs"
    MEDIA_PATH: str = "media"
    STATIC_PATH: str = "static"

    BLOG_PATH: str = "blog"
    LEARN_PATH: str = "learn"

    CONTENT_PATH: str = "content"
    TEMPLATE_PATH: str = "src/templates"
    LAYOUT_PATH: str = "src/templates/layouts"
    INCLUDE_PATH: str = "src/templates/layouts/includes"

    NAME: str = "Hack with Hyweene"
    
    DESCRIPTION: str = "Freelance Developer, DevOps, Ethical Hacker"
    KEYWORDS: list = [
        "Bruno",
        "Giarrizzo",
        "Hyweene",
        "Bruno Giarrizzo",
        "Developpeur",
        "DevOps",
        "Git",
        "Apple",
        "Golang",
        "Go",
        "Python",
        "Swift",
        "SwiftUI",
        "Docker",
        "Kubernetes",
        "POO",
        "OOP",
        "Programmation Orientée Objet",
        "Programmation Fonctionnelle",
    ]
    LANGUAGE: str = "fr"

    def get_working_directory(self):
        return os.getcwd()

    class Config:
        # pylint: disable=too-few-public-methods
        case_sensitive = True


settings = Settings()
