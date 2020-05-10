#!/usr/bin/env python
import rospy
import time
from mavros_msgs.srv import *#CommandBool, CommandTOL, SetMode, WaypointPush
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

def takeoff():
	rospy.wait_for_service('/mavros/cmd/takeoff')
	try:
	    takeoff = rospy.ServiceProxy('/mavros/cmd/takeoff', CommandTOL)
	    response = takeoff(0,0,0,0,100)
	    response.success
	except rospy.ServiceException, e:
	    print "Service call failed: %s"%e

def waypoint(x,y,z):
	rospy.wait_for_service('/mavros/mission/push')
	try:
		wp = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
		wp_list = []
		wp_list.append(home())
		wp_list.append(wp1(x,y,z))
		start_index = 0
		response = wp(start_index, wp_list)
		if (response.success):
			print "Sent %s waypoints"%(response.wp_transfered)
	except rospy.ServiceException, e:
	    print "Service call failed: %s"%e

def wp1(x,y,z):
	d = Waypoint()
	d.frame = 3
	d.command = 16
	d.is_current = True
	d.autocontinue = True
	d.param1 = 0.000000
	d.param2 = 0.000000
	d.param3 = 0.000000
	d.param4 = 0.000000
	d.x_lat = x #-35.362521
	d.y_long = y #149.170465
	d.z_alt = z #70.000000
	return d

def home(): #for home.
	d = Waypoint()
	d.frame = 0
	d.command = 16
	d.is_current = True
	d.autocontinue = True
	d.param1 = 0.000000
	d.param2 = 0.000000
	d.param3 = 0.000000
	d.param4 = 0.000000
	d.x_lat = -35.363262
	d.y_long = 149.165238
	d.z_alt = 584.090027
	return d
#	rospy.wait_for_service('/mavros/mission/push')
#	try:
#		seq = rospy.ServiceProxy('/mavros/mission/set_current', WaypointSetCurrent)
#		wp = rospy.ServiceProxy('/mavros/mission/push', WaypointPush)
#		response = wp(0,[d])
#		resp = seq(0)
#		resp.success
#		response.success
#		response.wp_transfered
#	except rospy.ServiceException, e:
#	    print "Service call failed: %s"%e

if __name__ == '__main__':
	rospy.init_node('ardu_mavros_node', anonymous=True)

	pytakeoff()
	time.sleep(2)
	setarm(1)
	time.sleep(2)
	waypoint(-35.362521,149.170465,70.000000)
	time.sleep(1)
	setmode('AUTO')
