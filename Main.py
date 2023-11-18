from ElasticSearchBulkIndexer import ElasticSearchBulkIndexer as ebi
from XMLParser import XMLParser
from Converter import Converter
from SearchingFunctions import SearchingFunctions
from Drawer import Drawer
from Classifier import Classifier
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
    #     bulk_indexer.bulk_index_data(xml_file)
    
    # Index only one XML file
    #xml_file = XML_FILES[0]
    #bulk_indexer.bulk_index_data(xml_file)

    # Update the max result window size
    bulk_indexer.update_max_result_windows("flows", 200000)

    # Wait few seconds for the indexing to be done
    time.sleep(5)

    # Init searching functions
    sf = SearchingFunctions(bulk_indexer.es, "flows")

    # Init the drawer
    drawer = Drawer(bulk_indexer.es, sf, "flows")

    # Init the converter
    cv = Converter(bulk_indexer.es, sf, "flows")

    # Init the classifier
    csf = Classifier(bulk_indexer.es, sf, cv, "flows")

    ###------------------------------------------------------------------------------------------###
    ###---------------------------------- Searching functions -----------------------------------###
    ###------------------------------------------------------------------------------------------###

    # If you want to get all the indexes
    # sf.get_all_indexes()

    # If you want to get all the flows
    #all_flows = sf.get_all_flows()
    # pprint.pprint(all_flows) # !!! NOT RECOMMENDED !!!

    # If you want to get the number of flows for each protocol
    #nb_flows_per_protocol = sf.get_nb_flows_for_each_protocol()
    #pprint.pprint(nb_flows_per_protocol)

    # If you want to get all the flows for a given protocol
    #protocol = "tcp_ip"
    #flows_by_protocol = sf.get_flows_for_protocol(protocol)
    #pprint.pprint(flows_by_protocol) # !!! NOT RECOMMENDED !!!

    # If you want to get the source and destination Payload size for each protocol
    #payload_size_per_protocol = sf.get_payload_size_for_each_protocol()
    #pprint.pprint(payload_size_per_protocol)

    # If you want to get the source and destination total bytes for each protocol
    #total_bytes_per_protocol = sf.get_total_bytes_for_each_protocol()
    #pprint.pprint(total_bytes_per_protocol)

    # If you want to get the total source/destination packets for each protocol
    #total_packets_per_protocol = sf.get_total_packets_for_each_protocol()
    #pprint.pprint(total_packets_per_protocol)

    # If you want to get the number of flows for each application
    #nb_flows_per_application = sf.get_nb_flows_for_each_application()
    #pprint.pprint(nb_flows_per_application)    

    # If you want to get the list of flows for a given application
    #application = "HTTPWeb"
    #flows_by_application = sf.get_flows_for_application(application)
    #pprint.pprint(flows_by_application) # !!! NOT RECOMMENDED !!!

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

    ###------------------------------------------------------------------------------------------###
    ###---------------------------------- Drawer functions --------------------------------------###
    ###------------------------------------------------------------------------------------------###

    # Draw the Zipf's law for the number of packets
    #drawer.draw_zipf_for_each_nb_packets()

    ###------------------------------------------------------------------------------------------###
    ###---------------------------------- Converter functions -----------------------------------###
    ###------------------------------------------------------------------------------------------###

    # Convert the application name to an integer
    # Exemple: appName_to_int("Unknown_UDP") -> 83
    # appName = "Unknown_UDP"
    # appNameInt = cv.appName_to_int(appName)
    # print(appName + " --> " + str(appNameInt))

    # Convert sourcePayloadAsBase64 or destinationPayloadAsBase64 to a list of occurence of each character
    # Exemple: payload_to_list("abbcccdddd") -> [1, 2, 3, 4]
    # payload = "VVNFUiB1c2VyMTINClBBU1MgbnNsdXNlcjEyDQpTVEFUDQpRVUlUDQo="
    # payloadList = cv.payload_to_list(payload)
    # print(payload + " --> " + str(payloadList))

    # Convert direction to a one-hot vector
    # Exemple: direction_to_one_hot("L2R") -> [0, 0, 1, 0]
    # direction = "L2R"
    # directionOneHot = cv.direction_to_one_hot(direction)
    # print(direction + " --> " + str(directionOneHot))

    # Convert sourceTCPFlagsDescription or destinationTCPFlagsDescription to an integer
    # Exemple: tcpFlags_to_int("F,S,R,P,A") -> 3 * 11 * 5 * 7 * 2 = 2310 (prime factor decomposition)
    # tcpFlags = "F,S,R,P,A"
    # tcpFlagsInt = cv.tcpFlags_to_int(tcpFlags)
    # print(tcpFlags + " --> " + str(tcpFlagsInt))

    # Convert the source and destination IP addresses to a vertor of 4 integers
    # Exemple: ip_to_int("192.168.2.111") -> [192, 168, 2, 111]
    # ip = "192.168.2.111"
    # ipVector = cv.ip_to_vector(ip)
    # print(ip + " --> " + str(ipVector))

    # Convert the protocol name to a one hot vector
    # Exemple: protocol_to_int("tcp_ip") -> [1, 0, 0, 0, 0, 0]
    # protocol = "tcp_ip"
    # protocolOneHot = cv.protocol_to_one_hot(protocol)
    # print(protocol + " --> " + str(protocolOneHot))

    # Convert the startDateTime or stopDateTime to a timestamp
    # Exemple: dateTime_to_timestamp("2010-06-14T00:01:24") -> 1276473684
    # dateTime = "2010-06-14T00:01:24"
    # timestamp = cv.dateTime_to_timestamp(dateTime)
    # print(dateTime + " --> " + str(timestamp))

    # Convert Tag into a one hot vector
    # Exemple: tag_to_one_hot("Normal") -> [1, 0] and tag_to_one_hot("Attack") -> [0, 1]
    # tag = "Normal"
    # tagOneHot = cv.tag_to_one_hot(tag)
    # print(tag + " --> " + str(tagOneHot))

    ###------------------------------------------------------------------------------------------###
    ###---------------------------------- Classifier functions ----------------------------------###
    ###------------------------------------------------------------------------------------------###

    # Partition flows of the same appName into 5 equal sized subsets
    # Exemple : partition_flows_by_appName("Unknown_UDP") -> {S1=[flow1, flow2, flow3], S2=[flow4, flow5, flow6], S3=[flow7, flow8, flow9], S4=[flow10, flow11, flow12], S5=[flow13, flow14, flow15]}
    #application = "HTTPWeb"
    #partition = csf.partition_flows_by_appName(application)
    #pprint.pprint(partition)

if __name__ == "__main__":
    main()