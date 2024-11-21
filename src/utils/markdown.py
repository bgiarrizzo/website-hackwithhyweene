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


def toc_to_html_list(toc_list):
    if not toc_list:
        return ""

    html = []
    current_level = 1
    stack = [1]

    for level, id, title in toc_list:
        while level < current_level:
            html.append("</ul></li>")
            stack.pop()
            current_level = stack[-1]

        if level > current_level:
            html.append("<ul>")
            stack.append(level)
        elif level < current_level:
            html.append("</li>")

        html.append(f'<li><a href="#{id}">{title}</a>')
        current_level = level

    while len(stack) > 1:
        html.append("</ul></li>")
        stack.pop()

    return "".join(html)


class CustomMarkdown(Markdown):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prism_processor = PrismCodeProcessor()
        self.toc_html = None

    def convert(self, text):
        text = self.prism_processor.process(text)
        html = super().convert(text)
        
        # Récupérer la table des matières
        if hasattr(self, '_toc'):
            # self.toc_html = self._toc
            self.toc_html = toc_to_html_list(self._toc)
        else:
            self.toc_html = ""  # Si aucune table des matières n'est générée
        
        return html

markdown_parser = CustomMarkdown(extras=["tables", "toc"])


def convert_markdown_text_to_html(markdown_content):
    html = markdown_parser.convert(markdown_content)
    toc_html = markdown_parser.toc_html
    return html, toc_html


def parse_yaml_header_and_markdown_body_in_file(markdown_file_path):
    with open(markdown_file_path, mode="r", encoding="utf-8") as markdown_file:
        content = markdown_file.read()
        
        pattern = r'^---\s*\n(.*?)\n---\s*\n'
        match = re.match(pattern, content, re.DOTALL)
        
        if match:
            yaml_header_str = match.group(1)
            yaml_header = yaml.safe_load(yaml_header_str)
            
            body_start = match.end()
            markdown_body = content[body_start:].strip()
        else:
            yaml_header = {}
            markdown_body = content

        return yaml_header, markdown_body


def parse_markdown_file_and_convert_to_html(file):
    yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(file)
    html_body, toc_html = convert_markdown_text_to_html(markdown_body)
    return yaml_header | {"body": html_body, "toc_html": toc_html}
