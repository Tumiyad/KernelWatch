from scapy.all import *

p=IP(dst="10.0.2.15")/ICMP()
res=sr1(p)
res.show()