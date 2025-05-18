import pgzrun
import sys    # For exit button

WIDTH = 480
HEIGHT = 240
TITLE = "Dino Platformer - Game in PG Zero"

GRAVITY = 1
JUMP_STRENGTH = -12
PLAYER_SPEED = 2
JUMP_SPEED = -10

# Tile Map
tile_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

background = Actor("background")

# Initial function to draw the actors of the game
def init():
    global player, enemies, blocks, game_over, victory, victory_door

    player = {
        "actor": Actor("player_stand1", (50, 150)),
        "vy": 0,
        "dx": 0,
        "on_ground": False,
        "alive": True,
        "dir": 1,
        "state": "idle",

        # Images for sprite
        "images_walk_right": ["player_walk1", "player_walk2", "player_walk3", "player_walk4", "player_walk5", "player_walk6"],
        "images_walk_left": ["player_left_walk1", "player_left_walk2", "player_left_walk3", "player_left_walk4", "player_left_walk5", "player_left_walk6"],
        "images_idle_right": ["player_stand1", "player_stand2", "player_stand3"],
        "images_idle_left": ["player_left_stand1", "player_left_stand2", "player_left_stand3"],

        # Defaut images
        "images": ["player_stand1", "player_stand2", "player_stand3"],
        "index": 0,
        "frame_count": 0,
        "frame_delay": 6
    }
    
    # Create enemies
    def create_enemies(position, speed, timer):
        enemy = {
            "actor": Actor("dino_stand1", position),
            "dir": 1,
            "speed": speed,
            "state": "moving",
            "timer": timer,

            "images_walk_right": ["dino_walk1", "dino_walk2", "dino_walk3", "dino_walk4", "dino_walk5", "dino_walk6"],
            "images_walk_left": ["dino_left_walk1", "dino_left_walk2", "dino_left_walk3", "dino_left_walk4", "dino_left_walk5", "dino_left_walk6"],
            "images_idle_right": ["dino_stand1", "dino_stand2", "dino_stand3"],
            "images_idle_left": ["dino_left_stand1", "dino_left_stand2", "dino_left_stand3"],

            "images": ["dino_stand1", "dino_stand2", "dino_stand3"],
            "index": 0,
            "frame_delay": 6,
            "frame_count": 0,
        }
        return enemy

    enemies = [
        create_enemies((160, HEIGHT - 71), 1, 60),
        create_enemies((150, HEIGHT - 168), 2, 30)
    ]

    # Create the map with the blocks
    blocks = []
    for y, row in enumerate(tile_map):
        for x, tile in enumerate(row):
            if tile == 1:
                block = Actor("block", (x * 16 + 8, y * 16 + 8))
                blocks.append(block)

    victory_door = Rect((32, 48), (32, 32))

    victory = False
    game_over = False

init()

def update():
    if not player["alive"]:
        return
    
    # Move player
    actor = player["actor"]
    player["dx"] = 0
    
    if keyboard.left:
        player["dx"] = -PLAYER_SPEED
        player["dir"] = -1
        player["state"] = "moving"
        player["images"] = player["images_walk_left"]
    elif keyboard.right:
        player["dx"] = PLAYER_SPEED
        player["dir"] = 1
        player["state"] = "moving"
        player["images"] = player["images_walk_right"]
    else:
        if player["dir"] == 1:
            player["images"] = player["images_idle_right"]
        else:
            player["images"] = player["images_idle_left"]

    actor.x += player["dx"]

    player["frame_count"] += 1
    if player["frame_count"] >= player["frame_delay"]:
        player["frame_count"] = 0
        player["index"] = (player["index"] + 1) % len(player["images"])
        actor.image = player["images"][player["index"]]

    # Handle Horizontal Collisions
    for block in blocks:
        if actor.colliderect(block):
            if player["dx"] > 0:
                actor.right = block.left
            elif player["dx"] < 0:
                actor.left = block.right
    
    # Apply gravity
    player["vy"] += GRAVITY
    actor.y += player["vy"]

    # Handle vertical collisions
    player["on_ground"] = False
    for block in blocks:
        if actor.colliderect(block):
            if player["vy"] > 0:
                actor.bottom = block.top
                player["vy"] = 0
                player["on_ground"] = True
            elif player["vy"] < 0:
                actor.top = block.bottom
                player["vy"] = 0

    # Update enemies
    for enemy in enemies:
        actor_enemy = enemy["actor"]

        enemy["timer"] -= 1
        if enemy["timer"] <= 0:
            if enemy["state"] == "moving":
                enemy["state"] = "idle"
                enemy["timer"] = 30
                if enemy["dir"] == 1:
                    enemy["images"] = enemy["images_idle_right"]
                else:
                    enemy["images"] = enemy["images_idle_left"]
                enemy["index"] = 0
            else:
                enemy["state"] = "moving"
                enemy["timer"] = 60
                enemy["dir"] *= -1

                if enemy["dir"] == 1:
                    enemy["images"] = enemy["images_walk_right"]
                else:
                    enemy["images"] = enemy["images_walk_left"]
                enemy["index"] = 0

        if enemy["state"] == "moving":
            actor_enemy.x += enemy["dir"] * enemy["speed"]

        # Sprite animations
        enemy["frame_count"] += 1
        if enemy["frame_count"] >= enemy["frame_delay"]:
            enemy["frame_count"] = 0
            enemy["index"] = (enemy["index"] + 1) % len(enemy["images"])
            actor_enemy.image = enemy["images"][enemy["index"]]

    # Check enemies collisions
    global sounds_on
    for enemy in enemies[:]:
        if actor.colliderect(enemy["actor"]):
            if player["vy"] > 0 and actor.bottom <= enemy["actor"].top + 10:
                enemies.remove(enemy)
                player["vy"] = JUMP_SPEED
                if sounds_on:
                    sounds.enemy_died.play()
            else:
                # Game over
                player["alive"] = False
                global game_over
                game_over = True
                if sounds_on:
                    sounds.game_over.play()

    # Victory
    if victory_door.collidepoint(actor.pos):
        player["alive"] = False
        global victory
        victory = True
        if sounds_on:
            sounds.victory.play()

def on_key_down(key):
    if key == keys.SPACE and player["on_ground"]:
        if sounds_on:
            sounds.jump.play()
        player["vy"] = JUMP_STRENGTH

# Game states
game_state = "menu"
music_playing = True
music.play("music")

# Menu buttons
start_btn = Rect((WIDTH // 2 - 75, 90), (125, 25))
music_btn = Rect((WIDTH // 2 - 62.5, 125), (100, 20))
sounds_btn = Rect((WIDTH // 2 - 62.5, 155), (100, 20))
exit_btn = Rect((WIDTH // 2 - 62.5, 185), (100, 20))

# End game buttons
play_again_rect = Rect((WIDTH//2 - 40, HEIGHT//2 + 20), (80, 20))
menu_rect = Rect((WIDTH//2 - 40, HEIGHT//2 + 50), (80, 20))

sounds_on = True

def draw():
    screen.clear()

    if game_state == "menu":
        draw_menu()
    
    elif game_state == "playing":
        draw_playing()
    
    elif game_state == "game_over":
        screen.draw.text("Game Over", center=(WIDTH//2, HEIGHT//2), fontsize=36, color="red")

def draw_playing():
    background.draw()
    
    for block in blocks:
        block.draw()
    
    screen.draw.filled_rect(victory_door, (0, 0, 0))
    
    for enemy in enemies:
        enemy["actor"].draw()
    
    if player["alive"]:
        player["actor"].draw()

    elif game_over:
        screen.draw.text("Game Over!", center=(WIDTH/2, HEIGHT/2 - 20), fontsize=38, color="black", fontname="pixel_font.ttf")
        screen.draw.text("Game Over!", center=(WIDTH/2, HEIGHT/2 - 20), fontsize=36, color="red", fontname="pixel_font.ttf")
        
        draw_button(play_again_rect, "Play Again", fontsize=12)
        draw_button(menu_rect, "Menu", fontsize=12)

    elif victory:
        screen.draw.text("Victory!", center=(WIDTH/2, HEIGHT/2 - 20), fontsize=38, color="black", fontname="pixel_font.ttf")
        screen.draw.text("Victory!", center=(WIDTH/2, HEIGHT/2 - 20), fontsize=36, color="blue", fontname="pixel_font.ttf")
        
        draw_button(play_again_rect, "Play Again", fontsize=12)
        draw_button(menu_rect, "Menu", fontsize=12)

def draw_menu():
    screen.draw.text("Dino Platformer", center=(WIDTH//2, 30), fontsize=30, color="white", fontname="pixel_font.ttf")
    screen.draw.text("Game in PG Zero", center=(WIDTH//2, 60), fontsize=24, color="white", fontname="pixel_font.ttf")
    
    draw_button(start_btn, "Start", fontsize=14)
    draw_button(music_btn, "Music", fontsize=12)
    draw_button(sounds_btn, "Sounds", fontsize=12)
    draw_button(exit_btn, "Exit", fontsize=12)

def draw_button(rect, text, fontsize):
    screen.draw.filled_rect(rect, "lightblue")
    screen.draw.rect(rect, "black")
    screen.draw.text(text, center=rect.center, fontsize=fontsize, color="black", fontname="pixel_font.ttf")

def on_mouse_down(pos):
    global game_state, music_playing, sounds_on

    # Define menu buttons
    if game_state == "menu":
        # Start game
        if start_btn.collidepoint(pos):
            if sounds_on:
                sounds.button.play()
            game_state = "playing"
            
        # Music on/off
        elif music_btn.collidepoint(pos):
            if sounds_on:
                sounds.button.play()
            if music_playing == True:
                music.stop()
                music_playing = False
            else:
                music.play("music")
                music_playing = True
        
        # Sounds on/off
        elif sounds_btn.collidepoint(pos):
            if sounds_on:
                sounds.button.play()
            sounds_on = False

        # Exit game
        elif exit_btn.collidepoint(pos):
            if sounds_on:
                sounds.button.play()
            sys.exit()

        else:
            if sounds_on:
                sounds.click.play()

    # End game buttons
    # Restart game
    elif game_state == "playing" and play_again_rect.collidepoint(pos):
        if sounds_on:
            sounds.button.play()
        init()
    # Direct to menu
    elif game_state == "playing" and menu_rect.collidepoint(pos):
        if sounds_on:
            sounds.button.play()
        game_state = "menu"
        init()

    else:
        if sounds_on:
            sounds.click.play()

pgzrun.go()