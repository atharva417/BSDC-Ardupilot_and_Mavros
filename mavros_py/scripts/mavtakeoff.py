import rospy
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode

rospy.wait_for_service('/mavros/cmd/takeoff')
try:
    takeoff = rospy.ServiceProxy('/mavros/cmd/takeoff', CommandTOL)
    response = takeoff(0,0,0,0,20)
    response.success
except rospy.ServiceException, e:
    print "Service call failed: %s"%e