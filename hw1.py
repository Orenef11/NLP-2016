#*********************************#
# Po
#
#
#*********************************#

import os, sys, requests, codecs
from lxml import html, etree

def createFile(path, nameFile, accessMode):
    #Save the *nameFile*.text file in resulting location
    html_file = open(os.path.join(path, nameFile), accessMode, -1, 'utf8')
    html_file.write(requests.get(url).text)
    html_file.close()

def splitTextToSentences(indexStart, indexEbd, nameFile, tagName):
    parser = etree.HTMLParser()
    tree = etree.parse(nameFile, parser)
    i = 0
    flag = True
    root = tree.getroot()
    for child in root:
        if flag == False:
            break
        print(child.tag)
        child.find(tagName)
        for x in child.iter(tagName):
            if x.text != None and len(x.text) > 3 and flag == True:
                if(i > indexStart and i < indexEbd):
                    outputFileStream.writelines(x.text + "\r\n")
                i += 1
                if i == indexEbd:
                    flag = False


url = 'http://www.ynet.co.il/articles/0,7340,L-4684564,00.html'
path = 'C:/Users\Oren\PycharmProjects\\NLP'

#if len(sys.argv) != 3:
#    sys.exit("Error: You have not entered two variables!")
#else:
#    url = sys.argv[1]
#    path = sys.argv[2]
#    print("The data folder is: " + path)

#Create new file
createFile(path, "html.html", "w")
createFile(path, "article.txt", "w")
#inputFileStream = codecs.open("in1.txt", "r", "utf-8")
outputFileStream = codecs.open("article.txt", "w", "utf-8")

splitTextToSentences(0, 3, "html.html", "div")
splitTextToSentences(0, 300, "html.html", "p")





os.remove(path + "\\html.html")


#print(tree.xpath())
#tree = etree.fromstring(page.text)
#xmlstr = tree.tostring(tree, encoding='utf8', method='xml')
