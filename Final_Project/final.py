##################################################
## Final Project - Implementing a Simple Router ##
##################################################
## Ashwin Chidambaram                           ##
## 03/06/2020                                   ##
##################################################
## final.py ######################################
##################################################

#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI

class MyTopology(Topo):
    """
    A basic topology
    """
    def __init__(self):
        Topo.__init__(self)

        # Set Up Topology Here
        switch1 = self.addSwitch('Floor_1')                                     ## Adds Switch 1    [s1]
        switch2 = self.addSwitch('Floor_2')                                     ## Adds Switch 2    [s2]
        switch3 = self.addSwitch('Floor_3')                                     ## Adds Switch 3    [s3]
        switch4 = self.addSwitch('Core')                                        ## Adds Switch 3    [s3]
        switch5 = self.addSwitch('Data_Center')                                 ## Adds Switch 3    [s3]

        host1 = self.addHost('h1')                                              ## Adds a Host      [h1]
        self.addLink(host1, switch1)                                            ## Link             [h1] to [s1]


        host2 = self.addHost('h2')                                              ## Adds a Host      [h2]
        self.addLink(host2, switch2)                                            ## Link             [h2] to [s2]

        host3 = self.addHost('h3')                                              ## Adds a Host      [h3]
        self.addLink(host3, switch3)                                            ## Link             [h3] to [s1]

        host4 = self.addHost('h4')                                              ## Adds a Host      [h4]
        self.addLink(host4, switch4)                                            ## Link             [h4] to [s2]

        host5 = self.addHost('h5')                                              ## Adds a Host      [h5]
        self.addLink(host5, switch5)                                            ## Link             [h5] to [s3]

        self.addLink(switch1, switch4)                                          ## addLink          [s1] to [s3]
        self.addLink(switch2, switch4)                                          ## addLink          [s2] to [s3]
        self.addLink(switch3, switch4)                                          ## addLink          [s2] to [s3]

        self.addLink(switch4, switch5)                                          ## addLink          [s2] to [s3]

if __name__ == '__main__':
    """
    If this script is run as an executable (by chmod +x), this is
    what it will do
    """

    topo = MyTopology()            ## Creates the topology
    net = Mininet( topo=topo )        ## Loads the topology
    net.start()                      ## Starts Mininet

    # Commands here will run on the simulated topology
    CLI(net)

    net.stop()                       ## Stops Mininet
