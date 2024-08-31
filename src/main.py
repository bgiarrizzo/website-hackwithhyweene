import shutil

from config import settings
from generators.blog import generate_blog
from generators.cname import add_cname_to_build
from generators.homepage import generate_homepage
from generators.links import generate_links
from generators.pages import generate_pages
from generators.resume import generate_resume
from generators.learning import generate_learning
from utils.collection import collect_media_files, collect_static_files

if __name__ == "__main__":
    print("#", "-" * 80)
    print("Cleaning build folder ...")
    shutil.rmtree(settings.BUILD_PATH, ignore_errors=True)

    collect_media_files()
    collect_static_files()

    print("#", "-" * 80)
    print("Building site ...")

    generate_blog(settings.BLOG_PATH)
    generate_links(settings.LINKS_PATH)
    generate_pages(settings.PAGES_PATH)
    generate_resume(settings.RESUME_PATH)

    generate_learning(settings.LEARN_PATH)

    generate_homepage(settings.BLOG_PATH, settings.LINKS_PATH)

    add_cname_to_build(settings.BUILD_PATH, settings.CNAME)
