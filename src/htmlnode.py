from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props != None:
            a = ""
            for i in self.props:
                a = a + f' {i}="{self.props[i]}"'
            return a
        else:
            return ""
    
    def __repr__(self):
        return f"HTMLNode(tag:{self.tag}, value:{self.value}, children:{self.children}, props:{self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        elif self.tag == None:
            return self.value
        elif self.tag == "img":
            return f"<{self.tag}{self.props_to_html()}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.children == None:
            raise ValueError("missing child")
        if self.tag == None:
            raise ValueError("missing tag")
        else:
            a = ""
            for child in self.children:
                a += child.to_html()
            return f"<{self.tag}{self.props_to_html()}>{a}</{self.tag}>"
            
#text_node = TextNode("something", TextType.TEXT)
#print(vars(text_node))

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        props = {"href": text_node.url}
        return LeafNode("a", text_node.text, props)
    if text_node.text_type == TextType.IMAGE:
        props = {"src": text_node.url, "alt": "image"}
        return LeafNode("img", "", props)
    else:
        raise ValueError("cannot create html node.  improper text type.")
