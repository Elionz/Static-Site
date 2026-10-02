import re
from enum import Enum

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")

    # Strip whitespace and remove empty blocks
    blocks = [block.strip() for block in blocks]
    blocks = [block for block in blocks if block]

    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    lines = block.split("\n")

    # Heading
    first_space = block.find(" ")
    if 1 <= first_space <= 6:
        prefix = block[:first_space]
        if all(c == "#" for c in prefix):
            return BlockType.HEADING

    # Code
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE

    # Quote
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Unordered list
    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Ordered list
    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH