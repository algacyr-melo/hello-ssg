from textnode import TextNode, TextType


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

