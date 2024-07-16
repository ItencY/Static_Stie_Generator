import unittest

from inline_render import split_nodes_delimiter
from textnode import TextNode, TEXT_TYPE_TEXT, TEXT_TYPE_BOLD, TEXT_TYPE_CODE, TEXT_TYPE_IMAGE, TEXT_TYPE_ITALIC, TEXT_TYPE_LINK


class TestInlineRender(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD)
        self.assertEqual([TextNode("This is text with a ", TEXT_TYPE_TEXT), TextNode("bolded", TEXT_TYPE_BOLD), TextNode(" word", TEXT_TYPE_TEXT)], new_nodes)

    def test_delim_bold_double(self):
        node = TextNode("This is text with a **bolded** word and **another**", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD)
        self.assertListEqual([TextNode("This is text with a ", TEXT_TYPE_TEXT), TextNode("bolded", TEXT_TYPE_BOLD), TextNode(" word and ", TEXT_TYPE_TEXT), TextNode("another", TEXT_TYPE_BOLD)], new_nodes)

    def test_delim_bold_multiword(self):
        node = TextNode("This is text with a **bolded word** and **another**", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TEXT_TYPE_BOLD)
        self.assertListEqual([TextNode("This is text with a ", TEXT_TYPE_TEXT), TextNode("bolded word", TEXT_TYPE_BOLD), TextNode(" and ", TEXT_TYPE_TEXT), TextNode("another", TEXT_TYPE_BOLD)], new_nodes)

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TEXT_TYPE_ITALIC)
        self.assertListEqual([TextNode("This is text with an ", TEXT_TYPE_TEXT), TextNode("italic", TEXT_TYPE_ITALIC), TextNode(" word", TEXT_TYPE_TEXT)], new_nodes)

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TEXT_TYPE_CODE)
        self.assertListEqual([TextNode("This is text with a ", TEXT_TYPE_TEXT), TextNode("code block", TEXT_TYPE_CODE), TextNode(" word", TEXT_TYPE_TEXT)], new_nodes)