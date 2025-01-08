import unittest
from inline_markdown import *

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



class TestMarkdownExtraction(unittest.TestCase):

    def Markdown_images_extract_test(self):
        text = "This is a ![cat](https://example.com/cat.jpg) and a ![dog](https://example.com/dog.jpg)"
        expected = [("cat", "https://example.com/cat.jpg"), ("dog", "https://example.com/dog.jpg")]
        self.assertEqual(extract_markdown_images(text), expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

    def test_split_nodes_image_basic(self):
        node = TextNode("Hello ![alt](image.png) World", TextType.NORMAL_TEXT)
        nodes = split_nodes_images([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
        self.assertEqual(nodes[1].text, "alt")
        self.assertEqual(nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(nodes[2].text, " World")
        self.assertEqual(nodes[2].text_type, TextType.NORMAL_TEXT)

    def test_split_nodes_links_basic(self):
        node = TextNode("Hello [alt](image.png) World", TextType.NORMAL_TEXT)
        nodes = split_nodes_links([node])
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text, "Hello ")
        self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
        self.assertEqual(nodes[1].text, "alt")
        self.assertEqual(nodes[1].text_type, TextType.LINKS)
        self.assertEqual(nodes[2].text, " World")
        self.assertEqual(nodes[2].text_type, TextType.NORMAL_TEXT)

    def test_multiple_images(self):
        node = TextNode("This has ![alt1](img1.png) two ![alt2](img2.png) images", TextType.NORMAL_TEXT)
        nodes = split_nodes_images([node])
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text_type, TextType.NORMAL_TEXT)
        self.assertEqual(nodes[0].text, "This has ")
        self.assertEqual(nodes[1].text, "alt1")
        self.assertEqual(nodes[1].text_type, TextType.IMAGES)
        self.assertEqual(nodes[1].url, "img1.png")
        self.assertNotEqual(nodes[1].url, "alt1")
        self.assertEqual(nodes[2].text, " two ")
        self.assertEqual(nodes[2].text_type, TextType.NORMAL_TEXT)
        self.assertEqual(len(nodes[2].text), 5)
        self.assertEqual(nodes[3].text_type, TextType.IMAGES)
        self.assertEqual(nodes[3].text, "alt2")
        self.assertEqual(nodes[3].url, "img2.png")
        self.assertEqual(nodes[4].text, " images")
        self.assertEqual(nodes[4].text_type, TextType.NORMAL_TEXT)


    def test_text_to_textnodes(self):

        nodes_italic = "This is *italic* text"
        expected = [TextNode("This is ", TextType.NORMAL_TEXT),
                    TextNode("italic", TextType.ITALIC_TEXT),
                    TextNode(" text", TextType.NORMAL_TEXT)]
        self.assertEqual(text_to_textnodes(nodes_italic), expected)

        nodes_code = "This is `code` text"
        expected = [TextNode("This is ", TextType.NORMAL_TEXT),
                    TextNode("code", TextType.CODE_TEXT),
                    TextNode(" text", TextType.NORMAL_TEXT)]
        self.assertEqual(text_to_textnodes(nodes_code), expected)

        nodes_bold_code = "This is **bold** and `code` text"
        expected = [TextNode("This is ", TextType.NORMAL_TEXT),
                    TextNode("bold", TextType.BOLD_TEXT),
                    TextNode(" and ", TextType.NORMAL_TEXT),
                    TextNode("code", TextType.CODE_TEXT),
                    TextNode(" text", TextType.NORMAL_TEXT)]
        self.assertEqual(text_to_textnodes(nodes_bold_code), expected)

        nodes_images_links = "This is text with ![funny image](le_monkeyfaec.png) and [epic link](lemon_keyface.png) lol"
        expected = [TextNode("This is text with ", TextType.NORMAL_TEXT),
                    TextNode("funny image", TextType.IMAGES, "le_monkeyfaec.png"),
                    TextNode(" and ", TextType.NORMAL_TEXT),
                    TextNode("epic link", TextType.LINKS, "lemon_keyface.png"),
                    TextNode(" lol", TextType.NORMAL_TEXT)]
        self.assertEqual(text_to_textnodes(nodes_images_links), expected)

        nodes_empty_string = ""
        expected = [TextNode("", TextType.NORMAL_TEXT)]
        self.assertEqual(text_to_textnodes(nodes_empty_string), expected)

        nodes_double_type = "This is **bold** text that is double **boldy** hehe"
        expected = [TextNode("This is ", TextType.NORMAL_TEXT),
                    TextNode("bold", TextType.BOLD_TEXT),
                    TextNode(" text that is double ", TextType.NORMAL_TEXT),
                    TextNode("boldy", TextType.BOLD_TEXT),
                    TextNode(" hehe", TextType.NORMAL_TEXT)]
        self.assertEqual(text_to_textnodes(nodes_double_type), expected)

if __name__ == '__main__':
    unittest.main()