import pygame
import time
import random
import math
import os

# Initialize pygame
pygame.init()

# Load background images
themes = [
    pygame.image.load("assets/theme1.jpg"),
    pygame.image.load("assets/theme2.jpg"),
    pygame.image.load("assets/theme3.jpg")
]
theme_names = ["Blue Sky", "Cosmic", "Rainbow"]
selected_theme_index = 0  # Default theme


try:
    click_sound = pygame.mixer.Sound("click.wav")
except:
    click_sound = None


# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Set up the display with the ability to resize the window
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("SNAKE RUSH")

# Clock for controlling the game's frame rate
clock = pygame.time.Clock()

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 20)
score_font = pygame.font.SysFont("bahnschrift", 25)

# Global variable for block size
BLOCK_SIZE = 25

def scale_block_size():
    global BLOCK_SIZE, WIDTH, HEIGHT
    BLOCK_SIZE = max(10, min(WIDTH, HEIGHT) // 40)

def start_menu():
    title_font = pygame.font.SysFont("impact", 60)
    button_font = pygame.font.SysFont("comicsansms", 30)
    credit_font = pygame.font.SysFont("bahnschrift", 18)

    button_play = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50)
    button_quit = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50)
    button_theme = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 160, 200, 50)

    theme_index = 0
    themes = ["Blue Sky", "Cosmic", "Rainbow"]
    rainbow_color = [0, 128, 255]
    title_y_offset = 0
    direction = 1

    glow_phase = 0  # for button glow effect

    running = True
    while running:
        # Background
        if themes[theme_index] == "Blue Sky":
            screen.fill((135, 206, 235))
        elif themes[theme_index] == "Cosmic":
            screen.fill((25, 0, 51))
        elif themes[theme_index] == "Rainbow":
            for i in range(3):
                rainbow_color[i] = (rainbow_color[i] + 1) % 256
            screen.fill(rainbow_color)

        # Title hover effect
        title_y_offset += direction
        if title_y_offset > 10 or title_y_offset < -10:
            direction *= -1

        title_text = title_font.render("🌟 SNAKE RUSH 🌟", True, WHITE)
        screen.blit(title_text, (
            WIDTH // 2 - title_text.get_width() // 2,
            HEIGHT // 4 + title_y_offset
        ))

        # Hover glow effect
        glow_phase = (glow_phase + 2) % 360
        glow_alpha = int(128 + 127 * abs(math.sin(glow_phase / 50)))

        mouse_pos = pygame.mouse.get_pos()

        def draw_button(rect, label, hover_color):
            color = hover_color if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, color, rect, border_radius=8)
            text = button_font.render(label, True, BLACK)
            screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

        draw_button(button_play, "▶ Play", (0, 255, 150))
        draw_button(button_quit, "❌ Quit", (255, 100, 100))
        draw_button(button_theme, f"🎨 Theme: {themes[theme_index]}", (200, 150, 255))

        # Credit line
        credit_text = credit_font.render("Made by Divyansh Rajput 💻", True, WHITE)
        screen.blit(credit_text, (WIDTH - credit_text.get_width() - 10, HEIGHT - 30))

        pygame.display.update()
        clock.tick(30)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if click_sound: click_sound.play()
                if button_play.collidepoint(event.pos):
                    running = False
                elif button_quit.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                elif button_theme.collidepoint(event.pos):
                    theme_index = (theme_index + 1) % len(themes)



def ask_name():
    pygame.display.set_caption("Enter Your Name")
    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_inactive
    active = False
    text = ''
    done = False
    prompt_text = font_style.render("Enter Player Name:", True, WHITE)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                active = input_box.collidepoint(event.pos)
                color = color_active if active else color_inactive
            if event.type == pygame.KEYDOWN and active:
                if event.key == pygame.K_RETURN:
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode

        screen.fill(BLACK)
        screen.blit(prompt_text, (WIDTH // 2 - 120, HEIGHT // 2 - 75))
        txt_surface = font_style.render(text, True, color)
        input_box.w = max(200, txt_surface.get_width() + 10)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, color, input_box, 2)
        pygame.display.flip()

    return text

def our_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(screen, GREEN, [block[0], block[1], BLOCK_SIZE, BLOCK_SIZE])

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def save_high_score(score, player_name):
    try:
        with open("highscore.txt", "r") as f:
            data = f.read().strip()
            high_score, high_score_name = (int(data.split(",")[0]), data.split(",")[1]) if data else (0, "None")
    except:
        high_score, high_score_name = 0, "None"

    if score > high_score:
        with open("highscore.txt", "w") as f:
            f.write(f"{score},{player_name}")

def get_high_score():
    try:
        with open("highscore.txt", "r") as f:
            data = f.read().strip()
            if data:
                high_score, high_score_name = data.split(",")
                return int(high_score), high_score_name
    except:
        pass
    return 0, "None"

def display_score(score, player_name):
    value = score_font.render(f"{player_name} Score: " + str(score), True, WHITE)
    screen.blit(value, [10, 10])
    high_score, high_score_name = get_high_score()
    high_score_text = score_font.render(f"High Score: {high_score} by {high_score_name}", True, WHITE)
    screen.blit(high_score_text, [10, 40])

def adjust_snake_position(snake_list):
    for block in snake_list:
        block[0] = min(max(block[0], 0), WIDTH - BLOCK_SIZE)
        block[1] = min(max(block[1], 0), HEIGHT - BLOCK_SIZE)

def gameLoop():
    global WIDTH, HEIGHT, BLOCK_SIZE, screen

    player_name = ask_name()

    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0
    snake_List = []
    Length_of_snake = 1
    foodx = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
    foody = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
    food_color = random.choice([RED, YELLOW, PURPLE, ORANGE])
    score = 0

    while not game_over:
        while game_close:
            screen.fill(BLUE)
            message("Game Over! Press Q-Quit or C-Play Again", RED)
            display_score(score, player_name)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.VIDEORESIZE:
                WIDTH, HEIGHT = event.w, event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                scale_block_size()
                adjust_snake_position(snake_List)
                foodx = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
                foody = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_d and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_w and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_s and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)
        pygame.draw.ellipse(screen, food_color, [foodx, foody, BLOCK_SIZE, BLOCK_SIZE])

        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for block in snake_List[:-1]:
            if block == snake_Head:
                game_close = True

        our_snake(snake_List)
        display_score(score, player_name)
        pygame.display.update()

        if x1 // BLOCK_SIZE == foodx // BLOCK_SIZE and y1 // BLOCK_SIZE == foody // BLOCK_SIZE:
            foodx = random.randrange(0, WIDTH - BLOCK_SIZE, BLOCK_SIZE)
            foody = random.randrange(0, HEIGHT - BLOCK_SIZE, BLOCK_SIZE)
            food_color = random.choice([RED, YELLOW, PURPLE, ORANGE])
            Length_of_snake += 1
            score += 10

        clock.tick(12)

    save_high_score(score, player_name)
    pygame.quit()
    quit()

# 🟢 START HERE
start_menu()
gameLoop()
