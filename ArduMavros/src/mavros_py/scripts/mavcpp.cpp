#include <ros/ros.h>
#include <mavros_msgs/WaypointPush.h>
#include <mavros_msgs/WaypointClear.h>
#include <mavros_msgs/CommandHome.h>
#include <std_msgs/String.h>
#include <cstdlib>
#include <mavros_msgs/Waypoint.h>
#include <geometry_msgs/PoseStamped.h>
#include <mavros_msgs/CommandBool.h>
#include <mavros_msgs/SetMode.h>
#include <list>
#include <unistd.h>

int main(int argc, char **argv)
{
  ros::init(argc, argv, "srv_waypoint");
  ros::NodeHandle p;
  ros::NodeHandle n;
  ros::NodeHandle l;
  ros::NodeHandle nh;
  ros::NodeHandle t;

  ros::ServiceClient wp_clear_client = p.serviceClient<mavros_msgs::WaypointClear>("/mavros/mission/clear");
  ros::ServiceClient wp_srv_client = n.serviceClient<mavros_msgs::WaypointPush>("mavros/mission/push");
  ros::ServiceClient set_mode_client = l.serviceClient<mavros_msgs::SetMode>("mavros/set_mode");
  ros::ServiceClient arming_client = nh.serviceClient<mavros_msgs::CommandBool>("mavros/cmd/arming");

  mavros_msgs::WaypointPush wp_push_srv;
  mavros_msgs::WaypointClear wp_clear_srv;
  mavros_msgs::CommandBool set_arm_srv;
  mavros_msgs::SetMode set_mode_srv;
  mavros_msgs::Waypoint wp_msg;

  wp_clear_srv.request = {};
  set_arm_srv.request.value = true;
  set_mode_srv.request.custom_mode = "AUTO";

  wp_msg.frame = 0; // mavros_msgs::Waypoint::FRAME_GLOBAL_REL_ALT;
  wp_msg.command = 16;
  wp_msg.is_current = true;
  wp_msg.autocontinue = true;
  wp_msg.param1 = 0;
  wp_msg.param2 = 0;
  wp_msg.param3 = 0;
  wp_msg.param4 = 0;
  wp_msg.x_lat = -35.363262;
  wp_msg.y_long = 149.165238;
  wp_msg.z_alt = 584.090027;

  wp_push_srv.request.start_index = 0;
  wp_push_srv.request.waypoints.push_back(wp_msg);

  wp_msg.frame = 3; // mavros_msgs::Waypoint::FRAME_GLOBAL_REL_ALT;
  wp_msg.command = 16;
  wp_msg.is_current = false;
  wp_msg.autocontinue = true;
  wp_msg.param1 = 0;
  wp_msg.param2 = 0;
  wp_msg.param3 = 0;
  wp_msg.param4 = 0;
  wp_msg.x_lat = -35.362521;
  wp_msg.y_long = 149.170465;
  wp_msg.z_alt = 70.000000;

  wp_push_srv.request.start_index = 0;
  wp_push_srv.request.waypoints.push_back(wp_msg);

  if (arming_client.call(set_arm_srv))
  {
    ROS_INFO("Success:%d", (bool)set_arm_srv.response.success);
  }
  else
  {
    ROS_ERROR("Arm unsuccessful");
    ROS_INFO("Success:%d", (bool)set_arm_srv.response.success);
  }
usleep(3000000);

  if (wp_srv_client.call(wp_push_srv))
  {
    ROS_INFO("Success:%d", (bool)wp_push_srv.response.success);
  }
  else
  {
    ROS_ERROR("Waypoint couldn't been sent");
    ROS_INFO("Success:%d", (bool)wp_push_srv.response.success);
  }

if (set_mode_client.call(set_mode_srv))
{
    ROS_INFO("Success:%d", (bool)set_mode_srv.response.mode_sent);
}
else
{
    ROS_ERROR("Arm unsuccessful");
    ROS_INFO("Success:%d", (bool)set_mode_srv.response.mode_sent);
}


   ros::spinOnce();

  return 0;
}
