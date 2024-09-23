from bs4 import BeautifulSoup
from prettierfier import prettify_html, prettify_xml


def beautify_html(content):
    soup = BeautifulSoup(content, "html.parser").prettify(formatter="html5")
    return prettify_html(html_string=soup)


def beautify_xml(content):
    soup = BeautifulSoup(content, "xml").prettify()
    return prettify_xml(xml_string=soup)
