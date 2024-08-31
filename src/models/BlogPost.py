from pydantic import BaseModel


class BlogPost(BaseModel):
    title: str
    summary: str
    cover: str
    cover_alt: str
    publish_date: str
    update_date: str
    tags: list[str]
    body: str
