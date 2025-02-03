import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    if old_nodes is None:
        return new_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown syntax: unpaired delimiter")
        
        for i, part in enumerate(parts):
            if part == "":
                if i % 2 == 1:
                    raise Exception("Invalid markdown syntax: empty delimiter")
                continue  # Skip empty text between delimiters
            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))
    
         # Add an empty TextNode if the last part is a delimiter
        if node.text.endswith(delimiter):
            new_nodes.append(TextNode("", TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    if old_nodes is None:
        return new_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        
        parts = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        for i, part in enumerate(parts):
            if i % 3 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            elif i % 3 == 1:
                new_nodes.append(TextNode("", TextType.IMAGE, images[i // 3][1]))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    if old_nodes is None:
        return new_nodes
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        
        parts = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
        for i, part in enumerate(parts):
            if i % 4 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            elif i % 4 == 1:
                new_nodes.append(TextNode("", TextType.LINK, links[i // 4][1]))
            elif i % 4 == 2:
                new_nodes[-1].text = part  # Update the text of the last added link node

    return new_nodes