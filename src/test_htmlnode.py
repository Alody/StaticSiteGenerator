import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
    unittest.main()