import pygame
import sys
import random
import os
import time

import death_screen as ds
import Start_screen as ss

# Add the path to the folder containing slider_testing.py
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src', 'Electrical Code', 'Testing'))
# Import the get_slider_value function from slider_testing.py
from slider_testing import get_slider_value
from button_testing import getRed_or_Green


# Initialize Pygame
pygame.init()

# Set up screen dimensions (fullscreen)
info = pygame.display.Info()  # Get display info
WIDTH, HEIGHT = info.current_w, info.current_h  # Set screen size to fullscreen width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)  # Set the display mode to fullscreen
pygame.display.set_caption("Car Game")

#Define fonts used
font_large = pygame.font.SysFont("arialblack", 70)  # Boom Productions
font_small = pygame.font.SysFont("arial", 50)  # presents & Play button
font_racing = pygame.font.SysFont("arialblack", 100)  # RACING! Title

# Define colors
BLUE = (50, 150, 255)
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

    def y_position(self):
        joystick_ratio = HEIGHT-20
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

# Define the WhiteBlock class (for the constant white blocks)
class WhiteBlock:
    def __init__(self, x, y):
        self.x = x  # X position of the block
        self.y = y  # Y position of the block
        self.width = 20  # Width of each white block
        self.height = 20  # Height of each white block
        self.speed = 200  # This will be updated based on car speed (in pixels/s)

    def move(self, delta_time):
        # Move the block left with speed adjusted by delta_time
        self.x -= self.speed * delta_time

    def draw(self):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Define the OtherCar class (for the cars that the player has to dodge)
class OtherCar:
    def __init__(self, x, y, speed):
        self.x = x  # X position of the car (start from the right side)
        self.y = y  # Y position of the car (randomized vertical position)
        self.width = 60  # Width of each other car
        self.height = 40  # Height of each other car
        self.speed = speed  # Speed of the car relative to the player's car (in pixels/s)

    def move(self, delta_time):
        # Move the car left based on speed
        self.x -= self.speed * delta_time

    def draw(self):
        pygame.draw.rect(screen, CAR_COLOR, (self.x, self.y, self.width, self.height))

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

#Start Screen 
screen.fill(BLUE)
racing_text = font_racing.render("RACING!", True, GREEN)
screen.blit(racing_text, racing_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
pygame.display.update()
time.sleep(2)  # Short delay before the button appears

# Play button fades in
while(1):
    if ss.fade_in_button():
        break


# Initialize car object
car = Car(10, HEIGHT // 2 - car_height // 2)

# List to store white blocks and other cars
white_blocks = []
other_cars = []

# Initialize scrolling background properties
bg_x = 0  # Starting position for the background
bg_width = 200  # Width of the background section to repeat (for the race track)
track_width = 200  # Width of the race track (you can adjust this to fit your design)
bg_speed_multiplier = 1  # Set multiplier to 1 for direct correlation with car speed

# Game loop
running = True
car_collied = False
clock = pygame.time.Clock()

# Constantly create white blocks at regular intervals from 0 to 100000
white_block_gap = 60  # Horizontal gap between blocks
max_x_position = 10000  # Max X position (end of the generated range)

# Vertical position for the row of white blocks (in the center of the screen)
middle_y = HEIGHT // 2 - 10  # The Y-coordinate for the row of blocks (center of screen)

# Generate blocks between 0 and max_x_position
for x_pos in range(0, max_x_position, white_block_gap):
    white_blocks.append(WhiteBlock(x_pos, middle_y))

# Function to create a new car
def create_other_car():
    # Randomized Y position on the road
    y_pos = random.randint(0, HEIGHT)  # Ensure the car stays within the screen bounds
    
    # Calculate the background speed and set the other cars' speed to a fixed offset
    speed_bg = car.speed * bg_speed_multiplier  # Speed of background
    speed_offset = 200  # Offset for other cars, relative to the background speed
    relative_speed = speed_bg - speed_offset  # Other cars move slower than background
    
    # Add a new car to the list
    other_cars.append(OtherCar(WIDTH, y_pos, relative_speed))

while running:
        
    while(car_collied==False):
        delta_time = clock.tick(60) / 1000  # Calculate delta time (time in seconds since the last frame)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Check if the user clicks the close button
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit the game when Esc key is pressed
                    running = False

        # Get the keys pressed by the player
        keys = pygame.key.get_pressed()

        car.y_position()

        ### ------------------------ Previous Move Code --------------------------------- ###

        # # Move the car using W and S keys (up and down)
        # if keys[pygame.K_w]:  # Move the car up with W
        #     car.move_up()
        # if keys[pygame.K_s]:  # Move the car down with S
        #     car.move_down()

        # # # Speed up or slow down the obstacles based on user input (A = faster, D = slower)
        # if keys[pygame.K_a]:  # Speed up (A key)
        #     car.speed = min(15, car.speed + 0.1)  # Cap speed at 15
        # if keys[pygame.K_d]:  # Slow down (D key)
        #     car.speed = max(1, car.speed - 0.1)  # Prevent speed from going below 1

        #--------------------------------------------------------------------------------
        
        #------------------------Button Implement--------------------------#

        button_colour = getRed_or_Green()

        if button_colour == 'green':  # Speed up (A key)
            car.speed = min(700, car.speed + 15)  # Cap speed at 15
        elif button_colour == 'red':  # Slow down (D key)
            car.speed = max(400, car.speed - 5)  # Prevent speed from going below 1


        #------------------------------------------------------------------#

        # Dynamically adjust obstacle speed based on car speed
        for block in white_blocks:
            block.speed = car.speed

        # Update the speed of all other cars based on the current car speed
        speed_bg = car.speed * bg_speed_multiplier  # Calculate background speed
        speed_offset = 50  # Offset for other cars
        for other_car in other_cars:
            other_car.speed = speed_bg - speed_offset  # Set other cars' speed relative to background

        # Move white blocks and remove those that are off the screen
        for block in white_blocks[:]:
            block.move(delta_time)
            if block.x + block.width < 0:  # If the block moves off the left side, reset its position
                # Move the block to the right (start of the range)
                block.x = max_x_position

        # Move the other cars and check for collisions
        for other_car in other_cars[:]:
            other_car.move(delta_time)
            if other_car.x + other_car.width < 0:  # If the other car moves off the left side, remove it
                other_cars.remove(other_car)

            # Check for collision with the player's car
            if car.get_rect().colliderect(other_car.get_rect()):
                car_collied = True  # End the game on collision

        # Occasionally spawn a new car
        if random.random() < 0.07:  # Increase the frequency of car spawns
            create_other_car()

        # Move the background to create the illusion of motion (like the obstacles)
        bg_speed = car.speed * bg_speed_multiplier  # Update the background speed based on car speed
        bg_x -= bg_speed * delta_time  # Move the background left, creating the illusion of motion

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

    if(car_collied):
        ds.display_end_score(score=10)
        while(1):
            if(ds.fade_in_buttons(score=10)==True):
                car_collied = False
                car.x = 0
                car.y = HEIGHT // 2 - car_height // 2
                break
            elif(ds.fade_in_buttons(score=10)==False):
                running = False
                # Quit Pygame
                pygame.quit()
                sys.exit()



