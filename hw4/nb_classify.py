from time import clock
from sklearn.naive_bayes import MultinomialNB
from div_train_test import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, ENGLISH_STOP_WORDS
from nltk.tokenize import TweetTokenizer
from random import shuffle
from sklearn.metrics import accuracy_score



SIZE_CATEGORY = 5

def div_instances_per_category(instances_list):
    cord_instances = []
    formation_instances = []
    phone_instances = []
    division_instances = []
    product_instances = []

    for instance in instances_list:
        if instance.senseid == "cord":
            cord_instances.append(instance)
        elif instance.senseid == "formation":
            formation_instances.append(instance)
        elif instance.senseid == "phone":
            phone_instances.append(instance)
        elif instance.senseid == "division":
            division_instances.append(instance)
        elif instance.senseid == "product":
            product_instances.append(instance)

    return [cord_instances, formation_instances, phone_instances, division_instances, product_instances]
# def feature_vector_by_category(instances_list):
#     bag_of_words_dict = {}
#     for item in instances_list:
#         tknzr = TweetTokenizer()
#         words_list = tknzr.tokenize(item.context)
#         for word in words_list:
#             bag_of_words_dict[word] = 0
#     bag_of_words_after_order = list(bag_of_words_dict.keys())
#     bag_of_words_after_order.sort()
#     # Create empty vector per instance
#     vectors_feature = []
#     vector = [0] * len(bag_of_words_after_order)
#     for i in range(len(instances_list)):
#         vectors_feature.append(vector)
#
#     for item in instances_list:
#         tknzr = TweetTokenizer()
#         words_list = tknzr.tokenize(item.context)
#         for word in words_list:
#             if word in bag_of_words_after_order:
#                 vectors_feature[0][bag_of_words_after_order.index(word)] = 1
#
#     return vectors_feature, bag_of_words_after_order
def feature_vector_by_category(instances_of_category_list, label_of_instance):
    cv = CountVectorizer()
    transformer = TfidfTransformer()

    file_data = []
    for item in instances_of_category_list:
        tknzr = TweetTokenizer()
        tokenize_text = tknzr.tokenize(item.context)
        s = " ".join(tokenize_text)
        file_data.append(s)

    features_vector = transformer.fit_transform(cv.fit_transform(file_data).toarray()).toarray()
    return features_vector, cv.get_feature_names(), [label_of_instance] * len(features_vector)

def build_and_shuffle_feature_vectors_train(instances_train, labels_dict):

    file_data = []
    shuffle(instances_train)
    d = {}

    cv = CountVectorizer()
    transformer = TfidfTransformer()
    vector_label = []
    start = clock()
    for item in instances_train:
        tknzr = TweetTokenizer()
        tokenize_text = tknzr.tokenize(item.context)
        s = " ".join(tokenize_text)
        file_data.append(s)
        key = item.senseid
        vector_label.append(labels_dict[key])
    #     if key in d:
    #         d[key] += 1
    #     else:
    #         d[key] = 1
    #
    # print(d)
    print(clock() - start)
    features_vector = transformer.fit_transform(cv.fit_transform(file_data)).toarray()
    return features_vector, cv.get_feature_names(), vector_label

def main():
    start = clock()
    instances_train = instance_parsing("train.xml")
    instances_test = instance_parsing("test.xml")

    # Create label to each category
    label_dict = {"cord": 1, "formation": 2, "phone": 3, "division": 4, "product": 5}

    # Create feature_vector and vector label to instance train to learn the classifier
    features_vector_train, bag_of_words, vector_label_train = \
        build_and_shuffle_feature_vectors_train(instances_train, label_dict)
    classifier = MultinomialNB()
    classifier.fit(features_vector_train, vector_label_train)

    # The order list is as follow: cord_instances, formation_instances, phone_instances, division_instances,
    #  product_instances
    instances_train_list = div_instances_per_category(instances_train)
    print(len(features_vector_train))
    # The all list's only to instances test
    bag_of_words_per_category_test = []
    feature_vectors_by_category_test = []
    label_per_category_test = []

    for idx, instances_of_category in enumerate(instances_train_list):
        feature_vector, bag_of_words, labels = feature_vector_by_category(instances_of_category,
                                                                          label_dict[instances_of_category[0].senseid])
        # print(type(features_vector_train));print(type(feature_vector));exit()
        classifier.predict(feature_vector)
        bag_of_words_per_category_test.append(bag_of_words)
        feature_vectors_by_category_test.append(feature_vector)
        label_per_category_test.append(labels)
        break;

    # for idx in range(len(feature_vectors_by_category_test)):
    #     print(type(features_vector_train))
    #     accuracy = 0
    #
    #     classifier.predict(features_vector_train)
    #     exit()
    #     accuracy += accuracy_score(bag_of_words_per_category_test[idx],
    #                                classifier.predict(feature_vectors_by_category_test[idx]))
    #     print(accuracy);exit()

    # for i in range(len(feature_vectors_by_category)):
    #     print(len(feature_vectors_by_category[i]))
    #     print(len(bag_of_words_per_category[i]))
    # print(len(features_vector[0]))
    # print(cv.get_feature_names());
    # for index, train_list in enumerate(instances_train_list):
    #     l = [it]
    #     instances_train_list[index], bag_of_words_per_category[index] = feature_vector_by_category(l)
    #     print(len(bag_of_words_per_category[index]));
    #     print(bag_of_words_per_category[index]);
    #     break;
    #
    # words = list(cv.get_feature_names())
    # for word in bag_of_words_per_category[0]:
    #     if word.lower() in bag_of_words_per_category[0]:
    #         words.remove(word)
    #
    # print(len(words))
    # print(words)
    # exit()



    print("All done :-), the time it takes to produce all the files ", clock() - start, "sec")

if __name__ == "__main__":
    main()