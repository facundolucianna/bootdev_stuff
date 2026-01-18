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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!\!)\[([^\]]*)\]\(([^)]*)\)"
    matches = re.findall(pattern, text)
    return matches


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
            if text_split[0].strip() != "":
                new_nodes.append(TextNode(text_split[0].strip() + " ", TextType.TEXT))
            new_nodes.append(TextNode(text_split[1].strip(), text_type))
            if text_split[2].strip() != "":
                new_nodes.append(TextNode(" " + text_split[2].strip(), TextType.TEXT))  
        else:
            new_nodes.append(node)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:

        images = extract_markdown_images(node.text)

        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        image_nodes = []
        initial_flag = True
        all_text = node.text.strip()
        for image in images:
            text_split = all_text.split(f"![{image[0]}]({image[1]})", 1)
            if text_split[0] != "":
                if not initial_flag:
                    image_nodes.append(TextNode(" " + text_split[0].strip() + " ", TextType.TEXT))
                else:
                    image_nodes.append(TextNode(text_split[0].strip() + " ", TextType.TEXT))
            image_nodes.append(TextNode(image[0], TextType.IMAGE, url=image[1]))
            all_text = " " + text_split[1]
            initial_flag = False
            
        if all_text.strip() != "" :
            image_nodes.append(TextNode(" " + all_text.strip(), TextType.TEXT))

        new_nodes.extend(image_nodes)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
                continue
            link_nodes = []
            initial_flag = True
            all_text = node.text.strip()
            for link in links:
                text_split = all_text.split(f"[{link[0]}]({link[1]})", 1)
                if text_split[0] != "":
                    if not initial_flag:
                        link_nodes.append(TextNode(" " + text_split[0].strip() + " ", TextType.TEXT))
                    else:
                        link_nodes.append(TextNode(text_split[0].strip() + " ", TextType.TEXT))
                link_nodes.append(TextNode(link[0], TextType.LINK, url=link[1]))
                all_text = " " + text_split[1]
                initial_flag = False
            
            if all_text.strip() != "":
                link_nodes.append(TextNode(" " + all_text.strip(), TextType.TEXT))
            new_nodes.extend(link_nodes)
        else:
            new_nodes.append(node)
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:

    nodes_after_images = split_nodes_image([TextNode(text, TextType.TEXT)])
    nodes_after_links = split_nodes_link(nodes_after_images)
    nodes_after_bold = split_nodes_delimiter(nodes_after_links, "**", TextType.BOLD)
    nodes_after_italic = split_nodes_delimiter(nodes_after_bold, "_", TextType.ITALIC)

    return nodes_after_italic
