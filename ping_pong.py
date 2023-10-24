import pygame
import random
import time
import sys


pygame.init()
# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Ping Pong")
player1_score = 0
player2_score = 0

# Set up the ball
ball_x = screen_width / 2
ball_y = screen_height / 2
ball_radius = 10
ball_speed_x = random.choice([-3, 3])
ball_speed_y = random.choice([-3, 3])

# Initialize the gamepads
pygame.joystick.init()

joysticks = []

for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)


# Set up the paddles
paddle_width = 20
paddle_height = 100
paddle_speed = 5

player1_paddle = pygame.Rect(50, screen_height/2 - paddle_height/2, paddle_width, paddle_height)
player2_paddle = pygame.Rect(screen_width - 50 - paddle_width, screen_height/2 - paddle_height/2, paddle_width, paddle_height)


player1_paddle_x = 50
player1_paddle_y = screen_height // 2 - paddle_height // 2

player2_paddle_x = screen_width - 50 - paddle_width
player2_paddle_y = screen_height // 2 - paddle_height // 2


# Game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if(len(joysticks) >= 2):
        if joysticks[0].get_axis(1) < -0.5:
            player1_paddle.move_ip(0, -paddle_speed)
        elif joysticks[0].get_axis(1) > 0.5:
            player1_paddle.move_ip(0, paddle_speed)
        if joysticks[1].get_axis(1) < -0.5:
            player2_paddle.move_ip(0, -paddle_speed)
        elif joysticks[1].get_axis(1) > 0.5:
            player2_paddle.move_ip(0, paddle_speed)

    # Move the paddles
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player1_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_s]:
        player1_paddle.move_ip(0, paddle_speed)
    if keys[pygame.K_UP]:
        player2_paddle.move_ip(0, -paddle_speed)
    if keys[pygame.K_DOWN]:
        player2_paddle.move_ip(0, paddle_speed)

    # Keep the paddles on the screen
    player1_paddle_y = max(0, player1_paddle_y)
    player1_paddle_y = min(screen_height - paddle_height, player1_paddle_y)

    player2_paddle_y = max(0, player2_paddle_y)
    player2_paddle_y = min(screen_height - paddle_height, player2_paddle_y)

    # Move the ball
    ball_x += ball_speed_x
    ball_y += ball_speed_y

    # Handle collisions
    if ball_x < 0 or ball_x > screen_width:
        ball_speed_x *= -1
    if ball_y < 0 or ball_y > screen_height:
        ball_speed_y *= -1
    if player1_paddle.collidepoint(ball_x, ball_y) or player2_paddle.collidepoint(ball_x, ball_y):
        ball_speed_x *= -1

    # Draw the game objects
        # Clear the screen
    screen.fill((0, 0, 0))

    # Draw the paddles
    pygame.draw.rect(screen, (255, 255, 255), player1_paddle)
    pygame.draw.rect(screen, (255, 255, 255), player2_paddle)

    # Draw the ball
    pygame.draw.circle(screen, (255, 255, 255), (int(ball_x), int(ball_y)), ball_radius)

    # Check for scoring
    if ball_x < 0:
        player2_score += 1
        print("Player 2 scores!")
        ball_x, ball_y = screen_width // 2, screen_height // 2
        ball_speed_x *= -1
    elif ball_x > screen_width:
        player1_score += 1
        print("Player 1 scores!")
        ball_x, ball_y = screen_width // 2, screen_height // 2
        ball_speed_x *= -1

    # Draw the scores
    font = pygame.font.SysFont(None, 30)
    player1_score_text = font.render("Player 1: " + str(player1_score), True, (255, 255, 255))
    player2_score_text = font.render("Player 2: " + str(player2_score), True, (255, 255, 255))
    screen.blit(player1_score_text, (20, 20))
    screen.blit(player2_score_text, (screen_width - player2_score_text.get_width() - 20, 20))
    # Update the screen
    pygame.display.update()

    # Wait for a short period of time
    time.sleep(0.01)
