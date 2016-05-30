from time import clock
from nltk import FreqDist
from math import log2
from nltk import word_tokenize
from div_train_test import instance_parsing
from collections import Counter

CATEGORY_SIZE = 5
BAD_CLASSIFY = -1
GOOD_CLASSIFY = 1
TEST_INSTANCE_SIZE = 50

def div_instances_per_category(instances_list):
    div_instances_to_category_dict = {}

    for instance in instances_list:
        senseid = instance.senseid
        if senseid in div_instances_to_category_dict.keys():
            div_instances_to_category_dict[senseid].append(instance)
        else:
            div_instances_to_category_dict[senseid] = [instance]


    #     if instance.senseid == "cord":
    #         cord_instances.append(instance)
    #     elif instance.senseid == "formation":
    #         formation_instances.append(instance)
    #     elif instance.senseid == "phone":
    #         phone_instances.append(instance)
    #     elif instance.senseid == "division":
    #         division_instances.append(instance)
    #     elif instance.senseid == "product":
    #         product_instances.append(instance)
    #
    # div_instances_to_category_list = []
    # for key in label_category:
    #     if label_category[key] == "cord":
    #         div_instances_to_category_list.append(cord_instances)
    #     elif label_category[key] == "formation":
    #         div_instances_to_category_list.append(formation_instances)
    #     elif label_category[key] == "phone":
    #         div_instances_to_category_list.append(phone_instances)
    #     elif label_category[key] == "division":
    #         div_instances_to_category_list.append(division_instances)
    #     elif label_category[key] == "product":
    #         div_instances_to_category_list.append(product_instances)
    return div_instances_to_category_dict
class NaiveBayes(object):
    def __init__(self):
        self.priors_per_category_dict = {}
        self.freq_dist_object = {}

    def train(self, instances_list):
        for instance in instances_list:
            senseid = instance.senseid
            if senseid not in self.freq_dist_object:
                # Create FreqDict variable
                self.freq_dist_object[senseid] = FreqDist()

            # Save the counter variable for each sentence in instance
            sentences = instance.context.split("\r\n")
            for sentence in sentences:
                self.freq_dist_object[senseid].update(word_tokenize(sentence))
            # Calculation of the prior per category
            self.priors_per_category_dict[senseid] = self.priors_per_category_dict.get(senseid, 0) + 1


        # keys = sorted([s for s in self.priors_per_category_dict])
        # for s in keys:
        #     s =s
        #     # print(s, "--", self.freq_dist_object[s])
        #     # print(s, "--", len(self.freq_dist_object[s].keys()), "---", self.freq_dist_object[s].N())
        # exit()

        # A division of the count of any instances of self 'instances_list' size
        for senseid in self.priors_per_category_dict:
            self.priors_per_category_dict[senseid] /= instances_list.__len__()

    def test(self, instances_test):
        true_positives = Counter()
        false_positives = Counter()
        false_negatives = Counter()
        percision = Counter()
        recall = Counter()
        results = []
        total_correct = 0
        kind_of_instance = sorted([senseid for senseid in self.priors_per_category_dict])


        ii = 0
        for instance in instances_test:
            senseid = instance.senseid
            scores = Counter()
            for kind_instance in kind_of_instance:
                scores[kind_instance] = self.priors_per_category_dict[kind_instance]
                freq_fict = FreqDist(instance.context)
                tokens = freq_fict.keys()

                for word in tokens:
                    # P(vj | sk )
                    word_smoothed_probability = (self.freq_dist_object[kind_instance][word] + 1) / \
                                                (len(self.freq_dist_object[kind_instance].keys()) +
                                                    self.freq_dist_object[kind_instance].N())
                    print((self.freq_dist_object[kind_instance][word] + 1), "/", len(self.freq_dist_object[kind_instance].keys()), "+", self.freq_dist_object[kind_instance].N())
                    exit()

                    scores[kind_instance] += log2(word_smoothed_probability)

            #
            # print(instance.instance_id)
            # sorted(scores)
            # print(scores);print(scores.most_common(1)[0][0]);exit()
            # result_senseid = scores.most_common(1)[0][0]
            # results.append((instance.instance_id, result_senseid))
            # if instance.senseid == result_senseid:
            #     true_positives[result_senseid] = true_positives.get(result_senseid, 0) + 1
            #     total_correct += 1
            # else:
            #     false_positives[result_senseid] = true_positives.get(result_senseid, 0) + 1
            #     false_negatives[instance.senseid] = false_negatives.get(instance.senseid, 0) + 1
            print(instance.instance_id, "    ", scores)

            ii += 1
            if ii == 10:
                exit()



        for senseid in kind_of_instance:
            percision[senseid] = true_positives[senseid] / (1 + true_positives[senseid] + false_positives[senseid])
            recall[senseid] = true_positives[senseid] / (1 + true_positives[senseid] + false_negatives[senseid])
        accuracy = total_correct / len(instances_test)

        return percision, recall, accuracy, results

def main():
    # Calculation Runtime
    start = clock()

    instances_train = instance_parsing("train.xml")
    instances_test = instance_parsing("test.xml")

    nb_classifier = NaiveBayes()

    nb_classifier.train(instances_train)
    percision, recall, accuracy, results = nb_classifier.test(instances_test)

    # max_word_len = max([len(w) for w in percision])
    # for senseid in sorted(percision.keys()):
    #     print(senseid + ' ' * (max_word_len - len(senseid)) + ' : percision: {: >.3f}, recall: {: >.3f}'.format(
    #         percision[senseid], recall[senseid]))
    # print()
    # print('total accuracy: {: >.3f}'.format(accuracy))

    print(percision)
    print(recall)

    # nb_classifyer = NBClassifyer()
    # nb_classifyer.train(args.train_file_path)
    # percision, recall, accuracy, results = nb_classifyer.test(args.test_file_path)

    # max_word_len = max([len(w) for w in percision])
    # for senseid in sorted(percision.keys()):
    #     print(senseid + ' ' * (max_word_len - len(senseid)) + ' : percision: {: >.3f}, recall: {: >.3f}'.format(
    #         percision[senseid], recall[senseid]))
    # print()
    # print('total accuracy: {: >.3f}'.format(accuracy))
    #
    # with open(args.output_file_path, 'w') as f:
    #     for result in results:
    #         f.write(result[0] + ' ' + result[1] + '\n')

    print("All done :-), the time it takes to produce all the files ", clock() - start, "sec")


if __name__ == '__main__':
    main()