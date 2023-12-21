from lxml import etree
import pprint

class XMLParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = None

    # A method to stock all flows in self.tree
    def load_xml(self):
        print("Parsing XML file. . .")
        try:
            context = etree.iterparse(self.xml_file, events=('start',))
            self.tree = []
            tag_to_parse = None
            flow_counter = 0
            for event, elem in context:
                if tag_to_parse is None and (elem.tag != 'dataroot'):
                    tag_to_parse = elem.tag
                    #print(f"Tag to parse 1: {tag_to_parse}")
                    #print(f"tree: {self.tree}")
                if elem.tag == tag_to_parse:
                    self.tree.append(self.element_to_dict(elem))
                    #print(f"elem to parse 2: {elem}")
                    #print(f"tree: {self.tree}")
                    elem.clear()
                    flow_counter += 1

                    if flow_counter % 500000 == 0:
                        print(f"{flow_counter} flows parsed")
        except Exception as e:
            raise Exception(f"Error loading XML file: {str(e)}")

    # A method to stock all flows in self.tree but not by using iterparse
    def load_xml2(self):
        try:
            self.tree = []
            context = etree.parse(self.xml_file)
            tag_to_parse = 'item'
            for element in context.iter(tag_to_parse):
                self.tree.append(self.element_to_dict(element))
        except Exception as e:
            raise Exception(f"Error loading XML file: {str(e)}")

    # A method to extract flow data from self.tree
    def get_flows(self):
        if self.tree is None:
            raise Exception("XML file not loaded")
        return self.tree

    # A method to convert an XML element to a dictionary
    def element_to_dict(self, element):
        result = {}
        for child in element.iterdescendants():
            result[child.tag] = child.text
        return result