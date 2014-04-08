Psst, Your Telnet Is Showing

The Psst, Your Telnet Is Showing application visualizes information about hosts connected to the user's network. Psst scans hosts connected to the user's network and gets the dirt on who's available: their IP addresses, which ports are open, what version of operating system they're running, and type of device. It displays the information on an interactive user interface, created with the D3 Javascript library.

Port Scanning
(portscanner.py)

By default, Psst begins by finding the user's IP address and the number of hosts on the network s/he is connected to. The number of hosts is determined via the subnet mask. For the scope of my project, I've set the default subnet mask as 255.255.255.0. The output of the scan will be sent to nmap-raw.xml. The user can change any of these values by running portscanner.py from terminal. 

To find reachable hosts, I used FPing,  which sends Internet Control Message Protocol (ICMP) echo request packets to each host; if it receives a response, then the host is available. Ping, the Unix utility typically used for host discovery (since 1983! (http://www.webcitation.org/5saCKBpgH)) waits for a response from each host until moving on to the next. FPing is great because it works in parallel — so much faster! 

Port scanning is handled using Python's NMAP (Network Mapper) module. NMAP is a security scanner that sends packets to target the available hosts and outputs the result in XML. 

beautifulsoupparser.py

Parses the XML output from portscanner.py into JSON, which D3 handles better.

Flask Views (aka the Controller) 
views.py
The web app runs on Python's Flask framework. 

 