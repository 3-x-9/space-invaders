import tkinter
import math


def main():
    canvas = tkinter.Canvas(width=800, height=800)
    canvas.config(background="gray")
    canvas.pack()
    get_triangle(canvas, 400, 250, 150, 300, -135)
    canvas.mainloop()


def get_triangle(canvas, x, y, height, width, angle):
    a = (x, y)
    b = (x + width, y)
    z = math.tan(math.radians(angle)) / height

    if angle > 0:
        height = height
    elif angle < 0:
        height = -1 * height
    else:
        return False
    c = (((z ** -1) + x), y - height)
    canvas.create_line(a, b, fill="black")
    canvas.create_line(a, c, fill="blue")
    canvas.create_line(b, c, fill="red")





def letter_t(canvas, x, y, height):
    canvas.create_line(x, y, x, y - height, fill="blue")
    canvas.create_line(x - 50, y - height, x + 50, y - height, fill="blue")


def letter_l(canvas, x, y, height):
    canvas.create_line(x, y, x, y - height, fill="red")
    canvas.create_line(x, y, x + y/4, y, fill="red")


def letter_h(canvas, x, y, height):
    canvas.create_line(x, y, x, y - height, fill="black")
    mid = (y-height/2)
    canvas.create_line(x, mid, x + height/2, mid, fill="black")
    canvas.create_line(x + height/2, y, x + height/2, y - height, fill="black")


def letter_z(canvas, x, y, height):
    canvas.create_line(x, y, x + y / 4, y, fill="green")
    canvas.create_line(x, y, x + y / 4, y - height, fill="green")
    canvas.create_line(x, y - height, x + y / 4, y - height, fill="green")


if __name__ == "__main__":
    main()
