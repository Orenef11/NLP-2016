#################
# Oren Efraimov  #
#                #
# Lior Portnoy   #
##################

from sys import argv
from time import clock
from nltk import FreqDist
from math import log2
from nltk import word_tokenize
from div_train_test import instance_parsing

###########################################################################
# Class 'NaiveBayes'
# Contain classifier functions for implement naive base classify algorithm
###########################################################################
class NaiveBayes(object):
    def __init__(self):
        self.priors_per_category_dict = {}
        self.freq_dist_object = {}

    ##############################################################
    # Function 'train'-
    # get train xml file and create language models for testing.
    ##############################################################
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

        # A division of the count of any instances of self 'instances_list' size
        for senseid in self.priors_per_category_dict:
            self.priors_per_category_dict[senseid] /= instances_list.__len__()

    ##############################################################
    # Function 'test'-
    # get test xml file and classify every instance in the file.
    ##############################################################
    def test(self, instances_test):

        results_to_file = {}
        true_positives = {}
        false_positives = {}
        false_negatives = {}
        correct_accuracy_size = 0

        ''' The kind of instances in alphabetical order '''
        kind_of_instance = sorted([senseid for senseid in self.priors_per_category_dict])

        '''  The variable initialization to include all types of instances '''
        for key in kind_of_instance:
            results_to_file[key] = []
            true_positives[key] = false_positives[key] = false_negatives[key] = 0

        for instance in instances_test:
            classify_predict = -1
            probability = probability_predict = 0
            for kind_instance in kind_of_instance:
                probability = self.priors_per_category_dict[kind_instance]
                tokens = word_tokenize(instance.context)

                for word in tokens:
                    '''len(self.freq_dist_object[kind_instance].keys()) -> size dictionary of 'kind_instance'
                    instances list.
                    self.freq_dist_object[kind_instance].N()  -> size all tokens's show in 'kind_instance'
                    FreqDict object. '''
                    probability_smoothing = (self.freq_dist_object[kind_instance][word] + 1) / \
                                            (len(self.freq_dist_object[kind_instance].keys()) +
                                             self.freq_dist_object[kind_instance].N())
                    probability += log2(probability_smoothing)

                if probability_predict == 0 or probability_predict < probability:
                    probability_predict = probability
                    classify_predict = kind_instance

            results_to_file[instance.senseid].append((instance.instance_id, classify_predict))
            if instance.senseid == classify_predict:
                true_positives[classify_predict] += 1
                correct_accuracy_size += 1
            else:
                false_positives[classify_predict] += 1
                false_negatives[instance.senseid] += 1

        precision_dict = {}
        recall_dict = {}
        for senseid in kind_of_instance:
            precision_dict[senseid] = true_positives[senseid] / (true_positives[senseid] + false_positives[senseid])
            recall_dict[senseid] = true_positives[senseid] / (true_positives[senseid] + false_negatives[senseid])

        accuracy = correct_accuracy_size / instances_test.__len__()

        return accuracy, results_to_file, precision_dict, recall_dict

def main(argv):
    # Calculation Runtime
    start = clock()
    if len(argv) < 4:
        exit("Error: You need to enter like that: python nb_classify.py <train_file_path> "
             "<test_file_path> <output_file_path>")
    else:
        print("The train file path entered is: ", argv[1])
        print("The test file path entered is: ", argv[2])
        print("The output file path entered is: ", argv[3])

    # open train and test xml files.
    instances_train = instance_parsing(argv[1])
    instances_test = instance_parsing(argv[2])

    # create classifier
    nb_classifier = NaiveBayes()

    nb_classifier.train(instances_train)
    accuracy, results_to_file, precision_dict, recall_dict = nb_classifier.test(instances_test)

    ''' Save the results classify to file '''
    with open(argv[3], 'w') as file:
        for line in results_to_file:
            file.write(line[0] + " " + line[1] + '\r\n')

    """ We calculate the maximum length of the word, to print beautiful Output """
    max_word_len = max([len(w) for w in precision_dict])
    for key in sorted(precision_dict.keys()):
        print("<", key, ">: ", (max_word_len - len(key)) * " ", "percision: <%.5f>," % precision_dict[key],
              "recall: <%.5f>" % recall_dict[key])
    print("\r\ntotal accuracy: <%.5f>" % accuracy)

    print("All done :-), the time it takes to produce all the files ", clock() - start, "sec")

if __name__ == '__main__':
    main(argv)