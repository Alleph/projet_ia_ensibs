from SearchingFunctions import SearchingFunctions

class Converter:
    def __init__(self, es, sf, index_name):
        self.es = es
        self.sf = sf
        self.index_name = index_name.lower()

    # Convert the application name to an integer
    # Exemple: appName_to_int("Unknown_UDP") -> 83
    def appName_to_int(self, application_name):
        applications = self.sf.get_applications()
        appNameList = [app['key'] for app in applications]
        appNameList.sort()
        return appNameList.index(application_name)

    # Convert sourcePayloadAsBase64 or destinationPayloadAsBase64 to a list of occurence of each character
    # Exemple: payload_to_list("abbcccdddd") -> [1, 2, 3, 4]
    def payload_to_list(self, payload):
        payloadList = [0] * 64
        for char in payload:
            # A-Z = 0-25
            if ord(char) >= 65 and ord(char) <= 90:
                payloadList[ord(char) % 65] += 1
            # a-z = 26-51
            elif ord(char) >= 97 and ord(char) <= 122:
                payloadList[ord(char) % 97 + 26] += 1
            # 0-9 = 52-61
            elif ord(char) >= 48 and ord(char) <= 57:
                payloadList[ord(char) % 48 + 52] += 1
            # + = 62
            elif ord(char) == 43:
                payloadList[62] += 1
            # / = 63
            elif ord(char) == 47:
                payloadList[63] += 1
        return payloadList

    # Convert direction to a one-hot vector
    # Exemple: direction_to_one_hot("L2R") -> [0, 0, 1, 0]
    def direction_to_one_hot(self, direction):
        if direction == "R2R":
            return [1, 0, 0, 0]
        elif direction == "R2L":
            return [0, 1, 0, 0]
        elif direction == "L2R":
            return [0, 0, 1, 0]
        elif direction == "L2L":
            return [0, 0, 0, 1]

    # Convert sourceTCPFlagsDescription or destinationTCPFlagsDescription to an integer
    # Exemple: tcpFlags_to_int("F,S,R,P,A") -> 3 * 11 * 5 * 7 * 2 = 2310 (prime factor decomposition)
    def tcpFlags_to_int(self, tcpFlags):
        i = 1
        if tcpFlags == "N/A":
            return 0
        tcpFlagsList = tcpFlags.split(",")
        for flag in tcpFlagsList:
            if flag == "A":
                i *= 2
            elif flag == "F":
                i *= 3
            elif flag == "R":
                i *= 5
            elif flag == "P":
                i *= 7
            elif flag == "S":
                i *= 11
            elif flag == "Illegal17":
                i *= 13
            elif flag == "Illegal18":
                i *= 17
        return i

    # Convert source or destination ip address to a vector of 4 integers
    # Exemple: 192.168.2.111 -> [192, 168, 2, 111]
    def ip_to_vector(self, ip):
        ipList = ip.split(".")
        return [int(i) for i in ipList]

    # Convert protocol to a one hot vector
    # Exemple: protocol_to_int("tcp_ip") -> [1, 0, 0, 0, 0, 0]
    def protocol_to_one_hot(self, protocol):
        if protocol == "tcp_ip":
            return [1, 0, 0, 0, 0, 0]
        elif protocol == "udp_ip":
            return [0, 1, 0, 0, 0, 0]
        elif protocol == "icmp_ip":
            return [0, 0, 1, 0, 0, 0]
        elif protocol == "igmp":
            return [0, 0, 0, 1, 0, 0]
        elif protocol == "ip":
            return [0, 0, 0, 0, 1, 0]
        elif protocol == "ipv6icmp":
            return [0, 0, 0, 0, 0, 1]

    # Convert startDateTime or stopDateTime to a timestamp
    # Exemple: dateTime_to_timestamp("2010-06-14T00:01:24") -> 1276473684
    def dateTime_to_timestamp(self, dateTime):
        return int(datetime.datetime.strptime(dateTime, "%Y-%m-%dT%H:%M:%S").timestamp())

    # Convert Tag into a one hot vector
    # Exemple: Normal -> [1, 0] and Attack -> [0, 1]
    def tag_to_one_hot(self, tag):
        if tag == "Normal":
            return [1, 0]
        elif tag == "Attack":
            return [0, 1]
    
