from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import linear_model
from sklearn.model_selection import KFold
import numpy as np
from sklearn.metrics import classification_report, precision_recall_fscore_support

DTREE = 'DTREE'
RF = 'RF'
SVM = 'SVM'
LIR = 'LIR'
LOR = 'LOR'


class Classifiers:
    # def __init__(self, tokens):
    def __init__(self, debug=True):
        self.debug = debug
        self.dtree = None
        self.rf = None
        self.svm = None
        self.lir = None
        self.lor = None

    def run_all_classifiers(self, x, y):
        kf = KFold(n_splits=5, shuffle=True, random_state=723)
        dtree_stats = []
        rf_stats = []
        svm_stats = []
        lir_stats = []
        lor_stats = []

        for train_index, test_index in kf.split(x):
            x_train, x_test = x[train_index], x[test_index]
            y_train, y_test = y[train_index], y[test_index]
            dtree_stats.append(self.decision_tree(x_train, y_train, x_test, y_test))
            rf_stats.append(self.random_forest(x_train, y_train, x_test, y_test))
            svm_stats.append(self.svm_model(x_train, y_train, x_test, y_test))
            lir_stats.append(self.linear_regression(x_train, y_train, x_test, y_test))
            lor_stats.append(self.logistic_regression(x_train, y_train, x_test, y_test))
        print DTREE
        self.print_avg_stats(dtree_stats)
        print RF
        self.print_avg_stats(rf_stats)
        print SVM
        self.print_avg_stats(svm_stats)
        print LIR
        self.print_avg_stats(lir_stats)
        print LOR
        self.print_avg_stats(lor_stats)

    def print_avg_stats(self, classifier_stats):
        count = 0
        precision = 0
        recall = 0
        fscore = 0
        for val in classifier_stats:
            count += 1
            precision += val[0]
            recall += val[1]
            fscore += val[2]
        print 'Precision: ' + str(precision / count)
        print 'Recall: ' + str(recall / count)
        print 'Fscore: ' + str(fscore / count)

    # TODO: Import feature and pass to it

    def decision_tree(self, x_train=None, y_train=None, x_test=None, y_test=None):
        if x_train is not None:
            self.dtree = tree.DecisionTreeClassifier()
            self.dtree.fit(x_train, y_train)
        if x_test is not None:
            predictions = self.dtree.predict(x_test)
            stats = precision_recall_fscore_support(y_test, predictions, labels=[1])
            return (stats[0][0], stats[1][0], stats[2][0])

    def random_forest(self, x_train=None, y_train=None, x_test=None, y_test=None):
        if x_train is not None:
            self.rf = RandomForestClassifier(n_estimators=10)
            self.rf.fit(x_train, y_train)
        if x_test is not None:
            predictions = self.rf.predict(x_test)
            stats = precision_recall_fscore_support(y_test, predictions, labels=[1])
            return (stats[0][0], stats[1][0], stats[2][0])

    def svm_model(self, x_train=None, y_train=None, x_test=None, y_test=None):
        if x_train is not None:
            self.svm = SVC(probability=True)
            self.svm.fit(x_train, y_train)
        if x_test is not None:
            predictions = self.svm.predict(x_test)
            stats = precision_recall_fscore_support(y_test, predictions, labels=[1])
            return (stats[0][0], stats[1][0], stats[2][0])

    def linear_regression(self, x_train=None, y_train=None, x_test=None, y_test=None):
        if x_train is not None:
            self.lir = linear_model.LinearRegression()
            self.lir.fit(x_train, y_train)
        if x_test is not None:
            predictions = self.lir.predict(x_test)
            pred_labels = []
            for pred in predictions:
                if pred > 0.5:
                    pred_labels.append(1)
                else:
                    pred_labels.append(0)
            stats = precision_recall_fscore_support(y_test, np.asarray(pred_labels), labels=[1])
            return (stats[0][0], stats[1][0], stats[2][0])

    def logistic_regression(self, x_train=None, y_train=None, x_test=None, y_test=None):
        if x_train is not None:
            self.lim = linear_model.LogisticRegression()
            self.lim.fit(x_train, y_train)
        if x_test is not None:
            predictions = self.lim.predict(x_test)
            stats = precision_recall_fscore_support(y_test, predictions, labels=[1])
            return (stats[0][0], stats[1][0], stats[2][0])
