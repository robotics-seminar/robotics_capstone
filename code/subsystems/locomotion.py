'''
Locomotion subsystem
'''
class LocomotionSystem(object):
    '''
    Contains locomotion subsystem.
    '''
    def __init__(self):
        self.locomotionData = LocomotionData()

    def updateLocomotion(self, localizationData, pathData):
        """
        Updates the LocomotionData command using the passed in localization
        data and path planning data
        @param localizationData LocalizationData struct
        @param pathData struct containing path planning data
        @return LocomotionData struct
        """
        return self.locomotionData

class LocomotionData(object):
    """
    Contains fields for locomotion data for a single robot
    Locomotion data includes wheel motor commands as well as motor commands
    for the writing implement
    """
    def __init__(self):
      self.motor_command = [0, 0, 0, 0] # TODO rename 'command' more accurately

