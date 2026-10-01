import unittest

from markdown import extract_markdown_images, extract_markdown_links, markdown_to_blocks
from textnode import TextNode, TextType


class TestMarkdown(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )

        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png")],
            matches,
        )

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "![cat](https://example.com/cat.png) "
            "and ![dog](https://example.com/dog.jpg)"
        )

        self.assertListEqual(
            [
                ("cat", "https://example.com/cat.png"),
                ("dog", "https://example.com/dog.jpg"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://www.boot.dev)"
        )

        self.assertListEqual(
            [("link", "https://www.boot.dev")],
            matches,
        )

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "[Boot.dev](https://www.boot.dev) "
            "[YouTube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertListEqual(
            [
                ("Boot.dev", "https://www.boot.dev"),
                ("YouTube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_links_dont_include_images(self):
        matches = extract_markdown_links(
            "![image](https://example.com/image.png) "
            "[link](https://example.com)"
        )

        self.assertListEqual(
            [("link", "https://example.com")],
            matches,
        )


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_markdown(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_excessive_newlines(self):
        md = """
# Heading


This is a paragraph.



- Item 1
- Item 2
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph.",
                "- Item 1\n- Item 2",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        md = "  # Heading  \n\n  Some paragraph  "
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# Heading",
                "Some paragraph",
            ],
        )

if __name__ == "__main__":
    unittest.main()