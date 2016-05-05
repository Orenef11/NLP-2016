# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import sys, time, os, codecs
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.cross_validation import KFold, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
import numpy as np

K_FOLDS = 10


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


def classifiers_function(vectors_data, vectors_kind, classifier):
    cv = KFold(len(vectors_data), n_folds=K_FOLDS)
    accuracy = 0
    for train_indexes, test_indexes in cv:
        training_data_set, training_data_set_kind, true_kind_of_test = make_data_set_lists_after_kfold_func(
            test_indexes, vectors_data, vectors_kind)
        # print(training_data_set);print(training_data_set_kind);exit()
        # for i in range(len(training_data_set)):
        #     print(training_data_set[i])
        # exit()

        classifier.fit(training_data_set, training_data_set_kind)
        accuracy += accuracy_score(true_kind_of_test, classifier.predict(
            vectors_data[test_indexes[0]:test_indexes[len(test_indexes) - 1] + 1]))

    return accuracy / K_FOLDS


def create_positive_and_negative_dict():
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
    review = 0
    with open(file_path, "r", encoding="utf8") as f:
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
    pos_and_neg_kind_list = []
    vectors_of_reviews = []

    for name_file in os.listdir(pos_path):
        vectors_dict_for_mixing["pos-" + name_file] = feature_vector(pos_words_dict, neg_words_dict,
                                                                     os.path.join(pos_path, name_file))
    for name_file in os.listdir(neg_path):
        vectors_dict_for_mixing["neg-" + name_file] = feature_vector(pos_words_dict, neg_words_dict,
                                                                     os.path.join(neg_path, name_file))

    for key in vectors_dict_for_mixing.keys():
        if key.split("-")[0] == "pos":
            vectors_of_reviews.append(vectors_dict_for_mixing[key])
            pos_and_neg_kind_list.append(1)
        else:
            vectors_of_reviews.append(vectors_dict_for_mixing[key])
            pos_and_neg_kind_list.append(0)

    return vectors_of_reviews, pos_and_neg_kind_list


def initial_classifier():
    svm_classifier = SVC()
    naive_bayes_classifier = MultinomialNB()
    decision_tree_classifier = tree.DecisionTreeClassifier()
    knn_classifier = KNeighborsClassifier()
    return [svm_classifier, naive_bayes_classifier, decision_tree_classifier, knn_classifier]


def create_feature_vectors_by_bag_of_words(pos_path, neg_path):
    words_of_reviews = {}
    pos_and_neg_kind_list = []
    words_of_reviews, vectors_dict_for_mixing = build_feature_vectors_of_bag_of_words(words_of_reviews, pos_path,
                                                                                      neg_path)
    return words_of_reviews, vectors_dict_for_mixing

    feature_vectors = []
    for key in vectors_dict_for_mixing.keys():
        if key.split("-")[0] == "pos":
            feature_vectors.append(vectors_dict_for_mixing[key])
            pos_and_neg_kind_list.append(1)
        else:
            feature_vectors.append(vectors_dict_for_mixing[key])
            pos_and_neg_kind_list.append(0)

    # print(len(feature_vectors[0])); print(len(vectors_dict_for_mixing.keys()));exit()
    return feature_vectors, pos_and_neg_kind_list


def build_feature_vectors_of_bag_of_words(words_of_reviews, pos_path, neg_path):
    file_data = []
    feature_label = []
    for file_name in os.listdir(pos_path):
        f = codecs.open(os.path.join(pos_path, file_name), 'r', "utf-8")
        file_data.append(f.read())
        f.close()
        feature_label.append(1)

    for file_name in os.listdir(neg_path):
        f = codecs.open(os.path.join(neg_path, file_name), 'r', "utf-8")
        file_data.append(f.read())
        f.close()
        feature_label.append(0)

    cv = CountVectorizer()
    transformer = TfidfTransformer()
    features = transformer.fit_transform(cv.fit_transform(file_data).toarray()).toarray()
    return list(features), feature_label



    vectors_dict_for_mixing = {}
    
    words_of_reviews = create_all_words_in_reviews(pos_path, words_of_reviews)
    words_of_reviews = create_all_words_in_reviews(neg_path, words_of_reviews)

    words_feature_list = sorted(words_of_reviews.keys(), key=lambda x:x[0])

    for name_file in os.listdir(pos_path):
        cv = CountVectorizer()
        feature_vector_list = [0] * len(words_of_reviews.keys())
        file = codecs.open(os.path.join(pos_path, name_file), "r", "utf-8")
        data = file.read()

        for word_idx, word in enumerate(words_feature_list):
            if word in data:
                feature_vector_list[word_idx] = 1

        vectors_dict_for_mixing["pos-" + name_file] = feature_vector_list

    for name_file in os.listdir(neg_path):
        feature_vector_list = [0] * len(words_of_reviews.keys())
        file = codecs.open(os.path.join(neg_path, name_file), "r", "utf-8")
        data = file.read()

        for word_idx, word in enumerate(words_feature_list):
            if word in data:
                feature_vector_list[word_idx] = 1

        vectors_dict_for_mixing["neg-" + name_file] = feature_vector_list
    return words_of_reviews, vectors_dict_for_mixing

def create_all_words_in_reviews(folder_path, words_of_reviews):
    for name_file in os.listdir(folder_path):
        cv = CountVectorizer()
        file = codecs.open(os.path.join(folder_path, name_file), "r", "utf-8")
        data = file.readlines()
        cv.fit_transform(data).toarray()
        file.close()

        for key in cv.get_feature_names():
            if key not in words_of_reviews.keys():
                words_of_reviews[key] = 1
            else:
                words_of_reviews[key] += 1

    return words_of_reviews

def main(argv):
    start = time.clock()

    pos_words_dict, neg_words_dict = create_positive_and_negative_dict()
    pos_path = r"imdb1.train\pos"
    neg_path = r"imdb1.train\neg"
    classifiers_name = ["SVM", "Navie-Bayes", "Decision-Tree", "KNN"]
    # vectors_of_reviews, pos_and_neg_kind_list = create_feature_vector_for_all_reviews(
    #     pos_path, neg_path, pos_words_dict, neg_words_dict)
    #
    # Sections of Question 1
    # classifiers = initial_classifier()
    # vectors_of_reviews, pos_and_neg_kind_list = create_vector_for_all_reviews\
    #     (pos_path, neg_path, pos_words_dict, neg_words_dict)
    # for classifier_idx, classifier in enumerate(classifiers):
    #     print(classifiers_name[classifier_idx] + " classifier" + "- the accuracy is of is ",
    #           classifiers_function(vectors_of_reviews, pos_and_neg_kind_list, classifier))

    # Sections of Question 2
    vectors_of_reviews, pos_and_neg_kind_list = create_feature_vectors_by_bag_of_words(pos_path, neg_path)
    classifiers = initial_classifier()
    for classifier_idx, classifier in enumerate(classifiers):
        print(classifiers_name[classifier_idx] + " classifier" + "- the accuracy is of is ",
              classifiers_function(vectors_of_reviews, pos_and_neg_kind_list, classifier))

    print("All done :-), it's take ", time.clock() - start, "sec")


if __name__ == "__main__":
    main(sys.argv)
