from SearchingFunctions import SearchingFunctions
from Converter import Converter

class Classifier:
    def __init__(self, es, sf, cv, index_name):
        self.es = es
        self.sf = sf
        self.cv = cv
        self.index_name = index_name.lower()

    # Function that partition flows of the same appName into 5 equal sized subsets
    # Exemple : partition_flows_by_appName("Unknown_UDP") -> {S1=[flow1, flow2, flow3], S2=[flow4, flow5, flow6], S3=[flow7, flow8, flow9], S4=[flow10, flow11, flow12], S5=[flow13, flow14, flow15]}
    def partition_flows_by_appName(self, application_name):
        # Get the list of flows for the given application
        flows = self.sf.get_flows_for_application(application_name)
        # Partition the list into 5 equal sized subsets
        partition = {}
        for i in range(0, 5):
            partition[f"S{i + 1}"] = flows[int(i * len(flows) / 5):int((i + 1) * len(flows) / 5)]
        return partition
    