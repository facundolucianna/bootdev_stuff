from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold_text"
    ITALIC = "italic_text"
    CODE = "code_text"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, o):
        bool_1 = self.text == o.text
        bool_2 = self.text_type = o.text_type
        bool_3 = self.url == o.url

        return bool_1 and bool_2 and bool_3

    def __repr__(self):
        repres = f"TextNode({self.text}, {self.text_type.value}"
        if self.url:
            repres += f", {self.url}"
        return repres + ")"
