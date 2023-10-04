from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from XMLParser import XMLParser

class ElasticsearchBulkIndexer:

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

    def index_data(self, xml_filename):
        # Parse XML file and extract data
        xml_parser = XMLParser(xml_filename)
        xml_parser.load_xml()
        flow_data = xml_parser.extract_flow_data()

        document = {
            'data': flow_data,
            'origin': xml_filename  # Store the origin (file name) as a field
        }
        
        # Index the flow data
        self.es.index(index=xml_filename, body=document)