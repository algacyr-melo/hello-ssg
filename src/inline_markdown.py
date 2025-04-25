import re
from textnode import TextNode, TextType


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


# Recursive approach
def split_node(text, delimiter, text_type, is_delimiter_open=False):
    parts = text.split(delimiter, 1)

    # No delimiter found
    if len(parts) == 1:
        # If we're expecting a closing delimiter but don't find one, that's an error
        if is_delimiter_open:
            raise ValueError(f"No closing delimiter '{delimiter}' found")

        # We don't want nodes with empty texts ""
        if parts[0]:
            return [TextNode(parts[0], TextType.TEXT)]
        return []

    if is_delimiter_open:
        # This is a closing delimiter, create a node with the special text type
        new_node = TextNode(parts[0], text_type)
        # Process the rest as regular text
        remaining_nodes = split_node(parts[1], delimiter, text_type)
    else:
        # This is an opening delimiter, create a regular text node
        new_node = TextNode(parts[0], TextType.TEXT)
        # Process the rest looking for the closing delimiter
        remaining_nodes = split_node(parts[1], delimiter, text_type, True)

    return [new_node] + remaining_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue

        new_nodes = split_node(node.text, delimiter, text_type)
        result.extend(new_nodes)

    return result


def split_nodes_delimiter_iterative(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else: split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_images(old_node.text)

        # Did we extract any images?
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        for image_alt, image_url in matches:
            split_nodes = []

            sections = original_text.split(f"![{image_alt}]({image_url})", 1)

            if len(sections[0]) > 0:
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            new_nodes.extend(split_nodes)

            original_text = sections[-1]
        return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        matches = extract_markdown_links(old_node.text)

        # Did we extract any links?
        if len(matches) == 0:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text
        for link_text, link_url in matches:
            split_nodes = []

            sections = original_text.split(f"[{link_text}]({link_url})", 1)

            if len(sections[0]) > 0:
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            new_nodes.extend(split_nodes)

            original_text = sections[-1]
        return new_nodes

