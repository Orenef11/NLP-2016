# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import os, sys, requests, time, codecs
from lxml import etree
from io import StringIO


def open_file(name_file, path):
    file = ""
    try:
        file = open(path + "\\" + name_file, 'w', -1, 'utf8')
    except FileNotFoundError as e:
        exit("File not found error({0}): {1}".format(e.errno, e.strerror))
    return file


def get_text_and_division(file_article, file_article_sentences, root, element_tag, index_start, index_end, if_iter=True):
    # Find all the elements the name thg as *element_tag*
    element_list = root.findall(".//" + element_tag)

    i = 0
    for element in element_list:
        if if_iter:
            data = "".join(element.itertext()).strip()
        else:
            data = "".join(str(element.text)).strip()
        if data != "None" and len(data) > 0:
            i += 1
            if (element_tag != 'p' and index_start <= i <= index_end) or (element_tag == 'p' and len(data) > 50):
                try:
                    data = data.replace("\t\t", " ")
                    data = data.replace("\t", " ")
                    data = data.replace("\r", "")
                    data = data.replace("\n", "")
                    file_article.write(data)
                    data = data.replace(". ", '.\r\n')
                    file_article_sentences.write(data + "\r\n")
                except IOError as e:
                    exit("I/O error({0}): {1}".format(e.errno, e.strerror))


# My code here
def main(argv):
    start = time.time()
    # url = "http://www.ynet.co.il/articles/0,7340,L-4684564,00.html"
    url = "http://www.ynet.co.il/articles/0,7340,L-4780286,00.html"
    path = r"c:\Users\Oren\Documents\GitHub\NLP-2016"

    # Receiving arguments from user
    if len(argv) == 3:
        url = str(sys.argv[1])
        path = str(sys.argv[2])
        print("The data folder is: " + path)
    else:
        sys.exit("Error: You have not entered two variables!")

    request = requests.get(url).text
    parser = etree.HTMLParser()
    tree = etree.parse(StringIO(request), parser)
    root = tree.getroot()
    tags_list = [('title', 'div', 2, 3, False), ('body', 'p', True)]

    file_article = open_file("article.txt", path)
    file_article_sentences = open_file("article_sentences.txt", path)

    for tag in tags_list:
        if tag[1] == 'div':
            get_text_and_division(file_article, file_article_sentences, root, tag[1], tag[2], tag[3], tag[4])
        else:
            get_text_and_division(file_article, file_article_sentences, root, tag[1], 0, 0, tag[2])

    print("All done :-), time ", time.time() - start)
    pass

if __name__ == "__main__":
    main(sys.argv)
