import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_html_props(self):
        node = HTMLNode("p", "Full text", None, {"class": "color", "href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' class="color" href="https://boot.dev"')

    # test incorrect option    
    """
    def test_html_props_two(self):
        node = HTMLNode("a", "Full Text", None, {"class": "color", "href": "https://yandex.ru"})
        self.assertEqual(node.props_to_html(), ' class="property" href="href="https://boot.dev"')
    """

    def test_html_no_children(self):
        node = LeafNode("div", "Full text")
        self.assertEqual(node.to_html(), "<div>Full text</div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(),"<div><span>child</span></div>")