import rospy
from mavros_msgs.srv import CommandBool, CommandTOL, SetMode

rospy.wait_for_service('/mavros/set_mode')
try:
    mode = rospy.ServiceProxy('/mavros/set_mode', SetMode)
    response = mode(0,'GUIDED')
    response.mode_sent
except rospy.ServiceException, e:
    print "Service call failed: %s"%e