from BulkData import ElasticsearchBulkIndexer as ebi
from XMLParser import XMLParser
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

    for xml_file in XML_FILES:
        print(f"Indexing {xml_file} . . .")
        # Index the XML file
        bulk_indexer.index_data(xml_file)

if __name__ == "__main__":
    main()

