import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """ """
    SHORT_URL: str = "hack-with-hyweene.com"
    CNAME: str = f"{SHORT_URL}"
    BASE_URL: str = f"https://www.{SHORT_URL}"

    BUILD_PATH: str = "build"
    MEDIA_PATH: str = "media"
    STATIC_PATH: str = "static"

    TEMPLATE_PATH: str = "templates"

    CONTENT_PATH: str = "content"
    BLOG_PATH: str = f"{ CONTENT_PATH }/blog"
    LINKS_PATH: str = f"{ CONTENT_PATH }/links"
    PAGES_PATH: str = f"{ CONTENT_PATH }/pages"
    RESUME_PATH: str = f"{ CONTENT_PATH }/resume"
    LEARN_PATH: str = f"{ CONTENT_PATH }/learn"

    NAME: str = "Bruno Giarrizzo"
    AUTHOR: str = "Bruno 'Hyweene' Giarrizzo"
    GITHUB_LINK: str = "https://github.com/bgiarrizzo/"
    LINKEDIN_LINK: str = "https://www.linkedin.com/in/bruno-giarrizzo/"

    DESCRIPTION: str = "Developpeur, DevOps, Linuxien, Ethical Hacker"
    KEYWORDS: list = [
        "Bruno",
        "Giarrizzo",
        "Hyweene",
        "Bruno Giarrizzo",
        "Developpeur",
        "Linuxien",
        "DevOps",
        "Ethical Hacker",
    ]
    LANGUAGE: str = "fr-FR"

    def get_working_directory(self):
        """ """
        return os.getcwd()

    class Config:
        """ """
        # pylint: disable=too-few-public-methods
        case_sensitive = True


settings = Settings()
