# -*- coding: utf-8 -*-

from .context import DataHolder
from .context import Token
from .context import PreProcessor

import unittest
import os
import glob


class FileParserTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_instantiation(self):
        current_file_path = os.path.dirname(__file__)
        file_name = os.path.join(current_file_path, '../' + 'data/tagged_input/url_1.txt')
        self.assertIsNotNone(DataHolder(file_name))

    def test_has_no_entity(self):
        current_file_path = os.path.dirname(__file__)
        dir_name = os.path.join(current_file_path, '../' + 'data/tagged_input/')
        # dir_name = os.path.join(current_file_path, '../' + 'data/B/')
        files = glob.glob(dir_name + '*.txt')
        # files=['/Users/Maharia/PycharmProjects/StageOne/tests/../data/tagged_input/url_63.txt']
        flag = True
        failed_files = []
        for file_name in files:
            parser = DataHolder(file_name)
            for token in parser.file_content:
                # print token.name
                if "Entity" in token.name:
                    failed_files.append(file_name)
                    flag = False
                    break
        for failed_file in failed_files:
            print failed_file
            self.assertTrue(flag)

    def test_positive_label(self):
        current_file_path = os.path.dirname(__file__)
        # dir_name = os.path.join(current_file_path, '../' + 'data/tagged_input/')
        dir_name = os.path.join(current_file_path, '../' + 'data/J/')
        files = glob.glob(dir_name + '*.txt')
        flag = True
        failed_tuple = []
        total_pos_labe = 0
        b_counts = {}
        t_counts = {}
        for file_name in files:
            base_file_name = os.path.basename(file_name)
            parser = DataHolder(file_name)
            parser.generate_n_grams()
            recognized_pos_label = 0
            for token in parser.n_grams:
                if token.label:
                    recognized_pos_label += 1
            with open(file_name) as f:
                data = f.read()
                actual_pos_label = data.count("</Entity>")
                if actual_pos_label != recognized_pos_label:
                    flag = False
                    failed_tuple.append((file_name, actual_pos_label, recognized_pos_label))
                    break
            total_pos_labe += recognized_pos_label
            '''file_toks = base_file_name.split("_")
            t_file_name_orig = file_toks[0] + '_' + file_toks[1] + '.txt'
            t_file_name = os.path.join(current_file_path, '../' + 'data/tagged_input/' + t_file_name_orig)
            if t_file_name_orig not in t_counts:
                with open(t_file_name) as f:
                    data = f.read()
                    actual_pos_label = data.count("</Entity>")
                    t_counts[t_file_name_orig] = actual_pos_label
            existing = 0
            if t_file_name_orig in b_counts:
                existing = b_counts[t_file_name_orig]
            b_counts[t_file_name_orig] = existing + recognized_pos_label
            total_pos_labe += recognized_pos_label

        for key in t_counts:
            if t_counts[key]!=b_counts[key]:
                print key
                break'''

        print 'Total Marked Labels are: ' + str(total_pos_labe)
        # s = set(pos_tokens)
        # print s
        # print len(s)
        for tuple in failed_tuple:
            print tuple[0] + ' ' + str(tuple[1]) + ' ' + str(tuple[2])
        self.assertTrue(flag)

    def test_notest(self):
        file_name = '/Users/Maharia/PycharmProjects/StageOne/data/I/url_1_1.txt'
        parser = DataHolder(file_name)
        parser.generate_n_grams()
        # for tok in parser.


if __name__ == '__main__':
    unittest.main()
