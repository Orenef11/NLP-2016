#*********************************#
# Po
#
#
#*********************************#

import os, sys, requests, codecs
from lxml import html, etree

def createFile(path, nameFile, accessMode):
    #Save the article.text file in resulting location
    path = os.path.join(path, nameFile)
    page = requests.get(url)
    html_file = open(path, accessMode, -1, 'utf8')
    html_file.write(page.text)
    html_file.close()

url = 'http://www.ynet.co.il/articles/0,7340,L-4684564,00.html'
path = 'C:/Users\Oren\PycharmProjects\\NLP'

#if len(sys.argv) != 3:
#    sys.exit("Error: You have not entered two variables!")
#else:
#    url = sys.argv[1]
#    path = sys.argv[2]

createFile(path, "article.html", "w")

parser = etree.HTMLParser()
tree = etree.parse("article.html", parser)

root = tree.getroot()
for child in root:
    print(child.tag)
    child.find("p")
    for x in child.iter("p"):
        if(x.text != None):
            str = x.text
            print(str)
            #print(x.tag, str.codecs.decode("cp1255").encode('utf8'))
        #, codecs.utf_8_encode(x.text(encoding='UTF-8')))




#print(tree.xpath())
#tree = etree.fromstring(page.text)
#xmlstr = tree.tostring(tree, encoding='utf8', method='xml')
