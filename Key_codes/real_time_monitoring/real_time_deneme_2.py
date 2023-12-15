import serial
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time


class data_setClass:
    system_time = 0
    altitude = 0
    pressure = 0
    velocity = 0
    accel_x = 0
    accel_y = 0
    accel_z = 0
    gyro_x = 0
    gyro_y = 0
    gyro_z = 0
    yaw = 0
    pitch = 0
    roll = 0


data_set = data_setClass()


def openSerial():
    try:
        ser = serial.Serial("COM6", 115200)
        return ser
    except:
        print("Port can't opened!!")
        sys.exit()


def readSerialData(ser):
    try:
        serial_data = ser.readline()[:-1].decode("latin1").split(",")
        data_set.system_time = serial_data[0]
        data_set.altitude = float(serial_data[1])
        data_set.pressure = float(serial_data[2])
        data_set.velocity = float(serial_data[3])
        data_set.accel_x = float(serial_data[4])
        data_set.accel_y = float(serial_data[5])
        data_set.accel_z = float(serial_data[6])
        data_set.gyro_x = float(serial_data[7])
        data_set.gyro_y = float(serial_data[8])
        data_set.gyro_z = float(serial_data[9])
        data_set.yaw = float(serial_data[10])
        data_set.pitch = float(serial_data[11])
        data_set.roll = float(serial_data[12])
        # print(
        #     f"Time: {data_set.system_time}, Altitude: {data_set.altitude}, Pressure: {data_set.pressure}, Velocity: {data_set.velocity}, Accel_X: {data_set.accel_x}, Accel_Y: {data_set.accel_y}, Accel_Z: {data_set.accel_z}, Gyro_X: {data_set.gyro_x}, Gyro_Y: {data_set.gyro_y}, Gyro_Z: {data_set.gyro_z}, Yaw: {data_set.yaw}, Pitch: {data_set.pitch}, Roll: {data_set.roll}"
        # )

    except:
        print("Can't read data!!!")


x_data = []
y_data = []

fig = plt.figure()
ax = fig.add_subplot(111)
plt.show()


def animate(i, x_Data, y_Data):
    ax.clear()
    ax.plot(x_Data, y_Data)

    ax.set_ylim(500, 1500)
    ax.set_title("Pressure Plot")
    ax.set_ylabel("Pressure")


def add_to_lists(x, y, xData, yData):
    xData.append(x)
    yData.append(y)

    xData = xData[-10:]
    yData = yData[-10:]

    return xData, yData


ser = openSerial()
while 1:
    readSerialData(ser)
    x_data, y_data = add_to_lists(
        data_set.system_time, data_set.pressure, x_data, y_data
    )
    ani = animation.FuncAnimation(
        fig, animate, frames=100, fargs=(x_data, y_data), interval=100
    )
    plt.show()


# fig, ax = plt.subplots(tight_layout=True)
#
# ax.set(xlabel="Time", ylabel="Pressure")
# ax.grid()
# ax.plot()
