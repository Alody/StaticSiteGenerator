from htmlnode import *
from textnode import *
import re

# Modules: text node to html, inline markdown, extract markdown images


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
            # Add non-normal text nodes as-is
            new_nodes.append(node)
        else:
            text_split = node.text.split(delimiter)

            # Check for unmatched delimiters
            if len(text_split) % 2 == 0:
                raise ValueError("Unmatched delimiter found in the text")
            
            for i, segment in enumerate(text_split):
                # Always add the segment, including empty ones
                if i % 2 == 0:
                    new_nodes.append(TextNode(segment, TextType.NORMAL_TEXT))
                else:
                    new_nodes.append(TextNode(segment, text_type))

    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def split_nodes_images(old_nodes):
    result = []
    for node in old_nodes:
        if "![" not in node.text:
            result.append(node)
            continue
        
        current_text = node.text

        for alt, url in extract_markdown_images(node.text):
            # split text on img + url delimiter
            sections = current_text.split(f"![{alt}]({url})", 1)
            # b4 img text
            if sections[0]:  # prevent adding empty text
                before_img = TextNode(sections[0], TextType.NORMAL_TEXT)
                result.append(before_img)
            
            # text node for img
            img_node = TextNode(alt, TextType.IMAGES, url)
            result.append(img_node)
            current_text = sections[1]
        
        if current_text:
            result.append(TextNode(current_text, TextType.NORMAL_TEXT))
    
    return result

def split_nodes_links(old_nodes):
    result = []
    for node in old_nodes:
        if "[" not in node.text:
            result.append(node)
            continue

        current_text = node.text
        
        for alt, url in extract_markdown_links(node.text):
            # split text on link syntax
            sections = current_text.split(f"[{alt}]({url})", 1)
            # text before link
            if sections[0]:  # prevent adding empty text
                before_link = TextNode(sections[0], TextType.NORMAL_TEXT)
                result.append(before_link)
            # text node for link
            link_node = TextNode(alt, TextType.LINKS, url)
            result.append(link_node)
            current_text = sections[1]
        
        if current_text:
            result.append(TextNode(current_text, TextType.NORMAL_TEXT))
    
    return result