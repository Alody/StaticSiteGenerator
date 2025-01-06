class HTMLNode:
    def __init__(self, tag= None, value= None, children= None, props= None):
        self.tag = tag
        self.value = value
        self.children = children if children else []
        self.props = props if props else {}

    def to_html(self):
        raise NotImplementedError("child classes must implement the to_html method")

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(f' {key}="{value}"' for key, value in self.props.items())
    
    def __repr__(self):
        children_length = 0 if self.children is None else len(self.children)
        return (
            f"HTMLNode(tag={self.tag}, value={self.value}, "
            f"children={children_length}, props={self.props})"
        )

class LeafNode(HTMLNode): # child with a required value and no children
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError("Error: tag must not be empty")
        if children is None:
            raise ValueError("Error: must have children")
        
        super().__init__(tag, None, children, props)

    def to_html(self):
        le_children = ""
        for child in self.children:
            le_children += child.to_html()
        return f'<{self.tag}{self.props_to_html()}>{le_children}</{self.tag}>'