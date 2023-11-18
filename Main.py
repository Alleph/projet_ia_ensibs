from ElasticSearchBulkIndexer import ElasticSearchBulkIndexer as ebi
from classification_preparer import *
from XMLParser import XMLParser
from Converter import Converter
from SearchingFunctions import SearchingFunctions
from Drawer import Drawer
import os
import pprint
import glob
import time

# Constants for the Elasticsearch connection
PROTOCOL = "https"
HOST = "localhost"
PORT = 9200
ELASTIC_USERNAME = "elastic"
ELASTIC_PASSWORD = "trouvemoica"
CRT_PATH = "certs/http_ca.crt"

# List of xml files to index
XML_DIR = "TRAIN_ENSIBS"
XML_FILES = glob.glob(os.path.join(XML_DIR, "*.xml"))


def main():
    ###------------------------------------------------------------------------------------------###
    ###----------- Start indexation and initialize researcher, drawer and converter -------------###
    ###------------------------------------------------------------------------------------------###

    # Create an ElasticsearchBulkIndexer object
    bulk_indexer = ebi(
        PROTOCOL,
        HOST,
        PORT,
        CRT_PATH,
        ELASTIC_USERNAME,
        ELASTIC_PASSWORD)

    # Delete all indexes at the beginning
    # bulk_indexer.delete_all_indexes()

    # Index all the XML files
    # for xml_file in XML_FILES:
    #    bulk_indexer.bulk_index_data(xml_file)

    # Index only one XML file
    # xml_file = XML_FILES[1]
    # bulk_indexer.bulk_index_data(xml_file)

    # Wait few seconds for the indexing to be done
    # time.sleep(5)

    # Init searching functions
    sf = SearchingFunctions(bulk_indexer.es, "flows")

    # Init the drawer
    # drawer = Drawer(bulk_indexer.es, sf, "flows")

    # Init the converter
    cv = Converter(bulk_indexer.es, sf, "flows")

    ###------------------------------------------------------------------------------------------###
    ###---------------------------------- Searching functions -----------------------------------###
    ###------------------------------------------------------------------------------------------###

    # If you want to get all the indexes
    # sf.get_all_indexes()

    # If you want to get all the flows
    # pprint.pprint(sf.match_all())

    # If you want to get all the protocols
    # protocols = sf.get_protocols()
    # pprint.pprint(protocols)

    # If you want to get all the flows for a given protocol
    # protocol = "tcp_ip"
    # flows_by_protocol = sf.get_flows_for_protocol(protocol)
    # pprint.pprint(flows_by_protocol)

    # If you want to get the number of flows for each protocol
    # nb_flows_per_protocol = sf.get_nb_flows_for_each_protocol()
    # pprint.pprint(nb_flows_per_protocol)

    # If you want to get the source and destination Payload size for each protocol
    # payload_size_per_protocol = sf.get_payload_size_for_each_protocol()
    # pprint.pprint(payload_size_per_protocol)

    # If you want to get the source and destination total bytes for each protocol
    # total_bytes_per_protocol = sf.get_total_bytes_for_each_protocol()
    # pprint.pprint(total_bytes_per_protocol)

    # If you want to get the total source/destination packets for each protocol
    # total_packets_per_protocol = sf.get_total_packets_for_each_protocol()
    # pprint.pprint(total_packets_per_protocol)

    # If you want to  get the list of all the distinct applications
    # applications = sf.get_applications()
    # pprint.pprint(applications)

    # If you want to get the list of flows for a given application
    application = "HTTPWeb"
    HTTPWeb_flows = sf.get_flows_for_application(application)
    print("len(HTTPWeb) = ", len(HTTPWeb_flows))
    # pprint.pprint(HTTPWeb_flows)

    # If you want to get the number of flows for each application
    # nb_flows_per_application = sf.get_nb_flows_for_each_application()
    # pprint.pprint(nb_flows_per_application)

    # It you want to get the source and destination Payload size for each application
    # payload_size_per_application = sf.get_payload_size_for_each_application()
    # pprint.pprint(payload_size_per_application)

    # If you want to get the source and destination total bytes for each application
    # total_bytes_per_application = sf.get_total_bytes_for_each_application()
    # pprint.pprint(total_bytes_per_application)

    # If you want to get the total source/destination packets for each application
    # total_packets_per_application = sf.get_total_packets_for_each_application()
    # pprint.pprint(total_packets_per_application)

    # If you want to get the number of flows for each number of packets
    # nb_flows_for_each_nb_packets = sf.get_nb_flows_for_each_nb_packets()
    # pprint.pprint(nb_flows_for_each_nb_packets)

    # If you want to get the number of flows for each tcp flags
    # nb_flows_for_each_tcp_flags = sf.get_nb_flows_for_each_tcp_flags()
    # pprint.pprint(nb_flows_for_each_tcp_flags)

    ###------------------------------------------------------------------------------------------###
    ###---------------------------------- Drawer functions --------------------------------------###
    ###------------------------------------------------------------------------------------------###

    # Draw the Zipf's law for the number of packets
    # drawer.draw_zipf_for_each_nb_packets()

    ###------------------------------------------------------------------------------------------###
    ###----------------------- Classification preparation --------------------------###
    ###------------------------------------------------------------------------------------------###
    print("--- Classification preparation ---")
    # split flow between normal and attack :
    HTTPWeb_flows_normal, HTTPWeb_flows_attack = get_normal_and_attack_flows(HTTPWeb_flows)

    # convert to vector :
    normal_vector = flows_to_vector(HTTPWeb_flows_normal, cv)
    attack_vector = flows_to_vector(HTTPWeb_flows_attack, cv)

    # split in 5 subsets and store in files :
    files = ['binarized_flows/binarized_flows_test_1', 'binarized_flows/binarized_flows_test_2',
             'binarized_flows/binarized_flows_test_3', 'binarized_flows/binarized_flows_test_4',
             'binarized_flows/binarized_flows_test_5']
    write_subsets_on_files(normal_vector, attack_vector, cv, files)

    # get the 5 subsets to verify
    subsets = read_subsets_from_files(files)
    for i in range(len(subsets)):
        print("subset n°", i+1, ":", len(subsets[i]), "vectors.")
        print("first vector of this subset is : ", subsets[i][0])


if __name__ == "__main__":
    main()
