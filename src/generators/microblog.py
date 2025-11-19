from typing import Optional

from generators.factory import Factory
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_file_and_convert_to_html
from utils.date import DateFormat


class MicroBlog(Factory):
    def __init__(self, posts: list):
        self.posts = posts

    def write_feed_file(self):
        data = {
            "page_title": "Microblog",
            "all_posts": self.posts,
        }
        template_name = "microblog/feed.j2"
        filename = "microblog/index.html"
        print("#", "-" * 70)
        print(f"Writing microblog feed: {filename}")
        write_file(data=data, template_name=template_name, filename=filename)


class MicroBlogPost(Factory):
    def __init__(
        self,
        file_path: str,
    ):
        self.file_path = file_path
        self.body: Optional[str] = None
        self.content: Optional[str] = None
        self.publish_date: Optional[DateFormat] = None
        self._process_file()

    def _process_file(self):
        data = parse_markdown_file_and_convert_to_html(self.file_path)
        self.body = data.get("body", "")
        self.content = data.get("body")
        self.publish_date = DateFormat(date=data.get("publish_date", "now"))


def process_microblog_data(microblog_path):
    print("#", "-" * 80)
    print("Processing microblog data ...")

    posts = []

    post_files = get_all_files_from_path(microblog_path)
    for post_file in post_files:
        post = MicroBlogPost(file_path=post_file)
        posts.append(post)

    microblog = MicroBlog(posts=posts)

    microblog.write_feed_file()
