import sys, socket, select, ipaddress
import beautiful_soup_parsing
import nmap
from subprocess import * 
import os
import shlex
# to open chrome from the command line : popen and a bunch of diff arguments 

def get_command_output(arguments, stderr=STDOUT):
    """
    arguments: A sequence of command arguments.
    Returns TODO
    """
    return Popen(arguments, stdout=PIPE,stderr=stderr).communicate()[0]

def find_available_hosts(hostnames):
    """
    hostnames: a sequence of hostnames (names or IP addresses).
    Returns a sequence of IP addresses of hosts that respond on the network.
    """

    available_hosts = []

    command = ["fping", "-e"] + hostnames
    for result in get_command_output(command).split('\n')[:-1]:
        if 'alive' not in result:
            continue
        first_word = result.split()[0]
        if not first_word:
            continue
        else:
            available_hosts.append(first_word)
    return available_hosts


def scan(available_hosts):
    """
    Available hosts: iterable of hostnames (names or IP addresses) that respond to a network.
    Returns iterable of open port numbers, possible os, devices for each available host. 
    """
 
    command = ["sudo","nmap", "PortScanner()", "-PN", "-O", "-oX", "-"] + available_hosts
    print 'command ', command
    scan_output = get_command_output(command)
    print 'scan output: ', scan_output
    return scan_output

# def find_open_ports(scan_output):
#     """
#     scan_output: an iterable of network scan results for available hosts.
#     Returns iterable of open port numbers and corresponding protocols for each available host.
#     """
    
#     for r in scan_output:
#         if 'open port' not in r:
#             continue
#         open_port = r.split()[0]
#         yield open_port


# def parse_scans(results):
#     """
#     TODO
#     """

#     print 'parsing the nmap port data ...'
#     tcps = {}
#     result = ''

#     # Rather than parse the hard-to-parse default nmap output, instead try
#     # the "greppable" or XML formats: http://nmap.org/book/output.html

#     for result in results:
#         # grab only the strings with 'tcp/port-number open protocol'
#         # beautiful, I know. 
#         host = str(result.split('Discovered')[1]).split(',')[0]
#         print host.split(' ')[-1]
#         result = result.split('STATE SERVICE')[1].split('MAC')[0].replace("'","")
#         pair = result.split('open')
#         key = str(pair[0]).strip().replace(",","")
#         value = str(pair[1]).strip().replace(",","")
#         tcps[key] = value

#     print tcps
 

def listHosts(ip):

    hostsCount = 254
    hosts = []

    for i in range(hostsCount):
        ip += 1
        hosts.append(str(ipaddress.IPv4Address(ip)))
    return hosts
 
# old way of pinging 
def pingscan(hosts):
    resp = []
    for host in hosts:
        a = sr1(IP(dst=host, ttl=32)/ICMP(),timeout=1, retry=-3)
        if hasattr(a, 'src'):
            resp.append(a.src)
            
    return resp


# def portscan(resp):
#     # if a port on a remote host is open for incoming connection requests
#     # and you send it a SYN packet, the remote host will respond
#     # with a SYN-ACK packet. if closed, sends RST packet

#     statuses = []
#     for r in range(len(resp)-1):
#         host_address = str(resp[r])
#         port_status = sr1(IP(dst=host_address)/TCP(dport=80,flags="S"),timeout=2, retry=-3)
#         statuses.append(port_status)

#     return statuses

def getTraceroute():
    
    # using traceroute to get public IP addresses
    hops = []
    try:
        response, unans = traceroute("www.google.com")
    except:
        print 'cannot trace route with scapy'
        return


    # response.get_trace() returns a dictionary in a dictionary
    host_key = response.get_trace().keys()[0]
    if len(host_key) <= 15:
        return host_key
    else:
        for key in response.get_trace()[host_key].keys():
            # get a list of ip's
            hops.append(response.get_trace()[host_key][key][0])
        return hops

"""
Finds and returns the local IP address as dotted-quad ints on my host computer. 
"""

def getIP():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # google public dns
    s.connect(('8.8.8.8',53))
    ip = s.getsockname()[0]
    print 'this is the ip', ip
    s.close()
    return ip

NETMASK = u'255.255.255.0'
IP = getIP()
FILENAME = 'static/nmap_raw.xml'
    
def main(netmask,ip,filename):

    subnetmask = int(ipaddress.IPv4Address(netmask))
    source_ip = int(ipaddress.IPv4Address(unicode(ip)))

    snet = int(ipaddress.IPv4Address(source_ip & subnetmask))
    snet = ipaddress.IPv4Address(snet)
    # print 'source ip',source_ip
    # snet = subnetmask & source_ip
    all_hosts = listHosts(snet)

    
    available_hosts = find_available_hosts(all_hosts)
    results = scan(available_hosts)
    # print results

    nmap_xml_output = open(filename, 'w')
    nmap_xml_output.write(results)
    nmap_xml_output.close()
    beautiful_soup_parsing.main(filename)



   
if __name__== "__main__":

    from getopt import getopt
  
    netmask = NETMASK

    ip = IP

    filename = FILENAME

    opts,vals = getopt(sys.argv[1:],'n:p:f:')
    print opts, ' ,', vals

    for option, arg in opts:
        if option == '-n':
            netmask = unicode(arg)
        elif option == '-f':
            filename = arg
        elif option == '-p':
            ip = arg

    main(netmask, ip, filename)

  

