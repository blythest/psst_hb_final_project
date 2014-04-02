import json


def get_nodes(json_pathname):

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


def extract_links(json_blob):
    link_dict = {}

    link_list = []

    for line in JSON_to_lines():

         = line[0].split(':')

        last_space_index = line[0].rfind(' ')
        link_value = line[0][last_space_index:]
        link_list.append(link_value)
    return link_list
        


def return_common_inputs():

    """
    function takes a list of inputs
    returns a list of index pairs
    where the inputs are common
    """

    duplicates_dict = {}
    input_list = extract_categories()
    itr = 0
    pairs = []
    
    for i in input_list:
        key = i
        if key in duplicates_dict:
            duplicates_dict[key].append(itr)
            for i in range(len(key)-1):
                pairs.append((key[i],key[i+1]))
                if len(key):
                    pairs.append((key[0], key[-1]))

        else:
            duplicates_dict[key] = [itr]

        itr += 1

    return duplicates_dict


def get_sources_and_targets(return_duplicates):

    """
    Takes in all possible source and target pairings of ID's with similar protocols.
    Returns values of the links dictionary.
    """
    dup_dict = return_duplicates
    pairs = []
    dupes = return_duplicates.values()
    itr = 0
   
    for i in range(len(dupes)):

        for d in range(len(dupes[i])-1):
            if i == len(dupes[i]):
                pairs.append({'source': dupes[i][0], 'target': dupes[i][-1], 'value': i})
            else:
                pairs.append({'source': dupes[i][d],'target': dupes[i][d+1], 'value': i})
            
    return pairs


print get_sources_and_targets(return_duplicates())

nmap_file = open('static/clean_data.json', 'w')
# json.dump(nmap_data, nmap_file)
