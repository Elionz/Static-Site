import unittest

from textnode import TextNode, TextType
from splitnodes_delimiter import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):

    def test_split_code(self):
        node = TextNode(
            "This is text with a `code block` word",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "`",
            TextType.CODE,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_bold(self):
        node = TextNode(
            "This is **bold** text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "**",
            TextType.BOLD,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_split_italic(self):
        node = TextNode(
            "This is _italic_ text",
            TextType.TEXT,
        )

        new_nodes = split_nodes_delimiter(
            [node],
            "_",
            TextType.ITALIC,
        )

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_unclosed_delimiter(self):
        node = TextNode(
            "This is **bold text",
            TextType.TEXT,
        )

        with self.assertRaises(Exception):
            split_nodes_delimiter(
                [node],
                "**",
                TextType.BOLD,
            )


if __name__ == "__main__":
    unittest.main()