import unittest
from inline_process import text_to_textnodes, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextType, TextNode

class TestInlineProcess(unittest.TestCase):

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual(len(nodes), 11)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "text")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " with an ")
        self.assertEqual(nodes[3].text, "italic")
        self.assertEqual(nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(nodes[4].text, " word and a ")
        self.assertEqual(nodes[5].text, "code block")
        self.assertEqual(nodes[5].text_type, TextType.CODE)
        self.assertEqual(nodes[6].text, " and an ")
        self.assertEqual(nodes[7].text, "")
        self.assertEqual(nodes[7].text_type, TextType.IMAGE)
        self.assertEqual(nodes[7].url, "https://i.imgur.com/fJRm4Vk.jpeg")
        self.assertEqual(nodes[8].text, " and a ")
        self.assertEqual(nodes[9].text, "link")
        self.assertEqual(nodes[9].text_type, TextType.LINK)
        self.assertEqual(nodes[9].url, "https://boot.dev")

    def test_split_nodes_delimiter(self):
        text = "This is **bold** text."
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is ")
        self.assertEqual(nodes[1].text, "bold")
        self.assertEqual(nodes[1].text_type, TextType.BOLD)
        self.assertEqual(nodes[2].text, " text.")

    def test_extract_markdown_images(self):
        text = "This is an image ![alt text](image_url)."
        images = extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "image_url"))

    def test_extract_markdown_links(self):
        text = "This is a [link](http://example.com)."
        links = extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link", "http://example.com"))

    def test_split_nodes_image(self):
        text = "This is an image ![alt text](image_url)."
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = split_nodes_image(nodes)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is an image ")
        self.assertEqual(nodes[1].text, "")
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[1].url, "image_url")
        self.assertEqual(nodes[2].text, ".")

    def test_split_nodes_link(self):
        text = "This is a [link](http://example.com)."
        nodes = [TextNode(text, TextType.TEXT)]
        nodes = split_nodes_link(nodes)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "This is a ")
        self.assertEqual(nodes[1].text, "link")
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[1].url, "http://example.com")
        self.assertEqual(nodes[2].text, ".")

if __name__ == '__main__':
    unittest.main()