#!/usr/bin/env python
import rospy
from sensor_msgs.msg import NavSatFix
from mpl_toolkits import mplot3d
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt



def callback(data):
    x = data.latitude
    y = data.longitude
    z = data.altitude
    ax = plt.axes(projection='3d')

    ax.plot3D(x, y, z, 'red')

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("/mavros/global_position/raw/fix", NavSatFix, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
