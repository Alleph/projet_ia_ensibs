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
        return self.es.search(index=self.index_name, body=body)

    # get the list of all the distinct protocols contained in XML files (the protocol field is named "protocolName" in the index)
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
        return self.es.search(index=self.index_name, body=body)
