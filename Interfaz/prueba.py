from  matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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
    for bloque in eje.patches:
        bloque.remove()
    for lín in eje.lines:
        lín.remove()

    # eje.hist(x, 20, normed=1, histtype='stepfilled', facecolor='g', alpha=0.75)

    x[300:500] = float('NaN')
    eje.plot(x)

    canvas.draw()

button = tk.Button(master=root, text='Cambiar', command=cambiar)
button.pack(side=tk.BOTTOM)

tk.mainloop()
# If you put root.destroy() here, it will cause an error if
# the window is closed with the window manager.