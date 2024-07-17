import unittest

from block_markdown import markdown_to_blocks

class TestBlockMarkdown(unittest.TestCase):

    def test_empty_input(self):
        result = markdown_to_blocks("")
        self.assertEqual(result, [])

    def test_multiple_blocks(self):
        input_str = "Block 1\n\nBlock 2\n\nBlock 3"
        result = markdown_to_blocks(input_str)
        self.assertEqual(result, ["Block 1", "Block 2", "Block 3"])

    def test_whitespace_blocks(self):
        input_str = "   Block 1   \n\n   Block 2   \n\n   Block 3   "
        result = markdown_to_blocks(input_str)
        self.assertEqual(result, ["Block 1", "Block 2", "Block 3"])

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )