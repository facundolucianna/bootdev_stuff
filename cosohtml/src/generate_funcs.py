from pathlib import Path
from markdownblocks import markdown_to_html_node
import re


def extract_title(markdown: str) -> str:
    
    obtain_all_lines = markdown.splitlines()

    for line in obtain_all_lines:
        new_line = line.strip()
        if re.match(r"^#{1} ", new_line):
            level = len(re.match(r"^#{1} ", new_line).group(0)) - 1
            return new_line[level+1:].strip()

    raise ValueError("No heading found in markdown")


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    print(f"Generating page from {from_path.resolve()} to {dest_path.resolve()} using {template_path.resolve()}")

    if not dest_path.parent.exists():
        dest_path.parent.mkdir(parents=True)

    markdown = from_path.read_text()
    template = template_path.read_text()

    title = extract_title(markdown)
    html = markdown_to_html_node(markdown).to_html()

    new_page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    dest_path.write_text(new_page)
    
    print(title)
    print(new_page)
    print("Done")