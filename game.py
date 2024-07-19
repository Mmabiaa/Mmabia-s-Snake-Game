import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Define colors
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Define display dimensions
dis_width = 800
dis_height = 600

# Create the display
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Mmabia Snake Game')

# Clock for controlling the speed of the snake
clock = pygame.time.Clock()
snake_block = 10

# Font styles
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

# Customization options
snake_colors = [black, yellow, green, blue]
current_color_index = 1
snake_color = snake_colors[current_color_index]

# Highest scores per level
highest_scores = [0] * 1

# Obstacles
obstacles = []
min_obstacle_size = 10  # Minimum size of obstacles (1 cm)
max_obstacle_size = 50  # Maximum size of obstacles (5 cm)

def our_snake(snake_block, snake_List, color):
    for x in snake_List:
        pygame.draw.rect(dis, color, [x[0], x[1], snake_block, snake_block])

def draw_obstacles(obstacle_list):
    for obstacle in obstacle_list:
        pygame.draw.rect(dis, black, [obstacle[0], obstacle[1], obstacle[2], obstacle[3]])

def message(msg, color, y_displace=0):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3 + y_displace])

def draw_score(score, level):
    value = score_font.render(f"Score: {score}", True, white)
    dis.blit(value, [0, 0])
    level_value = score_font.render(f"Level: {level}", True, white)
    dis.blit(level_value, [0, 40])
    highest_score = score_font.render(f"Highest Score: {highest_scores[level-1]}", True, white)
    dis.blit(highest_score, [0, 80])

def generate_obstacles():
    num_obstacles = 10
    return [(random.randint(0, dis_width // min_obstacle_size - 1) * min_obstacle_size,
             random.randint(0, dis_height // min_obstacle_size - 1) * min_obstacle_size,
             random.randint(min_obstacle_size, max_obstacle_size),
             random.randint(min_obstacle_size, max_obstacle_size))
            for _ in range(num_obstacles)]

def gameLoop(mode):
    game_over = False
    game_close = False
    paused = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    score = 0
    level = 1
    snake_speed = 10

    global snake_color, obstacles

    if mode == "Hard":
        obstacles = generate_obstacles()

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop(mode)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_p:
                    paused = not paused

        while paused:
            message("Paused! Press P to Continue", red)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                game_close = True

        if mode == "Hard":
            draw_obstacles(obstacles)
            for obstacle in obstacles:
                if (obstacle[0] <= x1 < obstacle[0] + obstacle[2]) and (obstacle[1] <= y1 < obstacle[1] + obstacle[3]):
                    game_close = True

        our_snake(snake_block, snake_List, snake_color)
        draw_score(score, level)
        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            score += 1
            if score % 5 == 0:
                level += 1
                snake_speed += 3
                if level > len(highest_scores):
                    highest_scores.append(0)

            if score > highest_scores[level-1]:
                highest_scores[level-1] = score

        clock.tick(snake_speed)

    pygame.quit()
    quit()

def start_menu():
    menu = True
    global snake_color, current_color_index

    while menu:
        dis.fill(white)
        message("Welcome to the Mmabia Snake Game", black, -50)
        message("Designed By : Boateng Prince Agyenim", black, -20)
        message("Press P to Play, C to Customize, or Q to Quit", black, 10)
        message("Press E for Easy Mode or H for Hard Mode", black, 70)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu = False
                    gameLoop("Easy")
                elif event.key == pygame.K_e:
                    menu = False
                    gameLoop("Easy")
                elif event.key == pygame.K_h:
                    menu = False
                    gameLoop("Hard")
                elif event.key == pygame.K_c:
                    customization_menu()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def customization_menu():
    customizing = True
    global snake_color, current_color_index

    while customizing:
        dis.fill(white)
        message("Customization Menu", black, -50)
        message(f"Current Snake Color: {snake_colors[current_color_index]}", black, 10)
        message("Press LEFT/RIGHT to Change Color, ENTER to Confirm", black, 50)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_color_index = (current_color_index - 1) % len(snake_colors)
                    snake_color = snake_colors[current_color_index]
                elif event.key == pygame.K_RIGHT:
                    current_color_index = (current_color_index + 1) % len(snake_colors)
                    snake_color = snake_colors[current_color_index]
                elif event.key == pygame.K_RETURN:
                    customizing = False
                    start_menu()

if __name__ == "__main__":
    start_menu()