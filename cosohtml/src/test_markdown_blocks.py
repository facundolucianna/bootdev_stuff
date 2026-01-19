import unittest

from markdownblocks import markdown_to_blocks, block_to_block_type, BlockType, markdown_to_html_node

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is **bolded** paragraph", 
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", 
        "- This is a list\n- with items"])

    def test_markdown_to_blocks_empty(self):
        md = """
        
        
        
        """
        with self.assertRaises(ValueError):
            markdown_to_blocks(md)

    def test_markdown_to_blocks_multiple_new_lines(self):
        md = """
        
        
        
        
             This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




                      - This is a list
- with items                            




"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is **bolded** paragraph", 
        "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line", 
        "- This is a list\n- with items"])

class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###### heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####### paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_code(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "```code```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = "> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = ">quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_unordered_list(self):
        block = "- list\n- item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "- list\nitem"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
    
    def test_block_to_block_type_ordered_list(self):
        block = "1. list\n99898. item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "1. list\n3 item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_block_to_block_type_paragraph(self):
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "paragraph\nlines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

if __name__ == "__main__":
    unittest.main()
