from utils.format import beautify_html, beautify_xml


def beautify(rendered_page, type, beautify=True):
    if beautify:
        if type == "html5":
            return beautify_html(rendered_page)
        else:
            return beautify_xml(rendered_page)

    return rendered_page
