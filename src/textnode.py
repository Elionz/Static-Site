from enum import Enum
from htmlnode import HTMLNode, LeafNode
from markdown import (
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
)


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)

    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)

    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        return LeafNode(
            "img",
            "",
            {"src": text_node.url, "alt": text_node.text},
        )

    raise Exception(f"Invalid text type: {text_node.text_type}")


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        images = extract_markdown_images(old_node.text)

        if not images:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        for image_alt, image_link in images:
            image_markdown = f"![{image_alt}]({image_link})"
            sections = original_text.split(image_markdown, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(
                TextNode(image_alt, TextType.IMAGE, image_link)
            )

            original_text = sections[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        links = extract_markdown_links(old_node.text)

        if not links:
            new_nodes.append(old_node)
            continue

        original_text = old_node.text

        for link_text, link_url in links:
            link_markdown = f"[{link_text}]({link_url})"
            sections = original_text.split(link_markdown, 1)

            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(
                TextNode(link_text, TextType.LINK, link_url)
            )

            original_text = sections[1]

        if original_text:
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            lines = block.split("\n")
            text = " ".join(lines)
            children = text_to_children(text)

            block_node = HTMLNode(
                "p",
                None,
                children,
                None,
            )

        elif block_type == BlockType.HEADING:
            first_space = block.find(" ")
            level = first_space

            text = block[first_space + 1:]
            children = text_to_children(text)

            block_node = HTMLNode(
                f"h{level}",
                None,
                children,
                None,
            )

        elif block_type == BlockType.CODE:
            lines = block.split("\n")
            code = "\n".join(lines[1:-1]) + "\n"

            text_node = TextNode(code, TextType.TEXT)
            code_html_node = text_node_to_html_node(text_node)

            code_node = HTMLNode(
                "code",
                None,
                [code_html_node],
                None,
            )

            block_node = HTMLNode(
                "pre",
                None,
                [code_node],
                None,
            )

        elif block_type == BlockType.QUOTE:
            lines = block.split("\n")
            text = "\n".join(line[1:].lstrip() for line in lines)
            children = text_to_children(text)

            block_node = HTMLNode(
                "blockquote",
                None,
                children,
                None,
            )

        elif block_type == BlockType.UNORDERED_LIST:
            lines = block.split("\n")
            children = []

            for line in lines:
                text = line[2:]
                item_children = text_to_children(text)

                children.append(
                    HTMLNode(
                        "li",
                        None,
                        item_children,
                        None,
                    )
                )

            block_node = HTMLNode(
                "ul",
                None,
                children,
                None,
            )

        elif block_type == BlockType.ORDERED_LIST:
            lines = block.split("\n")
            children = []

            for line in lines:
                text = line[line.find(".") + 2:]
                item_children = text_to_children(text)

                children.append(
                    HTMLNode(
                        "li",
                        None,
                        item_children,
                        None,
                    )
                )

            block_node = HTMLNode(
                "ol",
                None,
                children,
                None,
            )

        else:
            raise ValueError(f"Invalid block type: {block_type}")

        block_nodes.append(block_node)

    return HTMLNode(
        "div",
        None,
        block_nodes,
        None,
    )