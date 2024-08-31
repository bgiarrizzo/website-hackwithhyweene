from pydantic import BaseModel


class BlogLink(BaseModel):
    title: str
    url: str
    publish_date: str
    update_date: str
    body: str
