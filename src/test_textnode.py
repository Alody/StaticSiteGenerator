import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_noteq(self):
        firstVal = TextNode("this is another text node", TextType.ITALIC_TEXT)
        secondVal = TextNode("this is another text node", TextType.NORMAL_TEXT)
        message = "Error, not equal"
        self.assertNotEqual(firstVal, secondVal, message)

    def test_url_noteq(self):
        firstVal = TextNode("this is a third text node", TextType.ITALIC_TEXT)
        secondVal = TextNode("this is a third text node", TextType.ITALIC_TEXT, "https://owl.cafe")
        message = "Error, url is not None"
        self.assertNotEqual(firstVal, secondVal, message)

if __name__ == "__main__":
    unittest.main()
