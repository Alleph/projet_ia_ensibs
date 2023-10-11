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
        print("Match all request")
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
        print("Get protocols")
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
        print(f"Get flows for protocol {protocol}")
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
        print("Get number of flows for each protocol")
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
        print("Get payload size for each protocol")
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
                            "extended_stats": {
                                "script": {
                                "source": """
                                    if (!doc['sourcePayloadAsBase64.keyword'].empty) {
                                        return doc['sourcePayloadAsBase64.keyword'].value.length();
                                    } else {
                                        return 0;
                                    }
                                """
                                }
                            }
                        }, 
                        "destination_payload_size": {
                            "extended_stats": {
                                "script": {
                                "source": """
                                    if (!doc['destinationPayloadAsBase64.keyword'].empty) {
                                        return doc['destinationPayloadAsBase64.keyword'].value.length();
                                    } else {
                                        return 0;
                                    }
                                """
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.es.search(index=self.index_name, body=body)

        # Extract the relevant statistics
        list_of_stats = result["aggregations"]["payload_size_for_each_protocol"]["buckets"]
        for res in list_of_stats:
            relevant_source_stats = {
                "avg": res["source_payload_size"]["avg"],
                "min": res["source_payload_size"]["min"],
                "max": res["source_payload_size"]["max"],
                "sum": res["source_payload_size"]["sum"],
                "std_deviation": res["source_payload_size"]["std_deviation"]
            }
            relevant_destination_stats = {
                "avg": res["destination_payload_size"]["avg"],
                "min": res["destination_payload_size"]["min"],
                "max": res["destination_payload_size"]["max"],
                "sum": res["destination_payload_size"]["sum"],
                "std_deviation": res["destination_payload_size"]["std_deviation"]
            }

            res["source_payload_size"] = relevant_source_stats
            res["destination_payload_size"] = relevant_destination_stats

        return list_of_stats

    # get the total source/destination Bytes for each protocol taking in account that the totalSourceBytes and totalDestinationBytes are text fields and not integer fields
    def get_total_bytes_for_each_protocol(self):
        print("Get total bytes for each protocol")
        body = {
            "size": 0,
            "aggs": {
                "total_bytes_for_each_protocol": {
                    "terms": {
                        "field": "protocolName.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "source_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalSourceBytes.keyword'].value)"
                                }
                            }
                        }, 
                        "destination_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalDestinationBytes.keyword'].value)"
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.es.search(index=self.index_name, body=body)

        # Extract the relevant statistics
        list_of_stats = result["aggregations"]["total_bytes_for_each_protocol"]["buckets"]
        for res in list_of_stats:
            relevant_source_stats = {
                "avg": res["source_payload_size"]["avg"],
                "min": res["source_payload_size"]["min"],
                "max": res["source_payload_size"]["max"],
                "sum": res["source_payload_size"]["sum"],
                "std_deviation": res["source_payload_size"]["std_deviation"]
            }
            relevant_destination_stats = {
                "avg": res["destination_payload_size"]["avg"],
                "min": res["destination_payload_size"]["min"],
                "max": res["destination_payload_size"]["max"],
                "sum": res["destination_payload_size"]["sum"],
                "std_deviation": res["destination_payload_size"]["std_deviation"]
            }

            res["source_payload_size"] = relevant_source_stats
            res["destination_payload_size"] = relevant_destination_stats

        return list_of_stats

    # get the total source/destination packets for each protocol
    def get_total_packets_for_each_protocol(self):
        print("Get total packets for each protocol")
        body = {
            "size": 0,
            "aggs": {
                "total_packets_for_each_protocol": {
                    "terms": {
                        "field": "protocolName.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "source_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalSourceBytes.keyword'].value)"
                                }
                            }
                        }, 
                        "destination_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalDestinationBytes.keyword'].value)"
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.es.search(index=self.index_name, body=body)

        # Extract the relevant statistics
        list_of_stats = result["aggregations"]["total_packets_for_each_protocol"]["buckets"]
        for res in list_of_stats:
            relevant_source_stats = {
                "avg": res["source_payload_size"]["avg"],
                "min": res["source_payload_size"]["min"],
                "max": res["source_payload_size"]["max"],
                "sum": res["source_payload_size"]["sum"],
                "std_deviation": res["source_payload_size"]["std_deviation"]
            }
            relevant_destination_stats = {
                "avg": res["destination_payload_size"]["avg"],
                "min": res["destination_payload_size"]["min"],
                "max": res["destination_payload_size"]["max"],
                "sum": res["destination_payload_size"]["sum"],
                "std_deviation": res["destination_payload_size"]["std_deviation"]
            }

            res["source_payload_size"] = relevant_source_stats
            res["destination_payload_size"] = relevant_destination_stats

        return list_of_stats

    # get the list of all the distinct applications contained in the XML files
    def get_applications(self):
        print("Get applications")
        body = {
            "size": 0,
            "aggs": {
                "distinct_applications": {
                    "terms": {
                        "field": "appName.keyword",
                        "size": 100
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["aggregations"]["distinct_applications"]["buckets"]

        return res

    # get the list of flows for a given application
    def get_flows_for_application(self, application):
        print(f"Get flows for application {application}")
        body = {
            "query": {
                "match": {
                    "appName.keyword": application
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["hits"]["hits"]

        return res

    # get the number of flows for each application
    def get_nb_flows_for_each_application(self):
        print("Get number of flows for each application")
        body = {
            "size": 0,
            "aggs": {
                "nb_flows_for_each_application": {
                    "terms": {
                        "field": "appName.keyword",
                        "size": 100
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        res = res["aggregations"]["nb_flows_for_each_application"]["buckets"]

        return res

    # get the source and destination Payload size for each application by suming the length of the value of the sourcePayloadAsBase64 and destinationPayloadAsBase64 fields
    def get_payload_size_for_each_application(self):
        print("Get payload size for each application")
        body = {
            "size": 0,
            "aggs": {
                "payload_size_for_each_application": {
                    "terms": {
                        "field": "appName.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "source_payload_size": {
                            "extended_stats": {
                                "script": {
                                "source": """
                                    if (!doc['sourcePayloadAsBase64.keyword'].empty) {
                                        return doc['sourcePayloadAsBase64.keyword'].value.length();
                                    } else {
                                        return 0;
                                    }
                                """
                                }
                            }
                        }, 
                        "destination_payload_size": {
                            "extended_stats": {
                                "script": {
                                "source": """
                                    if (!doc['destinationPayloadAsBase64.keyword'].empty) {
                                        return doc['destinationPayloadAsBase64.keyword'].value.length();
                                    } else {
                                        return 0;
                                    }
                                """
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.es.search(index=self.index_name, body=body)

        # Extract the relevant statistics
        list_of_stats = result["aggregations"]["payload_size_for_each_application"]["buckets"]
        for res in list_of_stats:
            relevant_source_stats = {
                "avg": res["source_payload_size"]["avg"],
                "min": res["source_payload_size"]["min"],
                "max": res["source_payload_size"]["max"],
                "sum": res["source_payload_size"]["sum"],
                "std_deviation": res["source_payload_size"]["std_deviation"]
            }
            relevant_destination_stats = {
                "avg": res["destination_payload_size"]["avg"],
                "min": res["destination_payload_size"]["min"],
                "max": res["destination_payload_size"]["max"],
                "sum": res["destination_payload_size"]["sum"],
                "std_deviation": res["destination_payload_size"]["std_deviation"]
            }

            res["source_payload_size"] = relevant_source_stats
            res["destination_payload_size"] = relevant_destination_stats

        return list_of_stats

    # get the total source/destination Bytes for each application
    def get_total_bytes_for_each_application(self):
        print("Get total bytes for each application")
        body = {
            "size": 0,
            "aggs": {
                "total_bytes_for_each_application": {
                    "terms": {
                        "field": "appName.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "source_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalSourceBytes.keyword'].value)"
                                }
                            }
                        }, 
                        "destination_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalDestinationBytes.keyword'].value)"
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.es.search(index=self.index_name, body=body)

        # Extract the relevant statistics
        list_of_stats = result["aggregations"]["total_bytes_for_each_application"]["buckets"]
        for res in list_of_stats:
            relevant_source_stats = {
                "avg": res["source_payload_size"]["avg"],
                "min": res["source_payload_size"]["min"],
                "max": res["source_payload_size"]["max"],
                "sum": res["source_payload_size"]["sum"],
                "std_deviation": res["source_payload_size"]["std_deviation"]
            }
            relevant_destination_stats = {
                "avg": res["destination_payload_size"]["avg"],
                "min": res["destination_payload_size"]["min"],
                "max": res["destination_payload_size"]["max"],
                "sum": res["destination_payload_size"]["sum"],
                "std_deviation": res["destination_payload_size"]["std_deviation"]
            }

            res["source_payload_size"] = relevant_source_stats
            res["destination_payload_size"] = relevant_destination_stats

        return list_of_stats

    # get the total source/destination packets for each application
    def get_total_packets_for_each_application(self):
        print("Get total packets for each application")
        body = {
            "size": 0,
            "aggs": {
                "total_packets_for_each_application": {
                    "terms": {
                        "field": "appName.keyword",
                        "size": 100
                    },
                    "aggs": {
                        "source_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalSourceBytes.keyword'].value)"
                                }
                            }
                        }, 
                        "destination_payload_size": {
                            "extended_stats": {
                                "script": {
                                    "source": "Integer.parseInt(doc['totalDestinationBytes.keyword'].value)"
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.es.search(index=self.index_name, body=body)

        # Extract the relevant statistics
        list_of_stats = result["aggregations"]["total_packets_for_each_application"]["buckets"]
        for res in list_of_stats:
            relevant_source_stats = {
                "avg": res["source_payload_size"]["avg"],
                "min": res["source_payload_size"]["min"],
                "max": res["source_payload_size"]["max"],
                "sum": res["source_payload_size"]["sum"],
                "std_deviation": res["source_payload_size"]["std_deviation"]
            }
            relevant_destination_stats = {
                "avg": res["destination_payload_size"]["avg"],
                "min": res["destination_payload_size"]["min"],
                "max": res["destination_payload_size"]["max"],
                "sum": res["destination_payload_size"]["sum"],
                "std_deviation": res["destination_payload_size"]["std_deviation"]
            }

            res["source_payload_size"] = relevant_source_stats
            res["destination_payload_size"] = relevant_destination_stats

        return list_of_stats

    # get the number of flows for each number of packets
    def get_nb_flows_for_each_nb_packets(self):
        print("Get number of flows for each number of packets")
        body = {
            "size": 0,
            "aggs": {
                "nb_flows_for_each_nb_source_packets": {
                    "terms": {
                        "field": "totalSourcePackets.keyword",
                        "size": 100
                    }
                },
                "nb_flows_for_each_nb_destination_packets": {
                    "terms": {
                        "field": "totalDestinationPackets.keyword",
                        "size": 100
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        source = res["aggregations"]["nb_flows_for_each_nb_source_packets"]["buckets"]
        destination = res["aggregations"]["nb_flows_for_each_nb_destination_packets"]["buckets"]

        return source, destination