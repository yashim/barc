#!/usr/bin/env python

# ---------------------------------------------------------------------------
# Licensing Information: You are free to use or extend these projects for 
# education or reserach purposes provided that (1) you retain this notice
# and (2) you provide clear attribution to UC Berkeley, including a link 
# to http://barc-project.com
#
# Attibution Information: The barc project ROS code-base was developed
# at UC Berkeley in the Model Predictive Control (MPC) lab by Jon Gonzales
# (jon.gonzales@berkeley.edu). The cloud services integation with ROS was developed
# by Kiet Lam  (kiet.lam@berkeley.edu). The web-server app Dator was 
# based on an open source project by Bruce Wootton
# ---------------------------------------------------------------------------

from rospy import init_node, Subscriber, Publisher, spin 
from rospy import Rate, is_shutdown, ROSInterruptException
from barc.msg import ECU
from math import pi
import numpy as np
import rospy

############################################################
# [deg] -> [PWM]
def angle_2_servo(x):
    u   = 92.0558 + 1.8194*x  - 0.0104*x**2
    return u

############################################################
def ecu_callback(data, pub):
    # unpack msg and convert to PWM instructions
    u_motor     = data.throttle + 95
    u_servo     = angle_2_servo( data.str_ang )

    # publish low level commands to ECU
    pub.publish( ECU(u_motor, u_servo) ) 
    
#############################################################
def main_auto():
    # initialize ROS node
    init_node('auto_mode', anonymous=True)
    pub = Publisher('ecu_pwm', ECU, queue_size = 10)
    sub = Subscriber('ecu', ECU, (pub,), ecu_callback)

    # keep node alive
    spin()


#############################################################
if __name__ == '__main__':
	try:
		main_auto()
	except ROSInterruptException:
		pass
