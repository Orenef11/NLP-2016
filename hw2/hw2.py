# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import sys, time, codecs, os, math

separator_char = ' '
LOG_BASE = 2
ROUND_NUMBER = 3

#############################################################
# Function 'make_one_word_hash'
# This function get two parameters :
# one_word_hash : will contain the one word hash table.
# data_of_files : raw data with all tokens
# The function scan the raw data and insert the data to hash
# table by one token rule
#############################################################
def make_one_word_hash(one_word_hash, data_of_files):
    lines = data_of_files.split('\n')

    # scan data and take every one word and insert to hash table.
    for line in lines:
        words_in_line = line.split(" ")
        for i in range(0, len(words_in_line)):
            key = words_in_line[i]
            if key != "":
                if words_in_line[i] in one_word_hash.keys():
                    one_word_hash[key] += 1
                else:
                    one_word_hash[key] = 1

    size = 0
    for key in one_word_hash:
        size += one_word_hash[key]

    size -= 11
    for key in one_word_hash:
        one_word_hash[key] /= size

    return size, one_word_hash


#############################################################
# Function 'make_two_words_hash'
# This function get two parameters :
# one_word_hash : will contain the one word hash table.
# data_of_files : raw data with all tokens
# The function scan the raw data and insert the data to hash
# table by two tokens rule.
#############################################################
def make_two_words_hash(two_word_hash, data_of_files):
    lines = data_of_files.split('\n')

    # scan data and take every two words and insert to hash table.
    for line in lines:
        words_in_line = line.split(" ")
        for i in range(len(words_in_line) - 1):
            if (words_in_line[i] != '' and words_in_line[i + 1] != ''):
                key = words_in_line[i] + separator_char + words_in_line[i + 1]
                if key in two_word_hash.keys():
                    two_word_hash[key] += 1
                else:
                    two_word_hash[key] = 1

    size = 0
    for key in two_word_hash:
        size += two_word_hash[key]

    return size, two_word_hash


#############################################################
# Function 'make_three_words_hash'
# This function get two parameters :
# one_word_hash : will contain the one word hash table.
# data_of_files : raw data with all tokens
# The function scan the raw data and insert the data to hash
# table by three tokens rule
#############################################################
def make_three_words_hash(three_word_hash, data_of_files):
    lines = data_of_files.split('\n')

    # scan data and take every three words and insert to hash table.
    for line in lines:
        words_in_line = line.split(" ")
        for i in range(len(words_in_line) - 2):
            key = words_in_line[i] + separator_char + words_in_line[i + 1] + separator_char + words_in_line[i + 2]
            if words_in_line[i] != "" and words_in_line[i + 1] != "" and words_in_line[i + 2] != "":
                if key in three_word_hash.keys():
                    three_word_hash[key] += 1
                else:
                    three_word_hash[key] = 1

    size = 0
    for key in three_word_hash:
        size += three_word_hash[key]

    for key in three_word_hash:
        three_word_hash[key] /= size

    return size, three_word_hash


# ########################################################
# # Function 'split_to_sentences'
# # This function get three parameters :
# ########################################################
# def split_to_sentences(output_file_name, path, data_of_files):
#     sentncets_data_of_files = codecs.open(str(os.path.join(path, output_file_name)), 'w+', 'utf8')
#     # data_of_files = data_of_files.replace('\r', "")
#     # data_of_files = data_of_files.replace('\n', "\r\n")
#     data_of_files = sentncets_data_of_files.readline()
#     sentncets_data_of_files.close()
#     os.remove(str(os.path.join(path, output_file_name)))
#     return data_of_files


##########################################################
# Function 'raw_frequency_func'
# This function get three parameters :
# two_word_hash : contain the two word hash table.
# path :
# all_words_in_file_size : Size of raw data
# The function get hash table of two words and create the
# frequency file.
##########################################################
def raw_frequency_func(two_word_hash, path, all_words_in_file_size):
    start = time.clock()
    space = '\t\t'
    two_words_list = sorted(two_word_hash.items(), key=lambda x: x[0])
    two_words_list = sorted(two_words_list, key=lambda x: x[1], reverse=True)

    data_of_files_to_write = ''
    file = codecs.open(str(os.path.join(path, 'freq_raw.txt')), 'w+', 'utf8')
    file.write("Word1" + space + "Word2" + space + "W1W2" + space + "I(W1W2)" + '\r\n')

    # calculate the frequancy values and fill the file
    for cell in two_words_list:
        words_arr = cell[0].split(separator_char)
        file.write(words_arr[0] + space + words_arr[1] + space + words_arr[0] + separator_char + words_arr[1] + space \
                   + str(round(cell[1] * 1000 / all_words_in_file_size, ROUND_NUMBER)) + '\r\n')

    two_words_list.clear()
    file.write(data_of_files_to_write)
    file.close()

    print("Creates the file 'freq_raw.txt' in path " + path, " it's take ", time.clock() - start, "sec")


##################################################################
# Function 'pmi_pair_func'
# This function get five parameters :
# two_word_hash : contain one word hash table
# one_word_hash : contain two words hash table
# path :
# all_pairs_in_file_size : size of raw data - tokens
# all_words_in_file_size : size of raw data - 2 tokens
# The function get one\two hash tables and create pmi_pair file.
#################################################################
def pmi_pair_func(two_word_hash, one_word_hash, path, all_pairs_in_file_size, all_words_in_file_size):
    start = time.clock()
    # Space between to words
    space = '\t\t'
    two_words_order_by_value = {}
    for cell in two_word_hash:
        words_arr = cell.split(separator_char)
        word1_value = one_word_hash[words_arr[0]] * all_words_in_file_size
        word2_value = one_word_hash[words_arr[1]] * all_words_in_file_size

        if word1_value >= 0 and word2_value >= 0:
            probability = (two_word_hash[words_arr[0] + separator_char + words_arr[1]] / all_pairs_in_file_size) \
                          / (one_word_hash[words_arr[0]] * one_word_hash[words_arr[1]])

            two_words_order_by_value[words_arr[0] + separator_char + words_arr[1]] = math.log(probability, LOG_BASE)

    order_two_words_list = sorted(two_words_order_by_value.items(), key=lambda x: x[0])
    order_two_words_list = sorted(order_two_words_list, key=lambda x: x[1], reverse=True)

    data_of_files_to_write = ''
    file = codecs.open(str(os.path.join(path, 'pmi_pair.txt')), 'w+', 'utf8')
    file.write("Word1" + space + "Word2" + space + "W1W2" + space + "I(W1W2)" + '\r\n')
    i = 0

    # fill the file
    for cell in order_two_words_list:
        words_arr = cell[0].split(separator_char)
        file.write(words_arr[0] + space + words_arr[1] + space + cell[0] + space \
                   + str(round(cell[1], ROUND_NUMBER)) + '\r\n')
        i += 1
        if i == 100:
            break

    order_two_words_list.clear()
    two_words_order_by_value.clear()
    file.write(data_of_files_to_write)
    file.close()

    print("Creates the file 'pmi_pair.txt' in path " + path, " it's take ", time.clock() - start, "sec")


############################################################
# Function 'pmi_tri_a_func'
# This function get four parameters :
# three_word_hash : will contain the three word hash table.
# one_word_hash : will contain the one word hash table.
# path :
# all_words_in_file_size : size of raw data.
# The function create pmi_tri_a file.
############################################################
def pmi_tri_a_func(three_word_hash, one_word_hash, path, all_words_in_file_size):
    start = time.clock()
    # Space between to words
    space = '\t\t'
    three_words_order_by_value = {}
    for cell in three_word_hash:
        words_arr = cell.split(separator_char)
        word1_value = one_word_hash[words_arr[0]] * all_words_in_file_size
        word2_value = one_word_hash[words_arr[1]] * all_words_in_file_size
        word3_value = one_word_hash[words_arr[2]] * all_words_in_file_size
        if word1_value >= 20 and word2_value >= 20 and word3_value >= 20:
            key = words_arr[0] + separator_char + words_arr[1] + separator_char + words_arr[2]
            probability = (three_word_hash[key]) \
                          / (one_word_hash[words_arr[0]] * one_word_hash[words_arr[1]] * one_word_hash[words_arr[2]])
            three_words_order_by_value[key] = round(math.log(probability, LOG_BASE), ROUND_NUMBER)

    order_three_words_list = sorted(three_words_order_by_value.items(), key=lambda x: x[0])
    order_three_words_list = sorted(order_three_words_list, key=lambda x: x[1], reverse=True)

    data_of_files_to_write = ''
    file = codecs.open(str(os.path.join(path, 'pmi_tri_a.txt')), 'w+', 'utf8')
    file.write("Word1" + space + "Word2" + space + "Word3" + space + "W1W2W3" + space + "I(W1W2W3)" + '\r\n')
    i = 0

    # fill the file
    for cell in order_three_words_list:
        words_arr = cell[0].split(separator_char)
        file.write(words_arr[0] + space + words_arr[1] + space + words_arr[2] + \
                   space + cell[0] + space \
                   + str(cell[1]) + '\r\n')
        i += 1
        if i == 100:
            break

    order_three_words_list.clear()
    three_words_order_by_value.clear()
    file.write(data_of_files_to_write)
    file.close()

    print("Creates the file 'pmi_tri_a.txt' in path" + path, " it's take ", time.clock() - start, "sec")


############################################################
# Function 'pmi_tri_b_func'
# This function get six parameters :
# three_word_hash : will contain the three word hash table.
# two_word_hash : will contain the two word hash table.
# one_word_hash : will contain the one word hash table.
# path :
# all_pairs_in_file_size : size of raw data - tokens.
# all_words_in_file_size : size of raw data - 2 tokens.
# The function create pmi_tri_b file.
############################################################
def pmi_tri_b_func(three_word_hash, two_word_hash, one_word_hash, path, all_pairs_in_file_size, all_words_in_file_size):
    start = time.clock()
    # Space between to words
    space = '\t\t'
    three_words_order_by_value = {}
    for cell in three_word_hash:
        words_arr = cell.split(separator_char)
        words_arr = cell.split(separator_char)
        word1_value = one_word_hash[words_arr[0]] * all_words_in_file_size
        word2_value = one_word_hash[words_arr[1]] * all_words_in_file_size
        word3_value = one_word_hash[words_arr[2]] * all_words_in_file_size
        if word1_value >= 20 and word2_value >= 20 and word3_value >= 20:
            key = words_arr[0] + separator_char + words_arr[1] + separator_char + words_arr[2]
            probability = (three_word_hash[key]) \
                          / ((two_word_hash[words_arr[0] + separator_char + words_arr[1]] / all_pairs_in_file_size) * \
                             (two_word_hash[words_arr[1] + separator_char + words_arr[2]]) / all_pairs_in_file_size)
            three_words_order_by_value[key] = round(math.log(probability, LOG_BASE), ROUND_NUMBER)

    order_three_words_list = sorted(three_words_order_by_value.items(), key=lambda x: x[0])
    order_three_words_list = sorted(order_three_words_list, key=lambda x: x[1], reverse=True)

    data_of_files_to_write = ''
    file = codecs.open(str(os.path.join(path, 'pmi_tri_b.txt')), 'w+', 'utf8')
    file.write("Word1" + space + "Word2" + space + "Word3" + space + "W1W2W3" + space + "I(W1W2W3)" + '\r\n')
    i = 0

    # fill the file
    for cell in order_three_words_list:
        words_arr = cell[0].split(separator_char)
        file.write(words_arr[0] + space + words_arr[1] + space + words_arr[2] + \
                   space + cell[0] + space \
                   + str(cell[1]) + '\r\n')
        i += 1
        if i == 100:
            break

    order_three_words_list.clear()
    three_words_order_by_value.clear()
    file.write(data_of_files_to_write)
    file.close()

    print("Creates the file 'pmi_tri_b.txt' in path" + path, " it's take ", time.clock() - start, "sec")



###########################################################
# Function 'pmi_tri_c_func'
# This function get six parameters :
# three_word_hash : will contain the three word hash table.
# two_word_hash : will contain the two word hash table.
# one_word_hash : will contain the one word hash table.
# path :
# all_pairs_in_file_size : size of raw data - tokens.
# all_words_in_file_size : size of raw data - 2 tokens.
# The function create pmi_tri_c file.
###########################################################
def pmi_tri_c_func(three_word_hash, two_word_hash, one_word_hash, path, all_pairs_in_file_size, all_words_in_file_size):
    start = time.clock()
    # Space between to words
    space = '\t\t'
    three_words_order_by_value = {}
    for cell in three_word_hash:
        words_arr = cell.split(separator_char)
        words_arr = cell.split(separator_char)
        word1_value = one_word_hash[words_arr[0]] * all_words_in_file_size
        word2_value = one_word_hash[words_arr[1]] * all_words_in_file_size
        word3_value = one_word_hash[words_arr[2]] * all_words_in_file_size
        if word1_value >= 20 and word2_value >= 20 and word3_value >= 20:
            key = words_arr[0] + separator_char + words_arr[1] + separator_char + words_arr[2]
            probability = (three_word_hash[key]) \
                          / ((one_word_hash[words_arr[0]] * one_word_hash[words_arr[1]] * one_word_hash[words_arr[2]]) * \
                             ((two_word_hash[words_arr[0] + separator_char + words_arr[1]] / all_pairs_in_file_size) * \
                              (two_word_hash[words_arr[1] + separator_char + words_arr[2]]) / all_pairs_in_file_size))
            three_words_order_by_value[key] = round(math.log(probability, LOG_BASE), ROUND_NUMBER)

    order_three_words_list = sorted(three_words_order_by_value.items(), key=lambda x: x[0])
    order_three_words_list = sorted(order_three_words_list, key=lambda x: x[1], reverse=True)

    data_of_files_to_write = ''
    file = codecs.open(str(os.path.join(path, 'pmi_tri_c.txt')), 'w+', 'utf8')
    file.write("Word1" + space + "Word2" + space + "Word3" + space + "W1W2W3" + space + "I(W1W2W3)" + '\r\n')
    i = 0

    # fill the file
    for cell in order_three_words_list:
        words_arr = cell[0].split(separator_char)
        file.write(words_arr[0] + space + words_arr[1] + space + words_arr[2] + \
                   space + cell[0] + space + str(cell[1]) + '\r\n')
        i += 1
        if i == 100:
            break

    order_three_words_list.clear()
    three_words_order_by_value.clear()
    file.write(data_of_files_to_write)
    file.close()

    print("Creates the file 'pmi_tri_c.txt' in path" + path, " it's take ", time.clock() - start, "sec")



##############################################################
# Function 'run_collocation_functions'
# This function get three  parameters :
# input path :
# filename :
# output_path :
# The function run the functions for create the output files.
##############################################################
def run_collocation_functions(filename, output_path):
    one_word_hash = {}
    two_word_hash = {}
    three_word_hash = {}
    try:
        temp_file = codecs.open(filename, 'r', 'utf8')
    except:
        sys.exit("Error: Unable to read the file with all data!")
    data_of_files = temp_file.read()
    temp_file.close()

    if not os.path.exists(output_path):
        os.makedirs(output_path)


    all_words_in_file_size, one_word_hash = make_one_word_hash(one_word_hash, data_of_files)
    all_pairs_in_file_size, two_word_hash = make_two_words_hash(two_word_hash, data_of_files)
    three_word_hash_size, three_word_hash = make_three_words_hash(three_word_hash, data_of_files)

    raw_frequency_func(two_word_hash, output_path, all_words_in_file_size)
    pmi_pair_func(two_word_hash, one_word_hash, output_path, all_pairs_in_file_size, all_words_in_file_size)
    pmi_tri_a_func(three_word_hash, one_word_hash, output_path, all_words_in_file_size)
    pmi_tri_b_func(three_word_hash, two_word_hash, one_word_hash, output_path, all_pairs_in_file_size, \
                   all_words_in_file_size)
    pmi_tri_c_func(three_word_hash, two_word_hash, one_word_hash, output_path, all_pairs_in_file_size, \
                   all_words_in_file_size)


def main(argv):
    start = time.clock()
    if len(argv) == 3:
        input_path = argv[1]
        output_path = argv[2]
        print("The input data folder is: " + input_path)
        print("The output data folder is: " + output_path)
        print("Please wait processing")
    else:
        sys.exit("Error: You have not entered two variables!")

    data_of_files = ''

    # This step gets input folder and merge all files to one big
    # file for next step (create collocation files).
    try:
        f = codecs.open('bigFile.txt', "w+", 'utf8')
    except:
        sys.exit("Error: Unable to create the file that include all data!")

    for tempfile in os.listdir(input_path):
        try:
            file = codecs.open(str(os.path.join(input_path, tempfile)), "r", 'utf8')
        except:
            sys.exit("Error: Unable to read the file!" + tempfile)
        data_of_files = "".join(data_of_files + str(file.read()) + str('\n'))
        file.close()
    f.write(data_of_files)
    run_collocation_functions('bigFile.txt', output_path)
    f.close()

    os.remove('bigFile.txt')
    print("All done :-), it's take ", time.clock() - start, "sec")


if __name__ == "__main__":
    main(sys.argv)
