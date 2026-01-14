class HtmlNode:
    def __init__(self, tag: str | None = None, 
                 value: str | None = None, 
                 children: list | None = None, 
                 props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HtmlNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        if len(self.props) == 0:
            return ""

        output = " ".join([f'{key}="{value}"' for key, value in self.props.items()])
        
        return " " + output


class LeafNode(HtmlNode):
    def __init__(self, tag: str | None, 
                 value: str, 
                 props: dict | None = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("Value cannot be None")
        if not self.tag:
            return self.value

        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"


class ParentNode(HtmlNode):
    def __init__(self, tag: str, 
                 children: list, 
                 props: dict | None = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag cannot be None")
        
        if self.children is None or len(self.children) == 0:
            raise ValueError("Children cannot be None")
        
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{''.join([child.to_html() for child in self.children])}</{self.tag}>"