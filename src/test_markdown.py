import unittest

from markdown import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
)
from textnode import markdown_to_html_node


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


class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is a paragraph."),
            BlockType.PARAGRAPH,
        )

    def test_heading(self):
        self.assertEqual(
            block_to_block_type("# Heading"),
            BlockType.HEADING,
        )
        self.assertEqual(
            block_to_block_type("###### Heading"),
            BlockType.HEADING,
        )

    def test_invalid_heading(self):
        self.assertEqual(
            block_to_block_type("####### Heading"),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        self.assertEqual(
            block_to_block_type("```\nprint('hello')\n```"),
            BlockType.CODE,
        )

    def test_quote(self):
        self.assertEqual(
            block_to_block_type("> first\n> second"),
            BlockType.QUOTE,
        )

    def test_unordered_list(self):
        self.assertEqual(
            block_to_block_type("- first\n- second"),
            BlockType.UNORDERED_LIST,
        )

    def test_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first\n2. second\n3. third"),
            BlockType.ORDERED_LIST,
        )

    def test_ordered_list_must_start_at_one(self):
        self.assertEqual(
            block_to_block_type("2. first\n3. second"),
            BlockType.PARAGRAPH,
        )

    def test_ordered_list_must_increment(self):
        self.assertEqual(
            block_to_block_type("1. first\n3. second"),
            BlockType.PARAGRAPH,
        )


class TestMarkdownToHTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading one

### Heading with **bold**
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading one</h1><h3>Heading with <b>bold</b></h3></div>",
        )

    def test_quote(self):
        md = """
> This is a quote
> with _two_ lines
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <i>two</i> lines</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- item one
- item **two**
- item `three`
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ul><li>item one</li><li>item <b>two</b></li><li>item <code>three</code></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. first
2. second with _italic_
3. third
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first</li><li>second with <i>italic</i></li><li>third</li></ol></div>",
        )

    def test_mixed_document(self):
        md = """
# Title

A paragraph with a [link](https://example.com).

- one
- two
"""
        html = markdown_to_html_node(md).to_html()
        self.assertEqual(
            html,
            '<div><h1>Title</h1><p>A paragraph with a <a href="https://example.com">link</a>.</p><ul><li>one</li><li>two</li></ul></div>',
        )


if __name__ == "__main__":
    unittest.main()