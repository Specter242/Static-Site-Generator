from textnode import TextNode, TextType
from blocks import markdown_to_html_node
import os
import shutil

def main():
    current_dir = os.path.dirname(__file__)  # gets the src directory
    parent_dir = os.path.dirname(current_dir)  # goes up one level to project root
    source = os.path.join(parent_dir, "static")
    destination = os.path.join(parent_dir, "public")
    content = os.path.join(parent_dir, "content")
    print(f"Current directory: {current_dir}")
    print(f"Parent directory: {parent_dir}")
    print(f"Source directory: {source}")
    print(f"Content directory: {content}")
    print(f"Destination directory: {destination}")
    copyall(source, destination)
    generate_page(os.path.join(content, "index.md"), os.path.join(parent_dir, "template.html"), os.path.join(destination, "index.html"))

def copyall(source, destination):
    if not os.path.exists(source):
        print("Source does not exist")
        return
        
    # If destination exists, remove it and its contents
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    # Create the destination directory
    os.makedirs(destination)  # Using makedirs instead of mkdir to create parent dirs if needed
    
    # Now copy the files and directories
    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        
        if os.path.isdir(source_path):
            copyall(source_path, dest_path)
        else:
            shutil.copy2(source_path, dest_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No H1 title found in the markdown file.")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")
    with open(from_path, "r") as file:
        markdown = file.read()
    with open(template_path, "r") as template_file:
        template = template_file.read()
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    html_title = extract_title(markdown)
    final_html = template.replace("{{ Title }}", html_title).replace("{{ Content }}", html)
    with open(dest_path, "w") as output_file:
        output_file.write(final_html)

main()