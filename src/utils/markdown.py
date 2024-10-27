import yaml
from markdown2 import Markdown
import re

class PrismCodeProcessor:
    def __init__(self):
        self.fence_re = re.compile(r'^```\s*(\w+)?')

    def process(self, text):
        lines = text.split('\n')
        processed_lines = []
        in_code_block = False
        code_block = []
        lang = ''

        for line in lines:
            if self.fence_re.match(line):
                if not in_code_block:
                    in_code_block = True
                    lang = self.fence_re.match(line).group(1) or 'plaintext'
                    code_block = []
                else:
                    in_code_block = False
                    code_html = self.escape('\n'.join(code_block))
                    processed_lines.append(f'<pre class="rounded-xl"><code class="language-{lang}">{code_html}</code></pre>')
            elif in_code_block:
                code_block.append(line)
            else:
                processed_lines.append(line)

        if in_code_block:
            code_html = self.escape('\n'.join(code_block))
            processed_lines.append(f'<pre class="rounded-xl"><code class="language-{lang}">{code_html}</code></pre>')

        return '\n'.join(processed_lines)

    def escape(self, text):
        return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

class CustomMarkdown(Markdown):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prism_processor = PrismCodeProcessor()

    def convert(self, text):
        text = self.prism_processor.process(text)
        html = super().convert(text)
        return self.add_classes(html)

    def add_classes(self, html):
        class_mappings = {
            "h1": "text-4xl font-bold my-6 leading-tight",
            "h2": "text-3xl font-bold my-5 leading-snug",
            "h3": "text-2xl font-semibold my-4",
            "h4": "text-xl font-semibold my-3",
            "h5": "text-lg font-medium my-2",
            "h6": "text-base font-medium my-2",
            "p": "text-base my-4 leading-relaxed",
            "code": "bg-gray-600 rounded p-1 px-2 text-sm font-mono mr-1",
            "a": "text-sky-500 font-semibold underline hover:text-sky-600 transition-colors duration-300",
            "ul": "list-disc pl-5 my-3 space-y-2",
            "ol": "list-decimal pl-5 my-3 space-y-2",
            "blockquote": "border-l-4 border-gray-300 pl-4 py-2 italic my-4 text-gray-600",
            "hr": "border-t border-gray-300 my-6",
            "table": "min-w-full border-collapse my-4",
            "thead": "bg-gray-100",
            "th": "border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700",
            "td": "border border-gray-300 px-4 py-2 text-gray-600",
            "img": "max-w-full h-auto my-4 rounded-xl shadow-md",
            "strong": "font-bold",
            "em": "italic",
            "dl": "my-4",
            "dt": "font-semibold mb-1",
            "dd": "pl-4 mb-3 text-gray-600",
            "sub": "text-xs align-sub",
            "sup": "text-xs align-super",
            "abbr": "border-b border-dotted border-gray-500 cursor-help",
            "kbd": "bg-gray-200 rounded px-1 py-0.5 text-sm font-mono",
            "mark": "bg-yellow-200 px-1 rounded",
            "s": "line-through text-gray-500",
            "details": "my-3",
            "summary": "cursor-pointer font-semibold",
            "figure": "my-4",
            "figcaption": "text-sm mt-2 text-center"
        }

        for tag, classes in class_mappings.items():
            html = re.sub(f'<{tag}(>| )', f'<{tag} class="{classes}"\\1', html)

        return html


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


def parse_markdown_files_and_convert_to_html(item_files) -> list:
    items = []
    for item_file in item_files:
        yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(item_file)
        item = yaml_header | {"body": convert_markdown_text_to_html(markdown_body)}
        items.append(item)
    return items
