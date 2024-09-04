from utils.date import add_multiple_date_formats
from utils.file import get_all_files_from_path, write_file
from utils.markdown import parse_markdown_files_and_convert_to_html
from utils.slug import add_slug


def generate_rss_feed(posts: list):
    data = {"posts": posts}
    template_name = "blog/feed_rss.j2"
    filename = "blog/feed.xml"

    write_file(data=data, template_name=template_name, filename=filename)


def generate_blog_post(post):
    data = {
        "page_title": f"{post.get("title")} - Blog",
        "post": post
    }
    template_name = "blog/single.j2"
    filename = f"blog/{post['slug']}/index.html"

    write_file(data=data, template_name=template_name, filename=filename)


def generate_blog_page_list(posts: list):
    data = {
        "page_title": "Blog",
        "all_posts": posts
    }
    template_name = "blog/list.j2"
    filename = "blog/index.html"

    write_file(data=data, template_name=template_name, filename=filename)


def prepare_blog_post_data(blog_path):
    blog_post_files = get_all_files_from_path(blog_path)
    blog_posts = parse_markdown_files_and_convert_to_html(blog_post_files)

    posts = add_multiple_date_formats(blog_posts)
    posts = add_slug(posts)

    return posts


def generate_blog(blog_path):
    posts = prepare_blog_post_data(blog_path)

    print("#", "-" * 80)
    print("Generating blog ...")

    print("Generating RSS feed ...")
    generate_rss_feed(posts)

    print("Generating blog page list ...")
    generate_blog_page_list(posts)

    print("Generating blog posts ...")
    for post in posts:
        print(f"Generating blog post: {post.get('slug')}")
        generate_blog_post(post)

    return posts
