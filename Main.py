from ElasticSearchBulkIndexer import ElasticSearchBulkIndexer as ebi
from classification_preparer import *
from XMLParser import XMLParser
from Converter import Converter
from SearchingFunctions import SearchingFunctions
from Drawer import Drawer
from Classifier import Classifier
import os
import sys
import pprint
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
XML_TEST_HTTPWeb = "defi1/benchmark_HTTPWeb_test.xml"
XML_TEST_SSH = "defi1/benchmark_SSH_test.xml"
XML_TEST_DEFI2 = "defi2/traffic_os_TEST.xml"
XML_TRAIN_DEFI2 = "defi2/traffic_os_TRAIN.xml"

# List of command line arguments

def main():
    ###------------------------------------------------------------------------------------------###
    ###--------------------------------------- Arguments ----------------------------------------###
    ###------------------------------------------------------------------------------------------###

    if len(sys.argv) < 2 or  sys.argv[1] == "-h":
        print("""\nUSAGE : python3 Main.py [project|defi1|defi2] [appName] [KNN|MNB]""")
        print("""\nOPTIONAL :""")
        print("""|  -index    To index all the XML files in TRAIN_ENSIBS.""")
        print("""|  -delete   To delete all indexes.""")
        print("""|  -vect     To convert flows to vectors and save them in a file. (Must be used only once)""")
        print("""|  KNN 4     To use KNN classifier with k=4 (default k=1)""")
        print("""|  -h        To display help.""")
        print("""\nEXAMPLES : """)
        print("""|  python3 Main.py project HTTPWeb KNN 3""")
        print("""|  python3 Main.py defi1 SSH MNB -vect""")
        sys.exit(1)

    if sys.argv[1] not in ["project", "defi1", "defi2", "-index", "-delete"]:
        print("""Wrong argument : Please enter "project", "defi1" of "defi2" followed by the appName and the classifier type (KNN or MNB).""")
        print("EXAMPLES : ")
        print("|  python3 Main.py project HTTPWeb KNN 3")
        print("|  python3 Main.py defi1 SSH MNB")
        sys.exit(1)

    appList = ['HTTPWeb', 'HTTPImageTransfer', 'DNS', 'Unknown_UDP', 'SecureWeb', 'Unknown_TCP', 'NetBIOS-IP', 'POP', 'WindowsFileSharing', 'FTP', 'IMAP', 'BitTorrent', 'SSH', 'ICMP', 'SMTP', 'WebMediaDocuments', 'Flowgen', 'MiscApplication', 'WebFileTransfer', 'XWindows', 'Oracle', 'WebMediaVideo', 'Yahoo', 'Authentication', 'Real', 'RPC', 'Telnet', 'IRC', 'Filenet', 'Webmin', 'DNS-Port', 'MSMQ', 'MSN', 'IPSec', 'Timbuktu', 'H.323', 'Common-P2P-Port', 'AOL-ICQ', 'Web-Port', 'MS-SQL', 'MSN-Zone', 'MSTerminalServices', 'StreamingAudio', 'IGMP', 'Hotline', 'Misc-DB', 'LDAP', 'NNTPNews', 'SNMP-Ports', 'NETBEUI', 'WebMediaAudio', 'SMS', 'PPTP', 'SSDP', 'Common-Ports', 'RTSP', 'SunRPC', 'VNC', 'Tacacs', 'Gnutella', 'MDQS', 'ManagementServices', 'TimeServer', 'Citrix', 'Ingres', 'NFS', 'NortonAntiVirus', 'Anet', 'Groove', 'NTP', 'Squid', 'Misc-Ports', 'MicrosoftMediaServer', 'MiscApp', 'BGP', 'Hosts2-Ns', 'Misc-Mail-Port', 'OpenNap', 'POP-port', 'XFER', 'rsh', 'Google', 'Intellex', 'Network-Config-Ports', 'PCAnywhere', 'PostgreSQL', 'Printer', 'SSL-Shell', 'dsp3270', 'rexec', 'rlogin', 'OpenWindows', 'PeerEnabler', 'SAP', 'NortonGhost', 'SNA', 'Nessus', 'IPX', 'iChat', 'Kazaa']

    if sys.argv[1] in ["project", "defi1"] and sys.argv[2] not in appList:
        print("""Wrong appName : Please enter an appName among the list bellow, followed the classifier type (KNN or MNB).""")
        for appName in appList:
            print(f"- {appName}")
        print("EXAMPLES : ")
        print("|  python3 Main.py project HTTPWeb KNN 3")
        print("|  python3 Main.py defi1 SSH MNB")
        sys.exit(1)

    if sys.argv[1] in ["project", "defi1"] and sys.argv[2] in appList and sys.argv[3] not in ["KNN", "MNB"]:
        print("""Wrong classifier type : Please enter KNN or MNB after appName.""")
        print("EXAMPLES : ")
        print("|  python3 Main.py project HTTPWeb KNN 3")
        print("|  python3 Main.py defi1 SSH MNB")
        sys.exit(1)


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

    if "-delete" in sys.argv:
        # Delete all indexes at the beginning
        bulk_indexer.delete_all_indexes()
        print("\nPlease restart the program to index the XML files with -index.\n")

        sys.exit(1)

    if "-index" in sys.argv:

        # Index all the XML files
        for xml_file in XML_FILES:
            bulk_indexer.bulk_index_data(xml_file)
    
        # Index only one XML file
        #xml_file = XML_FILES[-1]
        #bulk_indexer.bulk_index_data(xml_file)

        sys.exit(1)

    # Update the max result window size
    bulk_indexer.update_max_result_windows("flows", 200000)

    # Wait few seconds for the indexing to be done
    time.sleep(5)

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
    # payload_size_per_protocol = sf.get_payload_size_for_each_protocol()
    # pprint.pprint(payload_size_per_protocol)

    # If you want to get the source and destination total bytes for each protocol
    # total_bytes_per_protocol = sf.get_total_bytes_for_each_protocol()
    # pprint.pprint(total_bytes_per_protocol)

    # If you want to get the total source/destination packets for each protocol
    # total_packets_per_protocol = sf.get_total_packets_for_each_protocol()
    # pprint.pprint(total_packets_per_protocol)

    # If you want to get the number of flows for each application
    #nb_flows_per_application = sf.get_nb_flows_for_each_application()
    #pprint.pprint(nb_flows_per_application)

    # If you want to get the list of flows for a given application
    #application = "HTTPWeb"
    #flows_by_application = sf.get_flows_for_application(application)
    #pprint.pprint(flows_by_application) # !!! NOT RECOMMENDED !!!

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
    ###---------------------------------- Converter functions -----------------------------------###
    ###------------------------------------------------------------------------------------------###

    # Convert the application name to an integer
    # Exemple: appName_to_int("Unknown_UDP") -> 83
    # appName = "Unknown_UDP"
    # appNameInt = cv.appName_to_int(appName)
    # print(appName + " --> " + str(appNameInt))

    # Convert sourcePayloadAsBase64 or destinationPayloadAsBase64 to a list of occurence 
    # of each character
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
    # Exemple: tag_to_int("Normal") -> 1 and tag_to_int("Attack") -> 2 
    # tag = "Normal"
    # tagOneHot = cv.tag_to_int(tag)
    # print(tag + " --> " + str(tagOneHot))

    ###------------------------------------------------------------------------------------------###
    ###-------------------------------- Classification preparation ------------------------------###
    ###------------------------------------------------------------------------------------------###

    files = None

    if sys.argv[1] == "project":

        files = ['binarized_flows/binarized_flows_test_1.pickle', 'binarized_flows/binarized_flows_test_2.pickle',
                'binarized_flows/binarized_flows_test_3.pickle', 'binarized_flows/binarized_flows_test_4.pickle',
                'binarized_flows/binarized_flows_test_5.pickle']

        # Prepare classification for the HTTPWeb protocol.
        print("---------- Classification preparation ----------")
        
        if len(sys.argv) > 4 and "-vect" in sys.argv:
            class_prep(appName, sf, cv, files, True)

    appName = sys.argv[2]

    if sys.argv[1] == "defi1":

        files = f"defi1/binarized_train_flows/{appName}_binarized_train_flows.pickle"

        # Prepare classification for the HTTPWeb protocol.
        print("---------- Classification preparation ----------")

        if len(sys.argv) > 4 and "-vect" in sys.argv:
            class_prep(appName, sf, cv, files, True)

    ###------------------------------------------------------------------------------------------###
    ###-------------------------------------- Classification ------------------------------------###
    ###------------------------------------------------------------------------------------------###

    if sys.argv[1] == "project" or sys.argv[1] == "defi1":
        print("---------- Classification ----------")
    
        classifier_type = sys.argv[3] # "KNN" or "MNB" for KNN classifier or Multinomial Naive Bayes classifier

    if isinstance(files, list):
        # Get subsets from files
        subsets = read_subsets_from_files(files)
        print("Subsets loaded from files.")

        # Show first vector of the subsets
        show_first_vector_of_each_subset(subsets)

        # Init the KNN classifier
        csf = Classifier(subsets)

        if classifier_type == "KNN":
            # Predict attack flows with KNN classifier
            if len(sys.argv) > 4 and sys.argv[4].isdigit():
                k = int(sys.argv[4])
            csf.classifyKNN(k=k)
        elif classifier_type == "MNB":
            # Predict attack flows with Multinomial Naive Bayes classifier
            csf.classifyMNB()

    ###------------------------------------------------------------------------------------------###
    ###---------------------------------------- Testing defi 1 ----------------------------------###
    ###------------------------------------------------------------------------------------------###
    elif sys.argv[1] == "defi1":
        print("---------- Defi 1 ----------")
        # Get vectors from files
        training_vectors = read_subsets_from_files(files)
        print("- Training vectors for defi 1 loaded from file.")

        # Init the classifier
        csf = Classifier(training_vectors)

        if len(sys.argv) > 4 and "-vect" in sys.argv:
            
            # Prepare testing flows for the protocol.
            if appName == "HTTPWeb":
            
                xml_parser = XMLParser(XML_TEST_HTTPWeb)
                xml_parser.load_xml2()
                testing_flows = xml_parser.get_flows()

            elif appName == "SSH":

                xml_parser = XMLParser(XML_TEST_SSH)
                xml_parser.load_xml2()
                testing_flows = xml_parser.get_flows()

            else:
                print("Wrong appName for defi1 : Please enter HTTPWeb or SSH appName.")
                sys.exit(1)

            print("Testing flows for defi 1 loaded from xml file.")
            print("Number of testing flows : ", len(testing_flows))

            # Convert flows to vectors
            testing_vectors = flows_to_vector(testing_flows, cv)
            print("Testing flows converted into testing vectors succesfully.")
            print("Number of testing vectors : ", len(testing_vectors))

            # Write testing vector on file
            write_test_vectors_on_file(testing_vectors, cv, f"defi1/binarized_test_flows/{appName}_binarized_test_flows.pickle")
        
        if "KNN" in sys.argv and len(sys.argv) > 4 and sys.argv[4].isdigit():
            k = int(sys.argv[4])

        # Load testing vector from file
        testing_vectors = read_subsets_from_files(f"defi1/binarized_test_flows/{appName}_binarized_test_flows.pickle")
        print("Testing vectors loaded from file.")

        # Predict attack flows with KNN classifier
        proba = csf.predict_attack(training_vectors, testing_vectors, classifier_type, k=k)

        # Make json file of results
        csf.make_json_res(proba, classifier_type, appName)

    ###------------------------------------------------------------------------------------------###
    ###------------------------------------------ Defi 2 ----------------------------------------###
    ###------------------------------------------------------------------------------------------###
    
    if sys.argv[1] == "defi2":
    
        print("---------- Defi 2 ----------")

        if "-vect" in sys.argv:
            # Prepare training flows.
            xml_parser = XMLParser(XML_TRAIN_DEFI2)
            xml_parser.load_xml()
            training_flows = xml_parser.get_flows()

            print("Training flows for defi 2 loaded from xml file.")
            print("Number of training flows : ", len(training_flows))

            # Prepare testing flows.
            xml_parser = XMLParser(XML_TEST_DEFI2)
            xml_parser.load_xml()
            testing_flows = xml_parser.get_flows()

            print("Testing flows for defi 2 loaded from xml file.")
            print("Number of testing flows : ", len(testing_flows))

        print("First flow of testing vectors : ", testing_flows[0])
        print("First flow of training vectors : ", training_flows[0])


if __name__ == "__main__":
    main()
