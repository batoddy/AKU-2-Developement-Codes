import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

# Create a figure and axis
fig, ax = plt.subplots()
x_data = np.linspace(0, 2 * np.pi, 100)
y_data = np.sin(x_data)
(line,) = ax.plot(x_data, y_data)


# Function to update the graph for each frame of the animation
def update(frame):
    line.set_ydata(np.sin(x_data + frame * 0.1))
    return (line,)


# Create the animation
ani = FuncAnimation(fig, update, frames=range(100), blit=True)

plt.show()
