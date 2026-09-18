print("hello world")


from textnode import TextNode, TextType


def main():
    node = TextNode("This is some text", TextType.BOLD)
    print(node)


main()

