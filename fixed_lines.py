import pygame
import sys
import random

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
CAR_COLOR = (255, 0, 0)  # Color of other cars (red for visibility)

# Load images
car_image = pygame.image.load("car.png")  # Replace with the actual path to your car image
car_width, car_height = car_image.get_size()  # Get the original size of the car image

# Resize the car to a new size (for example, 100x60)
new_car_width = 100
new_car_height = 60
car_image = pygame.transform.scale(car_image, (new_car_width, new_car_height))  # Resize the car image
car_width, car_height = car_image.get_size()  # Update the width and height of the resized car

# Define the Car class
class Car:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = car_width
        self.height = car_height
        self.speed = 5  # Speed of the car (this will control the obstacles' speed)

    def move_up(self):
        if self.y > 0:  # Prevent car from going off the screen
            self.y -= 5

    def move_down(self):
        if self.y < HEIGHT - self.height:  # Prevent car from going off the screen
            self.y += 5

    def draw(self):
        screen.blit(car_image, (self.x, self.y))  # Draw the resized car image at the current position

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Define the WhiteBlock class (for the constant white blocks)
class WhiteBlock:
    def __init__(self, x, y):
        self.x = x  # X position of the block
        self.y = y  # Y position of the block
        self.width = 20  # Width of each white block
        self.height = 20  # Height of each white block
        self.speed = 5  # Speed for all blocks (move them all at the same speed)

    def move(self):
        self.x -= self.speed  # Move the block left with the same speed

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Define the OtherCar class (for the cars that the player has to dodge)
class OtherCar:
    def __init__(self, x, y):
        self.x = x  # X position of the car (start from the right side)
        self.y = y  # Y position of the car (randomized vertical position)
        self.width = 60  # Width of each other car
        self.height = 40  # Height of each other car
        self.speed = 2  # Speed of the car (slower than the background/road)

    def move(self):
        self.x -= self.speed  # Move the car left

    def draw(self):
        pygame.draw.rect(screen, CAR_COLOR, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Initialize car object
car = Car(10, HEIGHT // 2 - car_height // 2)

# List to store white blocks and other cars
white_blocks = []
other_cars = []

# Initialize scrolling background properties
bg_x = 0  # Starting position for the background
bg_width = 200  # Width of the background section to repeat (for the race track)
track_width = 200  # Width of the race track (you can adjust this to fit your design)
bg_speed_multiplier = 0.5  # Multiplier to make the background move slower than the obstacles

# Game loop
running = True
clock = pygame.time.Clock()

# Constantly create white blocks at regular intervals from 0 to 100000
white_block_gap = 60  # Horizontal gap between blocks
max_x_position = 100000  # Max X position (end of the generated range)

# Vertical position for the row of white blocks (in the center of the screen)
middle_y = HEIGHT // 2 - 10  # The Y-coordinate for the row of blocks (center of screen)

# Generate blocks between 0 and max_x_position
for x_pos in range(0, max_x_position, white_block_gap):
    white_blocks.append(WhiteBlock(x_pos, middle_y))

# Function to create a new car
def create_other_car():
    # Randomized Y position on the road
    y_pos = random.randint(0, HEIGHT - 40)  # Ensure the car stays within the screen bounds
    other_cars.append(OtherCar(WIDTH, y_pos))  # Create a car at the far right of the screen

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Check if the user clicks the close button
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Exit the game when Esc key is pressed
                running = False

    # Get the keys pressed by the player
    keys = pygame.key.get_pressed()

    # Move the car using W and S keys (up and down)
    if keys[pygame.K_w]:  # Move the car up with W
        car.move_up()
    if keys[pygame.K_s]:  # Move the car down with S
        car.move_down()

    # Speed up or slow down the obstacles based on user input (A = faster, D = slower)
    if keys[pygame.K_a]:  # Speed up (A key)
        car.speed = min(15, car.speed + 0.1)  # Cap speed at 15
    if keys[pygame.K_d]:  # Slow down (D key)
        car.speed = max(1, car.speed - 0.1)  # Prevent speed from going below 1

    # Dynamically adjust obstacle speed based on car speed
    for block in white_blocks:
        block.speed = car.speed

    # Move white blocks and remove those that are off the screen
    for block in white_blocks[:]:
        block.move()
        if block.x + block.width < 0:  # If the block moves off the left side, reset its position
            # Move the block to the right (start of the range)
            block.x = max_x_position

    # Move the other cars and check for collisions
    for other_car in other_cars[:]:
        other_car.move()
        if other_car.x + other_car.width < 0:  # If the other car moves off the left side, remove it
            other_cars.remove(other_car)

        # Check for collision with the player's car
        if car.get_rect().colliderect(other_car.get_rect()):
            running = False  # End the game on collision

    # Occasionally spawn a new car
    if random.random() < 0.02:  # Adjust this value to control frequency
        create_other_car()

    # Collision detection
    car_rect = car.get_rect()

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
    screen.fill(DARK_GREY, (bg_x, 0, WIDTH, HEIGHT))  # Draw the current piece of the background
    screen.fill(DARK_GREY, (bg_x + bg_width, 0, WIDTH, HEIGHT))  # Repeat the background for a seamless effect

    # Draw the white blocks (scrolling from right to left)
    for block in white_blocks:
        block.draw()

    # Draw the other cars
    for other_car in other_cars:
        other_car.draw()

    # Draw the player's car
    car.draw()

    # Update the display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
