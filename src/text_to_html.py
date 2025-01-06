from htmlnode import *
from textnode import *

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.NORMAL_TEXT:
        leaf_node = LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD_TEXT:
        leaf_node = LeafNode("b", value=text_node.text)
    elif text_node.text_type == TextType.ITALIC_TEXT:
        leaf_node = LeafNode("i", value=text_node.text)
    elif text_node.text_type == TextType.CODE_TEXT:
        leaf_node = LeafNode("code", value=text_node.text)
    elif text_node.text_type == TextType.LINKS:
        leaf_node = LeafNode("a", value=text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGES:
        leaf_node = LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Unkown text type")
    return leaf_node