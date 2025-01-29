import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    def test_eq8(self):
        node = ParentNode("p", None)
        with self.assertRaisesRegex(ValueError, "missing child"):
            node.to_html()
    def test_eq9(self):
        node1 = LeafNode(None, "Hello world")
        a = [node1]
        node = ParentNode(None, a)
        with self.assertRaisesRegex(ValueError, "missing tag"):
            node.to_html()
    def test_eq10(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        a = [node1]
        node = ParentNode("p", a)
        self.assertEqual(node.to_html(), '<p><a href="https://www.google.com">Click me!</a></p>')
    def test_eq11(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node2 = LeafNode("p", "Hello world")
        a = [node1, node2]
        node = ParentNode("p", a)
        self.assertEqual(node.to_html(), '<p><a href="https://www.google.com">Click me!</a><p>Hello world</p></p>')
    def test_eq12(self):
        node1 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node1a = ParentNode("div", [node1])
        node2 = LeafNode("p", "Hello world")
        a = [node1a, node2]
        node = ParentNode("p", a)
        self.assertEqual(node.to_html(), '<p><div><a href="https://www.google.com">Click me!</a></div><p>Hello world</p></p>')
    def test_eq13(self):
        node1 = LeafNode("span", "Nested Text")
        node2 = ParentNode("div", [node1], {"class": "container"})
        node = ParentNode("section", [node2])
        self.assertEqual(
            node.to_html(),
            '<section><div class="container"><span>Nested Text</span></div></section>'
        )
    def test_eq14(self):
        node = LeafNode("span", "Deep text")
        for _ in range(10):
            node = ParentNode("div", [node])
        self.assertTrue("Deep text")


if __name__ == "__main__":
    unittest.main()