from lxml import etree
import pprint

class XMLParser:
    def __init__(self, xml_file):
        self.xml_file = xml_file
        self.tree = None

    # A method to load the XML file into memory
    def load_xml(self):
        try:
            self.tree = etree.parse(self.xml_file)
        except Exception as e:
            raise Exception(f"Error loading XML file: {str(e)}")

    # A method to convert an XML element to a dictionary
    def element_to_dict(self, element):
        result = {}
        for child in element.iterchildren():
            result[child.tag] = child.text
        return result

    # A method to extract the flow data from the XML file
    def extract_flow_data(self):
        if self.tree is None:
            raise Exception("XML file not loaded. Call load_xml() first.")

        # get the next element after <dataroot>
        flow_elements = self.tree.xpath(self.tree.getroot()[0].tag)

        return [self.element_to_dict(flow) for flow in flow_elements]