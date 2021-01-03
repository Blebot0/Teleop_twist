#!/usr/bin/env python

# Importing the required libraries
import rospy
from std_msgs.msg import Float64, String
import time
import math
import numpy as np
import yaml
from pynput.keyboard import Key, Listener

class Twist_():

    def __init__(self):
        # initializing ros node with name node_sparsh_controller
        rospy.init_node('node_twister_controller')

        # sample rate
        self.sample_rate = 60
        self.speed = 1.707
        self.x = 0
        self.sleep_rate = 0
        # publishers
        self.right_front = rospy.Publisher('/twister/right_front_wheel_to_chassis_controller/command', Float64, queue_size=0)
        self.left_front = rospy.Publisher('/twister/left_front_wheel_to_chassis_controller/command', Float64, queue_size=0)
        self.right_back = rospy.Publisher('/twister/right_back_wheel_to_chassis_controller/command', Float64, queue_size=0)
        self.left_back = rospy.Publisher('/twister/left_back_wheel_to_chassis_controller/command', Float64, queue_size=0)

    def Set_limit(self):
        if self.speed >1.9:
            self.speed = 1.8
        if self.speed < 0.1:
            self.speed = 0.1

    def Control(self):
        self.x += self.speed
        self.right_back.publish(self.x)
        self.left_back.publish(self.x)
        self.right_front.publish(self.x)
        self.left_front.publish(self.x)
        time.sleep(self.sleep_rate)

    def Control_back(self):
        self.x += self.speed
        self.right_back.publish(-self.x)
        self.left_back.publish(-self.x)
        self.right_front.publish(-self.x)
        self.left_front.publish(-self.x)
        time.sleep(self.sleep_rate)

    def Control_left(self):
        self.x += self.speed
        self.right_back.publish(self.x)
        self.left_back.publish(-self.x)
        self.right_front.publish(self.x)
        self.left_front.publish(-self.x)
        time.sleep(self.sleep_rate)

    def Control_right(self):
        self.x += self.speed
        self.right_back.publish(-self.x)
        self.left_back.publish(self.x)
        self.right_front.publish(-self.x)
        self.left_front.publish(self.x)
        time.sleep(self.sleep_rate)
    
    def Speed_Increase(self):
        self.speed += 0.1
        self.Set_limit()
        print("Speed has increased to: {}".format(self.speed))

    def Speed_Decrease(self):
        self.speed -= 0.1
        self.Set_limit()
        print("Speed has decreased to: {}".format(self.speed))




if __name__ == '__main__':
    obj = Twist_()
    r = rospy.Rate(obj.sample_rate)
    print("-------------CONTROLLER DESCRIPTION------------")
    print("    You need to press up key to move in front")
    print("    You need to press down key to move back")
    print("    You need to press left key to move left")
    print("    You need to press right key to move right")
    print("    You need to press 'w' key to increase speed")
    print("    You need to press 's' key to decrease speed")
    print("DISCLAIMER: You would need to press the key for continuous motion.")
    print("The actuations are discrete and wont move continuously")


    while not rospy.is_shutdown():
        def on_press(key):
            if key == Key.up:
                obj.Control()

            elif key == Key.down:
                obj.Control_back()
            
            elif key == Key.left:
                obj.Control_left()

            elif key == Key.right:
                obj.Control_right()   

            elif key.char == ('w'):
                obj.Speed_Increase()
            
            elif key.char == ('s'):
                obj.Speed_Decrease()
        
        def on_release(key):
            if key == Key.esc:
                return False

# Collect events until released
        with Listener(
            on_press=on_press,
            on_release=on_release) as listener:
            listener.join()
        r.sleep()
