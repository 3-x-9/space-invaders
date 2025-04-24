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

basic_enemy_sprite = None
basic_enemy_sprites = []
targeting_enemy_sprite = None
targeting_enemy_sprites = []
boss_enemy_sprite = None
boss_enemy_sprites = []

spawning_active = True

after_calls = []

can_shoot = True
shot_cd = 400
shot_cd_lvl = 0

lives = 3

green_hp = None
red_hp = None
lvl5_hp = []

boss_direction = 0
boss_timer = 0

boss_attack = 0
boss_bomb_sprite = None
boss_bomb_sprites = []
boss_move_after2 = None
boss_move_after1 = None

def main():
    global window, canvas, multishot_button, battleship, basic_enemy_alien, shot_cd_button, heart, battleship_sprite,\
        player_x, player_y, targeting_enemy_img, score, boss_enemy_img, bomb_img, explosion_img

    window = Tk()
    canvas = Canvas(window, width=1550, height=820, bg="black")

    # battleship
    battleship = resize_image("battleship.png", 100, 100)
    # basic_enemy
    basic_enemy_alien = resize_image("enemy.png", 75, 75)
    # targeting_enemy
    targeting_enemy_img = resize_image("targeting_enemy.png", 75, 75)
    # boss enemy
    boss_enemy_img = resize_image("boss_enemy.png", 300, 300)
    # heart
    heart = resize_image("heart.png", 100, 100)
    # background
    background = resize_image("background.png", 1550, 820)
    # bomb
    bomb_img = resize_image("bomb.png", 50, 50)
    # explosion
    explosion_img = resize_image("explosion.png", 300, 300)

    player_x = 600
    player_y = 650
    battleship_sprite = canvas.create_image(player_x, player_y, image=battleship, anchor="center", tags="player")

    canvas_background = canvas.create_image(0, 0, image=background, anchor="nw")
    canvas.tag_lower(canvas_background)

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    window.geometry(f"{screen_width}x{screen_height}")

    window.bind("<Motion>", player_pos)
    window.bind("<space>", shoot)

    score_label(0)

    lvl_frame = Frame(window)

    lvl_1 = Button(lvl_frame, text="LVL 1", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl1)
    lvl_2 = Button(lvl_frame, text="LVL 2", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl2)
    lvl_3 = Button(lvl_frame, text="LVL 3", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl3)
    lvl_4 = Button(lvl_frame, text="LVL 4", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl4)
    lvl_5 = Button(lvl_frame, text="LVL 5", font=("Press Start 2P", 32, "bold"), foreground="white",
                   background="black", command=lvl5)

    lvl_1.pack()
    lvl_2.pack()
    lvl_3.pack()
    lvl_4.pack()
    lvl_5.pack()

    upgrade_frame = Frame(window)
    upgrade_label = Label(upgrade_frame, text="UPGRADES", font=("Press Start 2P", 20, "bold"), foreground="white",
                        background="black", width=10)

    multishot_button = Button(upgrade_frame, text="Multishot", font=("Press Start 2P", 20, "bold"), foreground="red",
                              background="black", command=multishot, width=10)
    Hovertip(multishot_button, "Multishot, Makes u shoot 2 projectiles \n Cost: 50", hover_delay=100)

    shot_cd_button = Button(upgrade_frame, text="shot cd", font=("Press Start 2P", 20, "bold"), foreground="red",
                              background="black", command=lower_shot_cd, width=10)
    Hovertip(shot_cd_button, "Shot cooldown reduction, Makes u shoot projectiles faster \n Cost: 100 per level"
                             "\n Max lvl 8", hover_delay=100)

    buy_heart_button = Button(upgrade_frame, text="Buy a HEART", font=("Press Start 2P", 20, "bold"), foreground="red",
                              background="black", command=buy_heart, width=10)
    Hovertip(buy_heart_button, "Buy an extra life \n Cost: 150 per Heart \n Max Hearts: 4", hover_delay=100)

    upgrade_label.pack()

    multishot_button.pack()
    shot_cd_button.pack()
    buy_heart_button.pack()

    canvas.create_line(200, 550, 1200, 550, fill="white")
    canvas.create_rectangle(200, 2, 1200, 720, outline="white")
    # 1200, 720

    upgrade_frame.place(x=0, y=500)
    canvas.pack()
    lvl_frame.place(x=0, y=0)
    window.mainloop()


def resize_image(path, width, height):
    original_img = Image.open(path)
    resized_img = original_img.resize((width, height))
    return ImageTk.PhotoImage(resized_img)


def lower_shot_cd():
    global shot_cd_button, shot_cd, score, shot_cd_lvl

    if score >= 100 and shot_cd_lvl < 8:
        score -= 100
        shot_cd -= 25
        shot_cd_lvl += 1
        shot_cd_button.config(text=f"shot cd ({shot_cd_lvl})")
        score_label_obj.config(text=f"Score: {score}")


def multishot():
    global multishot_button, multishot_state, score
    if score >= 50:
        score -= 50
        multishot_state = True
        multishot_button.config(background="green")
        score_label_obj.config(text=f"Score: {score}")


def buy_heart():
    global lives, score

    if score > 150 and lives < 4:
        score -= 150
        lives += 1

        score_label_obj.config(text=f"Score: {score}")
        canvas.delete("hearts")

        for life in range(lives):
            canvas.create_image(1200 + 100 * life, 700, image=heart, anchor="center", tags="hearts")


def take_life():
    global lives, heart, score
    lives -= 1
    if lives <= 0:
        create_endgame_label()
        score = 0
        score_label_obj.config(text=f"Score: {score}")

    hearts = []
    canvas.delete("hearts")

    for life in range(lives):

        heart_img = canvas.create_image(1200 + 100*life, 700, image=heart, anchor="center", tags="hearts")
        hearts.append(heart_img)


def score_label(add):
    global score
    global score_label_obj
    score += add

    if not score_label_obj:
        score_label_obj = Label(window, text=f"Score: {score}", font=("Press Start 2P", 20, "bold"), foreground="red",
                                background="black")
        score_label_obj.place(x=1240, y=0)
    else:
        score_label_obj.config(text=f"Score: {score}")


def item_exists(canvas, item_id):
    return item_id in canvas.find_all()


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
        projectile = canvas.create_line(player_x + offset, player_y, player_x + offset, player_y - 20, width=10,
                                        fill="white", tags="projectile")
        move_projectile(projectile, 0, -30)


def reset_cooldown():
    global can_shoot
    can_shoot = True


def move_projectile(projectile, x, y):
    if not item_exists(canvas, projectile):
        return

    canvas.move(projectile, x, y)
    canvas.after(16, move_projectile, projectile, x, y)  # 60 FPS


def move_enemy(enemy, x, y):
    if not item_exists(canvas, enemy):
        return

    canvas.move(enemy, x, y)
    move_mult = random.randint(1, 10)

    if move_mult == 1:
        canvas.after(50, move_enemy, enemy, x + 5, y)
    elif move_mult == 2:
        canvas.after(50, move_enemy, enemy, x - 5, y)
    else:
        canvas.after(50, move_enemy, enemy, x, y)


def spawn_basic_enemy(count, delay, waves):
    global basic_enemy_sprite, after_calls

    if game_over:
        return
    if count <= 0:
        return

    if waves > 0:
        create_basic_enemy(count)
    waves -= 1

    basic_enemy_parent = canvas.after(5000, spawn_basic_enemy, count, delay, waves)
    after_calls.append(basic_enemy_parent)


def create_basic_enemy(count):
    global basic_enemy_sprite, spawning_active, after_calls

    if game_over or not spawning_active:
        return

    x_spawn = random.randint(250, 1150)
    y_spawn = 0

    basic_enemy_sprite = canvas.create_image(x_spawn, y_spawn, image=basic_enemy_alien, anchor="center",
                                             tags="enemy")
    basic_enemy_sprites.append(basic_enemy_sprite)

    move_enemy(basic_enemy_sprite, 0, 10)

    count -= 1
    if count == 0:
        return
    basic_enemy_loop = canvas.after(500, create_basic_enemy, count)
    after_calls.append(basic_enemy_loop)


def spawn_targeting_enemy(count, delay, waves):
    global targeting_enemy_sprite, after_calls

    if game_over:
        return

    if waves > 0:
        create_targeting_enemy(count)
    waves -= 1

    targeting_enemy_parent = canvas.after(5000, spawn_targeting_enemy, count, delay, waves)
    after_calls.append(targeting_enemy_parent)


def create_targeting_enemy(count):
    global targeting_enemy_sprite, spawning_active, after_calls

    if game_over or not spawning_active:
        return

    x_spawn = random.randint(250, 1150)
    y_spawn = 0

    targeting_enemy_sprite = canvas.create_image(x_spawn, y_spawn, image=targeting_enemy_img, anchor="center",
                                                 tags="enemy")
    targeting_enemy_sprites.append(targeting_enemy_sprite)

    move_targeting_enemy(targeting_enemy_sprite)

    count -= 1
    if count == 0:
        return
    targeting_enemy_loop = canvas.after(500, create_targeting_enemy, count)
    after_calls.append(targeting_enemy_loop)


def move_targeting_enemy(enemy):
    global player_x, player_y
    if not item_exists(canvas, enemy):
        return

    enemy_cords = canvas.coords(enemy)

    if player_x > enemy_cords[0]:
        if (player_x - enemy_cords[0]) > 10:
            x_direction = 10
        else:
            x_direction = (player_x - enemy_cords[0])

    elif player_x < enemy_cords[0]:
        if (player_x - enemy_cords[0]) < -10:
            x_direction = -10
        else:
            x_direction = -(player_x - enemy_cords[0])

    elif player_x == enemy_cords[0]:
        x_direction = 0

    y_direction = +10

    canvas.move(enemy, x_direction, y_direction)
    canvas.after(50, move_targeting_enemy, enemy)


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
    check_enemy(basic_enemy_sprites, 50, 50)

    check_enemy(targeting_enemy_sprites, 50, 50)

    check_boss_enemy(boss_enemy_sprites, 150, 150)


def check_enemy(enemy_list, width, height):
    for enemy in enemy_list[:]:
        enemy_cords = canvas.coords(enemy)
        if len(enemy_cords) >= 2 and enemy_cords[1] >= 550:
            canvas.delete(enemy)
            if enemy in enemy_list:
                enemy_list.remove(enemy)
            take_life()
            continue

        if len(enemy_cords) >= 2 and (enemy_cords[0] > 1200 or enemy_cords[0] < 150):
            canvas.delete(enemy)
            if enemy in enemy_list:
                enemy_list.remove(enemy)
            continue

        if len(enemy_cords) >= 2:
            enemy_cords = center_to_box(enemy_cords[0], enemy_cords[1], width, height)

            for projectile in canvas.find_withtag("projectile"):
                projectile_cords = canvas.coords(projectile)

                projectile_cords = line_to_box(projectile_cords)

                if is_collision(enemy_cords, projectile_cords):
                    canvas.delete(enemy)
                    if enemy in enemy_list:
                        enemy_list.remove(enemy)
                    canvas.delete(projectile)
                    score_label(10)
                    continue

            for player in canvas.find_withtag("player"):
                player_cords = canvas.coords(player)

                player_box = center_to_box(player_cords[0], player_cords[1], 100, 100)

                if is_collision(enemy_cords, player_box):
                    canvas.delete(enemy)
                    if enemy in enemy_list:
                        enemy_list.remove(enemy)
                    score_label(10)
                    take_life()
                    continue


def check_boss_enemy(enemy_list, width, height):
    global lvl5_hp

    for enemy in enemy_list[:]:
        enemy_cords = canvas.coords(enemy)

        if len(enemy_cords) >= 2:
            enemy_cords = center_to_box(enemy_cords[0], enemy_cords[1], width, height)
            for projectile in canvas.find_withtag("projectile"):
                projectile_cords = canvas.coords(projectile)

                projectile_cords = line_to_box(projectile_cords)

                if is_collision(enemy_cords, projectile_cords):
                    take_enemy_hp(enemy_cords)
                    canvas.delete(projectile)
                    score_label(10)
                    continue

            for player in canvas.find_withtag("player"):
                player_cords = canvas.coords(player)

                player_box = center_to_box(player_cords[0], player_cords[1], 100, 100)

                if is_collision(enemy_cords, player_box):
                    take_enemy_hp(enemy_cords)
                    score_label(10)
                    take_life()
                    continue

            for bomb in canvas.find_withtag("enemy_projectile"):
                bomb_cords = canvas.coords(bomb)
                bomb_cords = center_to_box(bomb_cords[0], bomb_cords[1], 50, 50)

                if is_collision(player_box, bomb_cords):
                    take_life()
                    canvas.delete(bomb)
                    create_explosion(bomb_cords[0], bomb_cords[1])
                    canvas.after(100, delete_explosion)
                    continue

                if bomb_cords[1] > 550:
                    create_explosion(bomb_cords[0], bomb_cords[1])
                    explosion_center = canvas.coords(bomb)
                    explosion_cords = center_to_box(explosion_center[0], explosion_center[1], 200, 200)
                    if is_collision(player_box, explosion_cords):
                        take_life()

                    canvas.after(100, delete_explosion)
                    canvas.delete(bomb)
                    continue

def take_enemy_hp(cords):
    global lvl5_hp, after_calls
    lvl5_hp.pop()
    print(lvl5_hp)
    create_hp_bar(lvl5_hp)


def create_hp_bar(hp_list):
    global green_hp, red_hp, boss_enemy_sprite
    if green_hp is not None:
        canvas.delete(green_hp)
        green_hp = None
    if red_hp is not None:
        canvas.delete(red_hp)
        red_hp = None

    if green_hp is None and red_hp is None:
        cords = canvas.coords(boss_enemy_sprite)

        if len(cords) > 0:
            hp_x_start = cords[0] - 100
            hp_y_start = cords[1] - 100
            hp_x_end_green = (cords[0] - 100) + (10*len(hp_list))
            hp_x_end_red = cords[0] + 100
            hp_y_end = cords[1] - 100



            red_hp = canvas.create_line(hp_x_start, hp_y_start, hp_x_end_red, hp_y_end, fill="red", width=10, tags="hp_bar")
            green_hp = canvas.create_line(hp_x_start, hp_y_start, hp_x_end_green, hp_y_end, fill="green", width=10, tags="hp_bar")
        if len(hp_list) == 0:
            canvas.delete("enemy")
        hp_bar_call = canvas.after(50, create_hp_bar, hp_list)
        after_calls.append(hp_bar_call)

def is_collision(box1, box2):
    # box format: [x1, y1, x2, y2]

    return not (
        box1[2] < box2[0] or  # enemy right < projectile left
        box1[0] > box2[2] or  # enemy left > projectile right
        box1[3] < box2[1] or  # enemy bottom < projectile top
        box1[1] > box2[3]     # enemy top > projectile bottom
    )


def center_to_box(x, y, width, height):
    x1 = x - width//2
    x2 = x + width//2
    y1 = y - height//2
    y2 = y + height//2

    box = [x1, y1, x2, y2]
    return box


def line_to_box(line):
    px1, py1, px2, py2 = line
    box = [min(px1, px2), min(py1, py2), max(px1, px2), max(py1, py2)]
    return box


def clear_canvas():
    global targeting_enemy_loop, basic_enemy_loop, spawning_active, after_calls, boss_enemy_sprite, lvl5_hp
    canvas.delete("projectile")
    canvas.delete("enemy")
    canvas.delete("hp_bar")
    targeting_enemy_sprites.clear()
    basic_enemy_sprites.clear()
    boss_enemy_sprites.clear()
    clear_endgame_label()
    boss_enemy_sprite = None
    for callid in after_calls:
        canvas.after_cancel(callid)
    lvl5_hp = []
    after_calls.clear()
    spawning_active = False
    for life in range(lives):
        heart_img = canvas.create_image(1200 + 100*life, 700, image=heart, anchor="center", tags="hearts")


def lvl1():
    global spawning_active
    clear_canvas()
    spawning_active = True
    enemy_count = 5
    enemy_spawn_delay = 1000
    waves = 3

    spawn_basic_enemy(enemy_count, enemy_spawn_delay, waves)
    start_collision_loop()


def lvl2():
    global spawning_active
    clear_canvas()
    spawning_active = True
    enemy_count = 7
    enemy_spawn_delay = 1000
    waves = 4

    spawn_basic_enemy(enemy_count, enemy_spawn_delay, waves)
    start_collision_loop()


def lvl3():
    global spawning_active
    clear_canvas()
    spawning_active = True
    enemy_count = 10
    enemy_spawn_delay = 1000
    waves = 5

    spawn_targeting_enemy(enemy_count, enemy_spawn_delay, waves)
    start_collision_loop()


def lvl4():
    global spawning_active
    clear_canvas()
    spawning_active = True
    tatgeting_enemy_count = 5
    enemy_count = 8
    enemy_spawn_delay = 500
    waves = 5

    spawn_targeting_enemy(tatgeting_enemy_count, enemy_spawn_delay, waves)
    spawn_basic_enemy(enemy_count, enemy_spawn_delay, waves)
    start_collision_loop()


def lvl5():
    global spawning_active, lvl5_hp
    clear_canvas()
    spawning_active = True
    hp = 20
    for i in range(hp):
        lvl5_hp.append(i)

    start_collision_loop()
    create_boss_enemy()



def create_boss_enemy():
    global boss_enemy_img, boss_enemy_sprite, boss_enemy_sprites

    ylvl = 150
    xspawn = 700

    if boss_enemy_sprite is None:
        boss_enemy_sprite = canvas.create_image(xspawn, ylvl, image=boss_enemy_img, anchor="center", tags="enemy")
        boss_enemy_sprites.append(boss_enemy_sprite)
        move_boss(boss_enemy_sprite, 0, 0)


def move_boss(boss, x, y):
    global boss_attack, boss_move_after1, boss_move_after2, boss_direction, boss_timer

    if not item_exists(canvas, boss_enemy_sprite):
        return

    canvas.move(boss, x, y)

    if boss_move_after1 is not None:
        canvas.after_cancel(boss_move_after1)
    elif boss_move_after2 is not None:
        canvas.after_cancel(boss_move_after2)

    prob = random.random()
    boss_cords = canvas.coords(boss)
    x = 1
    boss_x = boss_cords[0]

    if boss_attack < 20:
        boss_attack += 1
    if boss_attack == 20:
        boss_attack = 0
        boss_bomb(boss_cords[0], boss_cords[1])

    midpoint = 700
    bias_left = False

    boss_timer -= 1
    if boss_timer <= 0:
        if boss_x >= midpoint:
            bias_left = True
        if bias_left:
            boss_direction = -7 if prob < 0.75 else 7
        elif not bias_left:
            boss_direction = 7 if prob < 0.75 else -7

        boss_timer = random.randint(20, 60)












    if boss_x > 1200 or boss_x < 300:
        boss_direction *= -1

    canvas.after(50, move_boss, boss, boss_direction, y)

def boss_bomb(x, y):
    global bomb_img, boss_bomb_sprite, boss_bomb_sprites

    boss_bomb_sprite = canvas.create_image(x, y, image=bomb_img, anchor="center", tags="enemy_projectile")
    boss_bomb_sprites.append(boss_bomb_sprite)
    move_projectile(boss_bomb_sprite, 0, 10)


def create_explosion(x, y):
    global explosion_img
    explosion = canvas.create_image(x, y, image=explosion_img, anchor="center", tags="temp")


def delete_explosion():
    canvas.delete("temp")


def clear_endgame_label():
    global score, game_over, endgame_label, lives

    lives = 3

    if endgame_label:
        game_over = False
        endgame_label.destroy()
        endgame_label = None


if __name__ == "__main__":
    main()
