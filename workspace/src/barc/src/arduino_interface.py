#!/usr/bin/env python

# ---------------------------------------------------------------------------
# Licensing Information: You are free to use or extend these projects for
# education or reserach purposes provided that (1) you retain this notice
# and (2) you provide clear attribution to UC Berkeley, including a link
# to http://barc-project.com
#
# Attibution Information: The barc project ROS code-base was developed at UC
# Berkeley in the Model Predictive Control (MPC) lab by Jon Gonzales
# (jon.gonzales@berkeley.edu) and Greg Marcil (grmarcil@berkeley.edu). The cloud
# services integation with ROS was developed by Kiet Lam
# (kiet.lam@berkeley.edu). The web-server app Dator was based on an open source
# project by Bruce Wootton
# ---------------------------------------------------------------------------

# README: This node serves as an outgoing messaging bus from odroid to arduino
# Subscribes: steering and motor commands on 'servo_pwm' and 'motor_pwm' and
# Publishes: combined ecu commands as 'ecu'

# Eventually, there should be another node, or this node could be extended, as a
# central translator between steering angle and desired acceleration to servo
# and motor pwm. Making the translator a separate node would be nice because
# this node would be reusable with different translators (in case someone has a
# controller that outputs something other than desired acceleration, for
# example). Eg, my cruise controller operates directly on motor cmd

import rospy
from barc.msg import ECU
from input_map import angle_2_servo

def motor_callback(msg):
    global motor_pwm
    motor_pwm = msg.motor_pwm
    update_arduino()

def servo_callback(msg):
    global servo_pwm
    servo_pwm = msg.servo_pwm
    update_arduino()

def neutralize():
    global motor_pwm
    motor_pwm = 90
    update_arduino()

def update_arduino():
    global motor_pwm, servo_cmd, ecu_pub
    ecu_cmd = ECU(motor_pwm, servo_pwm)
    ecu_pub.publish(ecu_cmd)

def arduino_interface():
    global motor_pwm, servo_pwm, ecu_pub
    # launch node, subscribe to motorPWM and servoPWM, publish ecu
    rospy.init_node('arduino_interface')
    rospy.Subscriber('motor_pwm', ECU, motor_callback, queue_size = 10)
    rospy.Subscriber('servo_pwm', ECU, servo_callback, queue_size = 10)
    ecu_pub = rospy.Publisher('ecu', ECU, queue_size = 10)

    # initialize motor and servo at neutral
    motor_pwm = 90
    steering_angle = 0
    steering_offset = 2
    servo_pwm = angle_2_servo(steering_angle - steering_offset)

    # Set motor to neutral on shutdown
    rospy.on_shutdown(neutralize)

    # process callbacks and keep alive
    rospy.spin()

#############################################################
if __name__ == '__main__':
    try:
        arduino_interface()
    except rospy.ROSInterruptException:
        pass
