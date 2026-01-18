import re

from textnode import TextNode, TextType
from htmlnode import LeafNode


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Invalid text type: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            text_split = node.text.split(delimiter)
            if len(text_split) == 1:
                new_nodes.append(node)
                continue
            if len(text_split) != 3:
                raise ValueError(f"Delimeter {delimiter} incomplete")
            if text_split[0] != "":
                new_nodes.append(TextNode(text_split[0].strip() + " ", TextType.TEXT))
            new_nodes.append(TextNode(text_split[1].strip(), text_type))
            if text_split[2] != "":
                new_nodes.append(TextNode(" " + text_split[2].strip(), TextType.TEXT))  
        else:
            new_nodes.append(node)

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!\!)\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches