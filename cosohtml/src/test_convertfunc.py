import unittest

from textnode import TextNode, TextType
from convertfunc import text_node_to_html_node, split_nodes_delimiter

class TestNodeToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>This is a text node</b>")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<i>This is a text node</i>")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>This is a text node</code>")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<a href=\"https://www.google.com\">This is a text node</a>")

    def test_image(self):
        node = TextNode("This is a text node", TextType.IMAGE, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<img src=\"https://www.google.com\" alt=\"This is a text node\"></img>")

    def test_error_type(self):
        with self.assertRaises(ValueError):
            node = TextNode("This is a text node", "Invalid type")
            text_node_to_html_node(node)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        nodes = TextNode("**This is a text node**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is a text node", TextType.BOLD)])

    def test_split_nodes_delimiter(self):
        nodes = TextNode("This _is a text_ node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([nodes], "_", TextType.ITALIC)

        expected_nodes = [
            TextNode("This ", TextType.TEXT),
            TextNode("is a text", TextType.ITALIC),
            TextNode(" node", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_nodes(self):
        nodes = [TextNode("This _is a text_ node", TextType.TEXT), 
        TextNode("_This_ is a text node", TextType.TEXT),
        TextNode("This is a text _node_", TextType.TEXT),
        TextNode("This **is a text node**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)

        expected_nodes = [
            TextNode("This ", TextType.TEXT),
            TextNode("is a text", TextType.ITALIC),
            TextNode(" node", TextType.TEXT),

            TextNode("This", TextType.ITALIC),
            TextNode(" is a text node", TextType.TEXT),

            TextNode("This is a text ", TextType.TEXT),
            TextNode("node", TextType.ITALIC),

            TextNode("This **is a text node**", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_error_delimiter(self):
        with self.assertRaises(ValueError):
            nodes = TextNode("This _is a text node", TextType.TEXT)
            split_nodes_delimiter([nodes], "_", TextType.ITALIC)

if __name__ == "__main__":
    unittest.main()
