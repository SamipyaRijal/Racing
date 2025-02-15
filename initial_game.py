import pygame
import sys
import random
import os

# Add the path to the folder containing slider_testing.py
sys.path.append(os.path.join(os.path.dirname(__file__), 'src', 'Electrical Code', 'Testing'))

# Import the get_slider_value function from slider_testing.py
from slider_testing import get_slider_value



# Initialize Pygame
pygame.init()

# Set up screen dimensions (fullscreen)
info = pygame.display.Info()  # Get display info
WIDTH, HEIGHT = info.current_w, info.current_h  # Set screen size to fullscreen width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Set the display mode to fullscreen
pygame.display.set_caption("Car Game")

# Define colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
DARK_GREY = (50, 50, 50)
TRACK_EDGE_COLOR = (200, 200, 200)  # Color of the track edges (like lane lines)

# Load images
car_image = pygame.image.load("car.png")  # Replace with the actual path to your car image
car_width, car_height = car_image.get_size()  # Get the original size of the car image

# Resize the car to a new size (for example, 100x60)
new_car_width = 100
new_car_height = 60
car_image = pygame.transform.scale(car_image, (new_car_width, new_car_height))  # Resize the car image
car_width, car_height = car_image.get_size()  # Update the width and height of the resized car

# Obstacle properties
obstacle_width = 50
obstacle_height = 30
base_obstacle_speed = 5  # Base speed for obstacles, adjusted dynamically

# Define the Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = car_width
        self.height = car_height
        self.speed = 5  # Speed of the car (this will control the obstacles' speed)

    def y_position(self):
        joystick_ratio = HEIGHT
        self.y = get_slider_value() * joystick_ratio


#----------------------------Moving FUncs-----------------------------------#

    # def move_up(self):
    #     if self.y > 0:  # Prevent car from going off the screen
    #         self.y -= 5

    # def move_down(self):
    #     if self.y < HEIGHT - self.height:  # Prevent car from going off the screen
    #         self.y += 5

#---------------------------------------------------------------#

    def draw(self):
        screen.blit(car_image, (self.x, self.y))  # Draw the resized car image at the current position

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Define the Obstacle class
class Obstacle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = obstacle_width
        self.height = obstacle_height
        self.speed = base_obstacle_speed  # Initial speed for obstacles

    def move(self):
        self.x -= self.speed  # Move the obstacle left by the current speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Initialize car object
car = Car(10, HEIGHT // 2 - car_height // 2)

# List to store obstacles
obstacles = []

# Initialize scrolling background properties
bg_x = 0  # Starting position for the background
bg_width = 200  # Width of the background section to repeat (for the race track)
track_width = 200  # Width of the race track (you can adjust this to fit your design)
bg_speed_multiplier = 0.5  # Multiplier to make the background move slower than the obstacles

# Lane lines properties
lane_line_width = 5  # Width of the dashed lane lines
lane_line_gap = 40  # Gap between each dashed lane line

# Game loop
running = True
clock = pygame.time.Clock()
obstacle_creation_timer = 0  # Timer to control the frequency of obstacle creation
min_gap_between_obstacles = 150  # Minimum distance between obstacles (in pixels)
max_gap_between_obstacles = 300  # Maximum distance between obstacles (in pixels)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # Get the keys pressed by the player
    keys = pygame.key.get_pressed()

    car.y_position()

    ### ------------------------ HEAD --------------------------------- ###

    # # Move the car using W and S keys (up and down)
    # if keys[pygame.K_w]:  # Move the car up with W
    #     car.move_up()
    # if keys[pygame.K_s]:  # Move the car down with S
    #     car.move_down()

    #---------------------------------------------------------------#


    # Speed up or slow down the obstacles based on user input (A = faster, D = slower)
    if keys[pygame.K_a]:  # Speed up (A key)
        car.speed = min(15, car.speed + 0.1)  # Cap speed at 15
    if keys[pygame.K_d]:  # Slow down (D key)
        car.speed = max(1, car.speed - 0.1)  # Prevent speed from going below 1

    # Dynamically adjust obstacle speed based on car speed
    for obstacle in obstacles:
        obstacle.speed = car.speed

    # Periodically create obstacles across the center of the screen (left to right)
    obstacle_creation_timer += 1
    if obstacle_creation_timer > 60:  # Create an obstacle every second (60 FPS)
        obstacle_creation_timer = 0
        gap = random.randint(min_gap_between_obstacles, max_gap_between_obstacles)
        obstacle_x_pos = WIDTH + gap  # Position the new obstacle at the right side of the screen
        obstacle_y_pos = random.randint(0, HEIGHT - obstacle_height)  # Random vertical position in the center
        obstacles.append(Obstacle(obstacle_x_pos, obstacle_y_pos))

    # Move obstacles and remove those that are off the screen
    for obstacle in obstacles[:]:
        obstacle.move()
        if obstacle.x + obstacle.width < 0:
            obstacles.remove(obstacle)

    # Collision detection
    car_rect = car.get_rect()
    for obstacle in obstacles:
        if car_rect.colliderect(obstacle.get_rect()):
            print("Game Over!")
            running = False

    # Move the background to create the illusion of motion (like the obstacles)
    bg_speed = car.speed * bg_speed_multiplier  # Update the background speed based on car speed
    bg_x -= bg_speed  # Move the background left, creating the illusion of motion

    # Reset the background once it moves off the screen
    if bg_x <= -bg_width:
        bg_x = 0

    # Fill the screen with the background color (dark grey)
    screen.fill(DARK_GREY)  # Dark grey background for the track

    # Draw the track edges (race track lines) along with the background
    pygame.draw.rect(screen, TRACK_EDGE_COLOR, (0, 0, track_width, HEIGHT))  # Left track edge
    pygame.draw.rect(screen, TRACK_EDGE_COLOR, (WIDTH - track_width, 0, track_width, HEIGHT))  # Right track edge

    # Draw the moving background (dark grey track) from right to left
    # Repeat the background to create the illusion of continuous motion
    screen.fill(DARK_GREY, (bg_x, 0, WIDTH, HEIGHT))  # Draw the current piece of the background
    screen.fill(DARK_GREY, (bg_x + bg_width, 0, WIDTH, HEIGHT))  # Repeat the background for a seamless effect

    # Draw dashed lane lines in the center of the screen (move right to left)
    for i in range(0, HEIGHT, lane_line_gap):  # Draw a series of dashed lines vertically spaced by lane_line_gap
        # We calculate the horizontal position of each lane line based on the background's x position
        # We use (bg_x % lane_line_gap) to create a continuous scrolling effect of the lane lines
        pygame.draw.rect(screen, WHITE, (WIDTH // 2 - lane_line_width // 2 + bg_x % lane_line_gap, i, lane_line_width, 20))

    # Draw the car
    car.draw()

    # Draw all obstacles
    for obstacle in obstacles:
        obstacle.draw()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
