CS 839 (Stage One)
========================

Setup:
    - run make to fetch all dependencies

    - get nosetests (should be done via make but OSX has few issues and is recommended to install via easy_install
    instead of pip. Follow: https://stackoverflow.com/questions/32546228/installed-nose-but-cannot-use-on-command-line)

    - [OPTIONAL] run python setup.py install to install the repo in your path

    - to run test cases: type make test

To Run:
    - If in dev mode:
        * ./run.sh true
        * sh run.sh true
        This implies that documents from I folder will be read and Cross Validation and statistics of different models will get printed. And one can see the best model to select from the reported average precision, fscore and recall.
    - If not is dev mode(want to run on test data):
        * ./run.sh false
        * sh run.sh false
        This implies that the documents from I will be used for training and testing will be done on set J to report the precision, recall and fscore.
    - true/false signifies if you want to run the code in dev-mode or not
    - sh commands will be useful if the file executable permissions are not maintained while cloning or extracting the repository.

- Entry point for the code:
    src/StageOneDriver.py