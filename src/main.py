from textnode import TextNode
from htmlnode import HTMLNode

DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./public"

def main():
    new_text_node = TextNode("This is text", "bold", "https://www.boot.dev")
    print(new_text_node)
    new_html_node = HTMLNode("p", "text in paragraph", "gfas", "href")
    print(new_html_node)

main()