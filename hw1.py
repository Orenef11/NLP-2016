# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import codecs
import os
import sys
import requests
from lxml import etree


# My code here
def main(argv):
    url = 'http://www.ynet.co.il/articles/0,7340,L-4684564,00.html'
    path = 'C:\\Users\Oren\Documents\GitHub\\NLP-2016'

    arr_file_names = ['article.txt', 'article_sentences.txt', 'article_tokenized.txt']
    # Receiving arguments from user
    if len(argv) == 3:
        url = sys.argv[1]
        path = sys.argv[2]
        print("The data folder is: " + path)
    """else:
            sys.exit("Error: You have not entered two variables!")
    """
    # Files list with name of temp file
    arr_temp_files = ['text.txt', 'temp.txt', 'temp2.txt']
    create_files(arr_temp_files, path)
    create_files(arr_file_names, path)

    codecs.open("text.txt", "r+", "utf8").write(requests.get(url).text)
    get_text_from_html(0, 3, "text.txt", "temp.txt", 'div')
    get_text_from_html(1, 1000, "text.txt", "temp2.txt", 'p')
    

    arr_files = ['temp.txt', 'temp2.txt']
    merging_multiple_files(arr_files, arr_file_names[0])
    split_text_to_sentences(arr_file_names[0], arr_file_names[1])

    remove_files(arr_temp_files, path)
    arr_files.clear()
    arr_files.clear()
    pass

def get_text_from_html(index_start, index_end, name_file_source, name_file_target, tag_name):
    # Counter the number of 'child' in the tree
    i = 0
    # Stop the loop when get tne text from file
    flag = False
    output_file_stream = codecs.open(name_file_target, "w", 'utf8')

    parser = etree.HTMLParser()
    tree = etree.parse(name_file_source, parser)
    root = tree.getroot()
    for child in root:
        if flag is True:
            break
        for x in child.iter(tag_name):
            # If there is information in the font tag indise *tag_name* tag
            flag2 = False
            if tag_name == "p":
                for child_fort in x.iter("font"):
                    if child_fort.text is not None:
                        flag2 = True
                        output_file_stream.writelines(child_fort.text)
                    """for child_p in child_fort.iter("p"):
                        if child_p.text is not None:
                            output_file_stream.writelines(child_p.text)"""
            if flag2:
                output_file_stream.write(". ")
            if x.text is not None and len(x.text) > 5 and not flag:
                if index_start < i < index_end:
                    #print("i = ", i, x.tag + x.text)
                    if x.tag == "div":
                        output_file_stream.writelines(x.text + ". ")
                    else:
                        output_file_stream.writelines(x.text)
                i += 1
            if index_end == i:
                flag = True
    output_file_stream.close()
def merging_multiple_files(arr_files, name_file_target):
    file = codecs.open(name_file_target, "w", "utf8")
    for temp_file in arr_files:
        temp_file = codecs.open(temp_file, "r", "utf8")
        file.write(temp_file.read())
        temp_file.close()
    file.close()
def create_files(arr_files, path):
    # Create file for each name file
    for name in arr_files:
        codecs.open(os.path.join(path, name), "w", "utf8").close()
def split_text_to_sentences(name_file_source, name_file_target):
    input_file_stream = codecs.open("article.txt", "r", "utf8")
    output_file_stream = codecs.open("article_sentences.txt", "w", 'utf8')
    # lines = tuple(open(name_file_target, 'r'))
    for line in input_file_stream.readlines():
        lines = str(line).split("\r\n")
        for line2 in lines:
            lines2 = line2.split(". ")
            for line3 in lines2:
                lines3 = line3.split(".")
                for line4 in lines3:
                    if len(line4) > 2:
                        output_file_stream.write(line4 + ".\r\n")
    input_file_stream.close()
    output_file_stream.close()
def remove_files(list_files, path):
    for file in list_files:
        os.remove(path + "\\" + file)

if __name__ == "__main__":
    main(sys.argv)