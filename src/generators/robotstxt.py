from os import path 

from utils.file import write_file

def write_robotstxt(robots_txt_content):
    data = {"url": robots_txt_content}
    template_name = "robots.txt.j2"
    filename = "robots.txt"

    write_file(data, template_name, filename)


def add_robotstxt_to_build(robots_txt_content):
    write_robotstxt(robots_txt_content)
