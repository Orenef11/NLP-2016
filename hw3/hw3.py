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
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# according by Shuly lecture
K_FOLDS = 10


def make_dataset_lists_after_KFold_func(test_indexes, vectors_data, vectors_kind):
    training_dataset = vectors_data[0:test_indexes[0]]
    training_dataset.extend(vectors_data[test_indexes[len(test_indexes) - 1]:len(vectors_data) - 1])
    training_dataset_kind = vectors_kind[0:test_indexes[0]]
    training_dataset_kind.extend(vectors_kind[test_indexes[len(test_indexes) - 1]:len(vectors_data) - 1])
    true_kind_of_test = vectors_kind[test_indexes[0]:test_indexes[len(test_indexes) - 1] + 1]

    return training_dataset, training_dataset_kind, true_kind_of_test



def blabla(vectors_data, vectores_kind, classifier):
    cv = KFold(len(vectors_data), n_folds=K_FOLDS)
    accuracy = 0
    for train_indexes, test_indexes in cv:
        training_dataset, training_dataset_kind, true_kind_of_test = make_dataset_lists_after_KFold_func(test_indexes,
                                                                                                         vectors_data,
                                                                                                         vectores_kind)
        classifier.fit(training_dataset, training_dataset_kind)
        accuracy += accuracy_score(true_kind_of_test, classifier.predict(
            vectors_data[test_indexes[0]:test_indexes[len(test_indexes) - 1] + 1]))

    print("The accuracy is ", accuracy / K_FOLDS)


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


def create_vector_for_all_reviews(pos_path, neg_path, pos_words_dict, neg_words_dict):
    vectors_dict_for_mining = {}
    pos_and_neg_kind_list = []
    vectors_of_reviews = []

    for name_file in os.listdir(pos_path):
        vectors_dict_for_mining["pos-" + name_file] = feature_vector(pos_words_dict, neg_words_dict,
                                                                     os.path.join(pos_path, name_file))
    for name_file in os.listdir(neg_path):
        vectors_dict_for_mining["neg-" + name_file] = feature_vector(pos_words_dict, neg_words_dict,
                                                                     os.path.join(neg_path, name_file))

    for key in vectors_dict_for_mining.keys():
        if key.split("-")[0] == "pos":
            vectors_of_reviews.append(vectors_dict_for_mining[key])
            pos_and_neg_kind_list.append(1)
        else:
            vectors_of_reviews.append(vectors_dict_for_mining[key])
            pos_and_neg_kind_list.append(0)

    return vectors_of_reviews, pos_and_neg_kind_list


def initial_classifier():
    svm_classifier = SVC()
    naive_bayes_classifier = MultinomialNB()
    decision_tree_classifier = tree.DecisionTreeClassifier()
    knn_classifier = KNeighborsClassifier()
    return svm_classifier, naive_bayes_classifier, decision_tree_classifier, knn_classifier


def feature_vectors_by_bag_of_words(pos_path, neg_path):
    words_of_reviews = {}
    vectors_dict_for_mining = {}
    feature_vectors = []
    pos_and_neg_kind_list = []
    words_of_reviews, vectors_dict_for_mining = build_feature_vectors_of_bag_of_words(words_of_reviews,
                                                                                      vectors_dict_for_mining, pos_path,
                                                                                      "pos")
    words_of_reviews, vectors_dict_for_mining = build_feature_vectors_of_bag_of_words(words_of_reviews,
                                                                                      vectors_dict_for_mining, neg_path,
                                                                                      "neg")

    for key in vectors_dict_for_mining.keys():
        if key.split("-")[0] == "pos":
            feature_vectors.append(vectors_dict_for_mining[key])
            pos_and_neg_kind_list.append(1)
        else:
            feature_vectors.append(vectors_dict_for_mining[key])
            pos_and_neg_kind_list.append(0)

    return feature_vectors, pos_and_neg_kind_list


def build_feature_vectors_of_bag_of_words(words_of_reviews, vectors_dict_for_mining, path_of_folder, name_of_folder):
    for name_file in os.listdir(path_of_folder):
        cv = CountVectorizer()
        file = codecs.open(os.path.join(path_of_folder, name_file), "r", "utf-8")
        data = file.readlines()
        vector_review = cv.fit_transform(data).toarray()
        # Make vector_review that type is int64 (numpy) to list
        temp_vector_list = []
        for i in range(len(vector_review)):
            temp_vector_list.extend(list(vector_review[i]))

        vectors_dict_for_mining[name_of_folder + "-" + name_file] = temp_vector_list
        file.close()

        for key in cv.get_feature_names():
            if key not in words_of_reviews.keys():
                words_of_reviews[key] = 1
            else:
                words_of_reviews[key] += 1

    return words_of_reviews, vectors_dict_for_mining


def main(argv):
    start = time.clock()

    pos_words_dict, neg_words_dict = create_positive_and_negative_dict()
    pos_path = r"imdb1.train\pos"
    neg_path = r"imdb1.train\neg"
    # vectors_of_reviews, pos_and_neg_kind_list = create_vector_for_all_reviews(pos_path, neg_path, pos_words_dict, neg_words_dict)
    #
    # Sections of Question 1
    # svm_classifier, naive_bayes_classifier, decision_tree_classifier, knn_classifier = initial_classifier()
    # blabla(vectors_of_reviews, pos_and_neg_kind_list, svm_classifier)
    # blabla(vectors_of_reviews, pos_and_neg_kind_list, naive_bayes_classifier)
    # blabla(vectors_of_reviews, pos_and_neg_kind_list, decision_tree_classifier)
    # blabla(vectors_of_reviews, pos_and_neg_kind_list, knn_classifier)

    # Sections of Question 2
    vectors_of_reviews, pos_and_neg_kind_list = feature_vectors_by_bag_of_words(pos_path, neg_path)
    svm_classifier1, naive_bayes_classifier, decision_tree_classifier, knn_classifier = initial_classifier()

    blabla(vectors_of_reviews, pos_and_neg_kind_list, svm_classifier1)
    # blabla(vectors_of_reviews, pos_and_neg_kind_list, naive_bayes_classifier)
    # blabla(vectors_of_reviews, pos_and_neg_kind_list, decision_tree_classifier)
    # blabla(vectors_of_reviews, pos_and_neg_kind_list, knn_classifier)


    print("All done :-), it's take ", time.clock() - start, "sec")


if __name__ == "__main__":
    main(sys.argv)
