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


class TestTextParser(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("Hello **world**", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [
            TextNode("Hello ", TextType.NORMAL_TEXT),
            TextNode("world", TextType.BOLD_TEXT),
            TextNode("", TextType.NORMAL_TEXT)
        ])
    
    def test_multiple_bold_sections(self):
        node = TextNode("**Hello** world **there**", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(nodes, [
            TextNode("", TextType.NORMAL_TEXT),
            TextNode("Hello", TextType.BOLD_TEXT),
            TextNode(" world ", TextType.NORMAL_TEXT),
            TextNode("there", TextType.BOLD_TEXT),
            TextNode("", TextType.NORMAL_TEXT)
        ])

    def test_split_nodes_delimiter_code(self):
        node = TextNode("Hello `code` here", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(nodes, [
            TextNode("Hello ", TextType.NORMAL_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" here", TextType.NORMAL_TEXT)
        ])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("Hello *italic* text", TextType.NORMAL_TEXT)
        nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        self.assertEqual(nodes, [
            TextNode("Hello ", TextType.NORMAL_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" text", TextType.NORMAL_TEXT)
        ])






if __name__ == '__main__':
    unittest.main()