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
