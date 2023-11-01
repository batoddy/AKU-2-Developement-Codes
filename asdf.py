import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

df = pd.read_csv("AKU1_flight_Data.csv")

x = "Time"

fig, axes = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))

axes.plot(df[x], df["Altitude"],label="Altitude")

axes.legend()

main_window = tk.Tk()

line_graph1 = FigureCanvasTkAgg(fig, main_window)
line_graph1.get_tk_widget().pack()

#plt.show()

main_window.mainloop()


