import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(str(node), "TextNode(This is a text node, text)")

    def test_attr_text(self):
        node = TextNode("Apa", TextType.LINK)
        self.assertEqual(node.text, "Apa")

    def test_type(self):
        node = TextNode("Apa", TextType.IMAGE)
        self.assertNotEqual(node.text_type, TextType.TEXT)

    def test_url(self):
        node = TextNode("aaaa", TextType.LINK)   
        self.assertIsNone(node.url)

if __name__ == "__main__":
    unittest.main()
