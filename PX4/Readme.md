This folder contains all the resources useful for marker detection and its coordinate.
Please follow the given below instructions carefully.

1. Go to Firmware/launch, replace empty.world by plane_cam.world in mavros_posix_sitl.launch and posix_sitl.launch
2. Go to Firmware/Tools/sitl_gazebo/worlds, and replace plane_cam.world there with above plane_cam.world
3. Go to Firmware/Tools/sitl_gazebo/models/plane_cam, and replace plane_cam.sdf there with above plane_cam.sdf
4. Go to Firmware/Tools/sitl_gazebo/models/fpv_cam, and replace fpv_cam.sdf there with above fpv_cam.sdf
5. Go to Firmware/Tools/sitl_gazebo/models, and add above marker folder there.
6. Download broadcaster.py and globalmarker.py into some workspace or folder.
You are all set!!

Steps to run above files:
1. Start your px4 with gazebo by launching mavros_posix_sitl.launch as u do usually.
(A gazebo world is launched with grass plane, runway and a marker. If u want add some more markers.)
2. Run broadcaster.py in another terminal.(This is a tf broadcaster. U can check ur tf tree using 'rosrun tf view_frames')
3. Now run globalmarker.py in another terminal. (As the palne passes over marker its coordinates will be published with 'Marker Found' message)
