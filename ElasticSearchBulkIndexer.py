from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from elasticsearch.exceptions import ElasticsearchWarning
from XMLParser import XMLParser
import warnings
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
            #print(flow)
            action = {
                "_index": "flows"
            }
            for key, value in flow.items():
                action[key] = value
            actions.append(action)

        # Bulk index the flow data
        success, _ = bulk(self.es, actions)

        print(f"Successfully indexed {success} flows")

    def delete_index(self, index_name):
        self.es.indices.delete(index=index_name, ignore=[400, 404])

    def delete_all_indexes(self):
        try:
            warnings.filterwarnings("ignore", category=ElasticsearchWarning)

            # Get a list of all aliases without fetching the actual system indices
            response = self.es.indices.get_alias(index="*")

            # List of system indices to exclude from deletion
            system_indices = [".security-7"]

            # Filter out system indices from the list
            indexes_to_delete = [index for index in response.keys() if index not in system_indices]

            # Delete non-system indexes
            for index in indexes_to_delete:
                self.es.indices.delete(index=index)
                print(f"Index {index} deleted successfully.")

            print("Indexes deleted successfully (except system indices).")

        except Exception as e:
            print(f"An error occurred: {e}")
        
            