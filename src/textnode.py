from enum import Enum

class TextType(Enum):
    NORMAL_TEXT = "Normal text"
    BOLD_TEXT = "Bold text"        
    ITALIC_TEXT = "Italic text"
    CODE_TEXT = "Code text"
    LINKS = "Links"
    IMAGES = "Images"

class TextNode:
    def __init__(self, TEXT, TEXT_TYPE, URL=None):
        self.text = TEXT
        self.text_type = TEXT_TYPE
        self.url = URL

    def __eq__(self, other):
        if isinstance(other, TextNode):
            return (
                self.text == other.text and
                self.text_type == other.text_type and
                self.url == other.url
            )
        return False

    def __repr__(self):
        return f"TextNode({self.text!r}, {self.text_type.value!r}, {self.url!r})"
