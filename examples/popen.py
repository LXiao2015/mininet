#!/usr/bin/python

"""
This example monitors a number of hosts using host.popen() and
pmonitor()
"""


from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel, info
from mininet.util import custom, pmonitor

def monitorhosts( hosts=5, sched='cfs' ):
    "Start a bunch of pings and monitor them using popen"
    mytopo = SingleSwitchTopo( hosts )
    cpu = .5 / hosts
    myhost = custom( CPULimitedHost, cpu=cpu, sched=sched )
    net = Mininet( topo=mytopo, host=myhost )
    net.start()
    # Start a bunch of pings
    popens = {}
    last = net.hosts[ -1 ]
    for host in net.hosts:
        popens[ host ] = host.popen( "ping -c5 %s" % last.IP() )
        last = host
    # Monitor them and print output
    for host, line in pmonitor( popens ):
        if host:
            info( "<%s>: %s" % ( host.name, line ) )
    # Done
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    monitorhosts( hosts=5 )

"""
Output is like:
$ sudo python popen.py 
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 h3 h4 h5 
*** Adding switches:
s1 
*** Adding links:
(h1, s1) (h2, s1) (h3, s1) (h4, s1) (h5, s1) 
*** Configuring hosts
h1 (cfs 10000/100000us) h2 (cfs 10000/100000us) h3 (cfs 10000/100000us) h4 (cfs 10000/100000us) h5 (cfs 10000/100000us) 
*** Starting controller
c0 
*** Starting 1 switches
s1 ...
<h4>: PING 10.0.0.3 (10.0.0.3) 56(84) bytes of data.
<h4>: 64 bytes from 10.0.0.3: icmp_seq=1 ttl=64 time=5.91 ms
<h5>: PING 10.0.0.4 (10.0.0.4) 56(84) bytes of data.
<h5>: 64 bytes from 10.0.0.4: icmp_seq=1 ttl=64 time=7.02 ms
<h3>: PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
<h3>: 64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=6.53 ms
<h2>: PING 10.0.0.1 (10.0.0.1) 56(84) bytes of data.
<h2>: 64 bytes from 10.0.0.1: icmp_seq=1 ttl=64 time=7.08 ms
<h1>: PING 10.0.0.5 (10.0.0.5) 56(84) bytes of data.
<h1>: 64 bytes from 10.0.0.5: icmp_seq=1 ttl=64 time=12.3 ms
<h4>: 64 bytes from 10.0.0.3: icmp_seq=2 ttl=64 time=0.209 ms
<h5>: 64 bytes from 10.0.0.4: icmp_seq=2 ttl=64 time=0.170 ms
<h1>: 64 bytes from 10.0.0.5: icmp_seq=2 ttl=64 time=0.231 ms
<h2>: 64 bytes from 10.0.0.1: icmp_seq=2 ttl=64 time=0.195 ms
<h3>: 64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.105 ms
<h4>: 64 bytes from 10.0.0.3: icmp_seq=3 ttl=64 time=0.037 ms
<h5>: 64 bytes from 10.0.0.4: icmp_seq=3 ttl=64 time=0.025 ms
<h1>: 64 bytes from 10.0.0.5: icmp_seq=3 ttl=64 time=0.028 ms
<h2>: 64 bytes from 10.0.0.1: icmp_seq=3 ttl=64 time=0.009 ms
<h3>: 64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.014 ms
<h4>: 64 bytes from 10.0.0.3: icmp_seq=4 ttl=64 time=0.041 ms
<h5>: 64 bytes from 10.0.0.4: icmp_seq=4 ttl=64 time=0.022 ms
<h1>: 64 bytes from 10.0.0.5: icmp_seq=4 ttl=64 time=0.012 ms
<h2>: 64 bytes from 10.0.0.1: icmp_seq=4 ttl=64 time=0.036 ms
<h3>: 64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.010 ms
<h4>: 64 bytes from 10.0.0.3: icmp_seq=5 ttl=64 time=0.038 ms
<h4>: 
<h4>: --- 10.0.0.3 ping statistics ---
<h4>: 5 packets transmitted, 5 received, 0% packet loss, time 4001ms
<h4>: rtt min/avg/max/mdev = 0.037/1.248/5.918/2.335 ms
<h5>: 64 bytes from 10.0.0.4: icmp_seq=5 ttl=64 time=0.028 ms
<h5>: 
<h5>: --- 10.0.0.4 ping statistics ---
<h5>: 5 packets transmitted, 5 received, 0% packet loss, time 3998ms
<h5>: rtt min/avg/max/mdev = 0.022/1.454/7.027/2.787 ms
<h1>: 64 bytes from 10.0.0.5: icmp_seq=5 ttl=64 time=0.036 ms
<h2>: 64 bytes from 10.0.0.1: icmp_seq=5 ttl=64 time=0.012 ms
<h3>: 64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.010 ms
<h1>: 
<h2>: 
<h3>: 
<h1>: --- 10.0.0.5 ping statistics ---
<h2>: --- 10.0.0.1 ping statistics ---
<h3>: --- 10.0.0.2 ping statistics ---
<h1>: 5 packets transmitted, 5 received, 0% packet loss, time 3999ms
<h2>: 5 packets transmitted, 5 received, 0% packet loss, time 3999ms
<h3>: 5 packets transmitted, 5 received, 0% packet loss, time 3998ms
<h1>: rtt min/avg/max/mdev = 0.012/2.526/12.326/4.900 ms
<h2>: rtt min/avg/max/mdev = 0.009/1.467/7.084/2.809 ms
<h3>: rtt min/avg/max/mdev = 0.010/1.334/6.533/2.599 ms
*** Stopping 1 controllers
c0 
*** Stopping 5 links
.....
*** Stopping 1 switches
s1 
*** Stopping 5 hosts
h1 h2 h3 h4 h5 
*** Done
"""
