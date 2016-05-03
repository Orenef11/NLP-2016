# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import sys, time, codecs
import os
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree

# according by Shuly lecture 
DATA_K_FOLDS = 10


def create_postive_and_negtive_dict():
    pos_list = []
    neg_list = []
    with open("Positive.txt", "r") as f:
        for line in f.readlines():
            # pos_list[line.replace("\n", "")] = 0
            pos_list.append(line.replace("\n", ""))
    with open("Negative.txt", "r") as f:
        for line in f.readlines():
            # neg_list[line.replace("\n", "")] = 0
            neg_list.append(line.replace("\n", ""))

    # OrderedDict(neg_list)
    return pos_list, neg_list


def feature_vector(pos_words_dict, neg_words_dict, file_path):
    vector = [0] * (len(pos_words_dict) + len(neg_words_dict))
    rewview = 0
    with open(file_path, "r", encoding="utf8") as f:
        rewview = f.read()
    for index, word in enumerate(pos_words_dict):
        if word in rewview:
            vector[index] = 1
    for index, word in enumerate(neg_words_dict):
        if word in rewview:
            vector[len(pos_words_dict) + index] = 1

    return vector


def create_vector_for_all_review(pos_path, neg_path, pos_words_dict, neg_words_dict):
    vectors_dict = {}
    pos_and_neg_index_list = []
    pos_and_neg_value_list = []
    ## prepare vectors
    index = 1
    for name_file in os.listdir(pos_path):
        vectors_dict["pos-" + name_file] = feature_vector(pos_words_dict, neg_words_dict, os.path.join(pos_path, name_file))
        index += 1
    for name_file in os.listdir(neg_path):
        vectors_dict["neg-" + name_file] = feature_vector(pos_words_dict, neg_words_dict, os.path.join(neg_path, name_file))
        index += 1

    for key in vectors_dict.keys():
        if key.split("-")[0] == "pos":
            pos_and_neg_index_list.append(1)
        else:
            pos_and_neg_index_list.append(0)

    
    for value in vectors_dict.values():
        pos_and_neg_value_list.append(value)
    
    # print(vectors_dict.items())
    # print(vectors_dict.keys())
    # print(vectors_dict.values())

    return pos_and_neg_value_list, pos_and_neg_index_list


def initial_classifier():
    svm_classifier = SVC()
    naive_bayes_classifier = MultinomialNB()
    decision_tree_classifier = tree.DecisionTreeClassifier()
    knn_classifier = KNeighborsClassifier()
    return svm_classifier, naive_bayes_classifier, decision_tree_classifier, knn_classifier


def compute_classifier_ten_fold_cross_validation(classifier, vectors_data_set, vectors_data_results):
    fold_size = int(len(vectors_data_set) / DATA_K_FOLDS)
    classifier_error = classifier_accuracy = 0
    for i in range(DATA_K_FOLDS - 1):
        last_train_index = (i + 1) * fold_size
        classifier.fit(vectors_data_set[0:last_train_index], vectors_data_results[0:last_train_index])
        error, accuracy = test_range(vectors_data_set[last_train_index:], vectors_data_results[last_train_index:], classifier)
        classifier_error += error
        classifier_accuracy += accuracy
    return classifier_error / (DATA_K_FOLDS - 1), classifier_accuracy / (DATA_K_FOLDS - 1)


def test_range(testing_set, testing_results, classifier):
    classifier_results = classifier.predict(testing_set)
    false_count = 0
    for i in range(len(classifier_results)):
        if (classifier_results[i] != testing_results[i]):
            false_count += 1
    error_ratio = false_count / len(testing_set)
    accuracy_ratio = 1 - error_ratio
    return error_ratio, accuracy_ratio

def main(argv):
    start = time.clock()

    pos_words_dict, neg_words_dict = create_postive_and_negtive_dict()
    pos_path = r"imdb1.train\pos"
    neg_path = r"imdb1.train\neg"
    pos_and_neg_vectoer_value, pos_and_neg_vector_results = create_vector_for_all_review(pos_path, neg_path, pos_words_dict, neg_words_dict)
    svm_classifier, naive_bayes_classifier, decision_tree_classifier, knn_classifier = initial_classifier()
    a, b = compute_classifier_ten_fold_cross_validation(svm_classifier, pos_and_neg_vectoer_value, pos_and_neg_vector_results)
    print(str(a) + "       " + str(b))
    print("All done :-), it's take ", time.clock() - start, "sec")


if __name__ == "__main__":
    main(sys.argv)
