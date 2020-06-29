import pygame
import random
import os

pygame.mixer.init()

pygame.init()


# Colors in RGB
red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)
green = (0, 128, 0)
grey = (128, 128, 128)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Creating Window
screen_width = 900
screen_height = 600
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Background image
back_img = pygame.image.load("Screen images/background.jpg")
outro = pygame.image.load("Screen images/outro.png")

# Rescaling image to window size
back_img = pygame.transform.scale(back_img, (screen_width, screen_height)).convert_alpha()
outro = pygame.transform.scale(outro, (screen_width, screen_height)).convert_alpha()

# Game Title
pygame.display.set_caption("Snakes with Me")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)


def screen_show(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snk(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])  # For creating  Snake Head rect


# Welcome Screen
def welcome():
    exit_game = False
    while not exit_game:
        gameWindow.fill((233, 220, 223))
        screen_show("Welcome to Snakes", blue, 260, 250)
        screen_show("Press Space Bar to Play", blue, 220, 300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("Music/Background.mp3")  # Loading the file
                    pygame.mixer.music.play()
                    gameloop()

        pygame.display.update()
        clock.tick(60)


# Game Loop
def gameloop():
    # Game specific variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    velocity_x = 0
    velocity_y = 0
    snk_list = []
    snk_length = 1
    init_velocity = 5
    snake_size = 20
    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)
    score = 0
    fps = 60

# Check for Highscore File

    if not os.path.exists("Highscore.txt"):
        with open("Highscore.txt", "w") as f:
            f.write(0)
    with open("Highscore.txt", "r") as f:
        highscore = f.read()

# File Reading as String
    with open("Highscore.txt", "r") as f:
        highscore = f.read()

    while not exit_game:

        if game_over:
            with open("Highscore.txt", "w") as f:
                f.write(str(highscore))
                screen_show("Score: " + str(score), green, 385, 350)

# Game Over Screen
            gameWindow.blit(outro, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        welcome()
        else:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = - init_velocity
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = - init_velocity
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = init_velocity
                        velocity_x = 0

                    # Cheat key
                    if event.key == pygame.K_c:
                        score += 10

            snake_x += velocity_x
            snake_y += velocity_y

            if abs(snake_x - food_x) < 6 and abs(snake_y - food_y) < 6:
                score += 10
                food_x = random.randint(20, screen_width / 2)
                food_y = random.randint(20, screen_height / 2)
                snk_length += 5

                if score > int(highscore):
                    highscore = score

            # Display Color
            gameWindow.fill(white)
            gameWindow.blit(back_img, (0, 0))
            screen_show("Score: " + str(score) + "  Highscore: " + str(highscore), yellow, 3,
                        3)  # After filling white otherwise will not show
            pygame.draw.rect(gameWindow, red, [food_x, food_y, snake_size, snake_size])

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:  # for correct length mantainance
                del snk_list[0]

            # If body touch
            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load("Music/gameover.mp3")  # Loading the file
                pygame.mixer.music.play()

            # If window touch
            if snake_x < 0 or snake_x > screen_width or snake_y < 0 or snake_y > screen_height:
                game_over = True
                pygame.mixer.music.load("Music/gameover.mp3")  # Loading the file
                pygame.mixer.music.play()

            plot_snk(gameWindow, black, snk_list, snake_size)

        pygame.display.update()  # Every time there is a change in the game window
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()
