# author: Doğukan Yalçin
import sys
import threading
import time
from pathlib import Path
from tkinter import Tk, Canvas, Button, PhotoImage, Label, filedialog, messagebox
import cv2 as cv2
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import csv
import serial as sr
from PIL import ImageTk, Image, ImageDraw
from matplotlib import pyplot as plt
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import os
import datetime
# 41.027364854682524, 28.884793795314913
# 38.398377, 33.711335
SERIAL_DATA_SIZE = 17


GPS_CSV_FILE_NAME = "payload_coor.csv"
GPS_CSV_ICO = "amogus.png"

GPS2_CSV_FILE_NAME = "rocket_coor.csv"
GPS2_CSV_ICO = "cgcs.png"

# classin icinde fotonun koordinatlari da degistitilecek
GPS_MAP_IMAGE_FILE_NAME = "hisar.jpg"


THREE_D_MODEL_FILE_NAME = "roket.obj"

SERIAL_PORT_NAME = "/dev/tty.usbserial-A50285BI"
SERIAL_BAUD_RATE = 115200


GRAPH_DATA_SIZE = 100
GRAPH_FIGURE_SIZE = (4.5, 2.5)
GRAPH_FIGURE_DPI = 40


# sprintf(free_packet, "YRT,233,%d,%d,%.2f,%.2f,%.2f,%f,%f,%.2f,%f,%f, %f,%d,%d,%d, %.2f,%.2f,%.2f, %.2f,%.2f,%.2f\n",
#         packetNo, rocketState, altitude.pressure, altitude_payload.pressure,rocketGps.altitude,rocketGps.latitude, rocketGps.longitude, payloadGps.altitude, payloadGps.latitude, payloadGps.longitude,
#         velocity.verticalVelocity, (int)angle.roll, (int)angle.pitch, (int)angle.yaw,
#         accel.x, accel.y, accel.z
#         ,maxG, maxAltitude, maxSpeed);


# ======================================================================================================================
# sprintf(free_packet,
#    [0]          [1]           [2]               [3]                        [4]                      [5]                   [6]                            [7]                          [8]                      [9]              [10]             [11]           [12]            [13]            [14]            [15]                   [16]                         [17]                     [18]                   [19]                  [20]              [21]      [22]        [23]           [24]               [25]
# "YRT_TARS,      %d,           %d,              %.2f,                      %.2f,                    %.2f,                 %.2f,                          %.2f,                        %.2f,                    %.2f,            %.2f    ,        %.2f,         %.2f,            %.2f,           %.2f,            %f,                    %f,                         %.2f                     ,%f,                    %f,                   %.2f,             %.2f,     %.2f,       %.2f,          %.2f,             %.2f\n",
#               packetNo,   rocketState,   altitude.pressure,      altitude_payload.pressure,   altitude.altitude,   altitude_payload.altitude,      velocity.verticalVelocity,   altitude.temperature,       accel.x,         accel.y,          accel.z   ,    angle.rol,         angle.pitch,         angle.yaw,   rocketGps.latitude,    rocketGps.longitude   ,    rocketGps.altitude,        payloadGps.latitude,  payloadGps.longitude,  payloadGps.altitude,     maxG,    maxSpeed,  maxAltitude,  parachuteForce,   time.current);
# ======================================================================================================================


class Map(Label):
    points = (0, 0, 0, 0)
    data_path = GPS_CSV_FILE_NAME
    data2_path = GPS2_CSV_FILE_NAME
    map_path = GPS_MAP_IMAGE_FILE_NAME
    map = Image.open(map_path, 'r')
    color = (0, 0, 255)
    color2 = (255, 0, 0)
    width = 8
    img_points = []
    image_height = 0
    image_width = 0
    currentImage = None
    loop_speed = 0
    start_stop = True

    def __init__(self, window, image_height, image_width, place_x1, place_y1, loop_speed):
        self.image_height = image_height
        self.image_width = image_width

        # Yenibosna
        # TLlat = 41.00387
        # TLlong = 28.82462
        # BRlat = 40.99244
        # BRlong = 28.84479
        # self.points = (TLlat, TLlong, BRlat, BRlong)

        # YTU
        # TLlat = 41.035398
        # TLlong = 28.867805
        # BRlat = 41.016772
        # BRlong = 28.909124
        # self.points = (TLlat, TLlong, BRlat, BRlong)

        # VADI 41.028808, 28.882688    --    41.024533, 28.892162

        # HISAR 38.412258, 33.679329 -- 38.390892, 33.729674
        TLlat = 38.412258
        TLlong = 33.679329
        BRlat = 38.390892
        BRlong = 33.729674
        self.points = (TLlat, TLlong, BRlat, BRlong)

        img = ImageTk.PhotoImage(self.map.resize(
            (self.image_width, self.image_height), Image.Resampling.LANCZOS))
        super().__init__(window, image=img, borderwidth=0)
        self.image = img
        self.place(x=place_x1, y=place_y1)
        self.loop_speed = loop_speed

        print("Map initiliazed")

    def scale_to_img(self, lat_lon, h_w):
        old = (self.points[2], self.points[0])
        new = (0, h_w[1])
        y = ((lat_lon[0] - old[0]) * (new[1] - new[0]) /
             (old[1] - old[0])) + new[0]
        old = (self.points[1], self.points[3])
        new = (0, h_w[0])
        x = ((lat_lon[1] - old[0]) * (new[1] - new[0]) /
             (old[1] - old[0])) + new[0]
        return int(x), h_w[1] - int(y)

    def draw(self):
        x1, y1 = (0, 0)
        if not self.start_stop:
            try:
                self.after(500, self.draw)
            except:
                pass
            return None
        data = pd.read_csv(self.data_path, names=[
                           'LATITUDE', 'LONGITUDE'], sep=',')
        gps_data = zip(data['LATITUDE'].values, data['LONGITUDE'].values)
        for d in gps_data:
            try:
                x1, y1 = self.scale_to_img(
                    d, (self.map.size[0], self.map.size[1]))
                self.img_points.append((x1, y1))
            except:
                print("Error: GPS data not valid")

        img_amogus = Image.open(GPS_CSV_ICO, 'r').resize(
            (120, 120)).convert('RGBA')
        combine = self.map.copy()
        draw = ImageDraw.Draw(combine)
        draw.line(self.img_points, fill=self.color, width=self.width)
        combine.paste(img_amogus, (x1 - 60, y1 - 60), img_amogus)

        # draw second gps data
        self.img_points = []
        x1, y1 = (0, 0)
        data2 = pd.read_csv(self.data2_path, names=[
            'LATITUDE', 'LONGITUDE'], sep=',')
        gps_data2 = zip(data2['LATITUDE'].values, data2['LONGITUDE'].values)
        for d in gps_data2:
            try:
                x1, y1 = self.scale_to_img(
                    d, (self.map.size[0], self.map.size[1]))
                self.img_points.append((x1, y1))
            except:
                print("Error: GPS data not valid")

        img_amogus = Image.open(GPS2_CSV_ICO, 'r').resize(
            (120, 120)).convert('RGBA')
        draw = ImageDraw.Draw(combine)
        draw.line(self.img_points, fill=self.color2, width=self.width)
        combine.paste(img_amogus, (x1 - 60, y1 - 60), img_amogus)

        img = ImageTk.PhotoImage(combine.resize(
            (self.image_width, self.image_height)))
        self.configure(image=img)
        self.image = img

        self.img_points.clear()
        try:
            self.after(self.loop_speed, self.draw)
        except:
            pass
        # print("Map drawn")


class GraphForOne(FigureCanvasTkAgg):
    data = np.arange(0, GRAPH_DATA_SIZE, 1)
    x = np.arange(0, GRAPH_DATA_SIZE, 1)
    #fig, ax = plt.subplots(figsize=(3.8, 2.1), dpi=80)
    #ln = ax.plot(0, 0)[0]
    serialData = np.zeros(SERIAL_DATA_SIZE, dtype=np.float32)
    prevValue = np.zeros(1, dtype=np.float32)
    readyToDraw = True

    def __init__(self, window, place_x1, place_y1, data_position, lim_min=0, lim_max=100):
        style.use('dark_background')
        #4 , 2.3 ,80
        self.data = np.arange(0, GRAPH_DATA_SIZE, 1)
        self.fig, self.ax = plt.subplots(
            figsize=GRAPH_FIGURE_SIZE, dpi=GRAPH_FIGURE_DPI)
        self.ax.set_ylim(lim_min, lim_max)
        (self.ln,) = self.ax.plot(self.x, self.data, animated=True)
        self.ln.set_xdata(np.arange(0, len(self.data)))
        self.data_position = data_position
        super().__init__(self.fig, window)
        self.get_tk_widget().place(x=place_x1, y=place_y1)
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=50, blit=True)
        self.cond = True

    def animate(self, i):
        if not self.readyToDraw:
            return self.ln,

        try:
            data_1 = float(self.serialData[self.data_position])

        except Exception as e:
            print("GraphAnimate error / Value not numeric")
            print(e)
            return self.ln

        self.data[0:GRAPH_DATA_SIZE - 1] = self.data[1:GRAPH_DATA_SIZE]
        self.data[GRAPH_DATA_SIZE - 1] = data_1
        self.ln.set_ydata(self.data)
        self.prevValue = data_1
        self.readyToDraw = False
        return self.ln,

    def toggle_pause(self):
        self.cond = not self.cond
        if self.cond:
            self.ani.resume()
        else:
            self.ani.pause()


class GraphForOneGeneric(FigureCanvasTkAgg):
    data = np.arange(0, GRAPH_DATA_SIZE, 1)
    x = np.arange(0, GRAPH_DATA_SIZE, 1)
    #fig, ax = plt.subplots(figsize=(3.8, 2.1), dpi=80)
    #ln = ax.plot(0, 0)[0]
    serialData = np.zeros(SERIAL_DATA_SIZE, dtype=np.float32)
    prevValue = np.zeros(1, dtype=np.float32)
    readyToDraw = True

    def __init__(self, window, place_x1, place_y1, data_position, fig_size, dpi, lim_min=0, lim_max=100):
        style.use('seaborn-muted')
        #4 , 2.3 ,80
        self.data = np.arange(0, GRAPH_DATA_SIZE, 1)

        self.fig, self.ax = plt.subplots(figsize=fig_size, dpi=dpi)
        self.ax.set_ylim(lim_min, lim_max)
        (self.ln,) = self.ax.plot(self.x, self.data, animated=True)
        self.ln.set_xdata(np.arange(0, len(self.data)))
        self.data_position = data_position
        super().__init__(self.fig, window)
        self.get_tk_widget().place(x=place_x1, y=place_y1)
        self.ani = animation.FuncAnimation(
            self.fig, self.animate, interval=50, blit=True)
        self.cond = True

    def animate(self, i):
        if not self.readyToDraw:
            return self.ln,

        try:
            data_1 = float(self.serialData[self.data_position])

        except Exception as e:
            print("GraphAnimate error / Value not numeric")
            print(e)
            return self.ln

        self.data[0:GRAPH_DATA_SIZE - 1] = self.data[1:GRAPH_DATA_SIZE]
        self.data[GRAPH_DATA_SIZE - 1] = data_1
        self.ln.set_ydata(self.data)
        self.prevValue = data_1
        self.readyToDraw = False
        return self.ln,

    def toggle_pause(self):
        self.cond = not self.cond
        if self.cond:
            self.ani.resume()
        else:
            self.ani.pause()


class CSVOperations():

    def __init__(self, file_name, columns):
        self.file_name = file_name
        self.df = pd.DataFrame(columns=columns)
        self.create_file_name_date()
        self.df.to_csv(self.file_name, index=False)

    def create_file_name(self):
        i = 0
        while os.path.exists(f'{self.file_name}{i}.csv'):
            i += 1
        self.file_name = f'{self.file_name}{i}.csv'

    def create_file_name_date(self):
        self.file_name = time.strftime("%Y-%m-%d_%H-%M-%S_serial_log.csv")

    def append_array(self, array):
        with open(self.file_name, 'a') as f:
            writer = csv.writer(f)
            writer.writerow(array)


class App(Tk):

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("./assets")
    serialData = np.zeros(SERIAL_DATA_SIZE, dtype=np.float32)
    logging_start_stop = True
    app_condition = True

    def __init__(self):
        super().__init__()
        self.geometry("1288x694")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)
        threading.Thread(target=self.read_serial).start()
        self.resizable = (False, False)
        self.canvas = Canvas(self, bg="#FFFFFF", height=694,
                             width=1288, bd=0, highlightthickness=0, relief="ridge")
        self.canvas.place(x=0, y=0)

        self.create_widgets()
        self.create_serial_texts()
        self.create_models()
        self.update_serial_texts()

    def read_serial(self):
        while 1:
            try:
                self.ser = sr.Serial(SERIAL_PORT_NAME, SERIAL_BAUD_RATE)

                self.ser.reset_input_buffer()

                break
            except:
                print("Ana serial port acilamadi")
                time.sleep(3.5)

        # while 1:
        #     try:
        #         self.serReff = sr.Serial(
        #             SERIAL_REFF_PORT_NAME, SERIAL_BAUD_RATE, timeout=0.5)
        #         self.serReff.reset_input_buffer()
        #         break
        #     except:
        #         print("Ref serial port acilamadi")
        #         time.sleep(3.5)
        print("Seri okuma başladı")

    # // tlcTime - 4 bytes
    # // obcFlightState - 1 byte
    # // bpcFlightState - 1 byte

    # // obcAltitude - 2 bytes
    # // obcMaxAltitude - 2 bytes
    # // obcPressure - 2 bytes

    # // bpcAltitude - 2 bytes
    # // bpcMaxAltitude - 2 bytes
    # // bpcPressure - 2 bytes

    # // obcAbsG - 4 bytes
    # // obcMaxG - 4 bytes

    # // bpcAbsG - 4 bytes
    # // bpcMaxG - 4 bytes

    # // gps.utc_time - 4 bytes
    # // gps.latitude - 4 bytes
    # // gps.longtitude - 4 bytes

    # // crc - 2 bytes
    # // total - 48 bytes ======================================================================================================================
        serialWriteCSV = CSVOperations("su_anlik_tarihe_gore_yapiyor", ["tlcTime", "obcFlightState", "bpcFlightState", "obcAltitude", "obcMaxAltitude", "obcPressure",
                                       "bpcAltitude", "bpcMaxAltitude", "bpcPressure", "obcAbsG", "obcMaxG", "bpcAbsG", "bpcMaxG", "gps.utc_time", "gps.latitude", "gps.longtitude", "rssi"])

        while self.app_condition:
            try:
                self.serialData = self.ser.readline()[:-1]

                # if self.serialData.decode('latin1').split(",")[0] == "YRT_TARS":
                self.serialData = self.serialData.decode(
                    'latin1').split(",")
                print(self.serialData)
                serialWriteCSV.append_array(self.serialData)
                self.update_serial_texts()
                self.update_models()

                # arayuz paketi pesinden 78 byte alip hakeme gonderiyoruz
                # Bu read fonkun 1sn timeoutu var TEA'dan gelenle senkronize olmasi icin
                # TEA da YRT_TARS gonderdikten sonra 100ms sonra hakem pakti gonder.
                # self.serialData = self.ser.read(78)
                # if len(self.serialData) == 78:
                #     self.serReff.write(self.serialData)

            except Exception as e:
                print(e)
                print("Seri port okunurken hata")
                time.sleep(1.5)

    def update_serial_texts(self):
        if not self.logging_start_stop:
            self.after(500, self.update_serial_texts)
            return

        try:
            self.canvas.itemconfig(self.tlcTimeText, text=self.serialData[0])
            self.canvas.itemconfig(self.utcText, text=self.serialData[13])
            self.canvas.itemconfig(self.bpcStateText, text=self.serialData[2])
            self.canvas.itemconfig(self.obcAltitudeText,
                                   text=self.serialData[3])
            self.canvas.itemconfig(self.bpcAltitudeText,
                                   text=self.serialData[6])
            self.canvas.itemconfig(
                self.gpsLongtitudeText, text=self.serialData[15])
            self.canvas.itemconfig(self.rssiText, text=self.serialData[16])
            self.canvas.itemconfig(self.gpsLatitudeText,
                                   text=self.serialData[14])

            self.canvas.itemconfig(self.bpcPressureText,
                                   text=self.serialData[8])
            self.canvas.itemconfig(self.bpcAbsText, text=self.serialData[11])

            self.canvas.itemconfig(self.obcPressureText,
                                   text=self.serialData[5])
            self.canvas.itemconfig(self.obcAbsText, text=self.serialData[9])

            self.canvas.itemconfig(
                self.obcMaxG_text, text=f'{self.serialData[10]} g')
            self.canvas.itemconfig(self.obcMaxAltitude,
                                   text=f'{self.serialData[4]} m')
            self.canvas.itemconfig(
                self.bpcMaxG, text=f'{self.serialData[12]} g')
            self.canvas.itemconfig(self.bpcMaxAltitude,
                                   text=f'{self.serialData[7]} m')
            self.canvas.itemconfig(self.obcStateText, text=self.serialData[1])

        except Exception as e:
            print(e)
        # self.after(30, self.update_serial_texts)

    def update_models(self):

        # add coordinates to the coordinates.csv
        try:
            coor = [float(self.serialData[14]), float(self.serialData[15])]
            if coor[0] != 0 and coor[1] != 0:
                with open(GPS_CSV_FILE_NAME, "a") as f:
                    writer = csv.writer(f)
                    writer.writerow(coor)
        except Exception as e:
            print("Coordinates values invalid")
            print(e)

        try:
            coor = [38.398377, 33.711335]
            if coor[0] != 0 and coor[1] != 0:
                with open(GPS2_CSV_FILE_NAME, "a") as f:
                    writer = csv.writer(f)
                    writer.writerow(coor)
        except Exception as e:
            print("Coordinates values invalid")
            print(e)

        self.bpcPressGraph.serialData = self.serialData
        self.bpcAbsGraph.serialData = self.serialData
        self.obcPressGraph.serialData = self.serialData
        self.obcAbsGraph.serialData = self.serialData
        self.obcAltitudeGraph.serialData = self.serialData
        self.bpcAltitudeGraph.serialData = self.serialData

        self.bpcPressGraph.readyToDraw = True
        self.bpcAbsGraph.readyToDraw = True
        self.obcPressGraph.readyToDraw = True
        self.obcAbsGraph.readyToDraw = True
        self.obcAltitudeGraph.readyToDraw = True
        self.bpcAltitudeGraph.readyToDraw = True

    def create_models(self):

        # create empty coordinates.csv
        with open(GPS_CSV_FILE_NAME, "w") as f:
            writer = csv.writer(f)

        with open(GPS2_CSV_FILE_NAME, "w") as f:
            writer = csv.writer(f)

        coor = [38.398377, 33.711335]
        if coor[0] != 0 and coor[1] != 0:
            with open(GPS2_CSV_FILE_NAME, "a") as f:
                writer = csv.writer(f)
                writer.writerow(coor)

        self.map = Map(self, image_width=539, image_height=308,
                       place_x1=330, place_y1=20, loop_speed=200)
        self.map.draw()

        self.bpcPressGraph = GraphForOne(self, place_x1=610, place_y1=365,
                                         data_position=8, lim_min=0, lim_max=1100)
        self.bpcAbsGraph = GraphForOne(self, place_x1=340, place_y1=530,
                                       data_position=11, lim_min=-5, lim_max=40)
        self.obcPressGraph = GraphForOne(self, place_x1=610, place_y1=530,
                                         data_position=5, lim_min=0, lim_max=1100)
        self.obcAbsGraph = GraphForOne(self, place_x1=340, place_y1=365,
                                       data_position=9, lim_min=-5, lim_max=40)
        self.obcAltitudeGraph = GraphForOneGeneric(self, place_x1=915, place_y1=20,
                                                   data_position=3, fig_size=(4.65, 4.0), dpi=50, lim_min=-5, lim_max=8500)
        self.bpcAltitudeGraph = GraphForOneGeneric(self, place_x1=915, place_y1=370,
                                                   data_position=6, fig_size=(4.65, 4.0), dpi=50, lim_min=-5, lim_max=8500)

    def start_logging(self):
        if self.logging_start_stop:
            return
        self.logging_start_stop = True

        self.map.start_stop = True

        # self.video.start_stop = True

        self.bpcPressGraph.toggle_pause()
        self.bpcAbsGraph.toggle_pause()
        self.obcPressGraph.toggle_pause()
        self.obcAbsGraph.toggle_pause()
        self.obcAltitudeGraph.toggle_pause()
        self.bpcAltitudeGraph.toggle_pause()

        print("Logging started")

    def stop_logging(self):
        if not self.logging_start_stop:
            return
        self.logging_start_stop = False

        self.map.start_stop = False

        # self.video.start_stop = False

        self.bpcPressGraph.toggle_pause()
        self.bpcAbsGraph.toggle_pause()
        self.obcPressGraph.toggle_pause()
        self.obcAbsGraph.toggle_pause()
        self.obcAltitudeGraph.toggle_pause()
        self.bpcAltitudeGraph.toggle_pause()

        print("Logging stopped")

    def on_close(self):
        self.app_condition = False

        self.ser.close()

        self.destroy()

    def create_serial_texts(self):
        self.tlcTimeText = self.canvas.create_text(
            79.0,
            365.0,
            anchor="nw",
            text="419253",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.utcText = self.canvas.create_text(
            234.0,
            366.0,
            anchor="nw",
            text="123",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.obcStateText = self.canvas.create_text(
            79.0,
            393.0,
            anchor="nw",
            text="01/01/2001",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.bpcStateText = self.canvas.create_text(
            234.0,
            393.0,
            anchor="nw",
            text="01",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.bpcAltitudeText = self.canvas.create_text(
            234.0,
            419.0,
            anchor="nw",
            text="1 Pa",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.obcAltitudeText = self.canvas.create_text(
            79.0,
            419.0,
            anchor="nw",
            text="1 Pa",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.obcPressureText = self.canvas.create_text(
            79.0,
            447.0,
            anchor="nw",
            text="41.027327",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.obcAbsText = self.canvas.create_text(
            79.0,
            475.0,
            anchor="nw",
            text="28.884870",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.gpsLatitudeText = self.canvas.create_text(
            79.0,
            501.0,
            anchor="nw",
            text="500 m",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.rssiText = self.canvas.create_text(
            78.0,
            528.0,
            anchor="nw",
            text="0",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.bpcPressureText = self.canvas.create_text(
            234.0,
            448.0,
            anchor="nw",
            text="41.026830",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.bpcAbsText = self.canvas.create_text(
            234.0,
            474.0,
            anchor="nw",
            text="28.889181",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.gpsLongtitudeText = self.canvas.create_text(
            234.0,
            500.0,
            anchor="nw",
            text="400 m",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.obcMaxG_text = self.canvas.create_text(
            185.0,
            227.0,
            anchor="nw",
            text="2999 m/s^2",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 13 * -1)
        )

        self.obcMaxAltitude = self.canvas.create_text(
            185.0,
            260.0,
            anchor="nw",
            text="2999 m/s",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 13 * -1)
        )

        self.bpcMaxG = self.canvas.create_text(
            184.0,
            293.0,
            anchor="nw",
            text="2999 m",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 13 * -1)
        )

        self.bpcMaxAltitude = self.canvas.create_text(
            185.0,
            326.0,
            anchor="nw",
            text="2999 N",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 13 * -1)
        )

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def create_widgets(self):
        self.canvas.create_rectangle(
            .0,
            .0,
            1288.0,
            696.0,
            fill="#13152D",
            outline="")

        self.image_image_1 = PhotoImage(
            file=self.relative_to_assets("image_1.png"))
        image_1 = self.canvas.create_image(
            115.0,
            349.0,
            image=self.image_image_1
        )

        self.canvas.create_text(
            92.0,
            154.0,
            anchor="nw",
            text="GROUND STATION",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 12 * -1)
        )

        self.image_image_2 = PhotoImage(
            file=self.relative_to_assets("image_2.png"))
        image_2 = self.canvas.create_image(
            151.0,
            54.0,
            image=self.image_image_2
        )

        self.image_image_3 = PhotoImage(
            file=self.relative_to_assets("image_3.png"))
        image_3 = self.canvas.create_image(
            599.0,
            174.0,
            image=self.image_image_3
        )

        self.image_image_4 = PhotoImage(
            file=self.relative_to_assets("image_4.png"))
        image_4 = self.canvas.create_image(
            599.0,
            515.0,
            image=self.image_image_4
        )

        self.image_image_5 = PhotoImage(
            file=self.relative_to_assets("image_5.png"))
        image_5 = self.canvas.create_image(
            1090.0,
            173.0,
            image=self.image_image_5
        )

        self.image_image_6 = PhotoImage(
            file=self.relative_to_assets("image_6.png"))
        image_6 = self.canvas.create_image(
            1090.0,
            515.0,
            image=self.image_image_6
        )

        self.canvas.create_text(
            40.0,
            126.0,
            anchor="nw",
            text="YILDIZ ROCKET TEAM\n",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 20 * -1)
        )

        #self.image_image_10 = PhotoImage(file=self.relative_to_assets("image_10.png"))
        #image_10 = self.canvas.create_image(731.0,438.0,image=self.image_image_10)

        self.image_image_11 = PhotoImage(
            file=self.relative_to_assets("image_11.png"))
        image_11 = self.canvas.create_image(
            151.0,
            59.0,
            image=self.image_image_11
        )

        self.button_image_1 = PhotoImage(
            file=self.relative_to_assets("button_1.png"))
        button_1 = Button(
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        button_1.place(
            x=26.0,
            y=179.0,
            width=121.98065185546875,
            height=32.9384765625
        )

        self.button_image_2 = PhotoImage(
            file=self.relative_to_assets("button_2.png"))
        button_2 = Button(
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        button_2.place(
            x=154.0,
            y=179.0,
            width=121.98001098632812,
            height=32.9384765625
        )

        self.image_image_12 = PhotoImage(
            file=self.relative_to_assets("image_12.png"))
        image_12 = self.canvas.create_image(
            74.0,
            372.0,
            image=self.image_image_12
        )

        image_13 = self.canvas.create_image(
            224.0,
            372.0,
            image=self.image_image_12
        )

        image_14 = self.canvas.create_image(
            74.0,
            399.0,
            image=self.image_image_12
        )

        image_15 = self.canvas.create_image(
            224.0,
            399.0,
            image=self.image_image_12
        )

        image_16 = self.canvas.create_image(
            74.0,
            426.0,
            image=self.image_image_12
        )

        image_17 = self.canvas.create_image(
            224.0,
            426.0,
            image=self.image_image_12
        )

        image_18 = self.canvas.create_image(
            74.0,
            454.0,
            image=self.image_image_12
        )

        image_19 = self.canvas.create_image(
            224.0,
            454.0,
            image=self.image_image_12
        )

        image_20 = self.canvas.create_image(
            74.0,
            480.0,
            image=self.image_image_12
        )

        image_21 = self.canvas.create_image(
            224.0,
            480.0,
            image=self.image_image_12
        )

        image_22 = self.canvas.create_image(
            74.0,
            507.0,
            image=self.image_image_12
        )

        image_23 = self.canvas.create_image(
            224.0,
            507.0,
            image=self.image_image_12
        )

        image_24 = self.canvas.create_image(
            74.0,
            536.0,
            image=self.image_image_12
        )

        # self.button_image_6 = PhotoImage(
        #     file=self.relative_to_assets("button_6.png"))
        # button_6 = Button(
        #     image=self.button_image_6,
        #     borderwidth=0,
        #     highlightthickness=0,
        #     command=lambda: self.connect_satellite(),
        #     relief="flat"
        # )
        # button_6.place(
        #     x=41.948524475097656,
        #     y=170.92539978027344,
        #     width=213.11355590820312,
        #     height=39.0
        # )

        self.canvas.create_text(
            9.0,
            369.0,
            anchor="nw",
            text="TLC TIME:",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 9 * -1)
        )

        self.canvas.create_text(
            158.0,
            367.0,
            anchor="nw",
            text="GPS UTC:",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 9 * -1)
        )

        self.canvas.create_text(
            390.0,
            353.0,
            anchor="nw",
            text="OBC ABSOLUTE G GRAPH",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 10 * -1)
        )

        self.canvas.create_text(
            551.0,
            8.0,
            anchor="nw",
            text="ROCKET LOCATION",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 10 * -1)
        )

        self.canvas.create_text(
            1032.0,
            354.0,
            anchor="nw",
            text="BPC ALTITUDE GRAPH",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 10 * -1)
        )

        self.canvas.create_text(
            651.0,
            354.0,
            anchor="nw",
            text="OBC PRESSURE GRAPH",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 10 * -1)
        )

        self.canvas.create_text(
            390.0,
            516.0,
            anchor="nw",
            text="BPC ABSOLUTE G GRAPH",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 10 * -1)
        )

        self.canvas.create_text(
            648.0,
            515.0,
            anchor="nw",
            text="BPC PRESSURE GRAPH",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 10 * -1)
        )

        self.canvas.create_text(
            9.0,
            421.0,
            anchor="nw",
            text="OBC Altitude:",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 9 * -1)
        )

        self.canvas.create_text(
            158.0,
            421.0,
            anchor="nw",
            text="BPC Altitude:",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 9 * -1)
        )

        self.canvas.create_text(
            9.0,
            394.0,
            anchor="nw",
            text="OBC State:",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 9 * -1)
        )

        self.canvas.create_text(
            158.0,
            395.0,
            anchor="nw",
            text="BPC State:",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 9 * -1)
        )

        #self.image_image_36 = PhotoImage(file=self.relative_to_assets("image_36.png"))
        #image_36 = self.canvas.create_image( 460.0,438.0, image=self.image_image_36 )

        #self.image_image_37 = PhotoImage( file=self.relative_to_assets("image_37.png"))
        #image_37 = self.canvas.create_image( 731.0, 601.0,  image=self.image_image_37)

        #self.image_image_38 = PhotoImage(file=self.relative_to_assets("image_38.png"))
        #image_38 = self.canvas.create_image(460.0, 602.0,image=self.image_image_38 )

        self.canvas.create_text(
            1033.0,
            8.0,
            anchor="nw",
            text="OBC ALTITUDE GRAPH",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 10 * -1)
        )

        self.image_image_13 = PhotoImage(
            file=self.relative_to_assets("image_13.png"))
        image_37 = self.canvas.create_image(
            145.0,
            235.0,
            image=self.image_image_13
        )
        image_38 = self.canvas.create_image(
            145.0,
            268.0,
            image=self.image_image_13
        )
        image_39 = self.canvas.create_image(
            145.0,
            301.0,
            image=self.image_image_13
        )
        image_40 = self.canvas.create_image(
            145.0,
            334.0,
            image=self.image_image_13
        )

        self.canvas.create_text(
            26.0,
            229.0,
            anchor="nw",
            text="OBC MAX G: ",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 11 * -1)
        )

        self.canvas.create_text(
            26.0,
            262.0,
            anchor="nw",
            text="OBC MAX ALTITUDE: ",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 11 * -1)
        )

        self.canvas.create_text(
            26.0,
            295.0,
            anchor="nw",
            text="BPC MAX G: ",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 11 * -1)
        )

        self.canvas.create_text(
            26.0,
            328.0,
            anchor="nw",
            text="BPC MAX ALTIITUDE: ",
            fill="#FFFFFF",
            font=("Inter ExtraBold", 11 * -1)
        )

        self.canvas.create_text(
            9.0,
            444.0,
            anchor="nw",
            text="OBC",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            9.0,
            452.0,
            anchor="nw",
            text="Pressure:",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            9.0,
            472.0,
            anchor="nw",
            text="OBC",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            9.0,
            479.0,
            anchor="nw",
            text="Absolute G:",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            9.0,
            498.0,
            anchor="nw",
            text="GPS",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            9.0,
            506.0,
            anchor="nw",
            text="Latitude:",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            9.0,
            530.0,
            anchor="nw",
            text="RSSI:",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            158.0,
            444.0,
            anchor="nw",
            text="BPC",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            158.0,
            452.0,
            anchor="nw",
            text="Pressure:",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            157.0,
            471.0,
            anchor="nw",
            text="BPC",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            157.0,
            478.0,
            anchor="nw",
            text="Absolute G:",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            157.0,
            497.0,
            anchor="nw",
            text="GPS",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )

        self.canvas.create_text(
            157.0,
            505.0,
            anchor="nw",
            text="Longtitude:",
            fill="#FFFFFF",
            font=("Inter", 9 * -1)
        )


myApp = App()
myApp.protocol("WM_DELETE_WINDOW", myApp.on_close)
myApp.mainloop()
