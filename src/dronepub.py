#!/usr/bin/env python
# license removed for brevity
import roslib
import rospy
import math
import tf
import numpy
from std_msgs.msg import String
from std_msgs.msg import Char
from std_msgs.msg import Empty
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist
from geometry_msgs.msg import Vector3
from nav_msgs.msg import Odometry
from ardrone_autonomy.msg import Navdata
from ar_track_alvar_msgs.msg import AlvarMarkers, AlvarMarker


#Variables initialized
cmd_vel = Twist()
nav_data = Navdata()
imu_data = Imu()
odom = Odometry()
empty=Empty()
ar_data = AlvarMarkers()

cx = 0.0
cy = 0.0
cz = 0.0
markerFlag = 0
statusFlag = 1

def main():
    #Intialize the ROS Node
    rospy.init_node('drone_control', anonymous=True)

    #Publishers Initialized
    vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=10, latch=True)
    takeoff_pub = rospy.Publisher('ardrone/takeoff', Empty, queue_size=1, latch=True)
    land_pub = rospy.Publisher('ardrone/land', Empty, queue_size=1, latch=True)
    reset_pub = rospy.Publisher('ardrone/reset', Empty, queue_size=1, latch=True)
    
    # ar subscribe
    rospy.Subsciber("ar_pose_marker", AlvarMarkers, ar_callback )
    
    #TF listener initialized
    listener = tf.TransformListener()

    #Reset the drone 
    rospy.loginfo("Drone Resetting: Please step away")   
   # reset_pub.publish(empty)
    rospy.sleep(5.0)
    
    #Takeoff the drone first
    rospy.loginfo("Drone taking off")   
   # takeoff_pub.publish(empty)
    rospy.sleep(5.0)


    #The Control loop for navigation
    while not rospy.is_shutdown():
        try:
            (trans,rot) = listener.lookupTransform('ardrone/base_link', 'ardrone/base_frontcam', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        #Subscribers Initialized
        rospy.Subscriber("ardrone/navdata", Navdata, nav_callback)
        rospy.Subscriber("ardrone/odometry", Odometry, odom_callback)
        rospy.Subscriber("ardrone/imu", Imu, imu_callback)
        
        if markerFlag == 0:
            rospy.loginfo("Searching")
            cmd_vel.angular.z  = 0.1
            rospy.loginfo("Rotating")
          #  vel_pub.publish(cmd_vel)
            rospy.sleep(2.0)
        #else:
            
            
        
            
        ## hello_str = "hello world %s" % rospy.get_time()
      #  cmd_vel.linear.x=0.0    
      #  cmd_vel.linear.y=0.0    
      #  cmd_vel.linear.z=0.0    
      #  cmd_vel.angular.x=0.0    
      #  cmd_vel.angular.y=0.0    
      #  cmd_vel.angular.z=0.0    
      #  rospy.loginfo(cmd_vel)
      #  vel_pub.publish(cmd_vel)
      #  rate.sleep(2.0)

      #  cmd_vel.linear.x=0.0    
      #  cmd_vel.linear.y=0.0    
      #  cmd_vel.linear.z=0.0    
      #  cmd_vel.angular.x=0.0    
      #  cmd_vel.angular.y=0.0    
      #  cmd_vel.angular.z=0.0    
      #  rospy.loginfo(cmd_vel)
      #  vel_pub.publish(cmd_vel)
       # rate.sleep(2.0)
      #  takeoff_pub.publish(takeoff)
       # rate.sleep(5.0)
       # land_pub.publish(land)
       # rate.sleep(5.0)
       # rospy.loginfo(rospy.get_caller_id())
def ar_callback(data):
    ar_data = data
    
    if len(ar_data.markers) == 4:
        t0 = ar_data.markers[0].pose.pose.position
        t1 = ar_data.markers[1].pose.pose.position
        t2 = ar_data.markers[2].pose.pose.position
        t3 = ar_data.markers[3].pose.pose.position
        
        cx = (t0.x + t1.x + t2.x + t3.x)/4
        cy = (t0.y + t1.y + t2.y + t3.y)/4
        cz = (t0.z + t1.z + t2.z + t3.z)/4
        
        c = numpy.array([cx, cy, cz])
        c = numpy.dot(c, rot) + trans#might need to adjust
        rospy.loginfo(c)
        
        markerFlag = 1
    else:
        markerFlag= 0

def nav_callback(data):
    nav_data = data

def imu_callback(data):
    imu_data = data

def odom_callback(data):
    odom = data

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass
