import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import style

# ---Dummy Datas---
system_time = 110021
flight_time = 1201
apogee_time = 4501

flight_state = "AFTER LIFTOFF"
recovery_signal = "FALSE"
stabilization_flag = "STABLE"

data_rate = 172
pkg_no = 75

utc_time = "15.12.34"
lat = 28.456776
lng = 22.154748

altitude = 102.7485748
velocity = 14.577486
pressure = 1013.78
temprature = 25.5

max_Altitude = 166.330078
base_pressure = 1010.54

accel_x = 1.457865
accel_y = 2.784915
accel_z = 4.125746


distance_x = 1.152454
distance_y = 2.457452
distance_z = 1.154713

yaw = 170
pitch = 120
roll = 10
# -------------Defines---------------
bg_color = "#1A1A1A"
txt_color = "white"
txt_font = "Courier"
# -------------Get Data code---------------
df = pd.read_csv("AKU1_flight_Data.csv")
# -------------Main GUI code---------------
root = tk.Tk()
root.grid()
root.geometry("1920x1080")
root.state("zoomed")
root.title("AKU Interface")
root.configure(bg=bg_color)

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

# ------------------Plotter frames------------------
altitude_plot_frame = tk.Frame(root, bg="white")
altitude_plot_frame.place(x=400, y=50)

velocity_plot_frame = tk.Frame(root, bg="white")
velocity_plot_frame.place(x=900, y=50)

altitude2_plot_frame = tk.Frame(root, bg="white")
altitude2_plot_frame.place(x=400, y=350)

velocity2_plot_frame = tk.Frame(root, bg="white")
velocity2_plot_frame.place(x=900, y=350)


# ------------------Label Function------------------
class App:
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


# ------------------States & Flags data labels------------------
App.add_label(state_flag_data_frame, "Flight State: ", flight_state, 1)

App.add_label(state_flag_data_frame, "Recovery Signal: ", recovery_signal, 2)

App.add_label(state_flag_data_frame, "Stabilization Flag: ", stabilization_flag, 3)

# ------------------Time data labels------------------
App.add_label(time_data_frame, "System Time: ", str(system_time), 1)

App.add_label(time_data_frame, "Flight Time: ", str(flight_time), 2)

App.add_label(time_data_frame, "Apogee Time: ", str(apogee_time), 3)

# ------------------Telemetry data labels------------------
App.add_label(telemetry_data_frame, "Pkg No: ", str(pkg_no), 1)

App.add_label(telemetry_data_frame, "Data rate (ms): ", str(data_rate), 2)

# ------------------GPS data labels------------------
App.add_label(gps_data_frame, "UTC Time: ", utc_time, 1)

App.add_label(gps_data_frame, "LATITUDE: ", str(lat), 2)

App.add_label(gps_data_frame, "LONGTITUDE: ", str(lng), 3)

# ------------------Flight data labels------------------
App.add_label(flight_data_frame, "Altitude: ", str(altitude), 1)
App.add_label(flight_data_frame, "Velocity ", str(velocity), 2)
App.add_label(flight_data_frame, "Pressure ", str(pressure), 3)
App.add_label(flight_data_frame, "Temprature ", str(temprature), 4)

App.add_label(flight_data_frame, "Accel_X: ", str(accel_x), 5)
App.add_label(flight_data_frame, "Accel_Y: ", str(accel_y), 6)
App.add_label(flight_data_frame, "Accel_Z: ", str(accel_z), 7)

App.add_label(flight_data_frame, "Yaw: ", str(yaw), 8)
App.add_label(flight_data_frame, "Pitch: ", str(pitch), 9)
App.add_label(flight_data_frame, "Roll: ", str(roll), 10)

App.add_label(flight_data_frame, "Distance_X: ", str(distance_x), 11)
App.add_label(flight_data_frame, "Distance_Y: ", str(distance_y), 12)
App.add_label(flight_data_frame, "Distance_Z: ", str(distance_z), 13)

# accZ_plot_frame = tk.Frame(root, bg="white")
# accZ_plot_frame.place(x=10, y=10)

# alt_lbl_txt = "Altitude: " + str(altitude)
# alt_label = tk.Label(data_frame, text=alt_lbl_txt, bg="black", fg="white")
# alt_label.config(font=("Courier", 12))
# alt_label.grid(row=1, column=1, sticky="w")
#
#
# max_alt_lbl_txt = "Max Altitude: " + str(max_Altitude)
# max_alt_label = tk.Label(data_frame, text=max_alt_lbl_txt, bg="black", fg="white")
# max_alt_label.config(font=("Courier", 12))
# max_alt_label.grid(row=2, column=1, sticky="w")
#
# max_alt_lbl_txt = "Yaw: " + str(max_Altitude)
# max_alt_label = tk.Label(data_frame, text=max_alt_lbl_txt, bg="black", fg="white")
# max_alt_label.config(font=("Courier", 12))
# max_alt_label.grid(row=3, column=1, sticky="w")
#
# max_alt_lbl_txt = "Pitch: " + str(max_Altitude)
# max_alt_label = tk.Label(data_frame, text=max_alt_lbl_txt, bg="black", fg="white")
# max_alt_label.config(font=("Courier", 12))
# max_alt_label.grid(row=4, column=1, sticky="w")
#
# max_alt_lbl_txt = "Roll: " + str(max_Altitude)
# max_alt_label = tk.Label(data_frame, text=max_alt_lbl_txt, bg="black", fg="white")
# max_alt_label.config(font=("Courier", 12))
# max_alt_label.grid(row=5, column=1, sticky="w")

plt.style.use("dark_background")

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 3), facecolor=bg_color)

# fig.set_facecolor("black")
ax.plot(df["Time"], df["Altitude"], label="Altitude", color="orange")

ax.grid()
ax.set_title("Altitude")
ax.set_facecolor(bg_color)
ax.set_xlabel("Time (sn)")
ax.set_ylabel("Altitude (mt)")

# ax[1].plot(df["Time"], df["Altitude"],label="Altitude")
# ax[2].plot(df["Time"], df["Altitude"],label="Altitude")

# label = tk.Label(text = "DENEME 1")
# label.config(font=("Courier", 16))
# label.pack()

canvas = FigureCanvasTkAgg(fig, master=altitude_plot_frame)
canvas.draw()
canvas.get_tk_widget().pack()

canvas2 = FigureCanvasTkAgg(fig, master=velocity_plot_frame)
canvas2.draw()
canvas2.get_tk_widget().pack()

canvas3 = FigureCanvasTkAgg(fig, master=altitude2_plot_frame)
canvas3.draw()
canvas3.get_tk_widget().pack()

canvas4 = FigureCanvasTkAgg(fig, master=velocity2_plot_frame)
canvas4.draw()
canvas4.get_tk_widget().pack()


# scrolled_text = ScrolledText(master = raw_data_flow_frame)
# i = 0
# i += 1
# scrolled_text.insert(tk.INSERT, str(i))
# scrolled_text.pack(fill=tk.BOTH)


root.mainloop()
