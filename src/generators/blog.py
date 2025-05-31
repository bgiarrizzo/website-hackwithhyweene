from utils.date import add_multiple_date_formats
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_file_and_convert_to_html
from utils.slug import add_slug


def generate_rss_feed(posts: list):
    data = {"posts": posts}
    template_name = "blog/feed.xml"
    filename = "blog/feed.xml"

    write_file(data=data, template_name=template_name, filename=filename, filetype="xml")


def generate_blog_post(post):
    data = {"page_title": f"{post.get('title')} - Blog", "post": post}
    template_name = "blog/single.j2"
    filename = f"blog/{post['slug']}/index.html"

    write_file(data=data, template_name=template_name, filename=filename)


def generate_blog_page_list(posts: list):
    data = {"page_title": "Blog", "all_posts": posts}
    template_name = "blog/list.j2"
    filename = "blog/index.html"

    write_file(data=data, template_name=template_name, filename=filename)


def prepare_blog_post_data(blog_post_file):
    blog_post = parse_markdown_file_and_convert_to_html(blog_post_file)
    blog_post = add_multiple_date_formats(blog_post)
    blog_post = add_slug(blog_post)

    return blog_post


def build_blog(blog_path):
    posts = []

    print("#", "-" * 80)
    print("Generating blog ...")

    post_files = get_all_files_from_path(blog_path)

    for post_file in post_files:
        post = prepare_blog_post_data(post_file)
        generate_blog_post(post)

        posts.append(post)

    print("Generating blog page list ...")
    generate_blog_page_list(posts)

    print("Generating RSS feed ...")
    generate_rss_feed(posts)

    return posts
