from os import path


def add_cname_to_build(path_to_build, cname):
    with open(path.join(path_to_build, "CNAME"), "w") as f:
        f.write(cname)
