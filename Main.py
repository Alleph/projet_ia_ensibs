from ElasticSearchBulkIndexer import ElasticSearchBulkIndexer as ebi
from XMLParser import XMLParser
from Converter import Converter
from SearchingFunctions import SearchingFunctions
from Drawer import Drawer
import pprint
import os
import glob
import time

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

    #for xml_file in XML_FILES:
        # Index the XML file
        #bulk_indexer.bulk_index_data(xml_file)
    
    # Index the XML file
    #bulk_indexer.bulk_index_data(xml_file)

    # Wait few seconds for the indexing to be done
    time.sleep(5)

    # Init searching functions
    sf = SearchingFunctions(bulk_indexer.es, "flows")

    # Init the drawer
    drawer = Drawer(bulk_indexer.es, sf, "flows")

    # If you want to get all the indexes
    #sf.get_all_indexes()

    # If you want to get all the flows
    #pprint.pprint(sf.match_all())

    # If you want to get all the protocols
    protocols = sf.get_protocols()
    pprint.pprint(protocols)

    # If you want to get all the flows for a given protocol
    #protocol = "tcp_ip"
    #flows_by_protocol = sf.get_flows_for_protocol(protocol)
    #pprint.pprint(flows_by_protocol)

    # If you want to get the number of flows for each protocol
    #nb_flows_per_protocol = sf.get_nb_flows_for_each_protocol()
    #pprint.pprint(nb_flows_per_protocol)

    # If you want to get the source and destination Payload size for each protocol
    #payload_size_per_protocol = sf.get_payload_size_for_each_protocol()
    #pprint.pprint(payload_size_per_protocol)

    # If you want to get the source and destination total bytes for each protocol
    #total_bytes_per_protocol = sf.get_total_bytes_for_each_protocol()
    #pprint.pprint(total_bytes_per_protocol)

    # If you want to get the total source/destination packets for each protocol
    #total_packets_per_protocol = sf.get_total_packets_for_each_protocol()
    #pprint.pprint(total_packets_per_protocol)

    # If you want to  get the list of all the distinct applications
    #applications = sf.get_applications()
    #pprint.pprint(applications)

    # If you want to get the list of flows for a given application
    #application = "Unknown_UDP"
    #flows_by_application = sf.get_flows_for_application(application)
    #pprint.pprint(flows_by_application)

    # If you want to get the number of flows for each application
    #nb_flows_per_application = sf.get_nb_flows_for_each_application()
    #pprint.pprint(nb_flows_per_application)

    # It you want to get the source and destination Payload size for each application
    #payload_size_per_application = sf.get_payload_size_for_each_application()
    #pprint.pprint(payload_size_per_application)

    # If you want to get the source and destination total bytes for each application
    #total_bytes_per_application = sf.get_total_bytes_for_each_application()
    #pprint.pprint(total_bytes_per_application)

    # If you want to get the total source/destination packets for each application
    #total_packets_per_application = sf.get_total_packets_for_each_application()
    #pprint.pprint(total_packets_per_application)

    # If you want to get the number of flows for each number of packets
    #nb_flows_for_each_nb_packets = sf.get_nb_flows_for_each_nb_packets()
    #pprint.pprint(nb_flows_for_each_nb_packets)

    # If you want to get the number of flows for each tcp flags
    #nb_flows_for_each_tcp_flags = sf.get_nb_flows_for_each_tcp_flags()
    #pprint.pprint(nb_flows_for_each_tcp_flags)

    # Draw the Zipf's law for the number of packets
    #drawer.draw_zipf_for_each_nb_packets()

    # Init the converter
    cv = Converter(bulk_indexer.es, sf, "flows")

if __name__ == "__main__":
    main()