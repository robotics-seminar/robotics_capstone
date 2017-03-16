'''
Main offboard controller.
Runs fixed-rate loop that pulls data from subsystems
'''
import sys
import subsystems

class OffboardController(object):
    def __init__(self, robot_ip):
        '''
        Instantiates main subsystems based on input parameters
        '''
        self.robot_ip = robot_ip

        self.sys_planner = subsystems.PlannerSystem()
        self.sys_localization = subsystems.LocalizationSystem()
        self.sys_locomotion = subsystems.LocomotionSystem()
        self.sys_comm = subsystems.CommunicationSystem()
        self.sys_ui = subsystems.UISystem()


    def processInputData(self, data):
        '''
        Receives input image and runs planner
        '''
        paths = self.sys_planner.planTrajectories(data)

    def robotSetup(self):
        '''
        Sets up communication links with robot agents.
        Setup step for drawing loop
        '''
        for i in xrange(0, len(self.robot_ip)):
            success = self.sys_comm.connectToRobot(i, self.robot_ip[i])
            if not success:
                print 'FAILED TO CONNECT TO ROBOT'
                sys.exit(1)


        # TODO connect to camera, ensure valid connection

        # TODO start localization, planner and UI in threads

    def loop(self):
        '''
        Main offboard controller loop
        '''
        while True:
            if self.sys_planner.drawingComplete():
                break


            robot_messages = self.sys_comm.getTCPMessages()
            localization = self.sys_localization.getPositions()

            paths = self.sys_planner.updatePaths(localization)

            locomotion_msg = self.sys_locomotion.generateCommand(localization, paths)
            writing_msg = self.sys_writing.generateCommand(localization, paths)
            error_msg = self.sys_comm.generateErrorCommand()

            self.sys_comm.sendMessage(locomotion_msg, writing_msg, error_msg)

            self.sys_ui.displayInfo(locomotion_msg, writing_msg, error_msg)


    def _test(self):
        pass


if __name__ == "__main__":
    robotIPs = ['111.111.1.1', '222.222.2.2']

    # from messages import robot_commands_pb2
    # import socket

    # commsys = subsystems.CommunicationSystem()
    # commsys.connectToRobot('localhost', 0)
    # commsys.sendTCPMessages()

    loc = subsystems.LocalizationSystem()
    loc.setup()
    loc.loop()


    # serialized = cmd.SerializeToString()

    # commsys = CommunicationSystem()
    # address=('localhost', 5555)
    # buf_size = 1024
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # s.connect(address)
    # s.send(serialized)
    # while 1:
    # 	serialized = s.recv(buf_size)
    # 	data = cmd.ParseFromString(serialized)
    # 	if data is None:
    #         continue
    #     print 'received echo: '
    #     print data

    # s.close()



    # controller = OffboardController(robot_ip=robotIPs)
    # controller.robotSetup()
    # controller.loop()
