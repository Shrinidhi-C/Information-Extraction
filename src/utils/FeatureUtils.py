import re


# from src.preprocessor.PreProcessor import ends_with_delimiter, starts_with_delimiter


def starts_with_capital(input_string):
    return bool_to_int(input_string[0].isupper())


def all_words_caps(input_string):
    rv = True
    for string in input_string.split():
        if not string[0].isupper():
            rv = False
            break
    return bool_to_int(rv)


def number_of_words(input_string):
    return len(input_string.split())


def next_word_caps(fileparser, token):
    rv = False
    if token.hasAfter:
        rv = fileparser.file_content[token.content_index + 1].name[0].isupper()
    return bool_to_int(rv)


def previous_word_ends_with_punctuation(file_parser, token):
    rv = False
    if token.hasBefore:
        previous_index = token.content_index - 1
        previous_token = file_parser.file_content[previous_index]
        rv = previous_token.name.endswith(",")
        rv = rv or previous_token.name.endswith(";")
        rv = rv or previous_token.name.endswith(":")
    return bool_to_int(rv)


def previous_word_ends_with_dot(file_parser, token):
    rv = False
    if token.hasBefore:
        previous_index = token.content_index - 1
        previous_token = file_parser.file_content[previous_index]
        rv = previous_token.name.endswith(".")
    return bool_to_int(rv)


def check_prefix(fileparser, token, prefix_list, prefix_count):
    rv = False
    index = token.content_index
    while token.hasBefore and prefix_count > 0 and rv is False:
        index = index - 1
        token = fileparser.file_content[index]
        prefix_count = prefix_count - 1
        for prefix in prefix_list:
            # name = sanitize_name(token.name)
            name = token.name
            if name.lower() == prefix:
                rv = True
                break
    return bool_to_int(rv)


def ends_with_roman_numeral(token):
    words = token.name.split()
    flag = False
    regex = re.compile("^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$")
    if regex.search(words[-1]):
        flag = True
    return bool_to_int(flag)


def check_postfix(fileparser, token, postfix_list, postfix_count):
    rv = False
    index = token.content_index
    while token.hasAfter and postfix_count > 0 and rv is False:
        index = index + len(token.name.split())
        token = fileparser.file_content[index]
        postfix_count = postfix_count - 1
        for postfix in postfix_list:
            name = token.name
            if name.lower() == postfix:
                rv = True
                break

    return bool_to_int(rv)


def has_single_letter_word_abbrevation(token):
    words = token.name.split()
    rv = False
    for i in range(1, len(words) - 1):
        if len(words[i]) == 2 and words[i].endswith("."):
            rv = True
            break
    return bool_to_int(rv)


def bool_to_int(bool_value):
    if bool_value:
        return 1
    return 0
