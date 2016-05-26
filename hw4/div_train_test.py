import sys, time, os
from os.path import join
import xml.etree.ElementTree as ET
from random import randrange
from auxiliary_class import INSTANCE
# class INSTANCE:
#     def __init__(self, instance_id="", answer_id="", senseid="", data="", instance_xml=""):
#         self.instance_id = instance_id
#         self.answer_id = answer_id
#         self.senseid = senseid
#         self.data = data
#         self.instance_xml = instance_xml
#
#     def parsing_instance_to_object(self, instance_xml):
#         for child in instance_xml.iter():
#             sub_tags = list(child.attrib)
#
#             for tag in sub_tags:
#                 if tag == "id":
#                     self.instance_id = str(child.attrib[tag])
#                 if tag == "instance":
#                     self.answer_id = str(child.attrib[tag])
#                 if tag == "senseid":
#                     self.senseid = child.attrib[tag]
#             if child.tag == "context":
#                 texts = []
#                 for sub_child in child.iter():
#                     texts.append(sub_child.text)
#                 context = ""
#                 i = 1
#                 for text in texts:
#                     context += text
#                     if i < len(texts):
#                         context += "\r\n"
#                     i += 1
#
#                 self.context = context
#         self.instance_xml = instance_xml
#
#     def tostring(self):
#         print("Instance id is ", self.instance_id)
#         print("Answer instance id is ", self.answer_id, " and senseid is ", self.senseid)
#         print("The context is {0}".format(self.context))

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

def export_to_xml_file(object_instances_list, xml_file_name):
    root = ET.Element("corpus", lang="en")
    lexelt = ET.SubElement(root, "lexelt", item="line-n")
    # print(len(object_instances_list[0]))
    # exit()
    for i in range(len(object_instances_list)):
        j = 0
        for item in object_instances_list[i]:
            lexelt.append(item.instance_xml)
            j += 1
        print(i, " --------", j)

    print("Create xml file that name is ", xml_file_name)
    ET.ElementTree(root).write(xml_file_name)

def div_train_and_test_file(object_instances_list):
    cord_instances = []
    formation_instances = []
    phone_instances = []
    division_instances = []
    product_instances = []

    for instance in object_instances_list:
        # print(instance);print(type(instance));exit()
        if instance.senseid == "cord":
            cord_instances.append(instance)
        elif instance.senseid == "formation":
            formation_instances.append(instance)
        elif instance.senseid == "phone":
            phone_instances.append(instance)
        elif instance.senseid == "division":
            division_instances.append(instance)
        elif instance.senseid == "product":
            product_instances.append(instance)

    cord_instance_test, cord_instance_train = div_by_category(cord_instances)
    formation_instance_test, formation_instance_train = div_by_category(formation_instances)
    phone_instance_test, phone_instance_train = div_by_category(phone_instances)
    division_instance_test, division_instance_train = div_by_category(division_instances)
    product_instance_test, product_instance_train = div_by_category(product_instances)

    all_instance_test = [cord_instance_test, formation_instance_test, phone_instance_test,
                          division_instance_test, product_instance_test]
    all_instance_train = [cord_instance_train, formation_instance_train, phone_instance_train,
                          division_instance_train, product_instance_train]

    return all_instance_test, all_instance_train

    # print(len(cord_instances))
    # print(len(formation_instances))
    # print(len(phone_instances))
    # print(len(division_instances))
    # print(len(product_instances))
    #
    # print(len(cord_instances) + len(formation_instances) + len(phone_instances) +len(division_instances) +len(product_instances))

def div_by_category(object_instances_by_category_list):
    instance_test = {}
    while len(instance_test) < 50:
        index = randrange(0, len(object_instances_by_category_list))
        instance_test[index] = object_instances_by_category_list[index]

    for value in instance_test.values():
        object_instances_by_category_list.remove(value)

    print(len(object_instances_by_category_list), "----", len(instance_test))
    return list(instance_test.values()), object_instances_by_category_list


def main(argv):
    start = time.clock()
    if len(argv) < 3:
        exit("Error: You need to enter like that: python div_train_test.py <input_file_path> <output_files_path>")
    else:
        print("The input file path entered is: ", argv[1])
        print("The output file path entered is: ", argv[2])
    instances_list = instance_parsing(argv[1])
    all_instance_test, all_instance_train = div_train_and_test_file(instances_list)
    export_to_xml_file(all_instance_test, join(argv[2], "test.xml"))
    export_to_xml_file(all_instance_train, join(argv[2], "train.xml"))
    print("All done :-), the time it takes to produce all the files ", time.clock() - start, "sec")

if __name__ == "__main__":
    main(sys.argv)
