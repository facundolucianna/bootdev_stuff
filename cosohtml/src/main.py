from osfunc import clean_and_copy
from pathlib import Path
from generate_funcs import generate_pages_recursively
import sys 

def main():
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print(f"Using basepath: {basepath}")

    print("Copying static files to public directory")
    clean_and_copy(Path("static"), Path("docs"))
    print("Done")

    print("Generating pages recursively")
    generate_pages_recursively(Path("content"), Path("template.html"), Path("docs"), basepath)
    print("Done")

main()
