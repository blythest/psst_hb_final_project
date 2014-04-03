import json

"""
Retrieve JSON file object. 
Returns sequence of strings.
"""

def get_JSON():

    links_dict = {}

    f = open('static/nmap.json')
    myjson = json.loads(f.read())

    data_dict = {
    'nodes': myjson,
    'links': []
    }
    
    for v in myjson:
        host_id = v['Id']

        link_id = v['Links']

        if host_id not in links_dict:
            links_dict[host_id] = []

        links_dict[host_id].append(link_id)


        if host_id not in data_dict:
            data_dict[host_id] = []
        data_dict[host_id].append(v)

        print '\n'
       
    return data_dict

get_JSON()

# nmap_file = open('static/clean_data.json', 'w')
# json.dump(nmap_data, nmap_file)
