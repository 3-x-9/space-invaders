from tkinter import *
import random
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip


class GameState:
    def __init__(self):
        self.window = Tk()

        self.screen_width = self.window.winfo_screenwidth()
        self.screen_height = self.window.winfo_screenheight()

        self.scale_x = self.screen_width / 1550
        self.scale_y = self.screen_height / 820

        self.window.geometry(f"{self.screen_width}x{self.screen_height}")
        self.canvas = Canvas(self.window, width=self.screen_width, height=self.screen_height)

        self.canvas.pack()

        # battleship
        self.battleship_img = self.resize_image("battleship.png", 100, 100)
        # enemy
        self.enemy_img = self.resize_image("enemy.png", 75, 75)
        # targeting enemy
        self.targeting_enemy_img = self.resize_image("targeting_enemy.png", 75, 75)
        # boss enemy
        self.boss_img = self.resize_image("boss_enemy.png", 300, 300)
        # heart
        self.heart_img = self.resize_image("heart.png", 100, 100)
        # background
        self.background_img = self.resize_image("background.png", 1550, 820)
        # bomb
        self.bomb_img = self.resize_image("bomb.png", 50, 50)
        # explosion
        self.explosion_img = self.resize_image("explosion.png", 300, 300)

        self.canvas.create_image(0, 0, anchor="nw", image=self.background_img)

        self.player = Player(self, 600, 650)
        self.enemies = []

        self.after_calls = []

        self.score = 100
        self.lives = 3
        self.game_over = False

        self.multishot_state = False
        self.shot_cooldown = 300
        self.shot_cd_counter = 0

        self.window.bind("<Motion>", self.player.move)
        self.window.bind("<space>", self.player.shoot)

        self.lvl_frame = Frame(self.canvas)

        self.lvl_1 = Button(self.lvl_frame, text="LVL 1", font=("Press Start 2P", 32, "bold"), foreground="white",
                            background="black", command=self.lvl1)
        self.lvl_2 = Button(self.lvl_frame, text="LVL 2", font=("Press Start 2P", 32, "bold"), foreground="white",
                            background="black", command=self.lvl2)
        self.lvl_3 = Button(self.lvl_frame, text="LVL 3", font=("Press Start 2P", 32, "bold"), foreground="white",
                            background="black", command=self.lvl3)
        self.lvl_4 = Button(self.lvl_frame, text="LVL 4", font=("Press Start 2P", 32, "bold"), foreground="white",
                            background="black", command=self.lvl4)
        self.lvl_5 = Button(self.lvl_frame, text="LVL 5", font=("Press Start 2P", 32, "bold"), foreground="white",
                            background="black", command=self.lvl5)

        self.lvl_1.pack()
        self.lvl_2.pack()
        self.lvl_3.pack()
        self.lvl_4.pack()
        self.lvl_5.pack()

        self.upgrade_frame = Frame(self.window)
        self.upgrade_label = Label(self.upgrade_frame, text="UPGRADES", font=("Press Start 2P", 20, "bold"),
                                   foreground="white", background="black", width=10)
        self.multishot_button = Button(self.upgrade_frame, text="Multishot", font=("Press Start 2P", 20, "bold"),
                                       foreground="red", background="black", command=self.multishot, width=10)
        Hovertip(self.multishot_button, "Multishot, Makes u shoot 2 projectiles \n Cost: 50", hover_delay=100)
        self.shot_cd_button = Button(self.upgrade_frame, text="Shot CD", font=("Press Start 2P", 20, "bold"),
                                     foreground="red", background="black", command=self.lower_shot_cd, width=10)
        Hovertip(self.shot_cd_button, "Shot cooldown reduction, Makes u shoot projectiles faster \n Cost: 100 per level"
                 "\n Max lvl 8", hover_delay=100)
        self.buy_heart_button = Button(self.upgrade_frame, text="Buy a HEART", font=("Press Start 2P", 20, "bold"),
                                       foreground="red", background="black", command=self.buy_heart, width=10)
        Hovertip(self.buy_heart_button, "Buy an extra life \n Cost: 150 per Heart \n Max Hearts: 4", hover_delay=100)

        self.upgrade_label.pack()

        self.score_label = Label(self.window, text=f"Score: {self.score}", font=("Press Start 2P", 20, "bold"),
                                 foreground="red", background="black")

        self.multishot_button.pack()
        self.shot_cd_button.pack()
        self.buy_heart_button.pack()

        self.lvl_frame.place(x=0, y=0)

        self.upgrade_frame.place(x=0, y=self.screen_height - 100, anchor="sw")

        self.score_label.place(x=self.screen_width - 50, y=25, anchor="ne")
        self.endgame_label = Label(self.window, foreground="black", background="red", text="YOU LOST",
                                   font=("Arial", 80, "bold"))
        self.endgame_label.place_forget()

        self.canvas.create_line(self.screen_width/10*2, self.screen_height/10*7, self.screen_width/10*8,
                                self.screen_height/10*7, fill="white")
        self.canvas.create_rectangle(self.screen_width/10*2, self.screen_height/10*9, self.screen_width/10*8,
                                     0, outline="white")
        self.update_hearts()

        self.window.mainloop()

    def resize_image(self, path, rel_width, rel_height):
        original_img = Image.open(path)
        width = int(self.canvas.winfo_width() * rel_width)
        height = int(self.canvas.winfo_height() * rel_height)
        resized_img = original_img.resize((width, height))
        return ImageTk.PhotoImage(resized_img)

    def update_score(self, points):
        self.score += points
        self.score_label.config(text=f"SCORE: {self.score}")

    def take_life(self):
        self.lives -= 1
        self.update_hearts()
        if self.lives <= 0:
            self.end_game()

    def end_game(self):
        self.game_over = True
        self.endgame_label.place(x=self.screen_width/3, y=self.screen_height/3)
        for i in self.after_calls:
            self.canvas.after_cancel(i)
        self.canvas.delete("enemy")
        self.canvas.delete("projectile")
        self.score = self.score//2

    def buy_heart(self):
        if self.lives <= 4 and self.score >= 150:
            self.score -= 150
            self.lives += 1
            self.score_label.config(text=f"SCORE:{self.score}")
            self.update_hearts()

    def multishot(self):
        if self.score >= 100 and not self.multishot_state:
            self.score -= 100
            self.multishot_state = True
            self.score_label.config(text=f"SCORE:{self.score}")
            self.multishot_button.config(bg="green")

    def lower_shot_cd(self):
        if self.score >= 100 and self.shot_cooldown > 100:
            self.shot_cd_counter += 1
            self.score -= 100
            self.shot_cooldown -= 25
            self.score_label.config(text=f"SCORE:{self.score}")
            self.shot_cd_button.config(text=f"Shot CD ({self.shot_cd_counter})")

    def spawn_enemy(self, counter):
        if not self.game_over and counter > 0:
            x = random.randint((self.screen_width//10*3), (self.screen_width//10*7))
            enemy = Enemy(self, x, 0)
            self.enemies.append(enemy)
            call = self.canvas.after(500, self.spawn_enemy, counter - 1)
            self.after_calls.append(call)

    def spawn_targeting_enemy(self, counter):
        if not self.game_over and counter > 0:
            x = random.randint((self.screen_width//10*3), (self.screen_width//10*7))
            enemy = TargetingEnemy(self, x, 0)
            self.enemies.append(enemy)
            call = self.canvas.after(500, self.spawn_targeting_enemy, counter - 1)
            self.after_calls.append(call)

    def spawn_boss(self):
        if not self.game_over:
            enemy = BossEnemy(self, 700, 150)
            self.enemies.append(enemy)

    def update_hearts(self):
        self.canvas.delete("hearts")
        for i in range(self.lives):
            self.canvas.create_image(self.screen_width/10*6 + i*self.screen_width/10, self.screen_height/10*8,
                                     image=self.heart_img, tags="hearts")

    def lvl1(self):
            if self.lives < 1:
                self.lives = 2
                self.update_hearts()
            self.clear_canvas()
            self.spawn_enemy(10)

    def lvl2(self):
        if self.score >= 100:
            self.score -= 25
            if self.lives < 1:
                self.lives = 2
                self.update_hearts()
            self.clear_canvas()
            self.spawn_targeting_enemy(10)

    def lvl3(self):
        if self.score >= 100:
            self.score -= 50
            if self.lives < 1:
                self.lives = 2
                self.update_hearts()
            self.clear_canvas()
            self.spawn_enemy(5)
            self.spawn_targeting_enemy(5)

    def lvl4(self):
        if self.score >= 100:
            self.score -= 50
            if self.lives < 1:
                self.lives = 2
                self.update_hearts()
            self.clear_canvas()
            self.spawn_enemy(10)
            self.spawn_targeting_enemy(10)

    def lvl5(self):
        if self.score >= 100:
            self.score -= 100
            if self.lives < 1:
                self.lives = 2
                self.update_hearts()
            self.clear_canvas()
            self.spawn_boss()

    def clear_canvas(self):
        self.game_over = False
        self.canvas.delete("enemy")
        self.canvas.delete("boss_bar")
        for call in self.after_calls:
            self.canvas.after_cancel(call)
        self.after_calls.clear()
        self.enemies.clear()
        self.endgame_label.place_forget()


class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.sprite = self.game.canvas.create_image(self.x, self.y, image=self.game.battleship_img, anchor="center",
                                                    tags="player")
        self.can_shoot = True
        self.canvas = self.game.canvas

    def move(self, event):
        self.x = event.x
        self.y = event.y
        self.game.canvas.coords(self.sprite, self.x, self.y)
        self.check_collision()

    def shoot(self, event):
        if not self.can_shoot:
            return
        if self.game.multishot_state:
            self.can_shoot = False
            Projectile(self.game, self.x + 10, self.y - 20)
            Projectile(self.game, self.x - 10, self.y - 20)
            self.game.window.after(self.game.shot_cooldown, self.reset_cooldown)
        else:
            self.can_shoot = False
            Projectile(self.game, self.x, self.y - 20)
            self.game.window.after(self.game.shot_cooldown, self.reset_cooldown)

    def reset_cooldown(self):
        self.can_shoot = True

    def check_collision(self):
        player_box = self.canvas.bbox(self.sprite)
        for enemy in self.game.enemies:
            if isinstance(enemy, BossEnemy):
                enemy_box = self.canvas.bbox(enemy.sprite)
                if self.is_collision(player_box, enemy_box):
                    self.game.take_life()
                    self.game.update_score(10)
            else:
                enemy_box = self.canvas.bbox(enemy.sprite)
                if self.is_collision(player_box, enemy_box):
                    self.canvas.delete(enemy.sprite)
                    self.game.enemies.remove(enemy)
                    self.game.take_life()
                    self.game.update_score(10)
                    break

    @staticmethod
    def is_collision(box1, box2):
        # box format: [x1, y1, x2, y2]
        if not box1 or not box2:
            return False

        return not (
            box1[2] < box2[0] or  # enemy right < projectile left
            box1[0] > box2[2] or  # enemy left > projectile right
            box1[3] < box2[1] or  # enemy bottom < projectile top
            box1[1] > box2[3]     # enemy top > projectile bottom
        )


class Enemy:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.canvas = self.game.canvas
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.game.enemy_img, anchor="center", tags="enemy")
        self.start()

    def start(self):
        self.move(0)

    def move(self, x):
        if self.game.game_over:
            return
        move_mult = random.randint(1, 10)
        x = 0
        if move_mult == 1:
            x += 5
            self.game.canvas.move(self.sprite, x, 10)
        elif move_mult == 2:
            x -= 5
            self.game.canvas.move(self.sprite, x, 10)
        else:
            self.game.canvas.move(self.sprite, x, 10)

        cords = self.canvas.coords(self.sprite)

        if len(cords) < 1:
            return

        if cords[1] >= self.game.screen_height/10*7:
            self.game.enemies.remove(self)
            self.canvas.delete(self.sprite)
            self.game.take_life()

        elif cords[0] < self.game.screen_width/10*2 or cords[0] > self.game.screen_width//10*8:
            self.game.enemies.remove(self)
            self.canvas.delete(self.sprite)

        else:
            self.canvas.after(50, self.move, x)


class TargetingEnemy(Enemy):
    def __init__(self, game, x, y):
        super().__init__(game, x, y)
        self.canvas.itemconfig(self.sprite, image=self.game.targeting_enemy_img)

    def start(self):
        self.move()

    def move(self):
        if self.game.game_over:
            return

        player_x, player_y = self.canvas.coords(self.game.player.sprite)

        dx = 0
        dy = 10

        if player_x > self.x:
            dx += 10
        elif player_x < self.x:
            dx -= 10
        else:
            dx = 0

        self.canvas.move(self.sprite, dx, dy)
        self.x += dx
        self.y += dy

        cords = self.canvas.coords(self.sprite)
        if len(cords) < 1:
            return

        if cords[1] > self.game.screen_height/10*7:
            self.canvas.delete(self.sprite)
            self.game.enemies.remove(self)
            self.game.take_life()

        elif cords[0] < self.game.screen_width/10*2 or cords[0] > self.game.screen_width//10*8:
            self.game.enemies.remove(self)
            self.canvas.delete(self.sprite)

        else:
            self.canvas.after(50, self.move)


class BossEnemy:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.canvas = self.game.canvas
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.game.boss_img, anchor="center", tags="enemy")
        self.boss_attack = 0
        self.boss_timer = 0
        self.max_health = 40
        self.health = 40
        self.move_boss(0)


    def move_boss(self, dx):
        if not self.canvas.find_withtag(self.sprite):
            return

        prob = random.random()

        dx = dx

        if self.boss_attack < 20:
            self.boss_attack += 1
        if self.boss_attack == 20:
            self.boss_attack = 0
            BossBomb(self.game, self.x, self.y)

        midpoint = 700
        bias_left = False

        self.boss_timer -= 1

        if self.x <= self.game.screen_width/10*2 or self.x >= self.game.screen_width/10*8:
            dx *= -1

        self.x += dx
        if self.boss_timer <= 0:
            if self.x >= midpoint:
                bias_left = True
            if bias_left:
                dx = -7 if prob < 0.75 else 7
            elif not bias_left:
                dx = 7 if prob < 0.75 else -7

            self.boss_timer = random.randint(20, 60)

        self.canvas.move(self.sprite, dx, 0)
        self.draw_hp_bar()
        boss_after_call = self.canvas.after(50, self.move_boss, dx)
        self.game.after_calls.append(boss_after_call)

    def draw_hp_bar(self):
        if self.canvas.find_withtag("boss_bar"):
            self.canvas.delete("boss_bar")

        self.canvas.create_line(self.x - self.max_health/2*(200/self.max_health), self.y - self.game.screen_height/10,
                                self.x + self.max_health/2*(200/self.max_health), self.y - self.game.screen_height/10, fill="red",
                                width=5, tags="boss_bar")
        self.canvas.create_line(self.x - self.max_health/2*(200/self.max_health), self.y - self.game.screen_height/10,
                                self.x - self.max_health/2*(200/self.max_health) + self.health*(200/self.max_health),
                                self.y - self.game.screen_height/10, fill="green", width=5, tags="boss_bar")

    def take_hp(self):
        self.health -= 1
        self.draw_hp_bar()

    def remove_boss(self):
        self.canvas.delete(self.sprite)
        self.game.enemies.remove(self)
        self.game.update_score(300)
        self.canvas.delete("boss_bar")


class BossBomb:
    def __init__(self,game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.canvas = self.game.canvas
        self.sprite = self.canvas.create_image(self.x, self.y, image=self.game.bomb_img, anchor="center", tags="enemy")
        self.game.enemies.append(self)
        self.explosion = None
        self.start()

    def start(self):
        self.move()
    def move(self):
        if not self.canvas.find_withtag(self.sprite):
            return

        self.canvas.move(self.sprite, 0, 30)
        self.y += 30
        cord = self.canvas.coords(self.sprite)
        if cord[1] > self.game.screen_height/10*7:
            self.canvas.delete(self.sprite)
            self.explode()
        else:
            self.check_collision()

    def check_collision(self):
        bomb_box = self.canvas.bbox(self.sprite)
        player_box = self.canvas.bbox(self.game.player.sprite)
        self.game.window.after(30, self.move)
        if self.is_collision(bomb_box, player_box):
            self.canvas.delete(self.sprite)
            self.game.enemies.remove(self)
            self.game.take_life()


    @staticmethod
    def is_collision(box1, box2):
        # box format: [x1, y1, x2, y2]

        return not (
            box1[2] < box2[0] or  # enemy right < projectile left
            box1[0] > box2[2] or  # enemy left > projectile right
            box1[3] < box2[1] or  # enemy bottom < projectile top
            box1[1] > box2[3]     # enemy top > projectile bottom
        )

    def explode(self):
        self.explosion = self.canvas.create_image(self.x, self.y, image=self.game.explosion_img, anchor="center",
                                                  tags="explosion")
        explosion_box = self.canvas.bbox(self.explosion)
        player_box = self.canvas.bbox(self.game.player.sprite)

        if self.is_collision(explosion_box, player_box):
            self.game.take_life()
        self.canvas.after(100, self.delete_explosion)

    def delete_explosion(self):
        self.canvas.delete("explosion")

class Projectile:
    def __init__(self, game, x, y):
        self.game = game
        self.x = x
        self.y = y
        self.canvas = self.game.canvas

        self.sprite = self.game.canvas.create_line(self.x, self.y, self.x, self.y - 20, width=10, fill="white",
                                                   tags="projectile")

        self.move()

    def move(self):
        if not self.canvas.find_withtag(self.sprite):
            return
        self.canvas.move(self.sprite, 0, -30)
        cord = self.canvas.coords(self.sprite)
        if cord[1] < 0:
            self.canvas.delete(self.sprite)
        else:
            self.check_collision()

    def check_collision(self):
        projectile_box = self.canvas.bbox(self.sprite)
        self.game.window.after(30, self.move)
        for enemy in self.game.enemies:

            enemy_box = self.canvas.bbox(enemy.sprite)
            if self.is_collision(projectile_box, enemy_box):
                if isinstance(enemy, BossEnemy):
                    enemy.take_hp()
                    self.canvas.delete(self.sprite)
                    self.game.update_score(10)
                    if enemy.health <= 0:
                        enemy.remove_boss()
                else:
                    self.canvas.delete(self.sprite)
                    self.canvas.delete(enemy.sprite)
                    self.game.enemies.remove(enemy)
                    self.game.update_score(10)
                    break

    @staticmethod
    def is_collision(box1, box2):
        # box format: [x1, y1, x2, y2]

        if not box1 or not box2:
            return False

        return not (
            box1[2] < box2[0] or  # enemy right < projectile left
            box1[0] > box2[2] or  # enemy left > projectile right
            box1[3] < box2[1] or  # enemy bottom < projectile top
            box1[1] > box2[3]     # enemy top > projectile bottom
        )


if __name__ == "__main__":
    GameState()
