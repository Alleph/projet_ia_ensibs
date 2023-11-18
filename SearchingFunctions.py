from elasticsearch import Elasticsearch

class SearchingFunctions:
    def __init__(self, es, index_name):
        self.es = es
        self.index_name = index_name.lower()

    # Function called to scroll through the results of a search
    # useful for large datasets of flows in the request's response
    def scrolling_search(self, body, res):
        # Init scroll by search
        data = self.es.search(
            index=self.index_name,
            scroll="2m",
            body=body
        )

        scroll_id = data["_scroll_id"]
        count = 0
        print("Scrolling...")

        while True:

            for doc in data['hits']['hits']:
                res.append(doc)

            data = self.es.scroll(scroll_id=scroll_id, scroll="2m")

            if not data['hits']['hits']:
                break

            count += body["size"]

            if count % 100000 == 0:
                print(count," flows fetched")
        
        return res

    # Get the source and destination size/bytes/packets info depending on application/protocol
    def get_source_destination_info(self, payload_type, app_or_proto):
        if app_or_proto == "application":
            keyword1 = "appName.keyword"
            
        elif app_or_proto == "protocol":
            keyword1 = "protocolName.keyword"

        match (payload_type):
            case "payload_size":
                print(f"Get source and destination payload size info for each {app_or_proto}")
                source_script = """
                    if (!doc['sourcePayloadAsBase64.keyword'].empty) {
                        return doc['sourcePayloadAsBase64.keyword'].value.length();
                    } else {
                        return 0;
                    }
                """
                destination_script = """
                    if (!doc['destinationPayloadAsBase64.keyword'].empty) {
                        return doc['destinationPayloadAsBase64.keyword'].value.length();
                    } else {
                        return 0;
                    }
                """
            case "total_bytes":
                print(f"Get source and destination total bytes info for each {app_or_proto}")
                source_script = "Integer.parseInt(doc['totalSourceBytes.keyword'].value)"
                destination_script = "Integer.parseInt(doc['totalDestinationBytes.keyword'].value)"
            case "total_packets":
                print(f"Get source and destination total packets info for each {app_or_proto}")
                source_script = "Integer.parseInt(doc['totalSourcePackets.keyword'].value)"
                destination_script = "Integer.parseInt(doc['totalDestinationPackets.keyword'].value)"

        body = {
            "size": 0,
            "aggs": {
                f"{payload_type}_for_each_{app_or_proto}": {
                    "terms": {
                        "field": keyword1,
                        "size": 10000
                    },
                    "aggs": {
                        f"source_{payload_type}": {
                            "extended_stats": {
                                "script": {
                                    "source": source_script
                                }
                            }
                        },
                        f"destination_{payload_type}": {
                            "extended_stats": {
                                "script": {
                                    "source": destination_script
                                }
                            }
                        }
                    }
                }
            }
        }

        result = self.es.search(index=self.index_name, body=body)
        

        # Extract the relevant statistics
        list_of_stats = result["aggregations"][f"{payload_type}_for_each_{app_or_proto}"]["buckets"]
        for res in list_of_stats:
            relevant_source_stats = {
                "avg": res[f"source_{payload_type}"]["avg"],
                "min": res[f"source_{payload_type}"]["min"],
                "max": res[f"source_{payload_type}"]["max"],
                "sum": res[f"source_{payload_type}"]["sum"],
                "std_deviation": res[f"source_{payload_type}"]["std_deviation"]
            }
            relevant_destination_stats = {
                "avg": res[f"destination_{payload_type}"]["avg"],
                "min": res[f"destination_{payload_type}"]["min"],
                "max": res[f"destination_{payload_type}"]["max"],
                "sum": res[f"destination_{payload_type}"]["sum"],
                "std_deviation": res[f"destination_{payload_type}"]["std_deviation"]
            }

            res[f"source_{payload_type}"] = relevant_source_stats
            res[f"destination_{payload_type}"] = relevant_destination_stats

        return list_of_stats


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
        print("Match all request : Get all flows")

        page_size = 10000

        body = {
            "size": page_size,
            "query": {
                "match_all": {}
            }
        }

        return self.scrolling_search(body, [])

    # get the list of all the distinct protocols contained in XML files
    def get_nb_flows_for_each_protocol(self):
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

        page_size = 10000

        body = {
            "size": page_size,
            "query": {
                "match": {
                    "protocolName.keyword": protocol
                }
            }
        }

        return self.scrolling_search(body, [])

    # get the source and destination Payload size for each protocol
    def get_payload_size_for_each_protocol(self):
        return self.get_source_destination_info("payload_size", "protocol")

    # get the total source/destination Bytes for each protocol taking in account that the totalSourceBytes and totalDestinationBytes are text fields and not integer fields
    def get_total_bytes_for_each_protocol(self):
        return self.get_source_destination_info("total_bytes", "protocol")

    # get the total source/destination packets for each protocol
    def get_total_packets_for_each_protocol(self):
        return self.get_source_destination_info("total_packets", "protocol")

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

    # get the list of flows for a given application
    def get_flows_for_application(self, application):
        print(f"Get flows for application {application}")

        page_size = 10000

        body={  
            "size": page_size,
            "query": {
                "match": {
                    "appName.keyword": application
                }
            }
        }

        return self.scrolling_search(body, [])

    # get the source and destination Payload size for each application by suming the length of the value of the sourcePayloadAsBase64 and destinationPayloadAsBase64 fields
    def get_payload_size_for_each_application(self):
        return self.get_source_destination_info("payload_size", "application")

    # get the total source/destination Bytes for each application
    def get_total_bytes_for_each_application(self):
        return self.get_source_destination_info("total_bytes", "application")

    # get the total source/destination packets for each application
    def get_total_packets_for_each_application(self):
        return self.get_source_destination_info("total_packets", "application")

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

    # get the number of flows for each sourceTCPFlagsDescription and destinationTCPFlagsDescription
    def get_nb_flows_for_each_tcp_flags(self):
        print("Get number of flows for each TCP flags")
        body = {
            "size": 0,
            "aggs": {
                "nb_flows_for_each_source_tcp_flags": {
                    "terms": {
                        "field": "sourceTCPFlagsDescription.keyword",
                        "size": 100
                    }
                },
                "nb_flows_for_each_destination_tcp_flags": {
                    "terms": {
                        "field": "destinationTCPFlagsDescription.keyword",
                        "size": 100
                    }
                }
            }
        }

        res = self.es.search(index=self.index_name, body=body)
        source = res["aggregations"]["nb_flows_for_each_source_tcp_flags"]["buckets"]
        destination = res["aggregations"]["nb_flows_for_each_destination_tcp_flags"]["buckets"]

        return source, destination