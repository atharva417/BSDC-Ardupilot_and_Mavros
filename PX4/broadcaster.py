#!/usr/bin/env python  
import roslib
import rospy
from geometry_msgs.msg import PoseStamped
import tf

def handle_pose(msg):
    br = tf.TransformBroadcaster()
    br.sendTransform((msg.pose.position.x, msg.pose.position.y, msg.pose.position.z),
                     (msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w),
                     rospy.Time.now(),
                     "fpv_link",
                     "/world")

if __name__ == '__main__':
    rospy.init_node('cam_tf_broadcaster')
    rospy.Subscriber('/mavros/local_position/pose',
                     PoseStamped,
                     handle_pose)
    rospy.spin()