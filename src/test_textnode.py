import unittest
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://google.com")
        self.assertNotEqual(node, node2)

    def test_url_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode(
                    "image",
                    TextType.IMAGE,
                    "https://i.imgur.com/zjjcJKZ.png",
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image",
                    TextType.IMAGE,
                    "https://i.imgur.com/3elNhQu.png",
                ),
            ],
            new_nodes,
        )


def test_split_image_at_start(self):
    node = TextNode(
        "![image](https://example.com/image.png) followed by text",
        TextType.TEXT,
    )

    self.assertListEqual(
        [
            TextNode(
                "image",
                TextType.IMAGE,
                "https://example.com/image.png",
            ),
            TextNode(" followed by text", TextType.TEXT),
        ],
        split_nodes_image([node]),
    )


def test_split_image_at_end(self):
    node = TextNode(
        "Text before ![image](https://example.com/image.png)",
        TextType.TEXT,
    )

    self.assertListEqual(
        [
            TextNode("Text before ", TextType.TEXT),
            TextNode(
                "image",
                TextType.IMAGE,
                "https://example.com/image.png",
            ),
        ],
        split_nodes_image([node]),
    )


def test_split_adjacent_images(self):
    node = TextNode(
        "![one](https://example.com/one.png)![two](https://example.com/two.png)",
        TextType.TEXT,
    )

    self.assertListEqual(
        [
            TextNode("one", TextType.IMAGE, "https://example.com/one.png"),
            TextNode("two", TextType.IMAGE, "https://example.com/two.png"),
        ],
        split_nodes_image([node]),
    )


def test_split_images_no_images(self):
    node = TextNode("This has no images.", TextType.TEXT)

    self.assertListEqual(
        [node],
        split_nodes_image([node]),
    )


def test_split_images_preserves_non_text_nodes(self):
    node = TextNode("![image](https://example.com/image.png)", TextType.IMAGE)

    self.assertListEqual(
        [node],
        split_nodes_image([node]),
    )


def test_split_links(self):
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )

    self.assertListEqual(
        [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode(
                "to boot dev",
                TextType.LINK,
                "https://www.boot.dev",
            ),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube",
                TextType.LINK,
                "https://www.youtube.com/@bootdotdev",
            ),
        ],
        split_nodes_link([node]),
    )


def test_split_link_at_start(self):
    node = TextNode(
        "[Boot.dev](https://www.boot.dev) is a great site",
        TextType.TEXT,
    )

    self.assertListEqual(
        [
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" is a great site", TextType.TEXT),
        ],
        split_nodes_link([node]),
    )


def test_split_link_at_end(self):
    node = TextNode(
        "Visit [Boot.dev](https://www.boot.dev)",
        TextType.TEXT,
    )

    self.assertListEqual(
        [
            TextNode("Visit ", TextType.TEXT),
            TextNode("Boot.dev", TextType.LINK, "https://www.boot.dev"),
        ],
        split_nodes_link([node]),
    )


def test_split_adjacent_links(self):
    node = TextNode(
        "[one](https://example.com/one)[two](https://example.com/two)",
        TextType.TEXT,
    )

    self.assertListEqual(
        [
            TextNode("one", TextType.LINK, "https://example.com/one"),
            TextNode("two", TextType.LINK, "https://example.com/two"),
        ],
        split_nodes_link([node]),
    )


def test_split_links_no_links(self):
    node = TextNode("This has no links.", TextType.TEXT)

    self.assertListEqual(
        [node],
        split_nodes_link([node]),
    )


def test_split_links_preserves_non_text_nodes(self):
    node = TextNode("some text", TextType.BOLD)

    self.assertListEqual(
        [node],
        split_nodes_link([node]),
    )

def test_text_to_textnodes():
    text = (
        "This is **text** with an _italic_ word and a `code block` "
        "and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) "
        "and a [link](https://boot.dev)"
    )

    assert text_to_textnodes(text) == [
        TextNode("This is ", TextType.TEXT),
        TextNode("text", TextType.BOLD),
        TextNode(" with an ", TextType.TEXT),
        TextNode("italic", TextType.ITALIC),
        TextNode(" word and a ", TextType.TEXT),
        TextNode("code block", TextType.CODE),
        TextNode(" and an ", TextType.TEXT),
        TextNode(
            "obi wan image",
            TextType.IMAGE,
            "https://i.imgur.com/fJRm4Vk.jpeg",
        ),
        TextNode(" and a ", TextType.TEXT),
        TextNode("link", TextType.LINK, "https://boot.dev"),
    ]

if __name__ == "__main__":
    unittest.main()


