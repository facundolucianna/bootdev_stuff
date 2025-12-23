from textnode import TextNode, TextType


def main():
    new_obj = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(new_obj)


main()
