import serial
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

DATA_SIZE = 20


class dataSetClass:
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


data_set = dataSetClass()


class SerialApp:
    def openSerial(self):
        try:
            self.ser = serial.Serial("COM6", 115200)
            return self.ser
        except:
            print("Port can't connected!!")
            self.user_input = input("Press [C] to try again: ")
            if self.user_input == "c" or self.user_input == "C":
                self.openSerial()
            else:
                sys.exit()

    def readSerialData(self):
        try:
            self.ser = self.openSerial()
            self.serial_data = self.ser.readline()[:-1].decode("latin1").split(",")
            data_set.system_time = float(self.serial_data[0])
            data_set.altitude = float(self.serial_data[1])
            data_set.pressure = float(self.serial_data[2])
            data_set.velocity = float(self.serial_data[3])
            data_set.accel_x = float(self.serial_data[4])
            data_set.accel_y = float(self.serial_data[5])
            data_set.accel_z = float(self.serial_data[6])
            data_set.gyro_x = float(self.serial_data[7])
            data_set.gyro_y = float(self.serial_data[8])
            data_set.gyro_z = float(self.serial_data[9])
            data_set.yaw = float(self.serial_data[10])
            data_set.pitch = float(self.serial_data[11])
            data_set.roll = float(self.serial_data[12])

            print(self.serial_data)
        except:
            print("Data can't read clearly!!")


class plotterApp:
    def __init__(self):
        self.xData = []
        self.yData = []

        self.fig, self.ax = plt.subplots(figsize=(5, 5), dpi=80)
        self.aim()

    def aim(self):
        self.ax.plot(self.xData, self.yData)

        self.ani = animation.FuncAnimation(self.fig, self.animate, interval=50)

    def animate(self, i):
        self.xData.append(data_set.system_time)
        self.yData.append(data_set.pressure)

        self.xData = self.xData[-DATA_SIZE:]
        self.yData = self.yData[-DATA_SIZE:]
        self.ax.plot(self.xData, self.yData)
        
        


class App:
    def read_n_plot(self):
        ser_app = SerialApp()
        ser_app.readSerialData()
        plot_app = plotterApp()
        plot_app.aim()
        plt.show()


myApp = App()
while 1:
    myApp.read_n_plot()
