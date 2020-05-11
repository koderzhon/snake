from tkinter import *
import time
import _thread






def func():
    y = 0
    while y != 895:
        c.move(kvadrat, 1, 0)
        time.sleep(0.005)
        y += 1
    _thread.exit()


c = Canvas(width=1000, height=500, bg='grey80')
c.pack()
kvadrat = c.create_rectangle([5, 200], [105, 300], fill="red")

c.tag_bind(kvadrat, '<Button-1>', funkcia)

mainloop()