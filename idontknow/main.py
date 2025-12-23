import sys

from stats import obtain_num_words, number_times_char, sort_on


def get_book_text(path):
    file_contents = None

    with open(path) as f:
        file_contents = f.read()

    return file_contents


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <path_to_book>")
        sys.exit(1)

    text = get_book_text(sys.argv[1])
    # print(get_book_text("./books/frankenstein.txt"))
    num_words = obtain_num_words(text)
    char_dict = number_times_char(text)
    last_list = sort_on(char_dict)

    print("============ BOOKBOT ============")
    print(f"Analyzing book found at {sys.argv[1]}...")
    print("----------- Word Count ----------")
    print(f"Found {num_words} total words")
    print("--------- Character Count -------")
    for dictionary in last_list:
        letter = dictionary["letter"]
        if letter.isalpha():
            print(f"{letter}: {dictionary['num']}")
    print("============= END ===============")


main()
