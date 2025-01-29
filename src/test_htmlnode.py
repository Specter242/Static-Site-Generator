import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq1(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    def test_eq2(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
    def test_eq3(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
    def test_eq4(self):
        node = LeafNode(None, "Hello world")
        # Should output: "Hello world"
        self.assertEqual(node.to_html(), "Hello world")
    def test_eq5(self):
        node = LeafNode("p", "Hello world")
        # Should output: "<p>Hello world</p>"
        self.assertEqual(node.to_html(), "<p>Hello world</p>")    
    def test_eq6(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        # Should output: '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>') 
    def test_eq7(self):
        node = LeafNode("p", None)
        # Should raise ValueError when to_html() is called
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()