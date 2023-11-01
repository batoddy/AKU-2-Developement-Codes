import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style
import serial
import sys

# -------------Defines------------------------
bg_color = "#1A1A1A"
txt_color = "white"
txt_font = "Courier"

com_port = "COM6"

global board_time
global system_time
global flight_time
global apogee_time
global flight_state
global recovery_signal
global stabilization_flag
global data_rate
global pkg_no
global utc_time
global lat
global lng
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
global temperature
global max_Altitude
global base_pressure
global distance_x
global distance_y
global distance_z

system_time = 0
flight_time = 0
apogee_time = 0
flight_state = 0
recovery_signal = 0
stabilization_flag = 0
data_rate = 0
pkg_no = 0
utc_time = 0
lat = 0
lng = 0
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
temperature = 0
max_Altitude = 0
base_pressure = 0
distance_x = 0
distance_y = 0
distance_z = 0
# -------------Main GUI code---------------
root = tk.Tk()
root.grid()
root.geometry("1920x1080")
root.state("zoomed")
root.title("AKU Interface")
root.configure(bg=bg_color)


# -------------Serial Read Code---------------
class serialApp:
    def openSerial():
        try:
            ser = serial.Serial(com_port, 115200)
            return ser
        except:
            print(f'{com_port} can"t opened!!! ')
            sys.exit()

    def readSerial():
        ser = serialApp.openSerial()
        serial_data = ser.readline()[:-1].decode("latin1").split(",")

        try:
            board_time = serial_data[0]
            altitude = serial_data[1]
            pressure = serial_data[2]
            velocity = serial_data[3]
            accel_x = serial_data[4]
            accel_y = serial_data[5]
            accel_z = serial_data[6]
            gyro_x = serial_data[7]
            gyro_y = serial_data[8]
            gyro_z = serial_data[9]
            yaw = serial_data[10]
            pitch = serial_data[11]
            roll = serial_data[12]
        except:
            print("--------------Data couldn't wrote--------------")

    def printSerial():
        try:
            print(
                f"Time: {board_time}, Altitude: {altitude}, Pressure: {pressure}, Velocity: {velocity}, Accel_X: {accel_x}, Accel_Y: {accel_y}, Accel_Z: {accel_z}, Gyro_X: {gyro_x}, Gyro_Y: {gyro_y}, Gyro_Z: {gyro_z}, Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}"
            )
        except:
            print("-------------- Corrupted Data--------------")


# ------------------Label Function------------------
class App_assist:
    global label_list
    global label_variables

    label_list = []
    label_variables = []

    def add_label(
        self,
        text1,
        text2,
        row_,
    ):
        label_1 = tk.Label(self, text=text1, bg=bg_color, fg=txt_color)
        label_1.config(font=(txt_font, 12))
        label_1.grid(row=row_, column=1, sticky="w")

        label_2 = tk.Label(self, text=text2, bg=bg_color, fg=txt_color)
        label_2.config(font=(txt_font, 12))
        label_2.grid(row=row_, column=2, sticky="w")
        label_list.append(label_2)
        label_variables.append(text2)

    # def update_label():
    #     for index in label_list:
    #         index.config(text=label_variables(index))


# ------------------Label frames------------------
state_flag_data_frame = tk.Frame(root, width=300, height=800, bg=bg_color)
state_flag_data_frame.place(x=1500, y=100)

telemetry_data_frame = tk.Frame(root, width=300, height=800, bg=bg_color)
telemetry_data_frame.place(x=1500, y=300)

gps_data_frame = tk.Frame(root, width=300, height=800, bg=bg_color)
gps_data_frame.place(x=1500, y=200)

time_data_frame = tk.Frame(root, width=300, height=800, bg=bg_color)
time_data_frame.place(x=100, y=100)

flight_data_frame = tk.Frame(root, width=300, height=800, bg=bg_color)
flight_data_frame.place(x=100, y=200)

raw_data_flow_frame = tk.Frame(root, width=1720, height=250, bg="grey")
raw_data_flow_frame.place(x=100, y=700)

# ------------------States & Flags data labels------------------
App_assist.add_label(state_flag_data_frame, "Flight State: ", flight_state, 1)

App_assist.add_label(state_flag_data_frame, "Recovery Signal: ", recovery_signal, 2)

App_assist.add_label(
    state_flag_data_frame, "Stabilization Flag: ", stabilization_flag, 3
)

# ------------------Time data labels------------------
App_assist.add_label(time_data_frame, "System Time: ", str(system_time), 1)

App_assist.add_label(time_data_frame, "Flight Time: ", str(flight_time), 2)

App_assist.add_label(time_data_frame, "Apogee Time: ", str(apogee_time), 3)

# ------------------Telemetry data labels------------------
App_assist.add_label(telemetry_data_frame, "Pkg No: ", str(pkg_no), 1)

App_assist.add_label(telemetry_data_frame, "Data rate (ms): ", str(data_rate), 2)

# ------------------GPS data labels------------------
App_assist.add_label(gps_data_frame, "UTC Time: ", utc_time, 1)

App_assist.add_label(gps_data_frame, "LATITUDE: ", str(lat), 2)

App_assist.add_label(gps_data_frame, "LONGTITUDE: ", str(lng), 3)

# ------------------Flight data labels------------------
App_assist.add_label(flight_data_frame, "Altitude: ", str(altitude), 1)
App_assist.add_label(flight_data_frame, "Velocity ", str(velocity), 2)
App_assist.add_label(flight_data_frame, "Pressure ", str(pressure), 3)
App_assist.add_label(flight_data_frame, "Temperature ", str(temperature), 4)

App_assist.add_label(flight_data_frame, "Accel_X: ", str(accel_x), 5)
App_assist.add_label(flight_data_frame, "Accel_Y: ", str(accel_y), 6)
App_assist.add_label(flight_data_frame, "Accel_Z: ", str(accel_z), 7)

App_assist.add_label(flight_data_frame, "Yaw: ", str(yaw), 8)
App_assist.add_label(flight_data_frame, "Pitch: ", str(pitch), 9)
App_assist.add_label(flight_data_frame, "Roll: ", str(roll), 10)

App_assist.add_label(flight_data_frame, "Distance_X: ", str(distance_x), 11)
App_assist.add_label(flight_data_frame, "Distance_Y: ", str(distance_y), 12)
App_assist.add_label(flight_data_frame, "Distance_Z: ", str(distance_z), 13)

serialApp.openSerial()

while 1:
    serialApp.readSerial()
    serialApp.printSerial()

    # App_assist.update_label()
    root.mainloop()
