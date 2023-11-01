import serial
import sys
from serial.tools import list_ports

comports = serial.tools.list_ports.comports(include_links=False)

for port in comports:
    print(port.device)


def openSerial():
    try:
        ser = serial.Serial("COM6", 115200)
        return ser
    except:
        print("COM Port can't found!!!")
        sys.exit()


def readSerial():
    ser = openSerial()
    serialData = ser.readline()[:-1].decode("latin1").split(",")
    global time
    global altitude
    global pressure
    global velocity
    global accel_x
    global accel_y
    global accel_z
    global gyro_x
    global gyro_y
    global gyro_z
    global yaw
    global pitch
    global roll

    try:
        time = serialData[0]
        altitude = serialData[1]
        pressure = serialData[2]
        velocity = serialData[3]
        accel_x = serialData[4]
        accel_y = serialData[5]
        accel_z = serialData[6]
        gyro_x = serialData[7]
        gyro_y = serialData[8]
        gyro_z = serialData[9]
        yaw = serialData[10]
        pitch = serialData[11]
        roll = serialData[12]
    except:
        print("Corrupted Data !!!")


def printSerial():
    try:
        print(
            f"Time: {time}, Altitude: {altitude}, Pressure: {pressure}, Velocity: {velocity}, Accel_X: {accel_x}, Accel_Y: {accel_y}, Accel_Z: {accel_z}, Gyro_X: {gyro_x}, Gyro_Y: {gyro_y}, Gyro_Z: {gyro_z}, Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}"
        )
    except:
        print("Corrupted Data")


while 1:
    readSerial()
    printSerial()
