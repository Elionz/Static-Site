import unittest

from markdown import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    unittest.main()