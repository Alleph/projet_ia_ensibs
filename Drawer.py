import matplotlib.pyplot as plt
from SearchingFunctions import SearchingFunctions
import pprint

class Drawer:
    def __init__(self, es, sf, index_name):
        self.es = es
        self.sf = sf
        self.index_name = index_name.lower()

    # Function that draw the number of flow (y-axis) for each number of packets (x-axis)
    def draw_zipf_for_each_nb_packets(self):
        # Get the number of flows for each number of packets
        nb_flows_for_each_nb_source_packets = self.sf.get_nb_flows_for_each_nb_packets()[0]
        nb_flows_for_each_nb_destination_packets = self.sf.get_nb_flows_for_each_nb_packets()[1]

        # Sort the list by number of flow from the biggest number to the lowest (be careful, the doc_count is a string)
        nb_flows_for_each_nb_source_packets.sort(key=lambda pair: int(pair['doc_count']), reverse=True)
        nb_flows_for_each_nb_destination_packets.sort(key=lambda pair: int(pair['doc_count']), reverse=True)

        # Get the number of packets (x-axis)
        X_source = [n for n in range(1, len(nb_flows_for_each_nb_source_packets) + 1)]
        X_destination = [n for n in range(1, len(nb_flows_for_each_nb_destination_packets) + 1)]

        # Get the number of flows (y-axis)
        Y_source = [pair['doc_count'] for pair in nb_flows_for_each_nb_source_packets]
        Y_destination = [pair['doc_count'] for pair in nb_flows_for_each_nb_destination_packets]  
      

        # Draw the two charts on the same figure
        plt.figure(1)
        plt.plot(X_source, Y_source)
        plt.plot(X_destination, Y_destination)
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel("Rank")
        plt.ylabel("Number of flows")
        plt.title("Zipf's law for the number of packets")
        plt.legend(["Source", "Destination"])
        plt.show()

