import sys
import serial
import serial.tools.list_ports
import threading
import time


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap

from PyQt5.QtWidgets import *
from main_window import Ui_MainWindow as main_window_ui
from serial_port_window import Ui_SerialPortWindow as serial_port_window_ui


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
lock = threading.Lock()


class Serial_Port_App:
    def __init__(self):
        # self.serial_connection_flag = False
        self.ser = None
        # print(self.serial_connection_flag, " init")

    def list_serial_ports(self):
        self.port_list = list(serial.tools.list_ports.comports())
        return self.port_list

    def open_serial_port(self, com_port, baundrate):
        self.ser = serial.Serial(com_port, baundrate)
        # self.serial_connection_flag = True
        # print(self.serial_connection_flag, "open")
        print(self.ser)

    def check_is_ser_open(self):
        if self.ser.isOpen() == True:
            return True
        else:
            return False

    def close_serial_port(self):
        self.ser.close()

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
        self.serial_app = Serial_Port_App()

    def connect_serial(self, com, bd):
        self.serial_app.open_serial_port(com, bd)
        lock.release()

    def check_is_ser_open_1(self):
        return self.serial_app.check_is_ser_open()

    def list_comports(self):
        self.port_list = self.serial_app.list_serial_ports()
        return self.port_list

    def disconnect_serial(self):
        lock.acquire()

        self.serial_app.close_serial_port()

    def read_serial(self):
        # self.serial_app = Serial_Port_App()
        while True:
            with lock:
                # if self.serial_app.serial_connection_flag:
                #    self.serial_app.readSerialData()
                # print("data")
                self.serial_app.readSerialData()
                # print(self.serial_app.serial_connection_flag)
            time.sleep(0.001)


app = App()


class Ser_Port_Window(QMainWindow):
    def __init__(self, parent=None):
        super(Ser_Port_Window, self).__init__(parent)
        self.serial_port_ui = serial_port_window_ui()
        self.serial_port_ui.setupUi(self)

        self.com_list = []
        self.add_port_list()
        self.serial_port_ui.baundrate_combobox.addItems(("115200", "9600"))

        self.serial_port_ui.refresh_bttn.clicked.connect(self.add_port_list)
        self.serial_port_ui.connect_bttn.clicked.connect(self.connect_serial_port)
        self.serial_port_ui.disconnect_bttn.clicked.connect(self.disconnect_serial_port)
        self.serial_port_ui.disconnect_bttn.setEnabled(False)

    def add_port_list(self):
        com_list_tmp = app.list_comports()
        self.serial_port_ui.com_list_combobox.clear()

        for port, desc, hwid in sorted(com_list_tmp):
            self.serial_port_ui.com_list_combobox.addItem(port + " " + desc)
            self.com_list.append(port)

    def connect_serial_port(self):
        self.com_port = self.com_list[
            self.serial_port_ui.com_list_combobox.currentIndex()
        ]
        self.baundrate = (int)(self.serial_port_ui.baundrate_combobox.currentText())

        # try:
        app.connect_serial(str(self.com_port), self.baundrate)

        print(f"Connected to:{str(self.com_port)} / {str(self.baundrate)}")

        self.serial_port_ui.connect_bttn.setEnabled(False)
        self.serial_port_ui.refresh_bttn.setEnabled(False)
        self.serial_port_ui.com_list_combobox.setEnabled(False)
        self.serial_port_ui.baundrate_combobox.setEnabled(False)
        self.serial_port_ui.disconnect_bttn.setEnabled(True)

        # except:
        #    if app.check_is_ser_open_1():
        #        print(f"Already connected to {self.com_port}")
        #    else:
        #        print(f"Can't connect to {self.com_port}")

    def disconnect_serial_port(self):
        app.disconnect_serial()

        print(f"Disconnected from all ports")
        self.serial_port_ui.connect_bttn.setEnabled(True)
        self.serial_port_ui.refresh_bttn.setEnabled(True)
        self.serial_port_ui.com_list_combobox.setEnabled(True)
        self.serial_port_ui.baundrate_combobox.setEnabled(True)
        self.serial_port_ui.disconnect_bttn.setEnabled(False)


class main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.qtui = main_window_ui()
        self.qtui.setupUi(self)
        self.ser_port_window = Ser_Port_Window(self)

        lock.acquire()
        self.qtui.pushButton.clicked.connect(self.openSerialWindow)
        t1 = threading.Thread(target=app.read_serial, args=()).start()

    def openSerialWindow(self):
        self.ser_port_window.show()


q_app = QApplication([])
pencere = main()
pencere.show()
q_app.exec_()
