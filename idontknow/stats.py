from collections import Counter


def obtain_num_words(text):
    return len(text.split())


def number_times_char(text):
    text_list = list(text.lower())  # .split("")

    # temp = tuple(map(lambda x: (x[0], 1), text_list))
    # temp = [word[0] for word in text_list if word]
    output = dict(Counter(text_list))
    return output


def sort_on(dictionary):
    list_dicts = [{"letter": key, "num": value} for key, value in dictionary.items()]

    return list_dicts
