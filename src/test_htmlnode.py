import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"'
        )

    def test_props_to_html_child(self):
        child_node = HTMLNode(
            "a",
            "Visit Boot.dev website!",
            None,
            {"href": "https://boot.dev", "target": "_blank"},
        )
        parent_node = HTMLNode(
            "div",
            "Static Site Generator!",
            child_node,
            {"class": "container"},
        )
        self.assertEqual(
            child_node.props_to_html(),
            ' href="https://boot.dev" target="_blank"'
        )
        self.assertEqual(
            parent_node.props_to_html(),
            ' class="container"'
        )

    def test_props_to_html_none(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            None,
        )
        self.assertEqual(
            node.props_to_html(),
            ""
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish you were here"
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish you were here",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )


    def test_repr(self):
        node = HTMLNode(
            "p",
            "Why frontend sucks?",
            None,
            {"class": "text"}
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Why frontend sucks?, children: None, {'class': 'text'})",
        )


if __name__ == "__main__":
    unittest.main()

