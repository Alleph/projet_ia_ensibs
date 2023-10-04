from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from XMLParser import XMLParser
import os

class ElasticSearchBulkIndexer:

    def __init__(self, protocol, host, port, crt_path, username, password):

        # Elasticsearch connection settings
        self.es = Elasticsearch(
            f"{protocol}://{host}:{port}",
            ca_certs = crt_path,
            basic_auth = (username, password))

        # Elasticsearch connection check
        if not self.es.ping():
            raise ValueError("Connection to ElasticSearch server failed")

        print("Connection to ElasticSearch server successful !")

    def bulk_index_data(self, xml_filename):
            
        # Create an XMLParser object
        xml_parser = XMLParser(xml_filename)

        # Load the XML file (flows of the file are stocked in self.tree)
        xml_parser.load_xml()

        # Extract the flow data from the XML file
        flow_data = xml_parser.get_flows()

        # Get the base name of the XML file and remove the extension and lower case it
        xml_filename = os.path.basename(xml_filename)
        xml_filename = os.path.splitext(xml_filename)[0]
        xml_filename = xml_filename.lower()

        # Prepare a list of actions for bulk indexing
        actions = []
        for flow in flow_data:
            action = {
                "_index": xml_filename,
                "_source": {
                    'data': flow,
                    'origin': xml_filename  # Store the origin (file name) as a field
                }
            }
            actions.append(action)

        # Bulk index the flow data
        success, _ = bulk(self.es, actions)

        print(f"Successfully indexed {success} flows")
    
            