from copystatic import copy_static
from generate_page import generate_page


def main():
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


main()