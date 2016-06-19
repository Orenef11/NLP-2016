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
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, ENGLISH_STOP_WORDS
from sklearn.feature_selection import SelectKBest
from os.path import join


K_FOLDS = 10

################################################
# Function 'create_positive_and_negative_dict'
# the function read positive words file and
# negative words file and return lists of words.
#################################################
def create_positive_and_negative_list(name):
    words_list = []
    with open(name, "r") as f:
        for line in f.readlines():
            words_list.append(line.replace("\n", ""))

    return words_list

############################################################
# Function - 'feature_vector'
# the function create binary feature vector for input file
# using negative and positive words.
###########################################################
def label_vector(words_list, file_path, label):
    vector = [0] * (len(words_list))
    with codecs.open(file_path, "r", "utf8") as f:
        review = f.read()
        for index, word in enumerate(words_list):
            if word in review:
                vector[index] = label

    return vector

#############################################################
# Function - 'create_feature_vector_for_all_reviews'
# the function create binary feature vector for all reviews.
#############################################################
def create_feature_vector_for_all_reviews(pos_path, neg_path, words_list):
    vectors_dict_for_mixing = {}
    feature_label = []
    vectors_of_reviews = []

    for name_file in os.listdir(pos_path):
        vectors_dict_for_mixing["pos-" + name_file] = label_vector(words_list, join(pos_path, name_file), 1)
    for name_file in os.listdir(neg_path):
        vectors_dict_for_mixing["neg-" + name_file] = label_vector(words_list, join(neg_path, name_file), 1)

    for key in vectors_dict_for_mixing.keys():
        if key.split("-")[0] == "pos":
            vectors_of_reviews.append(vectors_dict_for_mixing[key])
            feature_label.append(1)
        else:
            vectors_of_reviews.append(vectors_dict_for_mixing[key])
            feature_label.append(0)

    return vectors_of_reviews, feature_label

###################################################
# Function - 'initial_classifier'
# the function init and return classifier objects.
###################################################
def initial_classifier():
    svm_classifier = SVC()
    naive_bayes_classifier = MultinomialNB()
    decision_tree_classifier = tree.DecisionTreeClassifier()
    knn_classifier = KNeighborsClassifier()
    return [svm_classifier, naive_bayes_classifier, decision_tree_classifier, knn_classifier]

########################################################################
# Function - 'make_data_set_lists_after_kfold_func'
# the function receive test indexes for vector data testing.
# the function return training data with test result and actual result.
########################################################################
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

############################################################
# Function - 'classifiers_function'
# the function receive vector data and classifier type and
# return the accuracy result.
############################################################
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

###################################################################################
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Function - 'build_feature_vectors_of_bag_of_words'
# the function receive negative and positive input files and build feature vectors
# by 'bag of words'.
###################################################################################
def build_feature_vectors_of_bag_of_words(pos_path, neg_path, sort_by_feature_label, vocabulary=None):
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

    if vocabulary == "None":
        cv = CountVectorizer(stop_words=ENGLISH_STOP_WORDS)
    else:
        cv = CountVectorizer(stop_words=ENGLISH_STOP_WORDS, vocabulary=vocabulary)
    transformer = TfidfTransformer()
    features_vector = transformer.fit_transform(cv.fit_transform(file_data).toarray()).toarray()
    return list(features_vector), sort_by_feature_label, cv.get_feature_names()


def best_words_features(vectors_of_reviews, feature_label, feature_words, file_patn, sum_best_words=50):
    sel = SelectKBest(k=sum_best_words)
    sel.fit_transform(vectors_of_reviews, feature_label)
    k_best_index = sel.get_support(indices="True")
    words = []
    for i in k_best_index:
        words.append(feature_words[i])

    f = open(file_patn, "w")
    i = 1
    for word in words:
        if i < len(words):
            f.write(word + "\r\n")
        else:
            f.write(word)

        i += 1
    f.close()

    return words

def main(argv):
    start = time.clock()

    if len(argv) != 4:
        exit("Error: You need to enter like that:"
             " 'python hw3.py <input_dir> <words_file_input_path> <best_words_file_output_path>'")
    else:
        print("The reviews folder path entered is: ", argv[1])
        print("The words file input path is: ", argv[2])
        print("The best words file pa thentered is: ", argv[3])

    input_file_words = argv[2]
    words_list = create_positive_and_negative_list(input_file_words)

    pos_path = join(argv[1], "pos")
    neg_path = join(argv[1], "neg")
    classifiers_name = ["SVM", "Navie-Bayes", "Decision-Tree", "KNN"]

    # Sections of Question 1
    classifiers = initial_classifier()
    vectors_of_reviews, feature_label = create_feature_vector_for_all_reviews(
        pos_path, neg_path, words_list)
    print("~~~~Question 1~~~~")
    for classifier_idx, classifier in enumerate(classifiers):
        t = time.clock()
        print(classifiers_name[classifier_idx] + " classifier " + "- the accuracy is of is {0:.6f}"
        .format(classifiers_function(vectors_of_reviews, feature_label, classifier)),
              " it's take {0:.4f}".format(time.clock() - t), "sec")

    # Sections of Question 2
    vectors_of_reviews, feature_label, feature_words = build_feature_vectors_of_bag_of_words(
        pos_path, neg_path, feature_label)
    classifiers = initial_classifier()
    print("~~~~Question 2~~~~")
    for classifier_idx, classifier in enumerate(classifiers):
        t = time.clock()
        print(classifiers_name[classifier_idx] + " classifier " + "- the accuracy is of is {0:.6f}"
              .format(classifiers_function(vectors_of_reviews, feature_label, classifier)),
              " it's take {0:.4f}".format((time.clock() - t) / 60), "min")

    # Sections of Question 3
    best_words = best_words_features(vectors_of_reviews, feature_label, feature_words, argv[3])

    # Sections of Question 4
    vectors_of_reviews, feature_label, feature_words = build_feature_vectors_of_bag_of_words(
        pos_path, neg_path, feature_label, best_words)
    classifiers = initial_classifier()
    print("~~~~Question 4~~~~")
    for classifier_idx, classifier in enumerate(classifiers):
        t = time.clock()
        print(classifiers_name[classifier_idx] + " classifier " + "- the accuracy is of is {0:.6f}"
              .format(classifiers_function(vectors_of_reviews, feature_label, classifier)),
              " it's take {0:.4f}".format(time.clock() - t), "sec")

    print("All done :-), it's take {0:.4f}".format((time.clock() - start) / 60), "min")

if __name__ == "__main__":
    main(sys.argv)
