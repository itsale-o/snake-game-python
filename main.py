import pygame
import random

pygame.init()
pygame.display.set_caption("Snake Game")
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

# style_configs
dark_green = (0, 156, 59)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
dark_red = (163, 11, 11)
green = (0, 255, 0)
yellow = (255, 223, 0)
dark_blue = (0, 39, 118)
font_title = pygame.font.SysFont('arial', 50)
font = pygame.font.SysFont('arial', 28)

# parameters
square_size = 10
frame_rate = 15


def start_menu():
    screen.fill((0, 0, 0))
    title = font_title.render('Snake - The Game', True, yellow)
    start_button = font.render('Press SPACE to start', True, dark_green)
    screen.blit(title, (width/2 - title.get_width()/2, height/2 - title.get_height()))
    screen.blit(start_button, (width/2 - start_button.get_width()/2, height/2 + start_button.get_height()/2))
    pygame.display.update()


def pause_menu():
    screen.fill(black)
    title = font_title.render('Pause', True, dark_blue)
    continue_button = font.render('Press SPACE to continue', True, white)
    quit_button = font.render('Press Q to quit', True, white)
    screen.blit(title, (width/2 - title.get_width()/2, height/2 - title.get_height()))
    screen.blit(continue_button, (width/2 - continue_button.get_width()/2, height/2 + continue_button.get_height()/2))
    screen.blit(quit_button, (width/2 - quit_button.get_width()/2, height/2 + quit_button.get_height()*2))
    pygame.display.update()


def game_over_screen():
    screen.fill(black)
    title = font_title.render('Game Over!', True, red)
    score = font.render(f'Your Score: {snake_size - 1}', True, dark_green)
    restart_button = font.render('Press R to restart', True, white)
    quit_button = font.render('Press Q to quit', True, white)
    screen.blit(title, (width/2 - title.get_width()/2, height/2 - title.get_height()))
    screen.blit(score, (width/2 - score.get_width()/2, height/2 + score.get_height()/3))
    screen.blit(restart_button, (width/2 - restart_button.get_width()/2, height/2 + restart_button.get_height()*5))
    screen.blit(quit_button, (width/2 - quit_button.get_width()/2, height/2 + quit_button.get_height()*6))
    pygame.display.update()


def generate_food():
    food_x = round(random.randrange(0, width - square_size)/float(square_size)) * float(square_size)
    food_y = round(random.randrange(0, height - square_size)/float(square_size)) * float(square_size)
    return food_x, food_y


def food(size, food_x, food_y):
    pygame.draw.rect(screen, dark_red, [food_x, food_y, size, size])


def snake(size, pixels):
    for pixel in pixels:
        pygame.draw.rect(screen, white, [pixel[0], pixel[1], size, size])


def score(score):
    font_score = pygame.font.SysFont("arial", 25)
    score = font_score.render(f"Socre: {score}", True, green)
    screen.blit(score, [2, 1])


game_state = "start_menu"
x = width/2
y = height/2
speed_x = 0
speed_y = 0
snake_size = 1
pixels = []
food_x, food_y = generate_food()

while True:
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    if game_state == "start_menu":
        start_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            x = width / 2
            y = height / 2
            speed_x = 0
            speed_y = 0
            snake_size = 1
            pixels = []
            game_state = "game"
            game_over = False
    elif game_state == "pause_menu":
        pause_menu()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game_state = "game"
            game_over = False
        elif keys[pygame.K_q]:
            pygame.quit()
            quit()
    elif game_state == "game_over":
        game_over_screen()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            game_state = "start_menu"
        elif keys[pygame.K_q]:
            pygame.quit()
            quit()
    elif game_state == "game":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            speed_x = 0
            speed_y = square_size
        elif keys[pygame.K_UP] or keys[pygame.K_w]:
            speed_x = 0
            speed_y = -square_size
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            speed_x = square_size
            speed_y = 0
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            speed_x = -square_size
            speed_y = 0
        elif keys[pygame.K_ESCAPE]:
            game_state = "pause_menu"

        food(square_size, food_x, food_y)
        if x < 0 or x >= width or y < 0 or y >= height:
            game_over = True
            game_state = "game_over"

        x += speed_x
        y += speed_y
        pixels.append([x, y])

        if len(pixels) > snake_size:
            del pixels[0]

        for pixel in pixels[:-1]:
            if pixel == [x, y]:
                game_over = True
                game_state = "game_over"

        if x == food_x and y == food_y:
            snake_size += 1
            food_x, food_y = generate_food()

        snake(square_size, pixels)
        score(snake_size - 1)
        pygame.display.update()

        clock.tick(frame_rate)
    elif game_over:
        game_state = "game_over"
        game_over = False

