import unittest

from inline_render import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
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

    def test_empty_old_nodes(self):
        result = split_nodes_image([])
        self.assertEqual(result, [])

    def test_no_images(self):
        node = TextNode("This is a text without any images", TEXT_TYPE_TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://www.example.com/image.png)", TEXT_TYPE_TEXT)
        expected_nodes = [
            TextNode("This is text with an ", TEXT_TYPE_TEXT),
            TextNode("image", TEXT_TYPE_IMAGE, "https://www.example.com/image.png")]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_nodes)

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image1](https://www.example.com/image1.png) and ![image2](https://www.example.com/image2.png)", TEXT_TYPE_TEXT)
        expected_nodes = [
            TextNode("This is text with an ", TEXT_TYPE_TEXT),
            TextNode("image1", TEXT_TYPE_IMAGE, "https://www.example.com/image1.png"),
            TextNode(" and ", TEXT_TYPE_TEXT),
            TextNode("image2", TEXT_TYPE_IMAGE, "https://www.example.com/image2.png")
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected_nodes)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXT_TYPE_TEXT),
                TextNode("image", TEXT_TYPE_IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode("![image](https://www.example.com/image.png)", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TEXT_TYPE_IMAGE, "https://www.example.com/image.png"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TEXT_TYPE_TEXT),
                TextNode("image", TEXT_TYPE_IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TEXT_TYPE_TEXT),
                TextNode(
                    "second image", TEXT_TYPE_IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("This is a text without links", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_single_link(self):
        node = TextNode("This is a text with a [single link](https://example.com)", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("This is a text with a ", TEXT_TYPE_TEXT),
            TextNode("single link", TEXT_TYPE_LINK, "https://example.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_multiple_links(self):
        node = TextNode(
            "Text with [link1](https://link1.com) and [link2](https://link2.com)", TEXT_TYPE_TEXT)
        new_nodes = split_nodes_link([node])
        expected_nodes = [
            TextNode("Text with ", TEXT_TYPE_TEXT),
            TextNode("link1", TEXT_TYPE_LINK, "https://link1.com"),
            TextNode(" and ", TEXT_TYPE_TEXT),
            TextNode("link2", TEXT_TYPE_LINK, "https://link2.com")
        ]
        self.assertEqual(new_nodes, expected_nodes)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TEXT_TYPE_TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TEXT_TYPE_TEXT),
                TextNode("link", TEXT_TYPE_LINK, "https://boot.dev"),
                TextNode(" and ", TEXT_TYPE_TEXT),
                TextNode("another link", TEXT_TYPE_LINK,
                         "https://blog.boot.dev"),
                TextNode(" with text that follows", TEXT_TYPE_TEXT),
            ],
            new_nodes,
        )