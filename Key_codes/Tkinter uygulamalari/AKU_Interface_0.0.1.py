import tkinter as tk
import serial
import threading
import sys

# -------------Defines------------------------
bg_color = "#1A1A1A"
txt_color = "white"
txt_font = "Courier"

com_port = "COM6"


# -------------Data Set Code---------------
class dataSet:
    def __init__(self, data_set):
        try:
            self.system_time = data_set[0]
            self.altitude = data_set[1]
            self.pressure = data_set[2]
            self.velocity = data_set[3]
            self.temprature = data_set[4]
            self.accel_x = data_set[5]
            self.accel_y = data_set[6]
            self.accel_z = data_set[7]
            self.gyro_x = data_set[8]
            self.gyro_y = data_set[9]
            self.gyro_z = data_set[10]
            self.yaw = data_set[11]
            self.pitch = data_set[12]
            self.roll = data_set[13]
        except:
            print("Data can't be wrote to variables!!")

    def print_to_terminal(self):
        try:
            print(
                f"Time: {self.system_time}, Altitude: {self.altitude}, Pressure: {self.pressure}, Velocity: {self.velocity}, Accel_X: {self.accel_x}, Accel_Y: {self.accel_y}, Accel_Z: {self.accel_z}, Gyro_X: {self.gyro_x}, Gyro_Y: {self.gyro_y}, Gyro_Z: {self.gyro_z}, Yaw: {self.yaw}, Pitch: {self.pitch}, Roll: {self.roll}"
            )
        except:
            print("-------------- Corrupted Data --------------")


# -------------Serial Read Code---------------
def openSerial():
    try:
        ser = serial.Serial(com_port, 115200)
        return ser
    except:
        print(f'{com_port} can"t opened!!! ')
        sys.exit()


def readSerial():
    ser = openSerial()
    data_set = ser.readline()[:-1].decode("latin1").split(",")
    return data_set


# -------------Main GUI code---------------
root = tk.Tk()
root.grid()
root.geometry("1920x1080")
root.state("zoomed")
root.title("AKU Interface")
root.configure(bg=bg_color)


def add_labels():
    # label_list = [flight_state_lbl_2]
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

    # ------------------ Labels ------------------

    # ------------------States & Flags data labels------------------
    flight_state_lbl_1 = tk.Label(
        master=state_flag_data_frame, text="Flight State: ", bg=bg_color, fg=txt_color
    )
    flight_state_lbl_1.config(font=(txt_font, 12))
    flight_state_lbl_1.grid(row=1, column=1, sticky="w")

    flight_state_lbl_2 = tk.Label(
        master=state_flag_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    flight_state_lbl_2.config(font=(txt_font, 12))
    flight_state_lbl_2.grid(row=1, column=2, sticky="w")

    recovery_signal_lbl_1 = tk.Label(
        master=state_flag_data_frame,
        text="Recovery Signal: ",
        bg=bg_color,
        fg=txt_color,
    )
    recovery_signal_lbl_1.config(font=(txt_font, 12))
    recovery_signal_lbl_1.grid(row=2, column=1, sticky="w")

    recovery_signal_lbl_2 = tk.Label(
        master=state_flag_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    recovery_signal_lbl_2.config(font=(txt_font, 12))
    recovery_signal_lbl_2.grid(row=2, column=2, sticky="w")

    stabilization_flag_lbl_1 = tk.Label(
        master=state_flag_data_frame,
        text="Stabilization Flag: ",
        bg=bg_color,
        fg=txt_color,
    )
    stabilization_flag_lbl_1.config(font=(txt_font, 12))
    stabilization_flag_lbl_1.grid(row=3, column=1, sticky="w")

    stabilization_flag_lbl_2 = tk.Label(
        master=state_flag_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    stabilization_flag_lbl_2.config(font=(txt_font, 12))
    stabilization_flag_lbl_2.grid(row=3, column=2, sticky="w")

    # ------------------Time data labels------------------

    system_time_lbl_1 = tk.Label(
        master=time_data_frame, text="System Time: ", bg=bg_color, fg=txt_color
    )
    system_time_lbl_1.config(font=(txt_font, 12))
    system_time_lbl_1.grid(row=1, column=1, sticky="w")

    system_time_lbl_2 = tk.Label(
        master=time_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    system_time_lbl_2.config(font=(txt_font, 12))
    system_time_lbl_2.grid(row=1, column=2, sticky="w")

    Flight_time_l_lbl_1 = tk.Label(
        master=time_data_frame, text="Flight Time: ", bg=bg_color, fg=txt_color
    )
    Flight_time_l_lbl_1.config(font=(txt_font, 12))
    Flight_time_l_lbl_1.grid(row=2, column=1, sticky="w")

    Flight_time_l_lbl_2 = tk.Label(
        master=time_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    Flight_time_l_lbl_2.config(font=(txt_font, 12))
    Flight_time_l_lbl_2.grid(row=2, column=2, sticky="w")

    apogee_time_lbl_1 = tk.Label(
        master=time_data_frame, text="Apogee Time: ", bg=bg_color, fg=txt_color
    )
    apogee_time_lbl_1.config(font=(txt_font, 12))
    apogee_time_lbl_1.grid(row=3, column=1, sticky="w")

    apogee_time_lbl_2 = tk.Label(
        master=time_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    apogee_time_lbl_2.config(font=(txt_font, 12))
    apogee_time_lbl_2.grid(row=3, column=2, sticky="w")

    # ------------------Telemetry data labels------------------

    pkg_no_lbl_1 = tk.Label(
        master=telemetry_data_frame, text="Package No: ", bg=bg_color, fg=txt_color
    )
    pkg_no_lbl_1.config(font=(txt_font, 12))
    pkg_no_lbl_1.grid(row=1, column=1, sticky="w")

    pkg_no_lbl_2 = tk.Label(
        master=telemetry_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    pkg_no_lbl_2.config(font=(txt_font, 12))
    pkg_no_lbl_2.grid(row=1, column=2, sticky="w")

    data_rate_lbl_1 = tk.Label(
        master=telemetry_data_frame, text="Data rate(ms): ", bg=bg_color, fg=txt_color
    )
    data_rate_lbl_1.config(font=(txt_font, 12))
    data_rate_lbl_1.grid(row=2, column=1, sticky="w")

    data_rate_lbl_2 = tk.Label(
        master=telemetry_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    data_rate_lbl_2.config(font=(txt_font, 12))
    data_rate_lbl_2.grid(row=2, column=2, sticky="w")

    # ------------------GPS data labels------------------
    utc_time_lbl_1 = tk.Label(
        master=gps_data_frame, text="UTC Time: ", bg=bg_color, fg=txt_color
    )
    utc_time_lbl_1.config(font=(txt_font, 12))
    utc_time_lbl_1.grid(row=1, column=1, sticky="w")

    utc_time_lbl_2 = tk.Label(
        master=gps_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    utc_time_lbl_2.config(font=(txt_font, 12))
    utc_time_lbl_2.grid(row=1, column=2, sticky="w")

    latitude_lbl_1 = tk.Label(
        master=gps_data_frame, text="Latitude: ", bg=bg_color, fg=txt_color
    )
    latitude_lbl_1.config(font=(txt_font, 12))
    latitude_lbl_1.grid(row=2, column=1, sticky="w")

    latitude_lbl_2 = tk.Label(
        master=gps_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    latitude_lbl_2.config(font=(txt_font, 12))
    latitude_lbl_2.grid(row=2, column=2, sticky="w")

    longtitude_lbl_1 = tk.Label(
        master=gps_data_frame, text="Longtitude: ", bg=bg_color, fg=txt_color
    )
    longtitude_lbl_1.config(font=(txt_font, 12))
    longtitude_lbl_1.grid(row=3, column=1, sticky="w")

    longtitude_lbl_2 = tk.Label(
        master=gps_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    longtitude_lbl_2.config(font=(txt_font, 12))
    longtitude_lbl_2.grid(row=3, column=2, sticky="w")

    # ------------------Flight data labels------------------

    altitude_lbl_1 = tk.Label(
        master=flight_data_frame, text="Altitude: ", bg=bg_color, fg=txt_color
    )
    altitude_lbl_1.config(font=(txt_font, 12))
    altitude_lbl_1.grid(row=1, column=1, sticky="w")

    altitude_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    altitude_lbl_2.config(font=(txt_font, 12))
    altitude_lbl_2.grid(row=1, column=2, sticky="w")

    velocity_lbl_1 = tk.Label(
        master=flight_data_frame, text="Velocirty: ", bg=bg_color, fg=txt_color
    )
    velocity_lbl_1.config(font=(txt_font, 12))
    velocity_lbl_1.grid(row=2, column=1, sticky="w")

    velocity_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    velocity_lbl_2.config(font=(txt_font, 12))
    velocity_lbl_2.grid(row=2, column=2, sticky="w")

    pressure_lbl_1 = tk.Label(
        master=flight_data_frame, text="Pressure: ", bg=bg_color, fg=txt_color
    )
    pressure_lbl_1.config(font=(txt_font, 12))
    pressure_lbl_1.grid(row=3, column=1, sticky="w")

    pressure_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    pressure_lbl_2.config(font=(txt_font, 12))
    pressure_lbl_2.grid(row=3, column=2, sticky="w")

    temprature_lbl_1 = tk.Label(
        master=flight_data_frame, text="Temprature: ", bg=bg_color, fg=txt_color
    )
    temprature_lbl_1.config(font=(txt_font, 12))
    temprature_lbl_1.grid(row=4, column=1, sticky="w")

    temprature_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    temprature_lbl_2.config(font=(txt_font, 12))
    temprature_lbl_2.grid(row=4, column=2, sticky="w")

    accel_x_lbl_1 = tk.Label(
        master=flight_data_frame, text="Accel_x: ", bg=bg_color, fg=txt_color
    )
    accel_x_lbl_1.config(font=(txt_font, 12))
    accel_x_lbl_1.grid(row=5, column=1, sticky="w")

    accel_x_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    accel_x_lbl_2.config(font=(txt_font, 12))
    accel_x_lbl_2.grid(row=5, column=2, sticky="w")

    accel_y_lbl_1 = tk.Label(
        master=flight_data_frame, text="Accel_y: ", bg=bg_color, fg=txt_color
    )
    accel_y_lbl_1.config(font=(txt_font, 12))
    accel_y_lbl_1.grid(row=6, column=1, sticky="w")

    accel_y_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    accel_y_lbl_2.config(font=(txt_font, 12))
    accel_y_lbl_2.grid(row=6, column=2, sticky="w")

    accel_z_lbl_1 = tk.Label(
        master=flight_data_frame, text="Accel_z: ", bg=bg_color, fg=txt_color
    )
    accel_z_lbl_1.config(font=(txt_font, 12))
    accel_z_lbl_1.grid(row=7, column=1, sticky="w")

    accel_z_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    accel_z_lbl_2.config(font=(txt_font, 12))
    accel_z_lbl_2.grid(row=7, column=2, sticky="w")

    yaw_lbl_1 = tk.Label(
        master=flight_data_frame, text="Yaw: ", bg=bg_color, fg=txt_color
    )
    yaw_lbl_1.config(font=(txt_font, 12))
    yaw_lbl_1.grid(row=8, column=1, sticky="w")

    yaw_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    yaw_lbl_2.config(font=(txt_font, 12))
    yaw_lbl_2.grid(row=8, column=2, sticky="w")

    pitch_lbl_1 = tk.Label(
        master=flight_data_frame, text="Pitch: ", bg=bg_color, fg=txt_color
    )
    pitch_lbl_1.config(font=(txt_font, 12))
    pitch_lbl_1.grid(row=9, column=1, sticky="w")

    pitch_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    pitch_lbl_2.config(font=(txt_font, 12))
    pitch_lbl_2.grid(row=9, column=2, sticky="w")

    roll_lbl_1 = tk.Label(
        master=flight_data_frame, text="Roll: ", bg=bg_color, fg=txt_color
    )
    roll_lbl_1.config(font=(txt_font, 12))
    roll_lbl_1.grid(row=10, column=1, sticky="w")

    roll_lbl_2 = tk.Label(
        master=flight_data_frame, text="NaN", bg=bg_color, fg=txt_color
    )
    roll_lbl_2.config(font=(txt_font, 12))
    roll_lbl_2.grid(row=10, column=2, sticky="w")

    # label_list[0] = system_time_lbl_2
    # label_list[1] = altitude_lbl_2
    # label_list[2] = velocity_lbl_2
    # label_list[3] = pressure_lbl_2
    # label_list[4] = temprature_lbl_2
    # label_list[5] = accel_x_lbl_2
    # label_list[6] = accel_y_lbl_2
    # label_list[7] = accel_z_lbl_2
    # label_list[8] = yaw_lbl_2
    # label_list[9] = pitch_lbl_2
    # label_list[10] = roll_lbl_2
    # return label_list


# def update_labels(data_set, label_list):
#    ds = dataSet(data_set)
#
#    label_list[0].configure(text=ds.system_time)
#    label_list[1].configure(text=ds.altitude)
#    label_list[2].configure(text=ds.velocity)
#    label_list[3].configure(text=ds.pressure)
#    label_list[4].configure(text=ds.temprature)
#    label_list[5].configure(text=ds.accel_x)
#    label_list[6].configure(text=ds.accel_y)
#    label_list[7].configure(text=ds.accel_z)
#    label_list[8].configure(text=ds.yaw)
#    label_list[9].configure(text=ds.pitch)
#    label_list[10].configure(text=ds.roll)
#
#    ds.print_to_terminal()


label_list = add_labels()


# def GUI_thread():
#     root.update()


def serial_read_thread():
    data_set = readSerial()
    update_labels(data_set, label_list)


while 1:
    serial_read_thread()
    root.update()
