import unittest

from inline_render import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
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

    def test_no_images(self):
        text = "This is a text without any images"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])
    
    def test_single_image(self):
        text = "This is a text with a single image ![alt text](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt text", "https://example.com/image.jpg")])

    def test_multiple_images(self):
        text = "This is a text with multiple images ![alt1](https://example.com/image1.jpg) and ![alt2](https://example.com/image2.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [("alt1", "https://example.com/image1.jpg"), ("alt2", "https://example.com/image2.jpg")])

    def test_no_alt_text(self):
        text = "This is a text with an image that has no alt text ![]https://example.com/image.gif)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_no_image_link(self):
        text = "This is a text with an image that has no image link ![alt text]"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_multiple_links(self):
        text = "This is a [link](https://example.com) and [another link](https://another.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://example.com"), ("another link", "https://another.com")])

    def test_no_links(self):
        text = "This is a text without any links"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_single_link(self):
        text = "This is a [single link](https://singlelink.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("single link", "https://singlelink.com")])

    def test_links_with_different_text_and_urls(self):
        text = "Here is a [link](https://example.com) and [another link](https://another.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [("link", "https://example.com"), ("another link", "https://another.com")])