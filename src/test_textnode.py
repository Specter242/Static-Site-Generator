import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node = TextNode("This is a text node", TextType.Bold_text)
        node2 = TextNode("This is a text node", TextType.Bold_text)
        self.assertEqual(node, node2)
    def test_eq2(self):
        node = TextNode("This is a text node", TextType.Italic_text)
        node2 = TextNode("This is a text node", TextType.Bold_text)
        self.assertNotEqual(node, node2)
    def test_eq3(self):
        node = TextNode("This is a text node", TextType.Code_text)
        node2 = TextNode("This is a text node", TextType.Bold_text)
        self.assertNotEqual(node, node2)
    def test_eq4(self):
        node = TextNode("This is a text node", TextType.Link)
        node2 = TextNode("This is a text node", TextType.Bold_text)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()