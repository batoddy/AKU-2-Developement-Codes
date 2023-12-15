import serial
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import time


class SerialApp:
    def __init__(self):
        self.system_time = 0
        self.altitude = 0
        self.pressure = 0
        self.velocity = 0
        self.accel_x = 0
        self.accel_y = 0
        self.accel_z = 0
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
        self.yaw = 0
        self.pitch = 0
        self.roll = 0

    def openSerial(self):
        try:
            self.ser = serial.Serial("COM6", 115200)
            return self.ser
        except:
            print("Port can't opened!!")
            sys.exit()

    def readSerialData(self):
        try:
            self.serial_data = self.ser.readline()[:-1].decode("latin1").split(",")
            self.system_time = self.serial_data[0]
            self.altitude = float(self.serial_data[1])
            self.pressure = float(self.serial_data[2])
            self.velocity = float(self.serial_data[3])
            self.accel_x = float(self.serial_data[4])
            self.accel_y = float(self.serial_data[5])
            self.accel_z = float(self.serial_data[6])
            self.gyro_x = float(self.serial_data[7])
            self.gyro_y = float(self.serial_data[8])
            self.gyro_z = float(self.serial_data[9])
            self.yaw = float(self.serial_data[10])
            self.pitch = float(self.serial_data[11])
            self.roll = float(self.serial_data[12])
            # print(
            #     f"Time: {self.system_time}, Altitude: {self.altitude}, Pressure: {self.pressure}, Velocity: {self.velocity}, Accel_X: {self.accel_x}, Accel_Y: {self.accel_y}, Accel_Z: {self.accel_z}, Gyro_X: {self.gyro_x}, Gyro_Y: {self.gyro_y}, Gyro_Z: {self.gyro_z}, Yaw: {self.yaw}, Pitch: {self.pitch}, Roll: {self.roll}"
            # )

        except:
            print("Can't read data!!!")


class PlotterApp:
    def __init__(self, xData, yData):
        self.x_data = []
        self.y_data = []
        self.x_val = xData
        self.y_val = yData

        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)

    def animate(self, i):
        self.x_data.append(self.x_val)
        self.y_data.append(self.y_val)

        self.x_data = self.x_data[-10:]
        self.y_data = self.y_data[-10:]

        self.ax.clear()
        self.ax.plot(self.x_data, self.y_data)

        self.ax.set_ylim(500, 1500)
        self.ax.set_title("Pressure Plot")
        self.ax.set_ylabel("Pressure")

    def plot(self):
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, frames=100, interval=100, blit=True
        )
        plt.show()


class App:
    def __init__(self):
        SerialApp().openSerial()

    def real_time_plot(self):
        serial_app = SerialApp()
        serial_app.readSerialData(),
        plotter_app = PlotterApp(serial_app.system_time, serial_app.pressure)
        plotter_app.plot()


app = App()
while 1:
    app.real_time_plot()


# fig, ax = plt.subplots(tight_layout=True)
#
# ax.set(xlabel="Time", ylabel="Pressure")
# ax.grid()
# ax.plot()
