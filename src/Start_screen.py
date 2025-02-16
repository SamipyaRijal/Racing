import pygame
import time

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fading Text with Button")

# Colors
BLUE = (50, 150, 255)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Font setup
font_large = pygame.font.SysFont("arialblack", 70)  # Boom Productions
font_small = pygame.font.SysFont("arial", 50)  # presents & Play button
font_racing = pygame.font.SysFont("arialblack", 100)  # RACING! Title

# Function to fade out text
def fade_out_texts(texts, colors, positions, fonts, fade_speed):
    alpha = 255
    text_surfaces = [fonts[i].render(texts[i], True, colors[i]).convert_alpha() for i in range(len(texts))]

    while alpha > 0:
        screen.fill(BLUE)

        for i in range(len(texts)):
            text_surfaces[i].set_alpha(alpha)
            screen.blit(text_surfaces[i], text_surfaces[i].get_rect(center=positions[i]))

        pygame.display.update()
        time.sleep(fade_speed)
        alpha -= 5

# Function to fade in the Play button
def fade_in_button():
    button_rect = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 80)
    play_text = font_small.render("Play", True, DARK_GRAY)
    
    alpha = 0  # Start fully transparent
    running = True
    screen.fill(BLUE)
    
    while running:

        # Keep "RACING!" visible
        racing_text = font_racing.render("RACING!", True, GREEN)
        screen.blit(racing_text, racing_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))

        # Increase alpha to fade in
        if alpha < 255:
            alpha += 5
        play_surface = play_text.copy()
        play_surface.set_alpha(alpha)

        # Draw button
        pygame.draw.rect(screen, GRAY, button_rect, border_radius=10)
        screen.blit(play_surface, play_surface.get_rect(center=button_rect.center))

        pygame.display.update()
        time.sleep(0.05)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    running = False  # Exit loop when Play is clicked
                    return True

# Run the fade-in/fade-out sequence
screen.fill(BLUE)

# "Boom Productions" and "presents" fade out together
fade_out_texts(
    ["Boom Productions", "presents"], 
    [WHITE, WHITE], 
    [(WIDTH//2, HEIGHT//3), (WIDTH//2, HEIGHT//3 + 80)], 
    [font_large, font_small], 
    0.05
)
if __name__ == "__main__":
    # "RACING!" stays on screen
    screen.fill(BLUE)
    racing_text = font_racing.render("RACING!", True, GREEN)
    screen.blit(racing_text, racing_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 100)))
    pygame.display.update()
    time.sleep(2)  # Short delay before the button appears

    # Play button fades in
    fade_in_button()

    pygame.quit()
