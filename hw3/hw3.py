# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import sys, time, codecs, os, math


class reviewWord():
    def __init__(self, word, exist):
        self.word = word
        self.exist = exist


class fileVector():
    def __init__(self, name, revWord):
        self.name = name
        self.revWord = revWord




reviewVector = []

allReviews = []


# def prepareVectorForFile(inFile, dictFile):
#
#
#     tmpReviewVector = fileVector(inFile,[])
#
#     for word in dictFile:
#
#         ## prepare word instance
#         tWord = reviewWord(word,0)
#
#         if word in inFile:
#             tWord.exist = 1


def create_postive_and_negtive_dict():
    pos_dict = {}
    neg_dict = {}
    with open("Positive.txt", "r") as f:
        for line in f.readlines():
            pos_dict[line.replace("\n", "")] = 0

    with open("Negative.txt", "r") as f:
        for line in f.readlines():
            neg_dict[line.replace("\n", "")] = 0
    return pos_dict, neg_dict


def feature_vector(pos_words_dict, neg_words_dict, file_path):
    vector = [0] *(len(pos_words_dict) + len(neg_words_dict))
    with open(file_path, "r", encoding="utf8") as f:
        for line in f.readlines():
            words = line.split(" ")
            for index, word in enumerate(pos_words_dict):
                if word in words:
                    vector[index] = 1
            for index, word in enumerate(neg_words_dict):
                if word in words:
                    vector[index] = 1

    return vector

def create_vector_for_all_review(pos_path, neg_path, pos_words_dict, neg_words_dict):
    vector_movies = {}
    ## prepare vectors
    for name_file in os.listdir(pos_path):
        # print("Now analyze file : " + name_file)
        # print("Finished analyze file : " + name_file)
        vector_movies[name_file] = feature_vector(pos_words_dict, neg_words_dict, os.path.join(pos_path, name_file))

    for name_file in os.listdir(neg_path):
        # print("Now analyze file : " + name_file)
        # print("Finished analyze file : " + name_file)
        vector_movies[name_file] = feature_vector(pos_words_dict, neg_words_dict, os.path.join(neg_path, name_file))

    return vector_movies


def main(argv):
    start = time.clock()

    pos_words_dict, neg_words_dict = create_postive_and_negtive_dict()
    pos_path = r"imdb1.train\pos"
    neg_path = r"imdb1.train\neg"
    vector_movies = create_vector_for_all_review(pos_path, neg_path, pos_words_dict, neg_words_dict)

    print(len(vector_movies))
    print("All done :-), it's take ", time.clock() - start, "sec")


if __name__ == "__main__":
    main(sys.argv)