import re

from enum import Enum

from htmlnode import LeafNode, ParentNode
from convertfunc import text_to_textnodes, text_node_to_html_node

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    markdown = markdown.strip()
    if markdown == "":
        raise ValueError("Markdown is empty")
    blocks = markdown.split("\n\n")
    blocks_clean = []
    for block in blocks:
        block_clean = block.strip()
        if block_clean == "":
            continue
        blocks_clean.append(block_clean)
    return blocks_clean
    

def block_to_block_type(block: str) -> BlockType:
    if re.search(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith("> "):
        return BlockType.QUOTE
    if block.startswith("- "):
        correct_flag = True
        for linea in block.splitlines():
            if not linea.strip().startswith("- "):
                correct_flag = False
                break
        if correct_flag:
            return BlockType.UNORDERED_LIST
    if re.search(r"^\d+\. ", block):
        correct_flag = True
        for linea in block.splitlines():
            if not re.search(r"^\d+\. ", linea):
                correct_flag = False
                break
        if correct_flag:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def markdown_to_html_node(markdown):
    pre_formed_blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in pre_formed_blocks:
        block_type = block_to_block_type(block)
        new_block = block.strip()
        match block_type:
            case BlockType.HEADING:
                level = len(re.match(r"^#{1,6} ", new_block).group(0)) - 1
                nodes.append(ParentNode(tag=f"h{level}", children=text_to_children(new_block[level+1:].strip())))

            case BlockType.CODE:
                new_block = new_block[4:-3]
                new_node = LeafNode(tag="code", value=new_block)
                nodes.append(ParentNode(tag="pre", children=[new_node]))

            case BlockType.QUOTE:
                # Handle multi-line quotes properly if needed, but per previous code it seemed basic
                # If the quote block has multiple lines, each starts with "> ".
                # Current code just did `new_block[2:]` which only strips the first one?
                # The `new_block` is `block.strip()`.
                # If there are newlines, `strip()` keeps them.
                # If every line starts with `>`, we should strip them.
                # The existing code was:
                # new_block = new_block[2:]
                # new_node = LeafNode(tag="blockquote", value=new_block)
                # This seems buggy for multi-line quotes if they all start with `>`.
                # But to follow "reuse/refactor" and pass tests (which don't test quotes explicitly but might rely on paragraph logic),
                # I'll stick to replacing LeafNode value with text_to_children.
                # HOWEVER, `text_to_children` returns a list of nodes.
                # So we should use ParentNode or put them in.
                # `blockquote` can contain other elements.
                
                # Let's fix the quote stripping logic to be safe:
                lines = new_block.splitlines()
                cleaned_lines = []
                for line in lines:
                    if line.strip().startswith(">"):
                        cleaned_lines.append(line.strip()[1:].strip())
                    else:
                        cleaned_lines.append(line.strip())
                content = " ".join(cleaned_lines) # Markdown quotes usually flow text?
                
                # Or stick to the previous simple logic if it was intended for single line?
                # The previous code: `new_block[2:]`.
                # If I want to be safe and just integrate text_to_children:
                # I'll use the previous logic but with Children.
                
                # Re-reading previous code:
                # case BlockType.QUOTE:
                #    new_block = new_block[2:]
                #    new_node = LeafNode(tag="blockquote", value=new_block)
                #    nodes.append(new_node)
                
                # If I just use text_to_children:
                # nodes.append(ParentNode(tag="blockquote", children=text_to_children(new_block[2:])))
                # BUT if it's multiline, `new_block[2:]` only strips first line's `> `.
                # I will improve it slightly:
                lines = new_block.split("\n")
                new_lines = []
                for line in lines:
                    if line.startswith(">"):
                         new_lines.append(line.lstrip(">").strip())
                    else:
                         new_lines.append(line)
                content = " ".join(new_lines)
                nodes.append(ParentNode(tag="blockquote", children=text_to_children(content)))
                
            case BlockType.UNORDERED_LIST:
                child_list = []
                for linea in new_block.splitlines():
                    # linea is like "- text"
                    # Previous: value=linea[2:].strip()
                    # New: children = text_to_children(...)
                    # Use ParentNode("li", children=...)
                    child_list.append(ParentNode(tag="li", children=text_to_children(linea[2:].strip())))
                nodes.append(ParentNode(tag="ul", children=child_list))

            case BlockType.ORDERED_LIST:
                child_list = []
                for linea in new_block.splitlines():
                    level = len(re.match(r"^\d+\. ", linea).group(0))
                    child_list.append(ParentNode(tag="li", children=text_to_children(linea[level:].strip())))
                nodes.append(ParentNode(tag="ol", children=child_list))

            case BlockType.PARAGRAPH:
                # Previous: LeafNode("p", value=new_block)
                # New: ParentNode("p", children=text_to_children(new_block))
                # Note: `new_block` might break newlines. Markdown treats single newlines as spaces usually, unless double space.
                # But `text_to_children` operates on the string.
                # For basic requirement, passing the block text is fine.
                # However, the test output shows newlines replaced by... wait.
                # Test input:
                # This is **bolded** paragraph
                # text in a p
                # tag here
                # Expected output:
                # <p>This is <b>bolded</b> paragraph text in a p tag here</p>
                # The newlines were replaced by spaces (implicitly or explicitly).
                # `block.strip()` keeps internal newlines.
                # `text_to_textnodes` processes the string.
                # If I pass "paragraph\ntext", `TextNode` will have it. `LeafNode` will have it.
                # Browser/HTML renders newlines as spaces.
                # But `unittest` check `assertEqual` is strict on string.
                # The expected string has spaces, no newlines.
                # So I should probably join the lines with space for paragraphs?
                # "This is **bolded** paragraph text in a p tag here"
                # Input was: "This is **bolded** paragraph\ntext in a p\ntag here"
                # So yes, I should replace newlines with spaces for Paragraphs (and probably others).
                
                nodes.append(ParentNode(tag="p", children=text_to_children(new_block.replace("\n", " "))))

            case _:
                raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode(tag="div", children=nodes)
            
        