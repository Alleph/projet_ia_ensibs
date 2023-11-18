import pickle


# Return the flows split in two lists, one for normal flows, and one for attack flows.
def get_normal_and_attack_flows(flows):
    normal_flows = []
    attack_flows = []

    for flow in flows:
        if '_source' in flow and flow['_source'].get('Tag') == 'Normal':
            normal_flows.append(flow)
        else:
            attack_flows.append(flow)
    print("Successfull split between normal and attack flows.")
    return normal_flows, attack_flows


# Return the vectorized form of a list of flows.
def flows_to_vector(list_flows, cv):
    # initialize the vector of vectors
    big_vector = []

    for flow in list_flows:
        flow_vector = []
        # convert each field of flow
        if '_source' not in flow:
            raise Exception("'_source' key not found in flow")
        for field in flow['_source']:
            value: any
            match field:
                # treat fields that requires conversion first
                case 'appName':
                    value = cv.appName_to_int(flow['_source'][field])
                case 'sourcePayloadAsBase64' | 'destinationPayloadAsBase64':
                    value = cv.payload_to_list(flow['_source'][field])
                case 'direction':
                    value = cv.direction_to_one_hot(flow['_source'][field])
                case 'sourceTCPFlagsDescription' | 'destinationTCPFlagsDescription':
                    value = cv.tcpFlags_to_int(flow['_source'][field])
                case 'source' | 'destination':
                    value = cv.ip_to_vector(flow['_source'][field])
                case 'protocolName':
                    value = cv.protocol_to_one_hot(flow['_source'][field])
                case 'startDateTime' | 'stopDateTime':
                    value = cv.dateTime_to_timestamp(flow['_source'][field])
                case 'Tag':
                    value = cv.tag_to_one_hot(flow['_source'][field])
                # treat fields that can be put as is
                case 'totalSourceBytes' | 'totalDestinationBytes' | 'totalDestinationPackets' | 'totalSourcePackets'\
                     | 'sourcePort' | 'destinationPort':
                    value = flow['_source'][field]
            # add the value to the vector
            flow_vector.append(value)
        big_vector.append(flow_vector)
    return big_vector


# Distributes the normal and attack vectorized flows between 5 subsets and store each of them in a separate file.
# (The subsets are written in a binary form)
def write_subsets_on_files(normal_vector, attack_vector, cv, files):
    # calculate length to divide in 5 subsets
    ln = int(len(normal_vector) / 5)
    la = int(len(attack_vector) / 5)

    # if length of big vector < 5, set length to 1 in order to minimize the number of empty subset
    if len(normal_vector) < 5:
        ln = 1
    if len(attack_vector) < 5:
        la = 1

    # write a subset on each file
    for i in range(5):
        f = open(files[i], 'wb')
        pickle.dump(normal_vector[i*ln:(i+1)*ln] + attack_vector[i*la:(i+1)*la], f)
        f.close()

    print("Vectors divided in 5 subsets and written to files.\nEach subset composed of", ln+la,
          "vectors (", ln, "normal and", la, "attack ).")


# Read content of each file and return it as list of objects.
def read_subsets_from_files(files):
    contents = []
    for i in range(5):
        f = open(files[i], 'rb')
        contents.append(pickle.load(f))
        f.close()

    print("Get content from ", len(files), "files.")
    return contents