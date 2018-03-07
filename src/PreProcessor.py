"""PreProcessor.py: To parse a input file into tokens and store to content list first.
Use the content list to form the words."""

import os
from src.Token import Token

comma = ","
quotes = "\""
dot = "."
apostrophe = "\'s"


def pre_process_data_holder(data_holder):
    n_grams = data_holder.n_grams
    cleaned_token_list = clean(n_grams)
    data_holder.set_pre_processed(prune(cleaned_token_list))


def clean(token_list):
    # type: (list(Token)) -> list(Token)
    for token in token_list:

        # cleaning quotes
        if starts_with_delimiter(token, quotes):
            token.starts_with_quotes = True
            token.name = token.name[1:]
        if ends_with_delimiter(token, quotes):
            token.ends_with_quotes = True
            token.name = token.name[:-1]

        # cleaning dot
        if ends_with_delimiter(token, dot):
            token.name = token.name[:-1]
            token.ends_with_dot = True

        # cleaning apostrophe
        if ends_with_delimiter(token, apostrophe):
            token.name = token.name[:-2]
            token.ends_with_apostrophes = True

        # cleaning comma
        if ends_with_delimiter(token, comma):
            token.name = token.name[:-1]
            token.ends_with_comma = True

        # cleaning braces
        if '[' in token.name or ']' in token.name:
            token.name = token.name.replace('[', '')
            token.name = token.name.replace(']', '')

    return token_list


def starts_with_delimiter(token, delimit):
    if token.name.startswith(delimit):
        return True
    return False


def ends_with_delimiter(token, delimit):
    if token.name.endswith(delimit):
        return True
    return False


def prune(tokens):
    # type: (list(Token)) -> list(Token)
    rv = list()
    for token in tokens:
        flag = should_prune(token, article_list)
        flag = flag or should_prune(token, title_list)
        flag = flag or should_prune(token, occupation_list)
        flag = flag or should_prune(token, pronoun_list)
        flag = flag or should_prune(token, places_list)
        flag = flag or should_prune(token, stop_words_list)
        flag = flag or contains_delimiter(token, comma)
        flag = flag or contains_delimiter(token, quotes)
        flag = flag or should_prune_becoz_whitespace(token)
        if flag is False:
            rv.append(token)
        # if flag is True and token.label:
        #     print token.documentId + ':' + str(token.lineNumber) + ':' + token.name
    return rv


def contains_delimiter(token, delimiter):
    if delimiter in token.name:
        return True
    return False

def should_prune_becoz_whitespace(token):
    import re
    name = re.sub(r"\s+", "", token.name, flags=re.UNICODE)
    if len(name) == 0:
        return True
    return False


def should_prune(token, filter_file):
    if token is None:
        return True
    token_value = token.name.lower()
    if len(token_value) == 0:
        return True
    for word in token_value.split():
        if word in filter_file:
            return True
    return False


def load_file_data(file_name):
    current_file_path = os.path.dirname(__file__)
    full_path = os.path.join(current_file_path, '../data/helper/' + file_name)
    rv = list()
    with open(full_path) as f:
        for word in f:
            rv.append(word.split('\n')[0].lower())
    return rv


stop_words_list = load_file_data('stopwords.txt')
places_list = load_file_data('places.txt')
article_list = load_file_data('articles.txt')
title_list = load_file_data('title.txt')
occupation_list = load_file_data('occupation.txt')
verbs_list = load_file_data('verbs.txt')
pronoun_list = load_file_data('pronoun.txt')
