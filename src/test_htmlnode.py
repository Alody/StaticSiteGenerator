import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_attributes(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_no_attributes(self):
        node = HTMLNode()
        expected = ''
        self.assertEqual(node.props_to_html(), expected)

    def test_repr(self):
        node = HTMLNode(tag="a", value="Click here", props={"href": "https://example.com"})
        expected = 'HTMLNode(tag=a, value=Click here, children=0, props={\'href\': \'https://example.com\'})'
        self.assertEqual(repr(node), expected)

class TestLeafNode(unittest.TestCase):
    def test_LeafNode_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected)

    def test_LeafNode_with_props(self):
        # Test with href attribute
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_LeafNode_no_tag(self):
        # Test with no tag (should return raw text)
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_LeafNode_no_value(self):
        # Test with no value (should raise ValueError)
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_parent_multiple_children(self):
        node = ParentNode("p", [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        expected = "<p><b>Bold text</b>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_parent_with_props(self):
        node = ParentNode("div", [LeafNode("p", "Hello")], {"class": "wrapper"})
        expected = '<div class="wrapper"><p>Hello</p></div>'
        self.assertEqual(node.to_html(), expected)

    def test_nested_node(self):
        node = ParentNode("div", [ParentNode("p", [LeafNode("span", "Nested")])])
        expected = '<div><p><span>Nested</span></p></div>'
        self.assertEqual(node.to_html(), expected)

    def test_no_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("p", "Hello")], None)

    def test_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("span", None, None)

    def test_empty_children_list(self):
        node = ParentNode("div", [], None)
        expected = "<div></div>"
        self.assertEqual(node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()