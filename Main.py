from ElasticSearchBulkIndexer import ElasticSearchBulkIndexer as ebi
from XMLParser import XMLParser
from SearchingFunctions import SearchingFunctions
import pprint
import os
import glob

# Constants for the Elasticsearch connection
PROTOCOL = "https"
HOST = "localhost"
PORT = 9200
ELASTIC_USERNAME = "elastic"
ELASTIC_PASSWORD = "uQksh15EsPWSzw1vq7s1"
CRT_PATH = "certs/http_ca.crt"

# List of xml files to index
XML_DIR = "TRAIN_ENSIBS"
XML_FILES = glob.glob(os.path.join(XML_DIR, "*.xml"))

def main():

    # Create an ElasticsearchBulkIndexer object
    bulk_indexer = ebi(
        PROTOCOL, 
        HOST, 
        PORT, 
        CRT_PATH, 
        ELASTIC_USERNAME, 
        ELASTIC_PASSWORD)

    # Delete all indexes at the beginning
    #bulk_indexer.delete_all_indexes()

    xml_file = XML_FILES[0]
    
    # Index the XML file
    #bulk_indexer.bulk_index_data(xml_file)

    # Init searching functions
    sf = SearchingFunctions(bulk_indexer.es, "flows")

    # If you want to get all the indexes
    #sf.get_all_indexes()

    # If you want to get all the flows
    #pprint.pprint(sf.match_all())

    # If you want to get all the protocols
    #pprint.pprint(sf.get_protocols())

    # If you want to get all the flows for a given protocol
    #pprint.pprint(sf.get_flows_for_protocol("tcp_ip"))

    # If you want to get the number of flows for each protocol
    # pprint.pprint(sf.get_nb_flows_for_each_protocol())

    # If you want to get the source and destination Payload size for each protocol
    #pprint.pprint(sf.get_payload_size_for_each_protocol())

    # If you want to get the source and destination total bytes for each protocol
    pprint.pprint(sf.get_total_bytes_for_each_protocol())


if __name__ == "__main__":
    main()