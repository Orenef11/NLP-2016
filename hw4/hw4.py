import sys, time, os, codecs
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, ENGLISH_STOP_WORDS
from sklearn.feature_selection import SelectKBest
from os.path import join

import xml.etree.ElementTree as ET

class INSTANCE:
    def __init__(self, instance_id="", answer_id="", senseid="", data="", instance_xml=""):
        self.instance_id = instance_id
        self.answer_id = answer_id
        self.senseid = senseid
        self.data = data
        self.instance_xml = instance_xml

    def parsing_instance_to_object(self, instance_xml):
        for child in instance_xml.iter():
            sub_tags = list(child.attrib)

            for tag in sub_tags:
                if tag == "id":
                    self.instance_id = str(child.attrib[tag])
                if tag == "instance":
                    self.answer_id = str(child.attrib[tag])
                if tag == "senseid":
                    self.senseid = child.attrib[tag]
            if child.tag == "context":
                texts = []
                for sub_child in child.iter():
                    texts.append(sub_child.text)
                context = ""
                i = 1
                for text in texts:
                    context += text
                    if i < len(texts):
                        context += "\r\n"
                    i += 1

                self.context = context
        self.instance_xml = instance_xml

    def to_string(self):
        print("Instance id is ", self.instance_id)
        print("Answer instance id is ", self.answer_id, " and senseid is ", self.senseid)
        print("The context is {0}".format(self.context))

def instance_parsing(path_file):
    etree = ET.parse(path_file)
    root = etree.getroot()
    instances = root.findall(".//instance")
    instances_list = []
    for child in instances:
        instance = INSTANCE()
        instance.parsing_instance_to_object(child)
        instances_list.append(instance)

    return instances_list


def export_to_xml_file(list_object_instances, xml_file_name):
    root = ET.Element("corpus", lang="en")
    lexelt = ET.SubElement(root, "lexelt", item="line-n")
    for item in list_object_instances:
        lexelt.append(item.instance_xml)

    ET.ElementTree(root).write(xml_file_name)

def main():
    start = time.clock()
    instances_list = instance_parsing("line.S2.data.clean.xml")
    export_to_xml_file(instances_list, "d1.xml")
    print("All done :-), the time it takes to produce all the files ", time.clock() - start, "sec")

if __name__ == "__main__":
    main()
