from pydantic import BaseModel

class BlogPage(BaseModel):
    title: str
    meta_title: str
    permalink: str
