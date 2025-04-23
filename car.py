import tkinter as tk
import random

WIDTH = 600
HEIGHT = 400
LANE_COUNT = 3
ROAD_COLOR = "#222"
LINE_COLOR = "white"
CAR_COLOR = "red"
FPS = 30

class Game:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="green")
        self.canvas.pack()

        self.road_lines = []
        self.speed = 5
        self.car_pos = 1  # Center lane (0=left, 1=center, 2=right)

        # Road perspective setup
        self.road_center = WIDTH // 2
        self.road_width = WIDTH * 0.6
        self.horizon = HEIGHT // 3

        # Car drawing
        self.car = self.canvas.create_polygon(0, 0, 0, 0, 0, 0, fill=CAR_COLOR)

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)

        self.generate_lines()
        self.draw_car()
        self.update()

    def move_left(self, event):
        if self.car_pos > 0:
            self.car_pos -= 1

    def move_right(self, event):
        if self.car_pos < LANE_COUNT - 1:
            self.car_pos += 1

    def generate_lines(self):
        for i in range(20):
            self.road_lines.append({
                "z": i * 20,
            })

    def project(self, z):
        scale = 300 / (z + 1)
        x = self.road_center
        w = self.road_width * scale / 300
        y = HEIGHT - (scale * 1.5)
        return (x - w, y, x + w, y)

    def draw_car(self):
        lane_width = self.road_width / LANE_COUNT
        car_width = 40
        car_height = 60

        # Car is always drawn near bottom of screen
        lane_x = self.road_center - self.road_width/2 + lane_width * self.car_pos + lane_width/2
        x1 = lane_x - car_width/2
        x2 = lane_x + car_width/2
        y1 = HEIGHT - car_height - 20
        y2 = HEIGHT - 20

        self.canvas.coords(self.car, x1, y2, x2, y2, (x1+x2)//2, y1)

    def update(self):
        self.canvas.delete("line")

        for line in self.road_lines:
            line["z"] -= self.speed
            if line["z"] < 1:
                line["z"] += 400  # Reset line to far distance

            x1, y1, x2, y2 = self.project(line["z"])
            self.canvas.create_line(x1, y1, x2, y2, fill=LINE_COLOR, width=2, tags="line")

        self.draw_car()
        self.root.after(int(1000 / FPS), self.update)

root = tk.Tk()
root.title("Pseudo-3D Front POV Car Game")
game = Game(root)
root.mainloop()
