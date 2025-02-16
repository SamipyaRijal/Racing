import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Displaying Score")

# Colors
BLUE = (50, 150, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)
BLACK = (0,0,0)

# Font setup
font_large = pygame.font.SysFont("arialblack", 70)  # Boom Productions
font_small = pygame.font.SysFont("arial", 50)  # presents & Play button

def display_end_score(score):
    int(score)

    screen.fill(BLUE)
    
    score_obj = font_small
    score_txt = score_obj.render((f"Score: {score:.2f}"), 1, WHITE )
    screen.blit(score_txt, (WIDTH//2 - 140, HEIGHT//2 - 100))
    pygame.display.update()
    
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return


def fade_in_buttons(score):
    int(score)

    play_button_rect = pygame.Rect(WIDTH//4 - 150, HEIGHT//2 + 50, 300, 80)
    quit_button_rect = pygame.Rect(3*WIDTH//4 - 150 , HEIGHT//2 + 50, 300, 80)

    play_text = font_small.render("Play Again", True, DARK_GRAY)
    quit_text = font_small.render("Quit", True, DARK_GRAY)
    
    alpha = 0  # Start fully transparent
    running = True
    screen.fill(BLUE)
    display_end_score(score)
    while running:

        # Keep "RACING!" visible

        # Increase alpha to fade in
        if alpha < 255:
            alpha += 10
        play_surface = play_text.copy()
        play_surface.set_alpha(alpha)

        quit_surface = quit_text.copy()
        quit_surface.set_alpha(alpha)

        # Draw button
        pygame.draw.rect(screen, GRAY, play_button_rect, border_radius=10)
        screen.blit(play_surface, play_surface.get_rect(center=play_button_rect.center))

        pygame.draw.rect(screen, GRAY, quit_button_rect, border_radius=10)
        screen.blit(quit_surface, quit_surface.get_rect(center=quit_button_rect.center))

        pygame.display.update()
        time.sleep(0.1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Exit the game when Esc key is pressed
                    pygame.quit()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    running = False  # Exit loop when Play is clicked
                    return True
                if quit_button_rect.collidepoint(event.pos):
                    running = False
                    return False


if __name__ == "__main__":
    score = 10  #Replace with a variable that stores speed

    display_end_score(score)
    time.sleep(1)

    fade_in_buttons(score)
    time.sleep(10)

    pygame.quit()