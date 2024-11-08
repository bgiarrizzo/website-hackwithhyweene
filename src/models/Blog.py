from typing import List


class BlogPost:
    id: str
    title: str
    slug: str
    tags: List[str]
    category: str
    cover: str
    cover_alt: str
    publish_date: str
    updated_date: str
    summary: str
    content: str

    template_name: str = "blog/single.j2"
    filename: str = f"blog/{slug}/index.html"
    page_title: str = f"{title} - Blog"


class BlogPostList:
    title: str = "Blog"

    posts: List[BlogPost] = []

    template_name: str = "blog/list.j2"
    file_name: str = "blog/index.html"


class Blog:
    posts: BlogPostList = BlogPostList()
