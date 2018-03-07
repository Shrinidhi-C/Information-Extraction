# coding=utf-8
import glob
import os
import sys

from src import PreProcessor
from src.Classifiers import *
from src.DataHolder import DataHolder
from scipy.stats import itemfreq


class Driver:
    def print_label_counts(self, file_parsers):
        pos_count = 0
        neg_count = 0
        for fp in file_parsers:
            pre_processed_n_grams = fp.pre_processed_n_grams
            for token in pre_processed_n_grams:
                if token.label:
                    pos_count += 1
                else:
                    neg_count += 1
        print 'Positive label count: ' + str(pos_count)
        print 'Negative label count: ' + str(neg_count)

    def __init__(self, dev_mode=True):
        self.dev_mode = dev_mode
        current_file_path = os.path.dirname(__file__)
        self.train_location = os.path.join(current_file_path, '../data/I/')
        self.test_location = os.path.join(current_file_path, '../data/J/')

    def run(self, max_length=4):
        files = glob.glob(self.train_location + '*.txt')
        train_file_parsers = self.get_parsed_files(files, max_length)
        # self.print_label_counts(train_file_parsers)
        x_train, y_train = self.get_features(train_file_parsers)

        classifier = Classifiers()
        if self.dev_mode:
            classifier.run_all_classifiers(x_train, y_train)

        if not self.dev_mode:
            files = glob.glob(self.test_location + '*.txt')
            test_file_parsers = self.get_parsed_files(files, max_length)
            # self.print_label_counts(test_file_parsers)
            x_test, y_test = self.get_features(test_file_parsers)
            stats = classifier.decision_tree(x_train, y_train, x_test, y_test)
            print 'Precision: ' + str(stats[0])
            print 'Recall: ' + str(stats[1])
            print 'FScore: ' + str(stats[2])

    def get_parsed_files(self, files, max_length):
        file_parsers = []
        for file_path in files:
            fp = DataHolder(file_path)
            fp.generate_n_grams(max_length)
            PreProcessor.pre_process_data_holder(fp)
            file_parsers.append(fp)
        return file_parsers

    def get_features(self, file_parsers):
        x_train = list()
        for fp in file_parsers:
            vectorize = fp.vectorize()
            x_train.extend(vectorize)

        np_array = np.asarray(x_train)
        x = np.delete(np_array, -1, axis=1)
        y = np_array[:, -1]
        # print itemfreq(y)
        return x, y


if __name__ == '__main__':
    cmd_args = sys.argv
    if len(cmd_args) != 2:
        print 'Expects command line argument as true or false'
    dev_mode_str = sys.argv[1]
    dev_mode = True
    if dev_mode_str == "false":
        dev_mode = False
    Driver(dev_mode).run()
