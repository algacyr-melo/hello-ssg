from htmlnode import HTMLNode
from textnode import TextNode, TextType


def main():
    html_node = HTMLNode(
        "a",
        "This is a Link",
        [],
        {
            "href": "https://www.google.com",
            "target": "_blank",
        }
    )
    print(repr(html_node))


main()

