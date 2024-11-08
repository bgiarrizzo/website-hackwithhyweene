import shutil

from config import settings
from generators.blog import build_blog
from generators.cname import add_cname_to_build
from generators.homepage import build_homepage
from generators.learn import build_learning
from generators.links import build_links
from generators.pages import build_pages
from generators.resume import build_resume
from utils.collectors import collect_media_files, collect_static_files

if __name__ == "__main__":
    print("#", "-" * 80)
    print("Cleaning build folder ...")
    shutil.rmtree(settings.BUILD_PATH, ignore_errors=True)

    collect_media_files()
    collect_static_files()

    print("#", "-" * 70)
    print("Building site ...")

    blog = build_blog(settings.BLOG_PATH)
    links = build_links(settings.LINKS_PATH)
    pages = build_pages(settings.PAGES_PATH)
    resume = build_resume(settings.RESUME_PATH)

    build_learning(settings.LEARN_PATH)

    build_homepage(blog, links)

    add_cname_to_build(settings.BUILD_PATH, settings.CNAME)
