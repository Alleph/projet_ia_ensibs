from lxml import etree
import pprint

class XMLParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = None

    # A method to stock all flows in self.tree
    def load_xml(self):
        try:
            context = etree.iterparse(self.xml_file, events=('start',))
            self.tree = []
            tag_to_parse = None
            for event, elem in context:
                if tag_to_parse is None and elem.tag != 'dataroot':
                    tag_to_parse = elem.tag
                if elem.tag == tag_to_parse:
                    self.tree.append(self.element_to_dict(elem))
                    elem.clear()
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