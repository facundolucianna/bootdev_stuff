from osfunc import clean_and_copy
from pathlib import Path

def main():
    print("Copying static files to public directory")
    clean_and_copy(Path("./static"), Path("./public"))
    print("Done")



main()
