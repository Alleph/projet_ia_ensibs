from elasticsearch import Elasticsearch

class SearchingFunctions:
    def __init__(self, es, index_name):
        self.es = es
        self.index_name = index_name.lower()

    # Get all indexes except the .security-7 index
    def get_all_indexes(self):
        # Get a list of all aliases without fetching the actual system indices
        response = self.es.indices.get_alias(index="*")

        # List of system indices to exclude from deletion
        system_indices = [".security-7"]

        # Filter out system indices from the list
        indexes = [index for index in response.keys() if index not in system_indices]

        # Print the indexes
        print("Indexes:")
        for index in indexes:
            print(f"  - {index}")
        
        return indexes

    # match all request
    def match_all(self):
        body = {
            "query": {
                "match_all": {}
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["hits"]["hits"]

        return res

    # get the list of all the distinct protocols contained in XML files
    def get_protocols(self):
        body = {
            "size": 0,
            "aggs": {
                "distinct_protocols": {
                    "terms": {
                        "field": "protocolName.keyword",
                        "size": 100
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["aggregations"]["distinct_protocols"]["buckets"]

        return res

    # get the list of flows for a given protocol
    def get_flows_for_protocol(self, protocol):
        body = {
            "query": {
                "match": {
                    "protocolName.keyword": protocol
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["hits"]["hits"]

        return res

    # get the number of flows for each protocol
    def get_nb_flows_for_each_protocol(self):
        body = {
            "size": 0,
            "aggs": {
                "nb_flows_for_each_protocol": {
                    "terms": {
                        "field": "protocolName.keyword",
                        "size": 100
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["aggregations"]["nb_flows_for_each_protocol"]["buckets"]

        return res

    # get the source and destination Payload size for each protocol
    def get_payload_size_for_each_protocol(self):
        body = {
            "size": 0,
            "aggs": {
                "payload_size_for_each_protocol": {
                    "terms": {
                        "field": "protocolName.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "source_payload_size": {
                            "sum": {
                                "field": "sourcePayloadSize"
                            }
                        },
                        "destination_payload_size": {
                            "sum": {
                                "field": "destinationPayloadSize"
                            }
                        }
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["aggregations"]["payload_size_for_each_protocol"]["buckets"]

        return res

    # get the total source/destination Bytes for each protocol
    def get_total_bytes_for_each_protocol(self):
        body = {
            "size": 0,
            "aggs": {
                "total_bytes_for_each_protocol": {
                    "terms": {
                        "field": "protocolName.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "total_source_bytes": {
                            "sum": {
                                "field": "totalSourceBytes"
                            }
                        },
                        "total_destination_bytes": {
                            "sum": {
                                "field": "totalDestinationBytes"
                            }
                        }
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["aggregations"]["total_bytes_for_each_protocol"]["buckets"]

        return res