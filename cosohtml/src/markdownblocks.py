import re

from enum import Enum

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

