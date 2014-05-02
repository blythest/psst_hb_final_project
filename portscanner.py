import sys, socket, select, ipaddress, psutil
import beautiful_soup_parsing
from subprocess import * 
import os
import shlex

LOCKFILE = '.lock'

def get_command_output(arguments, stderr=STDOUT):
    """
    arguments: A sequence of command arguments.
    Returns the output of the command line program. 
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
    command = ["nmap", "-PN", "-O", "-oX", "-"] + available_hosts
    # print 'command ', command
    scan_output = get_command_output(command)
    # print 'scan output: ', scan_output
    return scan_output


def list_hosts(ip):

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


def get_traceroute():
    
    # using traceroute to get public IP addresses
    hops = []
    try:
        response, unans = traceroute("www.google.com")
    except:
        print 'cannot trace route with scapy'
        return


    host_key = response.get_trace().keys()[0]
    if len(host_key) <= 15:
        return host_key
    else:
        for key in response.get_trace()[host_key].keys():
            hops.append(response.get_trace()[host_key][key][0])
        return hops



def get_IP():

    """
    Finds and returns the local IP address as dotted-quad ints on my host computer. 
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # google public dns
    s.connect(('8.8.8.8',53))
    ip = s.getsockname()[0]
    print 'this is the ip', ip
    s.close()
    return ip

NETMASK = u'255.255.255.0'
IP = get_IP()
FILENAME = 'static/nmap_raw.xml'
    
def main(netmask,ip,filename):

    subnetmask = int(ipaddress.IPv4Address(netmask))
    source_ip = int(ipaddress.IPv4Address(unicode(ip)))

    snet = int(ipaddress.IPv4Address(source_ip & subnetmask))
    snet = ipaddress.IPv4Address(snet)
    all_hosts = list_hosts(snet)

    
    available_hosts = find_available_hosts(all_hosts)
    results = scan(available_hosts)

    nmap_xml_output = open(filename, 'w')
    nmap_xml_output.write(results)
    nmap_xml_output.close()
    beautiful_soup_parsing.main(filename)



   
if __name__== "__main__":

    from getopt import getopt

    # check if pid is set to something.
    # if so, check if process is running.

    try:
        pid = os.readlink(LOCKFILE)
        if psutil.pid_exists(int(pid)):
            print 'portscanner already running.'
            os.sys.exit()
        else:
            os.unlink(LOCKFILE)
    except OSError:
        pass
            # make file
    os.symlink(str(os.getpid()), LOCKFILE)

    netmask = NETMASK


    ip = IP
    print ip

    filename = FILENAME

    opts,vals = getopt(sys.argv[1:],'n:p:f:')
 
    for option, arg in opts:
        if option == '-n':
            netmask = unicode(arg)
        elif option == '-f':
            filename = arg
        elif option == '-p':
            ip = arg

    main(netmask, ip, filename)
    os.unlink(LOCKFILE)

  

