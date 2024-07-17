import os


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page at {dest_path} from {from_path} and {template_path}...")
    with open(from_path, "r") as f:
        markdown = f.read()
    
    with open(template_path, "r") as f:
        template = f.read()

    