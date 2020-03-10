##################################################
## Final Project - Implementing a Simple Router ##
##################################################
## Ashwin Chidambaram                           ##
## 03/06/2020                                   ##
##################################################
## final_controller.py ###########################
##################################################

# Final Skeleton
#
# Hints/Reminders from Lab 4:
#
# To send an OpenFlow Message telling a switch to send packets out a
# port, do the following, replacing <PORT> with the port number the
# switch should send the packets out:
#
#    msg = of.ofp_flow_mod()
#    msg.match = of.ofp_match.from_packet(packet)
#    msg.idle_timeout = 30
#    msg.hard_timeout = 30
#
#    msg.actions.append(of.ofp_action_output(port = <PORT>))
#    msg.data = packet_in
#    self.connection.send(msg)
#
# To drop packets, simply omit the action.
#

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
    """
    A Firewall object is created for each switch that connects.
    A Connection object for that switch is passed to the __init__ function.
    """
    def __init__ (self, connection):

        # Keep track of the connection to the switch so that we can send it messages
        self.connection = connection

        # This binds our PacketIn event listener
        connection.addListeners(self)

    def do_final (self, packet, packet_in, port_on_switch, switch_id):

        idle_timeout = 30                                                               ## Time taken to timeout in seconds
        hard_timeout = 60                                                               ## Max time taken to timeout in seconds

        msg = of.ofp_flow_mod()

        # Match Packet
        msg.match = of.ofp_match.from_packet(packet)
        msg.data = packet_in

        # Timeout timers
        msg.idle_timeout = idle_timeout
        msg.hard_timeout = hard_timeout

        untrustedHost_IP = '128.114.50.10'

        #protocol_TCP = packet.find('tcp')
    	#protocol_ARP = packet.find('arp')
    	protocol_ICMP = packet.find('icmp')
        protocol_IPv4 = packet.find('ipv4')

        if protocol_IPv4 is not None:

            #### Switch 1 ######################################################
            if switch_id is 1:

                if port_on_switch is 8:
                    msgAction = of.ofp_action_output(port = 3)
                    msg.actions.append(msgAction)

                elif port_on_switch is 3:
                    msgAction = of.ofp_action_output(port = 8)
                    msg.actions.append(msgAction)
                    
            #### Switch 2 ######################################################
            elif switch_id is 2:

                if port_on_switch is 8:
                    msgAction = of.ofp_action_output(port = 3) #send to s4
                    msg.actions.append(msgAction)

                elif port_on_switch is 3:
                    msgAction = of.ofp_action_output(port = 8) #send to h1
                    msg.actions.append(msgAction)

            #### Switch 3 ######################################################
            elif switch_id is 3:

                if port_on_switch is 8:
                    msgAction = of.ofp_action_output(port = 3) #send to s4
                    msg.actions.append(msgAction)

                elif port_on_switch is 3:
                    msgAction = of.ofp_action_output(port = 8) #send to h1
                    msg.actions.append(msgAction)

            #### Switch 5 ######################################################
            elif switch_id is 5:

                if port_on_switch is 8:
                    msgAction = of.ofp_action_output(port = 3) #send to s4
    			    msg.actions.append(msgAction)

                elif port_on_switch is 3:
                    msgAction = of.ofp_action_output(port = 8) #send to h1
                    msg.actions.append(msgAction)

            #### Switch 4 ######################################################
            elif switch_id is 4:
    		#print 'ip at s4'
        		if port_on_switch is 1:
        			#from untrusted host h4 to server h5, drop
        			if icmp is not None:
        				self.connection.send(msg)
        				#print 'icmp packet from h4 dropped'
        				return
        		elif ip.dstip == untrustedHost_IP: #drop ip packet to h5 from h4
        				self.connection.send(msg)
        				#print 'ip packet from h4 to h5 dropped'
        				return
        			elif ip.dstip == '10.0.1.101': #forward to h1
        				msgAction = of.ofp_action_output(port = 1)
        				msg.actions.append(msgAction)
        				#print 'sent o host 1'
        			elif ip.dstip == '10.0.2.102': #forward to h2
        				msgAction = of.ofp_action_output(port = 2)
        				msg.actions.append(msgAction)
        				#print 'sent o host 2'
        			elif ip.dstip == '10.0.3.103': #forward to h3
        				msgAction = of.ofp_action_output(port = 3)
        				msg.actions.append(msgAction)
        				#print 'sent o host 3'

        		else:
        			if ip.dstip == untrustedHost_IP: #forward to h4
        				msgAction = of.ofp_action_output(port = 1)
        				msg.actions.append(msgAction)
        				#print 'sent o host 4'
        			elif ip.dstip == '10.0.1.101': #forward to h1
        				msgAction = of.ofp_action_output(port = 2)
        				msg.actions.append(msgAction)
        				#print 'sent o host 1'
        			elif ip.dstip == '10.0.2.102': #forward to h2
        				msgAction = of.ofp_action_output(port = 3)
        				msg.actions.append(msgAction)
        				#print 'sent o host 2'
        			elif ip.dstip == '10.0.3.103': #forward to h3
        				msgAction = of.ofp_action_output(port = 4)
        				msg.actions.append(msgAction)
        				#print 'sent o host 3'
        			elif ip.dstip == '10.0.4.104': #forward to h5
        				msgAction = of.ofp_action_output(port = 5)
        				msg.actions.append(msgAction)
        				#print 'sent o host 5'
        else:
        # RAW TEST SCRIPT###############
            #msg.data = packet_in
            action = of.ofp_action_output(port = of.OFPP_FLOOD)
            msg.actions.append(action)
            #self.connection.send(msg)

    def _handle_PacketIn (self, event):
        """
        Handles packet in messages from the switch.
        """
        packet = event.parsed # This is the parsed packet data.
        if not packet.parsed:
          log.warning("Ignoring incomplete packet")
          return

        packet_in = event.ofp # The actual ofp_packet_in message.
        self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
    """
    Starts the component
    """
    def start_switch (event):
        log.debug("Controlling %s" % (event.connection,))
        Final(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
