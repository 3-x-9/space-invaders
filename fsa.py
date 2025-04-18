import random
from tkinter import *
from tkinter import messagebox
import time


window = Tk()
global count

window.config(background="black"

              )
image = PhotoImage(file="Figure_1.png")

"""label = Label(window,
              text="Hello",
              font=("Arial", 40, "bold"),
              foreground="White",
              background="DarkRed",
              relief=SUNKEN,
              bd=10,
              padx=20,
              pady=20,
              image=image,
              compound="bottom"

"""

"""#label.pack()
count = 0

def click():
    global count
    count += 1

button = Button(window,
                text=count,
                command=click,
                font=("Arial", 30, "bold"),
                background="black",
                foreground="blue",
                image=image,
                compound="bottom"
"""


"""x = IntVar

entry = Entry(window,
              font=("Arial", 20, "bold"),
              show="-"
              )
entry.pack(side=LEFT)


def submit():
    print("Hello " + entry.get())
    delete()


submit_button = Button(window,
                text="Submit",
                font=("Arial", 20, "bold"),
                command=submit)
submit_button.pack(side=RIGHT)


def delete():
    entry.delete(0, END)

delete_button = Button(window,
                text="Delete",
                font=("Arial", 20, "bold"),
                command=delete)
delete_button.pack(side=RIGHT)


def show_password():
    return "*" if x == 1 else False


check_box = Checkbutton(window,
                        text="show password",
                        font=("Arial", 10, "italic"),
                        variable=x,
                        onvalue=1,
                        offvalue=0,
                        command=show_password


                        )
check_box.pack(side="right")
"""

"""foods = ["pizza", "burger", "hotdog"]

x = StringVar()

def order():
    for food in foods:
        if x.get() == food:
            print("you ordered " + food )

for i in foods:
    radio_button = Radiobutton(window,
                               text=i,
                               foreground="black",
                               font=("Arial", 40),
                               variable=x,
                               value=i,
                               command=order,

                               compound="left",
                               width=7,
                               indicatoron=0

                               )
    radio_button.pack(anchor=W)

"""



def click():
    for x in range(10):
        new_window = Toplevel()



button = Button(window, text="click", command=click)
button.pack()

window.mainloop()







