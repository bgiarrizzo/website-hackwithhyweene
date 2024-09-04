import yaml
from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


class AddClassTreeprocessor(Treeprocessor):
    def run(self, root):
        # Headings
        for elem in root.iter("h1"):
            elem.set("class", "text-4xl font-bold my-6 leading-tight")
        for elem in root.iter("h2"):
            elem.set("class", "text-3xl font-bold my-5 leading-snug")
        for elem in root.iter("h3"):
            elem.set("class", "text-2xl font-semibold my-4")
        for elem in root.iter("h4"):
            elem.set("class", "text-xl font-semibold my-3")
        for elem in root.iter("h5"):
            elem.set("class", "text-lg font-medium my-2")
        for elem in root.iter("h6"):
            elem.set("class", "text-base font-medium my-2")

        # Paragraphs
        for elem in root.iter("p"):
            elem.set("class", "text-base my-3 leading-relaxed")

        # Links
        for elem in root.iter("a"):
            elem.set(
                "class",
                "text-sky-500 font-semibold underline hover:text-sky-600 transition-colors duration-300",
            )

        # Lists
        for elem in root.iter("ul"):
            elem.set("class", "list-disc pl-5 my-3 space-y-2")
        for elem in root.iter("ol"):
            elem.set("class", "list-decimal pl-5 my-3 space-y-2")

        # Blockquotes
        for elem in root.iter("blockquote"):
            elem.set(
                "class",
                "border-l-4 border-gray-300 pl-4 py-2 italic my-4 text-gray-600",
            )

        # Code blocks
        for elem in root.iter("pre"):
            elem.set("class", "bg-gray-100 rounded-md p-4 my-4 overflow-x-auto")
        for elem in root.iter("code"):
            elem.set("class", "font-mono text-sm")

        # Inline code
        for elem in root.iter("code"):
            if elem.getparent().tag != "pre":
                elem.set("class", "bg-gray-100 rounded px-1 py-0.5 font-mono text-sm")

        # Horizontal rules
        for elem in root.iter("hr"):
            elem.set("class", "border-t border-gray-300 my-6")

        # Tables
        for elem in root.iter("table"):
            elem.set("class", "min-w-full border-collapse my-4")
        for elem in root.iter("thead"):
            elem.set("class", "bg-gray-100")
        for elem in root.iter("th"):
            elem.set(
                "class",
                "border border-gray-300 px-4 py-2 text-left font-semibold text-gray-700",
            )
        for elem in root.iter("td"):
            elem.set("class", "border border-gray-300 px-4 py-2 text-gray-600")

        # Images
        for elem in root.iter("img"):
            elem.set("class", "max-w-full h-auto my-4 rounded-lg shadow-md")

        # Strong and Emphasis
        for elem in root.iter("strong"):
            elem.set("class", "font-bold")
        for elem in root.iter("em"):
            elem.set("class", "italic")

        # Definition lists
        for elem in root.iter("dl"):
            elem.set("class", "my-4")
        for elem in root.iter("dt"):
            elem.set("class", "font-semibold mb-1")
        for elem in root.iter("dd"):
            elem.set("class", "pl-4 mb-3 text-gray-600")

        # Subscript and Superscript
        for elem in root.iter("sub"):
            elem.set("class", "text-xs align-sub")
        for elem in root.iter("sup"):
            elem.set("class", "text-xs align-super")

        # Abbreviations
        for elem in root.iter("abbr"):
            elem.set("class", "border-b border-dotted border-gray-500 cursor-help")

        # Keyboard input
        for elem in root.iter("kbd"):
            elem.set("class", "bg-gray-200 rounded px-1 py-0.5 text-sm font-mono")

        # Mark (highlighted text)
        for elem in root.iter("mark"):
            elem.set("class", "bg-yellow-200 px-1 rounded")

        # Strikethrough
        for elem in root.iter("s"):
            elem.set("class", "line-through text-gray-500")

        # Details and Summary
        for elem in root.iter("details"):
            elem.set("class", "my-3")
        for elem in root.iter("summary"):
            elem.set("class", "cursor-pointer font-semibold")

        # Figure and Figcaption
        for elem in root.iter("figure"):
            elem.set("class", "my-4")
        for elem in root.iter("figcaption"):
            elem.set("class", "text-sm mt-2 text-center")


class AddClassExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(AddClassTreeprocessor(md), "addclass", 15)


markdown_parser = Markdown(extensions=[AddClassExtension()])


def convert_markdown_text_to_html(markdown_content):
    return markdown_parser.convert(
        markdown_content,
    )


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
        yaml_header, markdown_body = parse_yaml_header_and_markdown_body_in_file(
            item_file
        )
        item = yaml_header | {"body": convert_markdown_text_to_html(markdown_body)}
        items.append(item)
    return items
