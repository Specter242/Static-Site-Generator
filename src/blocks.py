from htmlnode import HTMLNode, text_node_to_html_node
from inline_process import text_to_textnodes

def markdown_to_blocks(markdown):
    blocks = []
    blocks = markdown.split("\n\n")
    blocks = [block.strip() for block in blocks if block.strip()]
    return blocks

def block_to_block_type(block):
    if block.startswith("#"):
        heading_level = len(block.split(" ")[0])
        return f"HEADING_{heading_level}"
    elif block.startswith("```") and block.endswith("```"):
        return "CODE"
    elif block.startswith(">"):
        return "QUOTE"
    elif block.startswith("* ") or block.startswith("- "):
        return "UNORDERED_LIST"
    elif block.startswith("1. "):
        return "ORDERED_LIST"
    else:
        return "PARAGRAPH"
    
def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = [HTMLNode("text", node.text) for node in nodes]
    return children

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type.startswith("HEADING"):
            heading_level = block_type.split("_")[1]
            children.append(HTMLNode(f"h{heading_level}", text_to_children(block[heading_level + 1:].strip())))
        elif block_type == "CODE":
            children.append(HTMLNode("pre", [HTMLNode("code", text_to_children(block[3:-3].strip()))]))
        elif block_type == "QUOTE":
            children.append(HTMLNode("blockquote", text_to_children(block[2:].strip())))
        elif block_type == "UNORDERED_LIST":
            items = block.split("\n")
            children.append(HTMLNode("ul", [HTMLNode("li", text_to_children(item[2:].strip())) for item in items]))
        elif block_type == "ORDERED_LIST":
            items = block.split("\n")
            children.append(HTMLNode("ol", [HTMLNode("li", text_to_children(item[3:].strip())) for item in items]))
        else:
            children.append(HTMLNode("p", text_to_children(block)))
    return HTMLNode("div", children)