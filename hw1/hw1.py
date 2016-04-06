# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import sys, requests, time, codecs, os
from lxml import etree
from io import StringIO


# This function create and open file
# When the file not exist, the function create him
def open_file(path):
    try:
        file = codecs.open(path, 'w+', encoding='utf8')
    except FileNotFoundError as e:
        sys.exit("Error: File not found error({0}): {1} and name file is {2}".format(e.errno, e.strerror, name_file))
    except PermissionError as e:
        sys.exit("Error: Permission denied({0}): {1} and name file is {2}".format(e.errno, e.strerror, name_file))
    except:
        sys.exit("Error: Unable to create the file!")
    return file


# This function get text and split it to two files: "article.txt" and "article_sentences.txt"
def get_text_and_division(file_article, file_article_sentences, root, element_tag, index_start, index_end,
                          if_iter=True):
    # Find all the elements the name thg as *element_tag*
    element_list = root.findall(".//" + element_tag)

    # List char - end of sentences
    end_symbol_list = ['. ', "?", "!"]
    i = 0
    first_line = True
    for element in element_list:
        # Over all data in the "element_list"
        if if_iter:
            data = "".join(element.itertext()).strip()
        # Over data in one element the get in "element_tag"
        else:
            data = "".join(str(element.text)).strip()
        # This if check that data not 'None' Or empty
        if data != "None" and len(data) > 0:
            i += 1
            # This if check in the 'p' element that row big from 40 chars
            # and the title of article get from 'index_start' to 'index_end' indexes
            if (element_tag == 'p' and len(data) > 40) or (element_tag != 'p' and index_start <= i <= index_end):
                try:
                    # Replace all "spacial chars" line \t, \t\t,(space char), \n and \r to space char
                    data = data.replace("\t\t", " ")
                    data = data.replace("\t", " ")
                    data = data.replace("  ", " ")
                    data = data.replace("\n", "")
                    file_article.write(data + ". ")

                    for symbol in end_symbol_list:
                        if symbol == '. ':
                            data = data.replace(symbol, ".\r\n")
                        else:
                            data = data.replace(symbol + "\r", symbol + "\r\n")

                    if first_line and element_tag == 'div':
                        file_article_sentences.write(data)
                    else:
                        file_article_sentences.write("\r\n" + data)

                    first_line = False
                except IOError as e:
                    exit("I/O error({0}): {1}".format(e.errno, e.strerror))


def split_text_to_tokenized(file_article_tokenized, name_file):
    # Always add spaces before and after this tokens
    simple_separators = [".", "!", "?", ",", '<', '>', '@', '#',
                         '$', '%', '^', '&', '*', '(', ')', '+', '=',
                         '[', ']', '{', '}', "/", "\\", '_', '~', "-", "'", '"', ":", ";"]
    # Add spaces before and after this tokens only when not between 2 letters (???"? ?'?? ??-?????)
    special_word_separators = ["-", "'", '"']

    # Add spaces before and after this tokens only when not between 2 Digits (1,000,000 5.2,
    # date - 01/01/01 Or 01.01.01)
    special_digit_separators = [".", ",", "/", ':']
    # All lines in the text
    lines = [line.rstrip('\r\n') for line in codecs.open(name_file, 'r', 'utf8')]
    # The char separator between Tokes
    space = " "
    for line in lines:
        text = ""
        index = 0
        if line[index] in simple_separators and line[index + 1] not in simple_separators:
            text += "".join(line[index] + space)
        else:
            text += "".join(line[index])
        for index in range(index + 1, len(line) - 1):
            # the first if in line 89 Checked:
            # Special characters, not between two numbers or two letters
            # Check if line[index] between two digits
            # Check if line[index] between two letters
            if line[index] in simple_separators \
                    and (not (line[index] in special_digit_separators and line[index - 1].isdigit() \
                                      and line[index + 1].isdigit())) \
                    and (not (line[index] in special_word_separators and line[index - 1].isalpha() \
                                      and line[index + 1].isalpha())) \
                    and line[index - 1] != " ":
                # Checked if  '/' between to word   like oren\lior
                if line[index] == "/" and line[index - 1].isalpha() and line[index + 1]:
                    text += "".join(space + line[index] + space)
                # Checked if '-' between to word like the-house and no this-> the------house
                elif line[index] == "-" and line[index - 1].isalpha() and line[index + 1] not in simple_separators:
                    text += "".join(line[index])
                # Checked if  ''' or '"' between to char and before have 'simple separators
                # like this "'Oren bla bla bla'"
                elif (line[index] == "'" or line[index] == '"') and (line[index - 1] in simple_separators \
                                                                             and (line[index + 1].isalpha()) or line[
                        index + 1].isdigit()):
                    text += "".join(line[index] + space)
                else:
                    # Checked if '-' between two number like -> 100-300
                    if line[index] == "-" and line[index - 1].isdigit() and line[index + 1].isdigit():
                        text += "".join((line[index]))
                    else:
                        text += "".join(space + line[index])
            elif line[index] in simple_separators and \
                    (line[index - 1] == " " or line[index - 1] in simple_separators) and \
                    (line[index + 1].isalpha() or line[index + 1].isdigit()):
                text += "".join(line[index] + space)
            else:
                text += "".join(line[index])

        if line[len(line) - 1] in simple_separators:
            text += "".join(space + line[len(line) - 1])
        else:
            text += "".join(line[len(line) - 1])
        file_article_tokenized.write(text + '\r\n')


# Main function that get arguments from user
def main(argv):
    start = time.clock()

    # Receiving arguments from user
    if len(argv) == 3:
        url = str(sys.argv[1])
        path = str(sys.argv[2])
        print("The data folder is: " + path)
    else:
        sys.exit("Error: You have not entered two variables!")
    try:
        request = requests.get(url).text
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(request), parser)
        root = tree.getroot()
    except ConnectionError as e:
        sys.exit("Connection to the Ynet's website failed({0}): {1}".format(e.errno, e.strerror))
    except:
        sys.exit("Error: General fail that not support!!\n"
                 "Please contact the support department by phone - 054-9849566 (ask Oren :-))\n")

    tags_list = [('title', 'div', 2, 3, False), ('body', 'p', True)]
    file_article = open_file(os.path.join(path, "article.txt"))
    file_article_sentences = open_file(os.path.join(path, "article_sentences.txt"))

    file_article_tokenized = open_file(os.path.join(path, "article_tokenized.txt"))

    start2 = time.clock()

    for tag in tags_list:
        if tag[0] == 'title':
            get_text_and_division(file_article, file_article_sentences, root, tag[1], tag[2], tag[3], tag[4])
        else:
            get_text_and_division(file_article, file_article_sentences, root, tag[1], 0, 0, tag[2])
    print("Created the 'article.txt' file, the time taken is ", time.clock() - start2, "sec")
    print("Created the 'article_sentences.txt' file, the time taken is ", time.clock() - start2, "sec")

    file_article.close()
    file_article_sentences.close()

    start2 = time.clock()
    split_text_to_tokenized(file_article_tokenized, "article_sentences.txt")
    print("Created the 'article_sentences.txt' file, the time taken is ", time.clock() - start2, "sec")
    file_article_tokenized.close()
    print("All done :-), the time it takes to produce all the files ", time.clock() - start, "sec")
    pass


if __name__ == "__main__":
    main(sys.argv)
