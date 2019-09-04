# __author__ = 'root'

def getAllPortsInfo():
    """
    return: All ports' infomation 
    """
    result_list = []
    status = ""
    # Need add exception handle
    # Process the tcp port
    with open('/proc/net/tcp') as f_tcp:
       content_tcp = [x.strip('\n') for x in f_tcp.readlines()]
    
    for line in content_tcp[1:len(content_tcp)]:
        res = line.split()
        if res[3] == "0A":
            portID = int(res[1].split(':')[1], 16)
            pt_dict = {
                        "portID" : portID,
                        "portType" : "tcp",
                        "status" : "LISTEN"
                       }
            result_list.append(pt_dict)

    # Process the udp port
    with open('/proc/net/udp') as f_udp:
        content_udp = [x.strip('\n') for x in f_udp.readlines()]
    
    for line in content_udp[1:len(content_udp)]:
        res = line.split()
        portID = int(res[1].split(':')[1], 16)
        pt_dict = {
                    "portID" : portID,
                    "portType" : "udp",
                    "status" : "" 
                  }
        result_list.append(pt_dict)
    
    return result_list

def getConditionalPortsInfo(portType, portID, status):
    """
    return: The port's infomation based on the search condition
    """
    all_port_list = getAllPortsInfo()
    if len(portType) != 0:
        result_list = filter(lambda t: t['portType'] == portType, all_port_list)
    
    if len(portID) != 0:
        result_list = filter(lambda t: t['portID'] == int(portID), all_port_list)

    if len(status) != 0:
        result_list = filter(lambda t: t['status'] == status, all_port_list)

    return result_list

# if __name__ == "__main__":
#    flag, ip = getRabbitmqIp()
#    print ip
