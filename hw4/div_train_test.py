#################
# Oren Efraimov  #
#                #
# Lior Portnoy   #
##################


from time import clock
from sys import argv
from os.path import join
import xml.etree.ElementTree as ET
from random import randrange
from auxiliary_class import Instance

DIV_TEST_SIZE = 50


#######################################
# Function - 'instance_parsing'
# The function get in put path for file
# parsing and return instances list
# from xml.
#######################################
def instance_parsing(path_file):
    etree = ET.parse(path_file)
    root = etree.getroot()
    instances = root.findall(".//instance")
    instances_list = []
    for child in instances:
        instance = Instance()
        instance.parsing_instance_to_object(child)
        instances_list.append(instance)

    return instances_list


###################################################
# Function - 'div_train_and_test_file'
# The function get list of instances from xml file
# and return dictionary of instances by sense id
###################################################
def div_train_and_test_file(instances_list):
    div_instances_to_category_dict = {}

    for instance in instances_list:
        senseid = instance.senseid
        if senseid in div_instances_to_category_dict.keys():
            div_instances_to_category_dict[senseid].append(instance)
        else:
            div_instances_to_category_dict[senseid] = [instance]

    return div_by_category(div_instances_to_category_dict)


################################################
# Function - 'div_by_category'
# The function take from every section group of
# instances for testing file.
################################################
def div_by_category(instances_by_category_dict):
    instances_test = {}
    for key in instances_by_category_dict:
        i = 0
        dict_size = len(instances_by_category_dict[key])
        instances_test[key] = []
        while i < DIV_TEST_SIZE:
            index = randrange(0, dict_size - i)
            instance_temp = instances_by_category_dict[key][index]
            instances_test[key].append(instance_temp)
            instances_by_category_dict[key].remove(instances_by_category_dict[key][index])
            i += 1

    return instances_test, instances_by_category_dict


#############################################
# Function - 'export_to_xml_file'
# The function get instances list and create
# xml file with correct xml objects that
# contain the in stances.
#############################################
def export_to_xml_file(instances_dict, xml_file_name):
    root = ET.Element("corpus", lang="en")
    lexelt = ET.SubElement(root, "lexelt", item="line-n")
    for key in instances_dict:
        for instance in instances_dict[key]:
            # This item is Instance object
            lexelt.append(instance.instance_xml)

    print("Create xml file that name is ", xml_file_name)
    ET.ElementTree(root).write(xml_file_name)


def main(argv):
    start = clock()
    if len(argv) < 3:
        exit("Error: You need to enter like that: python div_train_test.py <input_file_path> <output_files_path>")
    else:
        print("The input file path entered is: ", argv[1])
        print("The output file path entered is: ", argv[2])

    instances_list = instance_parsing(argv[1])
    all_instance_test_dict, all_instance_train_dict = div_train_and_test_file(instances_list)
    export_to_xml_file(all_instance_test_dict, join(argv[2], "test.xml"))
    export_to_xml_file(all_instance_train_dict, join(argv[2], "train.xml"))
    print("All done :-), the time it takes to produce all the files ", clock() - start, "sec")

if __name__ == "__main__":
    main(argv)