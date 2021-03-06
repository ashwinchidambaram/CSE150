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
        h1 = self.addHost('h1',mac='00:00:00:00:00:01',ip='10.0.1.101/24',defaultRoute="h1-eth0")               ## Host 1
        h2 = self.addHost('h2',mac='00:00:00:00:00:02',ip='10.0.2.102/24',defaultRoute="h2-eth0")               ## Host 2
        h3 = self.addHost('h3',mac='00:00:00:00:00:03',ip='10.0.3.103/24',defaultRoute="h3-eth0")               ## Host 3
        h4 = self.addHost('h4',mac='00:00:00:00:00:04',ip='128.114.50.10/24',defaultRoute="h4-eth0")            ## Untrusted Host
        h5 = self.addHost('h5',mac='00:00:00:00:00:04',ip='10.0.4.104/24',defaultRoute="h5-eth0")               ## Server

        #### Set up Switches ###################################################
        s1 = self.addSwitch('s1')                                                                               ## Adds Floor 1 Switch
        s2 = self.addSwitch('s2')                                                                               ## Adds Floor 2 Switch
        s3 = self.addSwitch('s3')                                                                               ## Adds Floor 3 Switch
        s4 = self.addSwitch('s4')                                                                               ## Adds Core Switch
        s5 = self.addSwitch('s5')                                                                               ## Adds Data Center Switch

        #### Link Switches & Hosts #############################################

        # Link the Hosts to their relevent switches
        self.addLink(s1, h1, port1=8, port2=0)                                                                  ## Link Switch 1 & Host 1   -   [Floor Switch 1 <--> Host 1]
        self.addLink(s2, h2, port1=8, port2=0)                                                                  ## Link Switch 2 & Host 2   -   [Floor Switch 2 <--> Host 2]
        self.addLink(s3, h3, port1=8, port2=0)                                                                  ## Link Switch 3 & Host 3   -   [Floor Switch 3 <--> Host 3]
        self.addLink(s4, h4, port1=8, port2=0)                                                                  ## Link Switch 4 & Host 4   -   [Core Switch <--> Untrusted Host]
        self.addLink(s5, h5, port1=8, port2=0)                                                                  ## Link Switch 4 & Host 4   -   [Data Center Switch <--> Server]

        # Link to Core Switch
        self.addLink(s1, s4, port1=3, port2=1)                                                                  ## Link Switch 1 & Switch 4 -   [Floor Switch 1 <--> Core Switch]
        self.addLink(s2, s4, port1=3, port2=2)                                                                  ## Link Switch 2 & Switch 4 -   [Floor Switch 2 <--> Core Switch]
        self.addLink(s3, s4, port1=3, port2=3)                                                                  ## Link Switch 3 & Switch 4 -   [Floor Switch 3 <--> Core Switch]
        self.addLink(s5, s4, port1=3, port2=4)                                                                  ## Link Switch 5 & Switch 4 -   [Data Center Switch <--> Core Switch]

def configure():
    topo = final_topo()
    net = Mininet(topo=topo, controller=RemoteController)
    net.start()

    CLI(net)

    net.stop()

if __name__ == '__main__':
    configure()
