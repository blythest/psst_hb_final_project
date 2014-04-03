import json


def get_nodes(json_pathname):

    """
    Returns nmap data as Python-readable JSON object.
    """

    f = open(json_pathname, 'rb')
    myjson = json.loads(f.read())
    for element in myjson:
        element['name'] = element['Id']

    return myjson

def parse_os_and_protocol(os_protocol_string):

    """
    Takes in a string in the format:
    "Platform - Name Service - Name"
    Linux 2.4.21 - 2.4.31 (embedded) https
    Returns output tuple ("Linux 2.4.21 - 2.4.31 (embedded)", "https")
    """

    return os_protocol_string.rsplit(' ', 1)


def extract_link_tuples(json_blob):

    """
    Takes in nodes blob. For each node, finds the "Links" key,
    reformats its string value as a tuple. Returns list of tuples.

    """
    tuple_list = []

    for node in json_blob:
        for key, value in node.iteritems():
            if key == "Links":
                # convert the string value into a tuple
                node[key] = parse_os_and_protocol(value)
                tuple_list.append(node[key])
    return tuple_list


def return_common_os(tuple_list):

    """
    function takes a list of tuples of the form
    ("Linux 2.4.21 - 2.4.31 (embedded)", "https").
    Returns a list of indexes that share an os.
    """

    common_os_dict = {}
    # common_protocol_dict = {}
    itr = 0
    
    for t in tuple_list:
        os_key = t[0]

        if os_key in common_os_dict:
            common_os_dict[os_key].append(itr)
        else:
            common_os_dict[os_key] = [itr]

        itr += 1
    return common_os_dict

def return_common_protocols(tuple_list):

    """
    function takes a list of tuples of the form
    ("Linux 2.4.21 - 2.4.31 (embedded)", "https").
    Returns a list of indexes that share a protocol.
    """


    common_protocols_dict = {}
    # common_protocol_dict = {}
    itr = 0
    
    for t in tuple_list:
        protocol_key = t[1]

        if protocol_key in common_protocols_dict:
            common_protocols_dict[protocol_key].append(itr)
        else:
            common_protocols_dict[protocol_key] = [itr]

        itr += 1
    return common_protocols_dict

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

def create_nodes_and_links_dictionary(nodes,links):
    """
    Create a dictionary comprised of two lists to use in D3. 
    Nodes: The information for each host. Each host has a unique name,
    its Mac address.
    Links: A list of dictionaries that hold the source and target for 
    hosts that are running the same operating system.
    """
    nodes_and_links_dictionary = {"nodes":nodes, "links": links}
    return nodes_and_links_dictionary



# print get_sources_and_targets(return_duplicates())
blob_of_nodes = get_nodes('static/nmap.json')
# print 'BLOB O NODES'
# print blob_of_nodes
# print '\n'
tuple_list = extract_link_tuples(blob_of_nodes)
# print 'TUPLE LIST'
# print tuple_list
# print '\n'

common_os = return_common_os(tuple_list)
# print 'COMMON OSES'
# print common_os
# print '\n'

indices_list = get_os_indices_list(common_os)
# print 'INDICES LIST'
# print indices_list
# print '\n'

pairings = get_all_possible_os_pairings(indices_list)
# print 'ALL POSSIBLE PAIRINGS'
# print pairings
# print '\n'
# print 'GET SOURCES AND TARGETS'

links = get_sources_and_targets(pairings)

network_dictionary = create_nodes_and_links_dictionary(blob_of_nodes, links)
nmap_output = open('static/nmap_for_d3.json', 'w')
json.dump(network_dictionary, nmap_output)

