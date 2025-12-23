import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)

        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.NORMAL_TEXT)
        self.assertEqual(str(node), "TextNode(This is a text node, text)")

    def test_attr_text(self):
        node = TextNode("Apa", TextType.ITALIC_TEXT)
        self.assertEqual(node.text, "Apa")

    def test_type(self):
        node = TextNode("Apa", TextType.IMAGE)
        self.assertNotEqual(node.text_type, TextType.NORMAL_TEXT)

    def test_url(self):
        node = TextNode("aaaa", TextType.ITALIC_TEXT)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
