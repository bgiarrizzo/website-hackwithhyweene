from typing import Optional

from slugify import slugify

from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_file_and_convert_to_html
from utils.date import DateFormat


class Blog:
    def __init__(self, posts: list):
        self.posts = posts

    def write_post_list_file(self):
        data = {"page_title": "Blog", "all_posts": self.posts}
        template_name = "blog/list.j2"
        filename = "blog/index.html"
        print("#", "-" * 70)
        print(f"Writing blog post list: {filename}")
        write_file(data=data, template_name=template_name, filename=filename)

    def write_rss_feed(self):
        data = {"posts": self.posts}
        template_name = "blog/feed.xml"
        filename = "blog/feed.xml"
        print("#", "-" * 70)
        print(f"Writing blog RSS feed: {filename}")
        write_file(
            data=data, template_name=template_name, filename=filename, filetype="xml"
        )


class BlogPost:
    def __init__(
        self,
        file_path: str,
    ):
        self.file_path = file_path
        self.body: Optional[str] = None
        self.category: Optional['BlogPostCategory'] = None
        self.content: Optional[str] = None
        self.publish_date: Optional[DateFormat] = None
        self.slug: Optional[str] = None
        self.summary: Optional[str] = None
        self.tags: list = []
        self.title: Optional[str] = None
        self.update_date: Optional[DateFormat] = None
        self._process_file()

    def _process_file(self):
        data = parse_markdown_file_and_convert_to_html(self.file_path)
        self.title = data.get("title")
        self.body = data.get("body", "")
        category_name = data.get("category", "Uncategorized")
        self.category = BlogPostCategory(name=category_name)
        self.content = data.get("body")
        self.publish_date = DateFormat(date=data.get("publish_date", "now"))
        self.slug = slugify(self.title) if self.title else None
        self.summary = data.get("summary", "")
        self.tags = data.get("tags", [])
        self.update_date = DateFormat(date=data.get("update_date", "now"))

    def write_post_file(self):
        data = {"page_title": f"{self.title} - Blog", "post": self}
        template_name = "blog/single.j2"
        assert self.publish_date is not None
        filename = f"blog/{self.publish_date.short}-{self.slug}/index.html"
        print(f"Writing blog post: {filename}")
        write_file(data=data, template_name=template_name, filename=filename)


class BlogPostCategory:
    def __init__(self, name: str):
        self.name = name
        self.slug = slugify(name)


def process_blog_data(blog_path):
    print("#", "-" * 80)
    print("Processing blog data ...")

    blog_posts = []

    post_files = get_all_files_from_path(blog_path)

    for post_file in post_files:
        post = BlogPost(file_path=post_file)
        post.write_post_file()
        blog_posts.append(post)

    blog = Blog(posts=blog_posts)
    blog.write_post_list_file()
    blog.write_rss_feed()
