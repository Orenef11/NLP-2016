class Instance(object):

    def __init__(self, instance_id="", answer_id="", senseid="", context="", sentences_size_in_context="",
                 instance_xml=""):
        self.instance_id = instance_id
        self.answer_id = answer_id
        self.senseid = senseid
        self.context = context
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
                context = ""
                for sub_child in child.iter():
                    context += sub_child.text + "\r\n"

                self.context = context.strip()
        self.instance_xml = instance_xml

    def tostring(self):
        print("Instance id is ", self.instance_id)
        print("Answer instance id is ", self.answer_id, " and senseid is ", self.senseid)
        print("The context is {0}".format(self.context))
