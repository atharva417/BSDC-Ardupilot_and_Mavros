#!/usr/bin/env python
import rospy
import time
from mavros_msgs.srv import *
from pymavlink import mavutil, mavwp
from mavros_msgs.msg import *

def pytakeoff():
	master = mavutil.mavlink_connection('udpin:0.0.0.0:14550')
	master.wait_heartbeat()
	master.set_mode_apm("TAKEOFF")

def setmode(x): # input: mode in capital
	rospy.wait_for_service('/mavros/set_mode')
	try:
	    mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
	    response = mode(0,x)
	    response.mode_sent
	except rospy.ServiceException, e:
	    print "Service call failed: %s"%e

def setarm(x): # input: 1=arm, 0=disarm
	rospy.wait_for_service('/mavros/cmd/arming')
	try:
	    arming = rospy.ServiceProxy('/mavros/cmd/arming', CommandBool)
	    response = arming(x)
	    response.success
	except rospy.ServiceException, e:
	    print "Service call failed: %s"%e

def waypoint(x): # x is address of wp.txt file
	rospy.wait_for_service('/mavros/mission/push')
	try:
		wp = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
		start_index = 0
		response = wp(start_index, wpt(x))
		if (response.success):
			print "Sent %s waypoints"%(response.wp_transfered)
	except rospy.ServiceException, e:
	    print "Service call failed: %s"%e

def wpt(x):
    wp_list = []
    file = open(x, "r")
    for line in file:
        if line.startswith('#'):
            comment = line[1:].lstrip()
            continue
        line = line.strip()
        if not line:
            continue
        a = line.split()
        d = Waypoint()
        d.frame = int(a[2])
    	d.command = int(a[3])
    	d.is_current = int(a[1])
    	d.autocontinue = int(a[11])
    	d.param1 = float(a[4])
    	d.param2 = float(a[5])
    	d.param3 = float(a[6])
    	d.param4 = float(a[7])
    	d.x_lat = float(a[8])
    	d.y_long = float(a[9])
    	d.z_alt = float(a[10])
        wp_list.append(d)
    file.close()
    return wp_list

if __name__ == '__main__':
	rospy.init_node('ardu_mavros_node', anonymous=True)

	pytakeoff()
	time.sleep(2)
	setarm(1)
	time.sleep(2)
	waypoint('/home/atharva/ardumavros_ws/src/mavros_py/waypointfiles/wayptmav.txt')
	time.sleep(1)
	setmode('AUTO')
