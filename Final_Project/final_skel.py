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
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.node import RemoteController

class final_topo(Topo):
    def build(self):

        #### Set up Hosts ######################################################
        host1 = self.addHost('h1', mac='00:00:00:00:00:01', ip='10.0.1.101/24', defaultRoute="h1-eth0")                 ## Host 1
        host2 = self.addHost('h2', mac='00:00:00:00:00:02', ip='10.0.2.102/24', defaultRoute="h2-eth0")                 ## Host 2
        host3 = self.addHost('h3', mac='00:00:00:00:00:03', ip='10.0.3.103/24', defaultRoute="h3-eth0")                 ## Host 3
        host4 = self.addHost('S1', mac='00:00:00:00:00:04', ip='10.0.1.104/24', defaultRoute="s1-eth0")                 ## Server
        host5 = self.addHost('h4', mac='00:00:00:00:00:05', ip='128.114.50.10/24', defaultRoute="h4-eth0")              ## Untrusted Host [4]

        #### Set up Switches ###################################################
        switch1 = self.addSwitch('Floor_1')                                                                             ## Adds Floor 1 Switch
        switch2 = self.addSwitch('Floor_2')                                                                             ## Adds Floor 2 Switch
        switch3 = self.addSwitch('Floor_3')                                                                             ## Adds Floor 3 Switch
        switch4 = self.addSwitch('Core')                                                                                ## Adds Core Switch
        switch5 = self.addSwitch('Data_Center')                                                                         ## Adds Data Center Switch

        #### Link Switches & Hosts #############################################

        # Connect Port 8 on the Switch to Port 0 on Host 1 and Port 9 on the Switch to Port 0 on
        # Host 2. This is representing the physical port on the switch or host that you are
        # connecting to.

        # Link the Hosts to their relevent switches
        self.addLink(host1, switch1, port1=1, port2=2)
        self.addLink(host2, switch2, port1=1, port2=2)
        self.addLink(host3, switch3, port1=1, port2=2)
        self.addLink(host5, switch4, port1=1, port2=5)
        self.addLink(host4, switch5, port1=1, port2=5)

        # Link to Core Switch
        self.addLink(switch1, switch4, port1=3, port2=1)
        self.addLink(switch2, switch4, port1=3, port2=2)
        self.addLink(switch3, switch4, port1=3, port2=3)
        self.addLink(switch5, switch4, port1=3, port2=4)

def configure():
    topo = final_topo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    CLI(net)

    net.stop()


if __name__ == '__main__':
    configure()
