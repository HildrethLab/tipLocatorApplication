'''
Specific XYZ Stages that will send commands to the XPS system to control stage movement.
'''

# Imports
import tipLocatorStages # Generic stages that will be inherited by XYZ Stages

import XPS_Q8_drivers # Control module for the XPS system

import sys

# Main XYZ Stages class
class XYZStages(tipLocatorStages.stages):
    def __init__(self):
        print('XYZStages initalized')
        # Initializes the stages
        tipLocatorStages.stages.__init__(self)

        # Instance variables that will be defined during the stages initialization in below method
        self._XPSSystem = XPS_Q8_drivers.XPS()
        self._socketID1 = None
        self._socketID2 = None
        self.macroGroup = None
        self.positioner_X = None
        self.positioner_Y = None
        self.positioner_Z = None
        self.stageVelocity = 1.0

    def initalizeStages(self):
        # Checks for potential errors connecting to the XPS System (Code from XPS manufacture)
        def displayErrorAndClose (socketId, errorCode, APIName):
			if (errorCode != -2) and (errorCode != -108):
				[errorCode2, errorString] = self._XPSSystem.ErrorStringGet(socketId, errorCode)
				if (errorCode2 != 0):
					print (APIName + ': ERROR ' + str(errorCode))
				else:
					print (APIName + ': ' + errorString)
			else:
				if (errorCode == -2):
					print (APIName + ': TCP timeout')
				if (errorCode == -108):
					print (APIName + ': The TCP/IP connection was closed by an administrator')
			self._XPSSystem.TCP_CloseSocket(socketId)
			return

        # Creates an instance of the XPS system
        self._XPSSystem = XPS_Q8_drivers.XPS()

        ## Gets the socketIDs for the created system
        # SocketID1 is for initiating stage movements
        self._socketID1 = self._XPSSystem.TCP_ConnectToServer('192.168.0.254',5001,20) # Returns -1 if connection error occurs
        # SocketID2 is for interrupting stage movements
        self._socketID2 = self._XPSSystem.TCP_ConnectToServer('192.168.0.254',5001,21) # Returns -1 if connection error occurs

        # If statements to check to make sure that both sockets were created correctly
        if (self._socketID1 == -1):
            print('Connection to XPS failed, check IP and Port. SocketID1')
            sys.exit()
        if (self._socketID2 == -1):
            print('Connection to XPS failed, check IP and Port. SocketID2')
            sys.exit()

        # Sets up the macro group and the positioners
        self.macroGroup = 'XYZ'
        self.positioner_X = self.macroGroup + '.X'
        self.positioner_Y = self.macroGroup + '.Y'
        self.positioner_Z = self.macroGroup + '.Z'

        # Retrieves the velocity, acceleration and jerk information from the XPS System
        [_stage_X_parameterError, _stage_X_velocty, _stage_X_acceleration, _stage_X_minJerkTime, _stage_X_maxJerkTime] = self._XPSSystem.PositionerSGammaParametersGet(self._socketID1,self.positioner_X)
        [_stage_Y_parameterError, _stage_Y_velocty, _stage_Y_acceleration, _stage_Y_minJerkTime, _stage_Y_maxJerkTime] = self._XPSSystem.PositionerSGammaParametersGet(self._socketID1,self.positioner_Y)
        [_stage_Z_parameterError, _stage_Z_velocty, _stage_Z_acceleration, _stage_Z_minJerkTime, _stage_Z_maxJerkTime] = self._XPSSystem.PositionerSGammaParametersGet(self._socketID1,self.positioner_Z)

        # Updates the velocty, acceleration and jerk parameters for the XPS system (currently we are only changing the velocity and keeping everything else the same)
        self._XPSSystem.PositionerSGammaParametersSet(self._socketID1, self.positioner_X, self.stageVelocity, _stage_X_acceleration, _stage_X_minJerkTime, _stage_X_maxJerkTime)
        self._XPSSystem.PositionerSGammaParametersSet(self._socketID1, self.positioner_Y, self.stageVelocity, _stage_Y_acceleration, _stage_Y_minJerkTime, _stage_Y_maxJerkTime)
        self._XPSSystem.PositionerSGammaParametersSet(self._socketID1, self.positioner_Z, self.stageVelocity, _stage_Z_acceleration, _stage_Z_minJerkTime, _stage_Z_maxJerkTime)

    # Method for moving the stages to an aboslute position
    def moveStageAbsolute(self, direction, location):
        self._XPSSystem.GroupMoveAbsolute(self._socketID1,direction,location)

    # Method for moving the stages a relative distance
    def moveStageRelative(self, direction, distance):
        self._XPSSystem.GroupMoveRelative(self._socketID1,direction,distance)

     # Method for aborting stage movement (aborts all directions)
    def moveStageAbort(self):
        self._XPSSystem.GroupMoveAbort(self._socketID2, self.positioner_X)
        self._XPSSystem.GroupMoveAbort(self._socketID2, self.positioner_Y)
        self._XPSSystem.GroupMoveAbort(self._socketID2, self.positioner_Z)
        self._XPSSystem.GroupMoveAbort(self._socketID2, self.macroGroup)

    # Gets the current location of the stage
    def retrieveStagePostion(self):
        # Gets the current location of each axis of the stage
        [_stagePositionXError, _stagePositionX] = self._XPSSystem.GroupPositionCurrentGet(self._socketID1,self.positioner_X,1)
        [_stagePositionYError, _stagePositionY] = self._XPSSystem.GroupPositionCurrentGet(self._socketID1,self.positioner_Y,1)
        [_stagePositionZError, _stagePositionZ] = self._XPSSystem.GroupPositionCurrentGet(self._socketID1,self.positioner_Z,1)

        # Retruns the locations
        return _stagePositionX, _stagePositionY, _stagePositionZ

    def checkMotionStatus(self):
        # Gets the current motion status of each positioner
        [_stageMotionStatusXError, _stageMotionStatusX] = self._XPSSystem.GroupMotionStatusGet(self._socketID2,self.positioner_X,1)
        [_stageMotionStatusYError, _stageMotionStatusY] = self._XPSSystem.GroupMotionStatusGet(self._socketID2,self.positioner_X,1)
        [_stageMotionStatusZError, _stageMotionStatusZ] = self._XPSSystem.GroupMotionStatusGet(self._socketID2,self.positioner_X,1)
        [_stageMotionStatusError, _stageMotionStatus] = self._XPSSystem.GroupMotionStatusGet(self._socketID2,self.macroGroup,1)
        if _stageMotionStatusX == 0 and _stageMotionStatusY == 0 and _stageMotionStatusZ == 0:
            return 0
        else:
            return 1