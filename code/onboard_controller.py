'''
Main onboard controller.
'''
from __future__ import print_function

import sys
import math
import time

import numpy as np

from messages import robot_commands_pb2
from onboard.robot_communication import RobotCommunication
from onboard.motors import Motors
from utils.geometry import DirectedPoint

from utils.geometry import DirectedPoint


class OnboardController(object):
    def __init__(self, robot_ip):
        '''
        Instantiates main subsystems based on input parameters
        '''
        self.robot_ip = robot_ip
        self.comm = RobotCommunication()
        self.motors = Motors()

    def setup(self):
        self.comm.connectToOffboard()

    def loop(self):
        """
        Main offboard control loop. Listens for protobuf messages from the
        offboard system, parses and runs appropriate motor command.
        """
        print("onboard main loop")
        while(1):
            msg = self.comm.listenForMessage()
            if msg is None:
                continue
            else:
                robot_pos = DirectedPoint(msg.robot_x, msg.robot_y, theta=0)
                target_pos = DirectedPoint(msg.target_x, msg.target_y, theta=0)
                # self.moveMotorsTime(self.getMotorCommands(robot_pos, target_pos))
                

    def moveMotorsTime(command, t):
        """
        Commands all motors using a given command (such as DIR_UPLEFT) for a time
        in seconds.
        @param motors Motors object
        @param command Motor command to run
        @param t Time in seconds to move for
        """
        print("Moving", command, " for", time, " seconds.")
        for i in range(0, 4):
            self.motors.commandMotor(i, command[i])
        time.sleep(t)

        self.motors.stopMotors()
        time.sleep(0.01)

    def getMotorCommands(self, current, target, verbose=1):
        """
        Uses mechanum control equations to compute motor powers for each motor
            to move along a vector between the provided current/target points
        This function does not take into account whether or not the robot has
            reached the target, and does not scale speed based on distance to
            target.

        Motor powers are ordered 1-4, given a robot with motors in the
        following position, and forward defined as:
        #    1 ---- 2     .
        #    |      |    / \
        #    |      |     |
        #    3 ---- 4     |

        # Mecanum Control:
        # https://www.roboteq.com/index.php/component/easyblog/entry/driving-mecanum-wheels-omnidirectional-robots?Itemid=1208
        # This pdf has accurate equations: http://thinktank.wpi.edu/resources/346/ControllingMecanumDrive.pdf

        @param current DirectedPoint of robot current position
        @param target DirectedPoint of robot target position
        @param verbose Prints debugging output
        @return [V1, V2, V3, V4] list of motor powers for each robot
        """
        target_dpt = target - current

        # setup mecanum control params
        # angle to translate at, radians 0-2pi
        target_angle = (math.atan2(target_dpt.y, target_dpt.x)) % (2 * math.pi)
        target_speed = 1.0 # speed robot moves at [-1, 1]
        target_rot_speed = 0.0 # how quickly to change robot orientation [-1, 1]

        if verbose:
            print("Target Angle:", math.degrees(target_angle))

        # Compute motors, 1-4, with forward direction as specified:
        pi4 = math.pi / 4.0
        V1 = target_speed * math.sin(target_angle + pi4) + target_rot_speed
        V2 = target_speed * math.cos(target_angle + pi4) - target_rot_speed
        V3 = target_speed * math.cos(target_angle + pi4) + target_rot_speed
        V4 = target_speed * math.sin(target_angle + pi4) - target_rot_speed

        return self._rescaleMotorPower([V1, V2, V3, V4])

    def _rescaleMotorPower(self, motor_powers):
        """
        Internal function.
        Scales motor powers from the range [-1, 1] to [-255, 255].
        These motor powers can be directly used as inputs to the Motors class
        to move the motors.

        @param motor_powers List of 4 motor powers on the scale [-1, 1]
        @return motor_powers Motor powers rescaled [-255, 255]
        """
        min_scale = -1
        max_scale = 1
        for i in range(0, 4):
            motor_powers[i] = (motor_powers[i] - min_scale) / (max_scale - min_scale)
            motor_powers[i] = int((motor_powers[i] * (255 * 2)) - 255)
        return motor_powers

if __name__ == "__main__":

    controller = OnboardController(robot_ip="0.0.0.0")
    controller.setup()
    controller.loop()

    # TODO create Motors() class and add test targets
    # start_pt = DirectedPoint(0, 0, 0)
    # target_pt = DirectedPoint(0, 1, 0)
    # motor_powers = controller.getMotorCommands(start_pt, target_pt)
    # print(motor_powers)

    # up = controller.getMotorCommands(start_pt, DirectedPoint(0, 1, 0))
    # left = controller.getMotorCommands(start_pt, DirectedPoint(-1, 0, 0))
    # down = controller.getMotorCommands(start_pt, DirectedPoint(0, -1, 0))
    # right = controller.getMotorCommands(start_pt, DirectedPoint(1, 0, 0))

   
    # robotcomm = RobotCommunication()
    # robotcomm.connectToOffboard()
    # while(1):
    #     msg = robotcomm.listenForMessage()
    #     if msg is None:
    #         continue
    #     else:
    #         print msg
    #         break


