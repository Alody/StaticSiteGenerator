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

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.NORMAL_TEXT:
            new_nodes.append(node)

        else:
            text_split = node.text.split(delimiter)

            if len(text_split) % 2 == 0:
                raise ValueError("Unmatched delimiter found in the text")
            
            for i, segment in enumerate(text_split):
                if i % 2 == 0:
                    new_nodes.append(TextNode(segment, TextType.NORMAL_TEXT))
                else:
                    new_nodes.append(TextNode(segment, text_type))
    
    return new_nodes