from generators.factory import Factory
from utils.file import write_file


class SitemapXML(Factory):
    def __init__(self, url):
        self.url = url

    def write_sitemap_index_xml(self):
        data = {"url": self.url, "sitemaps": ["blog", "liens", "apprendre"]}
        template_name = "sitemap-index.xml.j2"
        filename = "sitemap-index.xml"
        print(f"Writing sitemap-index.xml: {filename}")
        write_file(data, template_name, filename)


def build_sitemap_index_xml(url):
    print("#", "-" * 80)
    print("Generating sitemap-index.xml ...")

    SitemapXML(url=url).write_sitemap_index_xml()
