# coding=utf-8
"""DataHolder.py: To parse a input file into tokens and store to content list first.
Use the content list to form the words."""

__author__ = "Ankit Maharia"

import codecs

from src.PreProcessor import title_list, pronoun_list, article_list, occupation_list, verbs_list
from src.Token import Token
from src.utils.FeatureUtils import *


class DataHolder:
    file_name = None
    file_content = None
    n_grams = None
    pre_processed_n_grams = None

    def __init__(self, file_name):
        self.n_grams = None
        self.file_name = file_name
        line_number = 1
        with codecs.open(self.file_name, encoding='utf-8') as f:
            self.file_content = list()
            # print self.file_name
            for line in f:
                self.__parse_line(line, line_number)
                line_number += 1

    def generate_n_grams(self, max_length=4):
        self.n_grams = list()
        for look_ahead in range(1, max_length + 1):
            num_tokens = len(self.file_content)
            for start_index in range(0, num_tokens):
                end_index = start_index + look_ahead
                if end_index > num_tokens:
                    break
                else:
                    # print start_index
                    # TODO: Need to account for punctuation rules
                    concatenated_token = Token.clone(self.file_content[start_index])
                    flag = True
                    for i in range(start_index + 1, end_index):
                        if not concatenated_token.hasAfter:
                            flag = False
                            break
                        concatenated_token.update(self.file_content[i])
                    if flag:
                        self.n_grams.append(concatenated_token)

    def set_pre_processed(self, pre_processed):
        self.pre_processed_n_grams = pre_processed

    def printContent(self):
        str = ''
        for token in self.file_content:
            str += ' ' + token.name
        print str

    def printTokens(self):
        for token in self.n_grams:
            # if token.label:
            print str(token.lineNumber) + ' ' + token.name + ' ' + str(token.hasAfter)

    def __parse_line(self, line, line_number):
        column_number = 1
        current_word = ''
        chars = list(line)
        has_before = False
        has_after = True
        for ch in chars:
            if ch == u'\u201c' or ch == u'\u201d':  # utf-8 to ascii quote
                ch = '\"'
            elif ch == u'\u2019':  # utf 8 to ascii '
                ch = '\''
            if ch == '\n':
                has_after = False
            if ch != ' ' and ch != '\n':
                current_word += ch
            else:
                column_number = self.add_word(column_number, current_word, line_number, has_before, has_after)
                has_before = True
                current_word = ''
            column_number += 1
        self.add_word(column_number, current_word, line_number, has_before, has_after)

    def add_word(self, column_number, current_word, line_number, has_before, has_after):
        if len(current_word) != 0:
            token = self.create_token(column_number, current_word, line_number, has_before, has_after)
            self.file_content.append(token)
            column_number = token.endPosition
        return column_number

    def create_token(self, column_number, current_word, line_number, has_before, has_after):
        return Token(current_word, self.file_name, line_number, column_number - len(current_word), column_number,
                     has_before, has_after, len(self.file_content))

    def vectorize(self):
        rv = []
        # Feature 12: Preposition(negative) --> need to check
        for token in self.pre_processed_n_grams:
            current_vector = list()
            current_vector.append(starts_with_capital(token.name))  # Feature: Starts with capital
            current_vector.append(all_words_caps(token.name))  # Feature: All word in the token starts with capital
            current_vector.append(next_word_caps(self, token))  # Feature: Next word starts with capital
            current_vector.append(bool_to_int(token.ends_with_apostrophes))  # Feature: Has 's in the end
            current_vector.append(bool_to_int(token.starts_with_quotes))  # Feature: Starts with quote
            current_vector.append(bool_to_int(token.ends_with_quotes))  # Feature: ends with quote
            current_vector.append(previous_word_ends_with_punctuation(self, token))  # Feature: previous word has ,:;
            current_vector.append(previous_word_ends_with_dot(self, token))  # Feature: previous word has .
            current_vector.append(
                has_single_letter_word_abbrevation(token))  # Feature: Token has single word with a dot George W. Bush
            current_vector.append(check_prefix(self, token, article_list, 3))  # Feature: token has article before it
            current_vector.append(check_prefix(self, token, pronoun_list, 3))  # Feature: token has pronoun before it
            current_vector.append(check_prefix(self, token, title_list, 1))  # Feature: token has a title before it
            current_vector.append(
                check_prefix(self, token, occupation_list, 3))  # Feature: token has a occupation before it
            current_vector.append(ends_with_roman_numeral(token))  # Feature : token ends with a roman numeral
            current_vector.append(check_postfix(self, token, pronoun_list, 3))  # Feature: pronoun in vicinity
            current_vector.append(check_postfix(self, token, verbs_list, 1))  # Feature: verbs in vicinity
            current_vector.append(bool_to_int(token.label))  # Label of the data point
            rv.append(current_vector)
            # print token.documentId + ':' + str(token.lineNumber) + ' ' + token.name + ' ' + ''.join(
            #     str(e) for e in current_vector)
        return rv


if __name__ == '__main__':
    p = DataHolder('/Users/Maharia/PycharmProjects/StageOne/tests/../data/tagged_input/url_68.txt')
    p.printContent()
    # p.printTokens()
