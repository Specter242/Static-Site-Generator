import unittest
from inline_process import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextType, TextNode

class TestInlineProcess(unittest.TestCase):

    def test_split_nodes_delimiter_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_unpaired(self):
        node = TextNode("This is text with an unpaired ` delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue("Invalid markdown syntax: unpaired delimiter" in str(context.exception))

    def test_split_nodes_delimiter_empty_delimiter(self):
        node = TextNode("This is text with a `` delimiter", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertTrue("Invalid markdown syntax: empty delimiter" in str(context.exception))

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("This is `code` and this is `another code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and this is ")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[3].text, "another code")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)
        self.assertEqual(new_nodes[4].text, "")
        self.assertEqual(new_nodes[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is text without delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "This is text without delimiter")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](image_url) in markdown"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "image_url"))

        text = "Multiple images ![first](url1) and ![second](url2)"
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("first", "url1"))
        self.assertEqual(images[1], ("second", "url2"))

    def test_extract_markdown_links(self):
        text = "This is a [link](url) in markdown"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "url"))

        text = "Multiple links [first](url1) and [second](url2)"
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("first", "url1"))
        self.assertEqual(links[1], ("second", "url2"))

    def test_split_nodes_image(self):
        node = TextNode("This is an image ![alt text](image_url) in markdown", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is an image ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "")
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(new_nodes[1].url, "image_url")
        self.assertEqual(new_nodes[2].text, " in markdown")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_link(self):
        node = TextNode("This is a [link](url) in markdown", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "link")
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)
        self.assertEqual(new_nodes[1].url, "url")
        self.assertEqual(new_nodes[2].text, " in markdown")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

if __name__ == '__main__':
    unittest.main()