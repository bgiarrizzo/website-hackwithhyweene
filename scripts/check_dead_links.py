import os
import json
from pathlib import Path

import requests


def is_link_dead(url) -> bool:
    try:
        response = requests.head(url, allow_redirects=True)
    except requests.RequestException as e:
        print(f"Error checking {url}: {e}")

    if response.status_code == 404:
        return True

    return False


def read_html_files(build_dir):
    for root, _, files in os.walk(build_dir):
        for file in files:
            if file.endswith(".html") and "stats" not in root:
                yield os.path.join(root, file)


if __name__ == "__main__":
    build_dir = os.path.join(
        Path(os.path.dirname(__file__)).parent.relative_to(Path.cwd()), "build"
    )

    print("Checking for dead links...")

    data = {"pages": []}

    data["pages"] = [
        {
            "path": item,
            "links": [],
            "dead_links": [],
        }
        for item in read_html_files(build_dir)
    ]

    print(f"Found {len(data['pages'])} HTML files.")

    for page in data["pages"].copy():
        with open(page["path"], "r", encoding="utf-8") as f:
            content = f.readlines()
            for line in content:
                if 'src="http' in line or 'href="http' in line:
                    link = line.split('"')[1]
                    page["links"].append(link)
                    if is_link_dead(link):
                        page["dead_links"].append(link)

        print(
            f"Checked {page['path']}: {len(page['links'])} links found, {len(page['dead_links'])} dead links."
        )

        if len(page["dead_links"]) == 0:
            data["pages"].remove(page)

    print(json.dumps(data, indent=4))
