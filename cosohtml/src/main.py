from textnode import TextNode, TextType
from markdownblocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node



def main():
    new_obj = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(new_obj)
    
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    blocks = markdown_to_html_node(md)
    #print(blocks)
    for block in blocks.children:
        print(block)

    
    


main()
