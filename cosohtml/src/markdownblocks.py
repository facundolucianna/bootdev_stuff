import re

from enum import Enum

from htmlnode import LeafNode, ParentNode

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


def markdown_to_html_node(markdown):
    pre_formed_blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in pre_formed_blocks:
        block_type = block_to_block_type(block)
        new_block = block.strip()
        match block_type:    
            case BlockType.HEADING:

                level = len(re.match(r"^#{1,6} ", new_block).group(0)) - 1 
                nodes.append(LeafNode(tag=f"h{level}", value=new_block[level+1:].strip()))

            case BlockType.CODE:
                new_block = new_block[4:-3]
                new_node = LeafNode(tag="code", value=new_block)
                nodes.append(ParentNode(tag="pre", children=[new_node]))

            case BlockType.QUOTE:
                new_block = new_block[2:]
                new_node = LeafNode(tag="blockquote", value=new_block)
                nodes.append(new_node)
                
            case BlockType.UNORDERED_LIST:
                child_list = []
                for linea in new_block.splitlines():
                    child_list.append(LeafNode(tag="li", value=linea[2:].strip()))
                nodes.append(ParentNode(tag="ul", children=child_list))
                
            case BlockType.ORDERED_LIST:
                child_list = []
                for linea in new_block.splitlines():
                    level = len(re.match(r"^\d+\. ", linea).group(0))
                    child_list.append(LeafNode(tag="li", value=linea[level:].strip()))
                nodes.append(ParentNode(tag="ol", children=child_list))
                
            case BlockType.PARAGRAPH:
                nodes.append(LeafNode(tag="p", value=new_block))
                
            case _:
                raise ValueError(f"Unknown block type: {block_type}")
        
    return ParentNode(tag="div", children=nodes)
            
        