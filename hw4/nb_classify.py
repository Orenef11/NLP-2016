from time import clock
from div_train_test import *
from nltk.tokenize import TweetTokenizer
from nltk import FreqDist
from math import log2, fabs

CATEGORY_SIZE = 5
BAD_CLASSIFY = -1
GOOD_CLASSIFY = 1
TEST_INSTANCE_SIZE = 50

def div_instances_per_category(instances_list, label_category):
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

    l = []
    for key in label_category:
        if label_category[key] == "cord":
            l.append(cord_instances)
        elif label_category[key] == "formation":
            l.append(formation_instances)
        elif label_category[key] == "phone":
            l.append(phone_instances)
        elif label_category[key] == "division":
            l.append(division_instances)
        elif label_category[key] == "product":
            l.append(product_instances)

    return l

def div_instances_to_tokens_data(instances_per_category_list):

    tokens_data_per_category = ""
    tknzr = TweetTokenizer()

    for item in instances_per_category_list:
        tokenize_text = tknzr.tokenize(item.context)
        s = " ".join(tokenize_text)
        tokens_data_per_category += s

    return tokens_data_per_category

def model_language(freq_dict_object):
    features_vector = {}
    keys_list = freq_dict_object.keys()
    size_tokens_in_category = keys_list.__len__()

    count_all_tokens = 0
    for key in freq_dict_object.keys():
        count_all_tokens += freq_dict_object[key]

    for key in keys_list:
        features_vector[key] = (freq_dict_object[key] + 1) / (size_tokens_in_category + count_all_tokens)

    return freq_dict_object, count_all_tokens

def classify_instances_to_category(instances_test, model_language_list, label_category_reverse,
                                   all_tokens_size, prior_list):
    classify_list = [0] * CATEGORY_SIZE
    for instance in instances_test:
        max_prediction = 0
        category_classify = -1
        for i in range(CATEGORY_SIZE):
            dictionary_size = len(model_language_list[i].keys())
            tokens_instance = div_instances_to_tokens_data([instance])
            prior = prior_list[i]
            probability = log2(prior)

            for token in tokens_instance:
                token_probability = model_language_list[i][token] + 1 / (dictionary_size + all_tokens_size[i])

                probability += log2(token_probability)

            if probability > max_prediction:
                max_prediction = probability
                category_classify = i

        if category_classify == label_category_reverse[instance.senseid]:
            classify_list[category_classify] += GOOD_CLASSIFY
        # else:
        #     classify_list[category_classify] += BAD_CLASSIFY

    return classify_list

def main():
    start = clock()
    instances_train = instance_parsing("train.xml")
    instances_test = instance_parsing("test.xml")

    # Create label to each category
    label_category = {0: "cord", 1: "formation", 2: "phone", 3: "division", 4: "product"}
    label_category_reverse = {"cord": 0, "formation": 1, "phone": 2, "division": 3, "product": 4}

    # The order list is as follow: cord, formation, phone, division, product
    instances_train_list = div_instances_per_category(instances_train, label_category)

    freq_dict_per_category, model_language_list, prior_list, all_tokens_size_list = [], [], [], []

    for i in range(CATEGORY_SIZE):
        tokens_data_per_category = div_instances_to_tokens_data(instances_train_list[i])
        freq_dict_per_category.append(FreqDist(tokens_data_per_category.split(' ')))
        model_language_temp, all_tokens_size = model_language(freq_dict_per_category[i])
        prior_list.append(instances_train_list[i].__len__() / len(instances_train))
        model_language_list.append(model_language_temp)
        all_tokens_size_list.append(all_tokens_size)

    # for model in model_language_list:
    #     count = 0
    #     d = len(model_language_list[i].keys())
    #     for key in model.keys():
    #         a = ( model_language_list[i][key] + 1) / (d + all_tokens_size_list[i])
    #         count += a
    #
    #     print(count)
    # exit()
    # print(instances_train_list[0].__len__(), )
    # print(instances_train_list[1].__len__())
    # print(instances_train_list[2].__len__())
    # print(instances_train_list[3].__len__())
    # print(instances_train_list[4].__len__())
    #
    # print(((instances_train_list[0].__len__()/ len(instances_train)))+\
    # ((instances_train_list[1].__len__()/ len(instances_train)))+\
    # ((instances_train_list[2].__len__()/ len(instances_train)))+\
    # (instances_train_list[3].__len__()/ len(instances_train))+\
    # (instances_train_list[4].__len__()/ len(instances_train)))
    # exit()

    freq_dict_per_category.clear()
    d = classify_instances_to_category(instances_test, model_language_list, label_category_reverse,
                                       all_tokens_size_list, prior_list)

    for i in range(CATEGORY_SIZE):
        print(d[i])

    print("All done :-), the time it takes to produce all the files ", clock() - start, "sec")

if __name__ == "__main__":
    main()