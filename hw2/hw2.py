# **************#
# Portnoy Lior
# Efraimov Oren
# **************#

import sys, requests, time, codecs, os, re
from lxml import etree
from io import StringIO

def split_to_sentncets(in_file_name, out_file_name):
    data = codecs.open(in_file_name, 'r', 'utf8').read()
    out_data = codecs.open(out_file_name, 'w+', 'utf8')
    end_symbol_list = ['. ', "? ", "! "]

    data = data.replace("\t\t", " ")
    data = data.replace("\t", " ")
    data = data.replace("  ", " ")
    data = data.replace("\r", "")
    data = data.replace("\n", "")
    for symbol in end_symbol_list:
        data = data.replace(symbol, symbol.split(" ")[0] + "\r\n")

    out_data.write(data)
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

    file_article_tokenized.close()


def main():
    split_to_sentncets('childes.txt', 'childes_out.txt')
    token_file = codecs.open('childes_out_token.txt', 'w+', 'utf8')
    split_text_to_tokenized(token_file, 'childes_out.txt')

    data = codecs.open('childes_out_token.txt', 'r', 'utf8').read()
    count_words = len(data.split())


    pass


if __name__ == "__main__":
    main()
