import unittest

from textnode import TextNode, TextType
from convertfunc import (text_node_to_html_node, 
                         split_nodes_delimiter, 
                         extract_markdown_images, 
                         extract_markdown_links, 
                         split_nodes_image, 
                         split_nodes_link,
                         text_to_textnodes)


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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_images_no_images(self):
        text = "This is text with no images"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

    def test_extract_markdown_no_imagen_but_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_links_no_links(self):
        text = "This is text with no links"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_links_no_links_but_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])


class TestSplitNodesImage(unittest.TestCase):
    def test_split_nodes_image(self):

        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and  ![image](https://i.imgur.com/zjjcJKZ.png) mama",
        TextType.TEXT,
        )
        node2 = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and  ![image](https://i.imgur.com/zjjcJKZ.png) mama",
        TextType.TEXT,
        )
        node3 = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,
        )
        node4 = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png) mamita",
        TextType.TEXT,
        )   

        new_nodes = split_nodes_image([node, node2, node3, node4])
        
        expected_nodes = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, url="https://i.imgur.com/3elNhQu.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" mama", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, url="https://i.imgur.com/3elNhQu.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" mama", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" mamita", TextType.TEXT),

        ]
        self.assertEqual(new_nodes, expected_nodes)


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode(
        "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
        )
        node2 = TextNode(
        "[link](https://www.boot.dev) and another [second link](https://www.youtube.com/@bootdotdev) mama",
        TextType.TEXT,
        )
        node3 = TextNode(
        "[link](https://www.boot.dev)",
        TextType.TEXT,
        )
        node4 = TextNode(
        "[link](https://www.boot.dev) mamita",
        TextType.TEXT,
        )   

        new_nodes = split_nodes_link([node, node2, node3, node4])
        
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
            TextNode("link", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, url="https://www.youtube.com/@bootdotdev"),
            TextNode(" mama", TextType.TEXT),
            TextNode("link", TextType.LINK, url="https://www.boot.dev"),
            TextNode("link", TextType.LINK, url="https://www.boot.dev"),
            TextNode(" mamita", TextType.TEXT),

        ]
        self.assertEqual(new_nodes, expected_nodes)

class TestSplitText(unittest.TestCase):
    def test_split_text(self):
        text = "This is _text with_ an [link](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/3elNhQu.png) **mama**"

        output = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text with", TextType.ITALIC),
            TextNode(" an", TextType.TEXT),
            TextNode("link", TextType.LINK, url="https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another", TextType.TEXT),
            TextNode("image", TextType.IMAGE, url="https://i.imgur.com/3elNhQu.png"),
            TextNode("mama", TextType.BOLD),
        ]

        nodes = text_to_textnodes(text)
        self.assertEqual(nodes, output)

if __name__ == "__main__":
    unittest.main()
