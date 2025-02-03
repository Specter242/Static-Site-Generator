import re

from textnode import TextType, TextNode


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
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
        
        parts = re.split(r"(\[.*?\]\(.*?\))", node.text)
        for part in parts:
            if re.match(r"\[.*?\]\(.*?\)", part):
                match = re.match(r"\[(.*?)\]\((.*?)\)", part)
                if match:
                    text, url = match.groups()
                    new_nodes.append(TextNode(text, TextType.LINK, url))
            else:
                new_nodes.append(TextNode(part, TextType.TEXT))
    
    return new_nodes

