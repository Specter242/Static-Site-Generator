from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        a = self.text == other.text
        b = self.text_type == other.text_type
        c = self.url == other.url
        return a and b and c

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    