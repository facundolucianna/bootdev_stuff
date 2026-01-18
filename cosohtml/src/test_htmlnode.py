import unittest
from htmlnode import HtmlNode, LeafNode, ParentNode


class TestHtmlNode(unittest.TestCase):
    def test_init(self):
        node = HtmlNode(tag="div", value="Hello")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_repr(self):
        node = HtmlNode(tag="div", value="Hello")
        self.assertEqual(str(node), "HtmlNode(tag=div, value=Hello, children=None, props=None)")
    
    def test_props_to_html(self):
        node = HtmlNode(props={"class": "container", "id": "main"})
        self.assertEqual(node.props_to_html(), ' class="container" id="main"')   
    
    def test_children(self):
        node = HtmlNode(tag="div", value="Hello", children=[HtmlNode(tag="p", value="Hello")])
        self.assertEqual(node.children[0].tag, "p") 
        self.assertEqual(node.children[0].value, "Hello")

class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode(tag="div", value="Hello")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "Hello")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)
    
    def test_error_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode(tag="div", value=None)
            node.to_html()

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_span(self):
        node = LeafNode("span", "Hello, world!")
        self.assertEqual(node.to_html(), "<span>Hello, world!</span>")
    
    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), "<a href=\"https://www.google.com\" target=\"_blank\">Hello, world!</a>")

    def test_leaf_repr(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(str(node), "LeafNode(tag=p, value=Hello, world!, props=None)")

class TestParentNode(unittest.TestCase):
    def test_init(self):
        node = ParentNode(tag="div", children=[HtmlNode(tag="p", value="Hello")])
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.children[0].tag, "p")
        self.assertEqual(node.children[0].value, "Hello")
        self.assertEqual(node.props, None)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        ) 

    def test_multiple_children_and_grandchildren(self):
        
        child_node = LeafNode("b", "Bold text")
        child_2_node = LeafNode(None, "Normal text")
        child_3_node = LeafNode("i", "italic text")
        grandchild_node = LeafNode("a", "Hello, world!", props={"href": "https://www.google.com", "target": "_blank"})
        parent_node = ParentNode("p", [child_node, child_2_node, child_3_node, child_2_node, grandchild_node, child_2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<a href=\"https://www.google.com\" target=\"_blank\">Hello, world!</a>Normal text</p>",
        )

    def test_error_tag_none(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [HtmlNode(tag="p", value="Hello")])
            node.to_html()
    
    def test_error_children_none(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)
            node.to_html()
