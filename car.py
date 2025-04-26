from tkinter import *

canvas = Canvas(width=1200, height=800)

# legs
canvas.create_oval(350, 500, 550, 700)

# body
canvas.create_oval(375, 350, 525, 500)
canvas.create_oval(325, 400, 375, 450)
canvas.create_oval(525, 400, 575, 450)

# head
canvas.create_oval(400, 250, 500, 350)

# dots
for dot in range(6):
    y = 650 - 55*dot
    canvas.create_oval(440, y - 10, 460, y+10, fill="black")

# nose
canvas.create_line(450, 285, 450, 315, fill="red", width=10)

# eyes
canvas.create_oval(425, 265, 440, 280, fill="black")
canvas.create_oval(465, 265, 480, 280, fill="black")

# mouth
canvas.create_oval(425, 325, 475, 340)

# hat
canvas.create_oval(375, 200, 525, 235, width=5)
canvas.create_rectangle(400, 185, 500, 250, fill="black")

# stick
canvas.create_line(575, 700, 575, 325, fill="brown", width=10)

canvas.create_line(575, 325, 550, 275, fill="brown", width=10)
canvas.create_line(575, 325, 600, 275, fill="brown", width=10)
canvas.create_line(575, 325, 575, 275, fill="brown", width=10)

canvas.pack()
canvas.mainloop()

