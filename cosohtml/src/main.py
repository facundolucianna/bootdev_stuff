from osfunc import clean_and_copy
from pathlib import Path
from generate_funcs import generate_pages_recursively

def main():
    print("Copying static files to public directory")
    clean_and_copy(Path("./static"), Path("./public"))
    print("Done")

    print("Generating pages recursively")
    generate_pages_recursively(Path("./content"), Path("./template.html"), Path("./public"))
    print("Done")

main()
