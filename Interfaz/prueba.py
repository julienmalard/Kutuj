from  matplotlib.figure import Figure
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import tkinter as tk
import numpy as np

root = tk.Tk()
root.wm_title("Embedding in TK")

mu = 200
sigma = 25
x = mu + sigma*np.random.randn(10000)

figura = Figure()
eje = figura.add_subplot(111)
eje.set_title('stepfilled')

# a tk.DrawingArea
canvas = FigureCanvasTkAgg(figura, master=root)
canvas.show()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


def cambiar():
    x = mu + sigma*np.random.randn(10000)
    try:
        eje.patches[0].remove()
    except IndexError:
        pass
    try:
        eje.lines[0].remove()
    except IndexError:
        pass
    eje.hist(x, 20, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)

    canvas.draw()

button = tk.Button(master=root, text='Cambiar', command=cambiar)
button.pack(side=tk.BOTTOM)

tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.