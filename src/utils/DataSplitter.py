import glob
import os
import random
from shutil import copy2

RANDOM_SEED = 5

SET_B_RELATIVE_PREFIX = 'data/B/'
SET_I_RELATIVE_PREFIX = 'data/I/'
SET_J_RELATIVE_PREFIX = 'data/J/'


def copy_files(from_files, to_dir):
    if any(File.endswith(".txt") for File in os.listdir(".")):
        print 'The destination folder: ' + to_dir + ' already has content. Aborting!!'
    else:
        for file in from_files:
            copy2(file, to_dir)


def get_files_split(files_to_split):
    partition_size = (len(files_to_split)) / 3
    random.Random(RANDOM_SEED).shuffle(files_to_split)
    return files_to_split[: partition_size * 2], files_to_split[2 * partition_size:]


def get_all_files(dir_name, extension='.txt'):
    return glob.glob(dir_name + '*' + extension)


def get_full_path(relative_path):
    current_file_path = os.path.dirname(__file__)
    return os.path.join(current_file_path, '../../' + relative_path)


if __name__ == '__main__':
    dir_B_path = get_full_path(SET_B_RELATIVE_PREFIX)
    all_files = get_all_files(dir_B_path)
    print len(all_files)
    set_I_files, set_J_files = get_files_split(all_files)
    copy_files(set_I_files, get_full_path(SET_I_RELATIVE_PREFIX))
    copy_files(set_J_files, get_full_path(SET_J_RELATIVE_PREFIX))
