import BeautifulSoup

xml_doc = BeautifulSoup.BeautifulSoup(open("static/nmap.xml"))

hosts = xml_doc.findAll("host")
node_list = []
node_dictionary = {}

def get_node_id(host):

    """
    Takes in a single NMAP XML host as a string.
    Outputs a string containing the node's mac address.
    """
    items = host.split('\n')
    for i in items:
        if 'addrtype="mac"' in i:
            mac_address = i.split('"')[1]
            if mac_address == "None":
                return "No mac address available."
            else:
                return mac_address

def get_os_match(host):
    """
    Takes in one Beautiful Soup object.
    Returns a string for an OSMatch value.
    """
    for h in host:
        os_match = str(h.osmatch)
        print type(os_match)
        if os_match == "None":
            return "No OS version available."
        else:
            os_match = os_match.split('"')[1].split('"')[0]
            return os_match
    
    # else:
    #     osmatch_to_string = h.osmatch
    #     os_name = osmatch_to_string.split('"')[1].split('"')[0]
    #     return os_name


for h in hosts:
    host = str(h)
    node_dictionary['Id'] = get_node_id(host)
    node_dictionary['OSMatch'] = get_os_match(h)

    print node_dictionary
