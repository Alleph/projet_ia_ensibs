from lxml import etree

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
        
        # Looking for the TestbedMonJun14Flows element
        flow_elements = self.tree.xpath("//TestbedMonJun14Flows")
        return [self.element_to_dict(flow) for flow in flow_elements]

# Example usage:
if __name__ == "__main__":
    xml_parser = XMLParser("./TRAIN_ENSIBS/TestbedMonJun14Flows.xml")
    xml_parser.load_xml()
    flow_data = xml_parser.extract_flow_data()
    if flow_data:
        print(flow_data)  # Print the first flow dictionary
