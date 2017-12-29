# Updated version

import bluetooth
import threading

BUFFSIZE = 1024


# Library of command
def listOfCommand(command):
    return {
        "ACK4S": 0,
        "ACK4C": 1,
        "UP": 2,
        "DOWN": 3,
        "LEFT": 4,
        "RIGHT": 5,
        "STOP": 6,
        "QUIT": 98
    }.get(command, 99)  # default will be WAIT


def messageHandler(connection, message, robot):
    # return:   True to keep the loop
    #           False to exit the loop
    # Error detection:
    if listOfCommand(message) == 99:
        print("Received error message, need send back new command!")
        return True
    # Else there is no error:
    else:
        # Quit when server decide to quit
        if message == "QUIT":
            return False
        else:
            # Else follow the command
            # Any command for the car will be modified here

            # Going up
            if listOfCommand(message) == 2:
                print("Go forward")
                robot.command('fwdDelta')

            # Going back
            elif listOfCommand(message) == 3:
                print("Go back")
            
            # Turn left
            elif listOfCommand(message) == 4:
                print("Turn left")

            # Turn right
            elif listOfCommand(message) == 5:
                print("Turn right")
                robot.command('fwdRTurn')

            # STOP
            elif listOfCommand(message) == 6:
                print("Stop the car!")


            # Send back when the car finish they go:
            dataSendBack = robot.status()
            connection.send(dataSendBack)
            return True


class communication_thread(threading.Thread):
    def __init__(self, serverAddress,robot):
        threading.Thread.__init__(self)
        self.serverAddress = serverAddress
        self.robot=robot ## Adds the robot to queue up comands
        self.port = 15
        self.serverConnection = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

    def connectToServer(self):
        # Establish connection between server and client
        self.serverConnection.connect((self.serverAddress, self.port))
        self.clientRecvData = self.serverConnection.recv(BUFFSIZE).decode("utf-8")
        self.communicate()

    def communicate(self):
        if listOfCommand(self.clientRecvData) == 0:
            self.serverConnection.send("ACK4C")
            print("Connection established")

            listening = True
            while listening:
                # Keep listening to Server
                self.clientRecvData = self.serverConnection.recv(BUFFSIZE).decode("utf-8")
                listening = messageHandler(self.serverConnection, self.clientRecvData, self.robot)



                ## Do the simulation wait here (countdown the count until it reach 0):
                #while count >0:

                #    listening

        print("Cut connection")
        self.robot.command('terminate')
        self.serverConnection.close()

    def run(self):
        print("Start the communication with server")
        # while self.running:
        self.connectToServer()
