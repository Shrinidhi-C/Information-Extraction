# -*- coding: utf-8 -*-

from .context import DataHolder
from .context import Token
from .context import PreProcessor

import unittest
import os
import glob


class PreProcessorTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_retain_positive_label(self):
        current_file_path = os.path.dirname(__file__)
        dir_name = os.path.join(current_file_path, '../' + 'data/tagged_input/')
        # dir_name = os.path.join(current_file_path, '../' + 'data/B/')
        files = glob.glob(dir_name + '*.txt')
        # files = ['/Users/Maharia/PycharmProjects/StageOne/tests/../data/tagged_input/url_53.txt']
        flag = True
        failed_tuple = []
        total = 0
        file_total = 0
        toks = []
        for file_name in files:
            parser = DataHolder(file_name)
            parser.generate_n_grams()
            PreProcessor.pre_process_data_holder(parser)
            recognized_pos_label = 0
            for token in parser.pre_processed_n_grams:
                if token.label:
                    recognized_pos_label += 1
                    toks.append(token.name)
            with open(file_name) as f:
                data = f.read()
                actual_pos_label = data.count("</Entity>")
                if actual_pos_label != recognized_pos_label:
                    flag = False
                    failed_tuple.append((file_name, actual_pos_label, recognized_pos_label))
                    break
            total += recognized_pos_label
            file_total += actual_pos_label
        for tuple in failed_tuple:
            print tuple[0] + ' ' + str(tuple[1]) + ' ' + str(tuple[2])
        print total
        print file_total
        s = set(toks)
        # print s
        print len(s)
        self.assertTrue(flag)


if __name__ == '__main__':
    unittest.main()
