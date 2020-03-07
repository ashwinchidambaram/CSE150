#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
    def build(self):

        # Set Up Topology Here
        switch1 = self.addSwitch('Floor_1')                                     ## Adds Switch 1    [s1]
        switch2 = self.addSwitch('Floor_2')                                     ## Adds Switch 2    [s2]
        switch3 = self.addSwitch('Floor_3')                                     ## Adds Switch 3    [s3]
        switch4 = self.addSwitch('Core')                                        ## Adds Switch 3    [s3]
        switch5 = self.addSwitch('Data_Center')                                 ## Adds Switch 3    [s3]

        host1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.1.101/24', defaultRoute="h1-eth0")
        self.addLink(host1, switch1)                                            ## Link             [h1] to [s1]

        host2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.1.102/24', defaultRoute="h2-eth0")
        self.addLink(host2, switch2)                                            ## Link             [h1] to [s1]

        host3 = self.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.1.103/24', defaultRoute="h3-eth0")
        self.addLink(host3, switch3)                                            ## Link             [h1] to [s1]

        self.addLink(switch1, switch4)                                            ## Link             [h1] to [s1]
        self.addLink(switch2, switch4)                                            ## Link             [h1] to [s1]
        self.addLink(switch3, switch4)                                            ## Link             [h1] to [s1]

        host4 = self.addHost('h4', mac='00:00:00:00:00:05', ip='128.114.50.10/24', defaultRoute="h4-eth1")
        self.addLink(host4, switch4)                                            ## Link             [h1] to [s1]

        self.addLink(switch4, switch5)                                            ## Link             [h1] to [s1]

        host5 = self.addHost('h5', mac='00:00:00:00:00:04', ip='10.0.1.104/24', defaultRoute="h5-eth0")
        self.addLink(host5, switch5)                                            ## Link             [h1] to [s1]


    # Examples!
    # Create a host with a default route of the ethernet interface. You'll need to set the
    # default gateway like this for every host you make on this assignment to make sure all
    # packets are sent out that port. Make sure to change the h# in the defaultRoute area
    # and the MAC address when you add more hosts!

    #h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='1.1.1.1/24', defaultRoute="h1-eth0")
    #h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='2.2.2.2/24', defaultRoute="h2-eth0")

    # Create a switch. No changes here from Lab 1.
    #s1 = self.addSwitch('s1')

    # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on
    # Host 2. This is representing the physical port on the switch or host that you are
    # connecting to.
    #self.addLink(s1,h1, port1=8, port2=0)
    #self.addLink(s1,h2, port1=9, port2=0)

def configure():
    topo = final_topo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    CLI(net)

    net.stop()


if __name__ == '__main__':
    configure()
