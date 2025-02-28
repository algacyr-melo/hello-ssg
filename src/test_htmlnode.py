import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(
            node.to_html(), "<p>Hello, world!</p>"
        )

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span></div>"
        )

    def test_to_html_with_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "Italic text"),
                LeafNode(None, "Normal text"),
            ]
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>Italic text</i>Normal text</p>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        self.assertRaises(
            ValueError,
            parent_node.to_html,
        )


if __name__ == "__main__":
    unittest.main()

