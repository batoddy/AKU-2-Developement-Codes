import serial
import sys
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import time

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QThread
from pyQT_deneme_1 import Ui_MainWindow

DATA_SIZE = 200


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
    def __init__(self):
        try:
            self.ser = serial.Serial("COM6", 115200)
        except:
            print("Port can't opened!!!")
            sys.exit()

    def readSerialData(self):
        try:
            self.serial_data = self.ser.readline()[:-1].decode("latin1").split(",")
            data_set.system_time = int(self.serial_data[0])
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
            print("Data fail!")


class App:
    def __init__(self):
        self.serial_app = SerialApp()

    def read_serial(self):
        while True:
            self.serial_app.readSerialData()
            time.sleep(0.001)

    def update_label_text(self):
        while True:
            # print("label update")
            pass


class main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.qtui = Ui_MainWindow()
        self.qtui.setupUi(self)
        self.app = App()
        t1 = threading.Thread(target=self.app.read_serial, args=()).start()
        t2 = threading.Thread(target=self.update_label_text, args=()).start()

    def update_label_text(self):
        while True:
            self.qtui.sys_tim_lbl.setText(str(data_set.system_time))
            self.qtui.altitude_label.setText(str(data_set.altitude))
            self.qtui.pressure_label.setText(str(data_set.pressure))
            self.qtui.velocity_label_4.setText(str(data_set.velocity))
            self.qtui.acc_x_label.setText(str(data_set.accel_x))
            self.qtui.acc_y_label.setText(str(data_set.accel_y))
            self.qtui.acc_z_label.setText(str(data_set.accel_z))
            self.qtui.yaw_label_4.setText(str(data_set.yaw))
            self.qtui.pitch_label_5.setText(str(data_set.pitch))
            self.qtui.roll_label_6.setText(str(data_set.roll))
            time.sleep(0.001)


q_app = QApplication([])
pencere = main()

pencere.show()
q_app.exec_()
