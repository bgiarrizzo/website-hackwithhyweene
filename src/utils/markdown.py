import yaml
from markdown2 import Markdown
import re


class PrismCodeProcessor:
    def __init__(self):
        self.fence_re = re.compile(r"^```\s*(\w+)?")

    def process(self, text):
        lines = text.split("\n")
        processed_lines = []
        in_code_block = False
        code_block = []
        lang = ""

        for line in lines:
            if self.fence_re.match(line):
                if not in_code_block:
                    in_code_block = True
                    lang = self.fence_re.match(line).group(1) or "plaintext"
                    code_block = []
                else:
                    in_code_block = False
                    code_html = self.escape("\n".join(code_block))
                    processed_lines.append(
                        f'<pre><code class="language-{lang}">{code_html}</code></pre>'
                    )
            elif in_code_block:
                code_block.append(line)
            else:
                processed_lines.append(line)

        if in_code_block:
            code_html = self.escape("\n".join(code_block))
            processed_lines.append(
                f'<pre><code class="language-{lang}">{code_html}</code></pre>'
            )

        return "\n".join(processed_lines)

    def escape(self, text):
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class CustomMarkdown(Markdown):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prism_processor = PrismCodeProcessor()

    def convert(self, text):
        text = self.prism_processor.process(text)
        return super().convert(text)


markdown_parser = CustomMarkdown(extras=["fenced-code-blocks"])


def convert_markdown_text_to_html(markdown_content):
    return markdown_parser.convert(markdown_content)


def parse_yaml_header_and_markdown_body_in_file(markdown_file_path):
    with open(markdown_file_path, mode="r", encoding="utf-8") as markdown_file:
        markdown_file_content = markdown_file.read()
        markdown_file_content = markdown_file_content.split("---")

        yaml_header = yaml.load(markdown_file_content[1], Loader=yaml.FullLoader)
        markdown_body = markdown_file_content[2]

        return yaml_header, markdown_body


def parse_markdown_file_and_convert_to_html(file):
    yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(
        file
    )
    return yaml_header | {"body": convert_markdown_text_to_html(markdown_body)}
