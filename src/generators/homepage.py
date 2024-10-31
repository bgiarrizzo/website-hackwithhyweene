from generators.blog import prepare_blog_post_data
from generators.links import prepare_link_data
from utils.file import write_file


def write_homepage(posts, links):
    data = {"posts": posts, "links": links}
    template_name = "homepage.j2"
    filename = "index.html"

    write_file(data=data, template_name=template_name, filename=filename)


def get_blog_posts_links_data(blog_path, links_path):
    posts = prepare_blog_post_data(blog_path)
    links = prepare_link_data(links_path)

    return posts, links


def build_homepage(posts, links):
    
    print("#", "-" * 80)
    print("Generating homepage ...")

    write_homepage(posts, links)

    # write_homepage()
