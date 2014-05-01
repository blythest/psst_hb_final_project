import BeautifulSoup
import json
import os


def get_node_id(host):

    """
    Takes in a single NMAP XML host as a string.
    Outputs a string containing the node's mac address.
    """

    for h in host:

        mac_address = h.find("address").nextSibling
        address = repr(mac_address)
        if 'addrtype="mac"' in address:
            host_id = address.split('\n')[0].split('"')[1]
            return host_id

def get_group_number_from_name(name):
    if "iPhone" in name:
        return 1
    elif "Linux" in name:
        return 2
    elif "Microsoft Windows" in name:
        return 3
    elif "Apple Mac OS X" in name:
        return 4
    else:
        return 5

def check_if_unicode(entry):
    try:
        entry = unicode(entry, 'utf-8')
    except TypeError:
        return entry


def get_open_port_numbers(host):
    """
    Takes in one Beautiful Soup object.
    Returns a list of a host's open ports).
    """
    ports_per_host =[]
    for h in host:
        ports = h.findAll("port")
        for port in ports:
            port_id = check_if_unicode(port["portid"])
            ports_per_host.append(port_id)
        return ports_per_host

def get_ports_services(host):
    """
    Takes in one Beautiful Soup object.
    Returns a list of services running a host's open port(s).
    """
    services_per_host =[]
    for h in host:
        services = h.findAll("service")
        for service in services:
            port_service = check_if_unicode(service['name'])
            # print port_service
            services_per_host.append(port_service)
        return services_per_host

def get_ip_address(host):
    """
    Takes in one Beautiful Soup object.
    Returns a string of the IP value.
    """
    for h in host:
        ip = h.address['addr']
        return ip

def get_os_class(host):
    """
    Takes in one Beautiful Soup object.
    Returns a string for an OSMatch value.
    """
    for h in host:
        os_class = h.osclass
        if os_class is not None:
            os_class = str(os_class)
            string_os_class = os_class.split('"')[1].split('"')[0]
            return string_os_class
        else:
            return "No OS class available."
            
def get_os_match(host):
    """
    Takes in one Beautiful Soup object.
    Returns a string for an OSMatch value.
    """
    for h in host:
        os_match = h.osmatch
        if os_match is not None:
            os_match = str(os_match)
            return os_match.split('"')[1].split('"')[0]
        else:
            return "No OS version available."


def make_dictionaries(hosts):
    node_list = []
    n_dict = {}
    json_blob_dictionary = {}
    node_dictionary = {}

    for h in hosts:
        n_dict = create_nodes_dictionary(h)
        node_list.append(n_dict)
    return node_list


def get_common_os(tuple_list):

    """
    function takes a list of tuples of the form
    ("Linux 2.4.21 - 2.4.31 (embedded)", "https").
    Returns a dictionary of indexes that share an os.
    """
    common_os_dict = {}
    # common_protocol_dict = {}
    itr = 0

    for t in tuple_list:
   
        os_key = get_group_number_from_name(t[0])

        if os_key in common_os_dict:
            common_os_dict[os_key].append(itr)
        else:
            common_os_dict[os_key] = [itr]

        itr += 1
    return common_os_dict

def get_os_indices_list(common_os_dict):

    """
    Takes in the dictionary of hosts with common os's. 
    Returns list of all the value' indexes.
    """

    indices_list = []
    os_values_list = common_os_dict.values()
    for os_entry in os_values_list:
        indices_list.append(os_entry)

    return indices_list


def get_all_possible_os_pairings(indices_list):

    """
    Takes in list of lists. Each list contains the indexes of what
    hosts are running the same OS.
    Returns a list of all possible pairings between hosts.
    """
    pairs = []
    itr = 0

    for links in indices_list:

        for item in links:
            for i in range(itr,len(links)):

                if item == links[i]:
                    continue
                else:
                    pair = item, links[i]
                    pairs.append(pair)
    return pairs


def get_sources_and_targets(index_pairings):

    """
    Takes in all possible pairings of indexes that have OS's in common.
    Returns dictionary of sources and targets.
    """

    source_target_dictionary = {}
    links_list = []
    
    itr = 0
   
    for pair in index_pairings:
        source = pair[0]
        target = pair[1]

        source_target_dictionary = {"source":source, "target":target}
        links_list.append(source_target_dictionary)

    return links_list

        
def create_nodes_dictionary(h):
    node_dictionary = {}

    node_dictionary['Id'] = get_node_id(h)
    node_dictionary['IP'] = get_ip_address(h)
    node_dictionary['OpenPorts'] = get_open_port_numbers(h)
    node_dictionary['Links'] = [get_os_match(h), get_ports_services(h)]
    node_dictionary['PortServices'] = get_ports_services(h)
    node_dictionary['OSMatch'] = get_os_match(h)
    node_dictionary['group'] = get_group_number_from_name(get_os_match(h))
    node_dictionary['OSType'] = get_os_class(h)

    return node_dictionary

def get_links(hosts):
    links_list = []
    for h in hosts:
        link = create_nodes_dictionary(h)['Links']
        links_list.append(link)
    return links_list


def modification_date(filename):
    time_stamp = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)


# last_modifed = modification_date("static/nmap_raw.xml")

def main(pathname):

    xml_doc = BeautifulSoup.BeautifulSoup(open(pathname))
    hosts = xml_doc.findAll("host")

    links_list = get_links(hosts)
    pairings = get_common_os(links_list)

    indices_list = get_os_indices_list(pairings)

    pairs = get_all_possible_os_pairings(indices_list)

    links = get_sources_and_targets(pairs)

    json_blob_dictionary = {}
    json_blob_dictionary = {"nodes" : make_dictionaries(hosts), "links" : links}


    file_output = open("static/json_dictionary.json", "w")
    json.dump(json_blob_dictionary, file_output)


if __name__ == '__main__':
    main("static/nmap_raw.xml")