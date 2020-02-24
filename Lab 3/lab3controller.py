############################################
## Lab 3 - Simple Firewall Using OpenFlow ##
############################################
## Ashwin Chidambaram                     ##
## 02/22/2020                             ##
############################################

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

############################################
class Firewall (object):
    def __init__(self, connection):
        # Keep track of the connection to the switch so that we can
    	# send it messages
    	self.connection = connection

    	# This binds our PacketIn event listener
    	connection.addListeners(self)

    def do_firewall(self, packet, packet_in):
        # Variables
        idle_timeout = 30                                                       # Time taken to timeout in seconds
        hard_timeout = 60                                                       # Max time taken to timeout in seconds

        msg = of.ofp_flow_mod()

    	# Match Packet
    	msg.match = of.ofp_match.from_packet(packet)

        # Timeout timers
    	msg.idle_timeout = idle_timeout
    	msg.hard_timeout = hard_timeout

    	protocol_ARP = packet.find('arp')
    	protocol_TCP = packet.find('tcp')
    	protocol_ICMP = packet.find('icmp')

    	# ARP, TCP, or ICMP Check

        #### ARP Check #########################################################
        if protocol_ARP is not None:

            # Take in data packet
            msg.data = packet_in

            # Check if ARP type
            msg.match.dl_type = 0x8086                                          ###-*-###

            # Action to send to specified port                                  ###-*-###
            action = of.ofp_action_output(port = of.OFPP_FLOOD)
            msg.actions.append(action)

            # Send message to switch
            self.connection.send(msg)


        ### TCP Check ##########################################################
        elif protocol_TCP is not None:

            # Check if IPv4
            protocol_IPv4 = packet.find('ipv4')

            # Determine if traffic flow from 10.0.1.40 to 10.0.1.10 or vice versa
            if (protocol_IPv4.srcip == '10.0.1.40' and protocol_IPv4.dstip == '10.0.1.10') or (protocol_IPv4.srcip == '10.0.1.10' and protocol_IPv4.dstip == '10.0.1.40'):

                # Take in data packet
                msg.data = packet_in

                # Check if TCP type
                msg.nw_proto = 6                                                ###-*-###

                # Action to send to specified port                              ###-*-###
                action = of.ofp_action_output(port = of.OFPP_FLOOD)
                msg.actions.append(action)

                # Send message to switch
                self.connection.send(msg)

            # If source/destination IP don't match condition, then just direct to switch
            else:
                # Send message to switch
                self.connection.send(msg)


        ### ICMP Check #########################################################
        elif protocol_ICMP is not None:

            # Take in data packet
            msg.data = packet_in

            # Check if TCP type
            msg.IP_PROTO = 1                                                    ###-*-###

            # Action to send to specified port                                  ###-*-###
            action = of.ofp_action_output(port = of.OFPP_FLOOD)
            msg.actions.append(action)

            # Send message to switch
            self.connection.send(msg)


        ########################################################################
        else:
		self.connection.send(msg)

	###################################################

  def _handle_PacketIn (self, event):
	"""
	Handles packet in messages from the switch.
	"""

	packet = event.parsed # This is the parsed packet data.
	if not packet.parsed:
	  log.warning("Ignoring incomplete packet")
	  return

	packet_in = event.ofp # The actual ofp_packet_in message.
	self.do_firewall(packet, packet_in)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
	log.debug("Controlling %s" % (event.connection,))
	Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)




  ############# Sources Utilized ###############################################
  ## http://sdnhub.org/tutorials/pox/
  ## http://flowgrammable.org/sdn/openflow/classifiers/
  ## https://openflow.stanford.edu/display/ONL/POX+Wiki.html#POXWiki-Example%3AInstallingatableentry
  ##
