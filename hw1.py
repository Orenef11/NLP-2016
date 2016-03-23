import os, sys, requests, time, codecs
from lxml import etree
from io import StringIO


def open_file(name_file, path):
    file = ""
    try:
        file = codecs.open(path + "\\" + name_file, 'w+', encoding='utf8')
    except FileNotFoundError as e:
        exit("File not found error({0}): {1} and name file is {2}".format(e.errno, e.strerror, name_file))
    return file


def get_text_and_division(file_article, file_article_sentences, root, element_tag, index_start, index_end, \
                          if_iter=True):
    # Find all the elements the name thg as *element_tag*
    element_list = root.findall(".//" + element_tag)

    end_symbol_list = ['. ', "?", "!"]
    i = 0
    first_line = True
    for element in element_list:
        if if_iter:
            data = "".join(element.itertext()).strip()
        else:
            data = "".join(str(element.text)).strip()
        if data != "None" and len(data) > 0:
            i += 1
            if (element_tag == 'p' and len(data) > 50) or (element_tag != 'p' and index_start <= i <= index_end):
                try:
                    data = data.replace("\t\t", " ")
                    data = data.replace("\t", " ")
                    data = data.replace("  ", " ")
                    data = data.replace("\n", "")
                    file_article.write(data)

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


def split_text_to_tokenized(file_article_tokenized):
    # with codecs.open(file_article_sentences, 'r', 'utf8') as f:
    #    print(f.readlines())
    # Always add spaces before and after this tokens



    simple_separators = [".", "!", "?", ",", ";", '<', '>', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=',
                        '[', ']', '{', '}', "/", "\\", '_', '~', "-", "'", '"']

    # Add spaces before and after this tokens only when not between 2 letters (???"? ?'?? ??-?????)
    SpecialSeparators = ["-", "'", '"']

    # Add spaces before and after this tokens only when not between 2 Digits (1,000,000 5.2)
    SpecialDigitSeparators = [".", ",", "/"]

    lines = [line.rstrip('\r\n') for line in codecs.open("article_sentences.txt", 'r', 'utf8')]

    for line in lines:
        # print(line)
        text = ""
        if line[0] in simple_separators:
            text += "".join(line[0] + " ")
        else:
            text += "".join(line[0])
        index = 1
        for index in range(1, len(line)-1):
            if line[index] not in simple_separators  or \
                    line[index] in SpecialDigitSeparators and line[index-1].isdigit() and line[index+1].isdigit() \
                    or line[index] in SpecialSeparators and line[index-1].isalpha() and line[index+1].isalpha():
                text += "".join(line[index])
                #the char is spiceal char
            elif line[index] in simple_separators and line[index] not in SpecialSeparators and \
                    line[index] not in SpecialDigitSeparators:
                text += "".join(line[index] + " ")
            elif ((line[index] in SpecialSeparators and (line[index - 1].isalpha() and line[index + 1] == " ")) \
                    or (line[index] or (line[index+1] == " " and line[index-1] != " "))):
                text += "".join(" " + line[index])
            else:
                text += "".join(line[index])

        if line[len(line)-1] in simple_separators and line[len(line)-2] not in simple_separators:
            text += "".join(" " + line[len(line)-1])
        else:
            text += "".join(line[len(line)-1])
        file_article_tokenized.write(text + '\r\n')







# My code here
def main(argv):
    start = time.clock()
    # url = "http://www.ynet.co.il/articles/0,7340,L-4684564,00.html"
    # url = "http://www.ynet.co.il/articles/0,7340,L-4780286,00.html"

    url = "http://www.ynet.co.il/articles/0,7340,L-4636763,00.html"
    path = r"c:\Users\Oren\Documents\GitHub\NLP-2016"

    """
    # Receiving arguments from user
    if len(argv) == 3:
        url = str(sys.argv[1])
        path = str(sys.argv[2])
        print("The data folder is: " + path)

    else:
        sys.exit("Error: You have not entered two variables!")
    """

    request = requests.get(url).text
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(request), parser)
    root = tree.getroot()

    tags_list = [('title', 'div', 2, 3, False), ('body', 'p', True)]
    #  tag = ('title', 'div', 2, 3, False) -------------('body', 'p', True) -------------------('sun-titke', 'a', True)
    file_article = open_file("article.txt", path)
    file_article_sentences = open_file("article_sentences.txt", path)
    file_article_tokenized = open_file("article_tokenized.txt", path)

    for tag in tags_list:
        if tag[0] == 'title':
            get_text_and_division(file_article, file_article_sentences, root, tag[1], tag[2], tag[3], tag[4])
        else:
            get_text_and_division(file_article, file_article_sentences, root, tag[1], 0, 0, tag[2])

    file_article.close()
    file_article_sentences.close()
    split_text_to_tokenized(file_article_tokenized)
    file_article_tokenized.close()

    print("All done :-), time ", time.clock() - start, "sec")
    pass


if __name__ == "__main__":
    main(sys.argv)
