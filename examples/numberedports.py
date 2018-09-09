#!/usr/bin/python

"""
Create a network with 5 hosts, numbered 1-4 and 9.
Validate that the port numbers match to the interface name,
and that the ovs ports match the mininet ports.
"""


from mininet.net import Mininet
from mininet.node import Controller
from mininet.log import setLogLevel, info, warn

def validatePort( switch, intf ):
    "Validate intf's OF port number"
    ofport = int( switch.cmd( 'ovs-vsctl get Interface', intf,
                              'ofport' ) )
    if ofport != switch.ports[ intf ]:
        warn( 'WARNING: ofport for', intf, 'is actually', ofport, '\n' )
        return 0
    else:
        return 1

def testPortNumbering():

    """Test port numbering:
       Create a network with 5 hosts (using Mininet's
       mid-level API) and check that implicit and
       explicit port numbering works as expected."""

    net = Mininet( controller=Controller )

    info( '*** Adding controller\n' )
    net.addController( 'c0' )

    info( '*** Adding hosts\n' )
    h1 = net.addHost( 'h1', ip='10.0.0.1' )
    h2 = net.addHost( 'h2', ip='10.0.0.2' )
    h3 = net.addHost( 'h3', ip='10.0.0.3' )
    h4 = net.addHost( 'h4', ip='10.0.0.4' )
    h5 = net.addHost( 'h5', ip='10.0.0.5' )

    info( '*** Adding switch\n' )
    s1 = net.addSwitch( 's1' )

    info( '*** Creating links\n' )
    # host 1-4 connect to ports 1-4 on the switch
    net.addLink( h1, s1 )
    net.addLink( h2, s1 )
    net.addLink( h3, s1 )
    net.addLink( h4, s1 )
    # specify a different port to connect host 5 to on the switch.
    net.addLink( h5, s1, port1=1, port2= 9)

    info( '*** Starting network\n' )
    net.start()

    # print the interfaces and their port numbers
    info( '\n*** printing and validating the ports '
          'running on each interface\n' )
    for intfs in s1.intfList():
        if not intfs.name == "lo":
            info( intfs, ': ', s1.ports[intfs],
                  '\n' )
            info( 'Validating that', intfs,
                   'is actually on port', s1.ports[intfs], '... ' )
            if validatePort( s1, intfs ):
                info( 'Validated.\n' )
    info( '\n' )

    # test the network with pingall
    net.pingAll()
    info( '\n' )

    info( '*** Stopping network\n' )
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    testPortNumbering()

    
"""
# Output is like:

$ sudo python mininet/examples/numberedports.py 
*** Adding controller
*** Adding hosts
*** Adding switch
*** Creating links
*** Starting network
*** Configuring hosts
h1 h2 h3 h4 h5 
*** Starting controller
c0 
*** Starting 1 switches
s1 ...

*** printing and validating the ports running on each interface
s1-eth1 :  1 
Validating that s1-eth1 is actually on port 1 ... Validated.
s1-eth2 :  2 
Validating that s1-eth2 is actually on port 2 ... Validated.
s1-eth3 :  3 
Validating that s1-eth3 is actually on port 3 ... Validated.
s1-eth4 :  4 
Validating that s1-eth4 is actually on port 4 ... Validated.
s1-eth9 :  9 
Validating that s1-eth9 is actually on port 9 ... Validated.

*** Ping: testing ping reachability
h1 -> h2 h3 h4 h5 
h2 -> h1 h3 h4 h5 
h3 -> h1 h2 h4 h5 
h4 -> h1 h2 h3 h5 
h5 -> h1 h2 h3 h4 
*** Results: 0% dropped (20/20 received)

*** Stopping network
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
