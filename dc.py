from tkinter import *
import random
from PIL import Image, ImageTk
from idlelib.tooltip import Hovertip

window_width = 1200
window_height = 720
endgame_label = None
score_label_obj = None
game_over = False
score = 0
multishot_state = False
multishot_button = None

battleship_sprite = None
enemy_sprite = None
enemy_sprites = []

can_shoot = True
shot_cd = 300
shot_cd_lvl = 0


def main():
    global window, canvas, multishot_button, battleship, enemy_alien, shot_cd_button
    game_over = False

    window = Tk()
    canvas = Canvas(window, width=1550, height=820)

    # battleship
    original_img = Image.open("img.png")
    resized_img = original_img.resize((100, 100))
    battleship = ImageTk.PhotoImage(resized_img)

    # enemy
    original_img = Image.open("img_1.png")
    resized_img = original_img.resize((50, 50))  # ← change size as needed
    enemy_alien = ImageTk.PhotoImage(resized_img)

    window.config(bg="black")
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{screen_width}x{screen_height}")

    window.bind("<Motion>", player_pos)
    window.bind("<space>", shoot)

    lvl_frame = Frame(window)

    lvl_1 = Button(lvl_frame, text="LVL 1", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl1)
    lvl_2 = Button(lvl_frame, text="LVL 2", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl2)
    lvl_3 = Button(lvl_frame, text="LVL 3", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl3)
    lvl_4 = Button(lvl_frame, text="LVL 4", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl4)

    lvl_1.pack()
    lvl_2.pack()
    lvl_3.pack()
    lvl_4.pack()

    upgrade_frame = Frame(window)
    upgrade_label = Label(upgrade_frame, text="UPGRADES", font=("Press Start 2P", 20, "bold"), foreground="white",
                        background="black", width=10)
    multishot_button = Button(upgrade_frame, text="Multishot", font=("Press Start 2P", 20, "bold"), foreground="red",
                              background="black", command=multishot, width=10)
    Hovertip(multishot_button, "Multishot, Makes u shoot 2 projectiles \n Cost: 50", hover_delay=200)
    shot_cd_button = Button(upgrade_frame, text="shot cd", font=("Press Start 2P", 20, "bold"), foreground="red",
                              background="black", command=lower_shot_cd, width=10)
    Hovertip(shot_cd_button, "Shot cooldown reduction, Makes u shoot projectiles faster \n Cost: 100 per level", hover_delay=200)

    upgrade_label.pack()

    multishot_button.pack()
    shot_cd_button.pack()

    canvas.create_line(200, 550, 1200, 550)
    canvas.create_rectangle(200, 2, 1200, 720)
    # 1200, 720

    upgrade_frame.place(x=0, y=500)
    canvas.pack()
    lvl_frame.place(x=0, y=0)
    window.mainloop()


def lower_shot_cd():
    global shot_cd_button, shot_cd, score, shot_cd_lvl

    if score >= 100:
        score -= 100
        shot_cd -= 25
        shot_cd_lvl += 1
        shot_cd_button.config(text=f"shot cd ({shot_cd_lvl})")


def multishot():
    global multishot_button, multishot_state, score
    if score >= 50:
        score -= 50
        multishot_state = True
        multishot_button.config(background="green")


def score_label():
    global score
    global score_label_obj
    score += 10
    if not score_label_obj:
        score_label_obj = Label(window, text=f"Score: {score}", font=("Press Start 2P", 20, "bold"), foreground="red", background="black")
        score_label_obj.place(x=1240, y=0)
    else:
        score_label_obj.config(text=f"Score: {score}")


def player_pos(event):
    global player_x, player_y, battleship_sprite

    player_x = event.x_root
    player_y = event.y_root



    """   canvas.create_line(event.x - 50, event.y, event.x + 50, event.y, width=20, tags="player")
    canvas.create_line(event.x, event.y - 50, event.x + 50, event.y, width=20, tags="player")
    canvas.create_line(event.x, event.y - 50, event.x - 50, event.y, width=20, tags="player")
    """

    if battleship_sprite is None:
        battleship_sprite = canvas.create_image(player_x, player_y, image=battleship, anchor="center",
                                                tags="player")
    else:
        canvas.coords(battleship_sprite, player_x, player_y)


def shoot(event):
    global multishot_state, can_shoot, shot_cd

    if not can_shoot:
        return

    can_shoot = False
    window.after(shot_cd, reset_cooldown)


    offsets = [-10, 10] if multishot_state else [0]
    for offset in offsets:
        projectile = canvas.create_line(player_x + offset, player_y, player_x + offset, player_y - 20, width=10, tags="projectile")
        move_projectile(projectile, 0, -30)


def reset_cooldown():
    global can_shoot
    can_shoot = True



def move_projectile(projectile, x, y):
    canvas.move(projectile, x, y)
    canvas.after(16, move_projectile, projectile, x, y)  # 60 FPS


def move_enemy(enemy, x, y):
    canvas.move(enemy, x, y)
    move_mult = random.randint(1, 10)

    if move_mult == 1:
        canvas.after(100, move_enemy, enemy, x + 10, y)
    elif move_mult == 2:
        canvas.after(100, move_enemy, enemy, x - 10, y)
    else:
        canvas.after(100, move_enemy, enemy, x, y)


def spawn_enemy(count, delay):
    global enemy_sprite
    if game_over:
        return
    if count <= 0:
        return

    x_spawn = random.randint(250, 1150)
    y_spawn = 0

    enemy_sprite = canvas.create_image(x_spawn, y_spawn, image=enemy_alien, anchor="center",
                                                tags="enemy")
    enemy_sprites.append(enemy_sprite)

    move_enemy(enemy_sprite, 0, 20)

    count -= 1

    canvas.after(delay, spawn_enemy, count, delay)


def create_endgame_label():
    global game_over, endgame_label
    game_over = True
    endgame_label = Label(window, foreground="black", background="red", text="YOU LOST", font=("Arial", 80, "bold"))
    endgame_label.place(x=500, y=300)
    canvas.delete("enemy")
    canvas.delete("projectile")


def start_collision_loop():
    get_enemy_cord()
    canvas.after(20, start_collision_loop)


def get_enemy_cord():
    if game_over:
        return
    for enemy in enemy_sprites:
        enemy_cords = canvas.coords(enemy)
        if enemy_cords[1] >= 550:
            create_endgame_label()
            return
        elif enemy_cords[0] >= 1200 or enemy_cords[0] <= 150:
            canvas.delete(enemy)
            enemy_sprites.remove(enemy)

        for projectile in canvas.find_withtag("projectile"):
            projectile_cords = canvas.coords(projectile)

            if is_collision(enemy_cords, projectile_cords):
                canvas.delete(enemy)
                enemy_sprites.remove(enemy)
                canvas.delete(projectile)
                score_label()
                return


def is_collision(enemy_cords, projectile_cords):
    # box format: [x1, y1, x2, y2]

    ex, ey = enemy_cords
    enemy_box = [ex - 25, ey - 25, ex + 25, ey + 25]

    px1, py1, px2, py2 = projectile_cords
    proj_box = [min(px1, px2), min(py1, py2), max(px1, px2), max(py1, py2)]

    return not (
        enemy_box[2] < proj_box[0] or  # enemy right < projectile left
        enemy_box[0] > proj_box[2] or  # enemy left > projectile right
        enemy_box[3] < proj_box[1] or  # enemy bottom < projectile top
        enemy_box[1] > proj_box[3]     # enemy top > projectile bottom
    )


def clear_canvas():
    canvas.delete("projectile")
    canvas.delete("enemy")
    enemy_sprites.clear()
    clear_endgame_label()


def lvl1():
    clear_canvas()
    enemy_count = 5
    enemy_spawn_delay = 1000
    spawn_enemy(enemy_count, enemy_spawn_delay)
    start_collision_loop()


def lvl2():
    clear_canvas()
    enemy_count = 7
    enemy_spawn_delay = 1000
    spawn_enemy(enemy_count, enemy_spawn_delay)
    start_collision_loop()


def lvl3():
    clear_canvas()
    enemy_count = 10
    enemy_spawn_delay = 1000
    spawn_enemy(enemy_count, enemy_spawn_delay)
    start_collision_loop()


def lvl4():
    clear_canvas()
    enemy_count = 10
    enemy_spawn_delay = 500
    spawn_enemy(enemy_count, enemy_spawn_delay)
    start_collision_loop()


def clear_endgame_label():
    global score, game_over, endgame_label
    if endgame_label:
        game_over = False
        endgame_label.destroy()
        endgame_label = None


if __name__ == "__main__":
    main()
