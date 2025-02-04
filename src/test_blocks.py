import unittest
from blocks import markdown_to_blocks, block_to_block_type, markdown_to_html_node
from htmlnode import HTMLNode

class TestMarkdownToBlocks(unittest.TestCase):
    def test_single_paragraph(self):
        markdown = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_multiple_paragraphs(self):
        markdown = "This is the first paragraph.\n\nThis is the second paragraph."
        expected = ["This is the first paragraph.", "This is the second paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_paragraphs_with_whitespace(self):
        markdown = "  This is the first paragraph.  \n\n  This is the second paragraph.  "
        expected = ["This is the first paragraph.", "This is the second paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_empty_string(self):
        markdown = ""
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_only_whitespace(self):
        markdown = "   \n\n   "
        expected = []
        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_mixed_content(self):
        markdown = "This is a paragraph.\n\n# This is a heading\n\nThis is another paragraph."
        expected = ["This is a paragraph.", "# This is a heading", "This is another paragraph."]
        self.assertEqual(markdown_to_blocks(markdown), expected)

class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# This is a heading"
        expected = "HEADING_1"
        self.assertEqual(block_to_block_type(block), expected)

    def test_subheading(self):
        block = "### This is a subheading"
        expected = "HEADING_3"
        self.assertEqual(block_to_block_type(block), expected)

    def test_code_block(self):
        block = "```\ncode block\n```"
        expected = "CODE"
        self.assertEqual(block_to_block_type(block), expected)

    def test_quote(self):
        block = "> This is a quote"
        expected = "QUOTE"
        self.assertEqual(block_to_block_type(block), expected)

    def test_unordered_list(self):
        block = "* Item 1\n* Item 2"
        expected = "UNORDERED_LIST"
        self.assertEqual(block_to_block_type(block), expected)

    def test_ordered_list(self):
        block = "1. Item 1\n2. Item 2"
        expected = "ORDERED_LIST"
        self.assertEqual(block_to_block_type(block), expected)

if __name__ == '__main__':
    unittest.main()