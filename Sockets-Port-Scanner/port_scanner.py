#!/usr/bin/env python3

import socket
import re

# Regex Patterns
ipv4_pattern = re.compile("^([0-9]{1,3}\.){3}([0-9]{1,3})$")
ports_pattern = re.compile("^([0-9]+)-([0-9]+)$")


min_port = 0
max_port = 65535


# User Interface
print("""
__   __              _  __    ____           _ 
\ \ / /__  _   _ ___(_)/ _|  / ___| __ _  __| |
 \ V / _ \| | | / __| | |_  | |  _ / _` |/ _` |
  | | (_) | |_| \__ \ |  _| | |_| | (_| | (_| |
  |_|\___/ \__,_|___/_|_|    \____|\__,_|\__,_|\n""")
print("*" * 50)  
print("\n*Disclaimer: use this tool for educational purposes only on devices you own")
print("\nCopyright of Yousif Gad, 2022\n")
print("*" * 50)


open_ports = []

while True:
    ip_input = input("\nEnter the IP you want to scan: ")
    if ipv4_pattern.search(ip_input):
        print(f"{ip_input} is a valid IP")
        break


while True:
    print("Enter the range of ports you want to scan in format: <int>-<int> (ex 20-25)")
    ports_range = input("Enter the range of ports: ")
    ports_range_if_valid = ports_pattern.search(ports_range.replace(" ", ""))
    
    if ports_range_if_valid:
        min_port_scan = int(ports_range_if_valid.group(1))
        max_port_scan = int(ports_range_if_valid.group(2))
        break


for port in range(min_port_scan , max_port_scan + 1):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sock:
        sock.settimeout(0.5)
        r = sock.connect_ex((ip_input,port))

        if r:
            pass
        else:
            open_ports.append(port)


if open_ports:
    for port in open_ports:
        print(f"Port {port} is open")

else:
    print("No ports are open")
