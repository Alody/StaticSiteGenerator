import unittest
from text_to_html import *

class TestTextToHtml(unittest.TestCase):
    def test_normal_text(self):
        text_node = TextNode("Hello", TextType.NORMAL_TEXT)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, None)
        self.assertEqual(leaf_node.value, "Hello")

    def test_bold_text(self):
        text_node = TextNode("Bold", TextType.BOLD_TEXT)
        leaf_node = text_node_to_html_node(text_node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "Bold")
    
    def test_throws_on_unknown_type(self):
        with self.assertRaises(ValueError):
            text_node = TextNode("Unknown", "UnknownType")
            text_node_to_html_node(text_node)

if __name__ == '__main__':
    unittest.main()