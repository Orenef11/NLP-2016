# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import sys, time, os, codecs
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.feature_selection import SelectKBest, chi2
from os.path import join
import numpy as np
K_FOLDS = 10

def create_positive_and_negative_dict():
    pos_list = []
    neg_list = []
    with open("Positive.txt", "r") as f:
        for line in f.readlines():
            pos_list.append(line.replace("\n", ""))
    with open("Negative.txt", "r") as f:
        for line in f.readlines():
            neg_list.append(line.replace("\n", ""))

    return pos_list, neg_list
def feature_vector(pos_words_dict, neg_words_dict, file_path):
    vector = [0] * (len(pos_words_dict) + len(neg_words_dict))
    review = 0
    with codecs.open(file_path, "r", "utf8") as f:
        review = f.read()
    for index, word in enumerate(pos_words_dict):
        if word in review:
            vector[index] = 1
    for index, word in enumerate(neg_words_dict):
        if word in review:
            vector[len(pos_words_dict) + index] = 1

    return vector
def create_feature_vector_for_all_reviews(pos_path, neg_path, pos_words_dict, neg_words_dict):
    vectors_dict_for_mixing = {}
    feature_label = []
    vectors_of_reviews = []

    for name_file in os.listdir(pos_path):
        vectors_dict_for_mixing["pos-" + name_file] = feature_vector(pos_words_dict, neg_words_dict,
                                                                     join(pos_path, name_file))
    for name_file in os.listdir(neg_path):
        vectors_dict_for_mixing["neg-" + name_file] = feature_vector(pos_words_dict, neg_words_dict,
                                                                     join(neg_path, name_file))

    for key in vectors_dict_for_mixing.keys():
        if key.split("-")[0] == "pos":
            vectors_of_reviews.append(vectors_dict_for_mixing[key])
            feature_label.append(1)
        else:
            vectors_of_reviews.append(vectors_dict_for_mixing[key])
            feature_label.append(0)

    return vectors_of_reviews, feature_label
def initial_classifier():
    svm_classifier = SVC()
    naive_bayes_classifier = MultinomialNB()
    decision_tree_classifier = tree.DecisionTreeClassifier()
    knn_classifier = KNeighborsClassifier()
    return [svm_classifier, naive_bayes_classifier, decision_tree_classifier, knn_classifier]
def make_data_set_lists_after_kfold_func(test_indexes, vectors_data, vectors_kind):
    if len(vectors_data[0:test_indexes[0]]) != 0:
        training_data_set = vectors_data[0:test_indexes[0]]
        training_data_set.extend(vectors_data[test_indexes[len(test_indexes) - 1]:len(vectors_data) - 1])
    else:
        training_data_set = vectors_data[test_indexes[len(test_indexes) - 1]:len(vectors_data) - 1]

    if len(vectors_kind[0:test_indexes[0]]) != 0:
        training_data_set_kind = vectors_kind[0:test_indexes[0]]
        training_data_set_kind.extend(vectors_kind[test_indexes[len(test_indexes) - 1]:len(vectors_data) - 1])
    else:
        training_data_set_kind = vectors_kind[test_indexes[len(test_indexes) - 1]:len(vectors_data) - 1]

    true_kind_of_test = vectors_kind[test_indexes[0]:test_indexes[len(test_indexes) - 1] + 1]

    return training_data_set, training_data_set_kind, true_kind_of_test
def classifiers_function(vectors_data, vectors_label, classifier):
    cv = KFold(len(vectors_data), n_folds=K_FOLDS)
    accuracy = 0
    for train_indexes, test_indexes in cv:
        training_data_set, training_data_set_label, true_label_of_test = make_data_set_lists_after_kfold_func(
            test_indexes, vectors_data, vectors_label)
        classifier.fit(training_data_set, training_data_set_label)
        accuracy += accuracy_score(true_label_of_test, classifier.predict(
            vectors_data[test_indexes[0]:test_indexes[len(test_indexes) - 1] + 1]))

    return accuracy / K_FOLDS
def build_feature_vectors_of_bag_of_words(pos_path, neg_path, sort_by_feature_label):
    pos_file_data = []
    neg_file_data = []
    for file_name in os.listdir(pos_path):
        with codecs.open(os.path.join(pos_path, file_name), 'r', "utf-8") as f:
            pos_file_data.append(f.read())

    for file_name in os.listdir(neg_path):
        with codecs.open(join(neg_path, file_name), 'r', "utf-8") as f:
            neg_file_data.append(f.read())

    pos_idx = neg_idx = 0
    file_data = []
    for i in range(len(sort_by_feature_label)):
        if sort_by_feature_label[i] == 1:
            file_data.append(pos_file_data[pos_idx])
            pos_idx += 1
        else:
            file_data.append(neg_file_data[neg_idx])
            neg_idx += 1

    cv = CountVectorizer()
    transformer = TfidfTransformer()
    features_vector = transformer.fit_transform(cv.fit_transform(file_data).toarray()).toarray()
    return list(features_vector), sort_by_feature_label

def main(argv):
    start = time.clock()

    if len(argv) != 2:
        exit("Error: You need to enter like that: 'python hw3.py <input_dir>'")
    else:
        print("The path entered is: ", argv[1])

    pos_words_dict, neg_words_dict = create_positive_and_negative_dict()
    pos_path = join(argv[1], "pos")
    neg_path = join(argv[1], "neg")
    classifiers_name = ["SVM", "Navie-Bayes", "Decision-Tree", "KNN"]

    # Sections of Question 1
    classifiers = initial_classifier()
    vectors_of_reviews, feature_label = create_feature_vector_for_all_reviews(
        pos_path, neg_path, pos_words_dict, neg_words_dict)
    print("~~~~Question 1~~~~")
    for classifier_idx, classifier in enumerate(classifiers):
        t = time.clock()
        print(classifiers_name[classifier_idx] + " classifier " + "- the accuracy is of is ",
              classifiers_function(vectors_of_reviews, feature_label, classifier),
              " it's take ", time.clock() - t, "sec")

    # Sections of Question 2
    vectors_of_reviews, feature_label = build_feature_vectors_of_bag_of_words(pos_path, neg_path, feature_label)
    classifiers = initial_classifier()
    print("~~~~Question 2~~~~")
    for classifier_idx, classifier in enumerate(classifiers):
        t = time.clock()
        print(classifiers_name[classifier_idx] + " classifier " + "- the accuracy is of is ",
              classifiers_function(vectors_of_reviews, feature_label, classifier),
              " it's take ", time.clock() - t, "sec")

    # sel = SelectKBest(k=50)
    # c = sel.fit_transform(vectors_of_reviews, feature_label)
    # print(sel.get_params())
    # print(len(sel.get_support()))
    # print(len(c))
    # selector = SelectKBest(k=45)
    # s = selector.fit(vectors_of_reviews, feature_label)

    print("All done :-), it's take ", time.clock() - start, "sec")


if __name__ == "__main__":
    main(sys.argv)
