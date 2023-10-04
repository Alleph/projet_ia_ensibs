class SearchingFunctions:
    def __init__(self, es, index_name):
        self.es = es
        self.index_name = index_name.lower()

    def get_distinct_protocols(self):
        body = {
            "aggs": {
                "distinct_protocols": {
                    "terms": {
                        "field": "protocolName.keyword",
                        "size": 10000
                    }
                }
            },
            "size": 0
        }
        res = self.es.search(index=self.index_name, body=body)
        return [bucket['key'] for bucket in res['aggregations']['distinct_protocols']['buckets']]

    def get_flows_for_protocol(self, protocol):
        body = {
            "query": {
                "match": {
                    "protocolName": protocol
                }
            }
        }
        res = self.es.search(index=self.index_name, body=body)
        return res['hits']['hits']
