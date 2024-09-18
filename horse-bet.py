import random
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Horse Betting Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

# Horse data
horses = ["Thunder", "Lightning", "Blaze", "Shadow", "Spirit"]
odds = [2, 3, 5, 10, 20]

# Load horse images
def load_horse_images():
    images = {}
    for horse in horses:
        images[horse] = pygame.image.load(f"assets/{horse.lower()}.png").convert_alpha()
        images[horse] = pygame.transform.scale(images[horse], (80, 60))
    return images

horse_images = load_horse_images()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def betting_screen():
    selected_horse = None
    bet_amount = 0
    input_active = False
    input_text = ""

    while True:
        screen.fill(WHITE)
        draw_text("Horse Betting", large_font, BLACK, 300, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 100 <= event.pos[1] <= 300:
                    selected_horse = (event.pos[1] - 100) // 40
                if 400 <= event.pos[1] <= 440 and 300 <= event.pos[0] <= 500:
                    input_active = True
                else:
                    input_active = False
                if 500 <= event.pos[1] <= 540 and 300 <= event.pos[0] <= 500:
                    if selected_horse is not None and bet_amount > 0:
                        return selected_horse, bet_amount
            if event.type == pygame.KEYDOWN and input_active:
                if event.key == pygame.K_RETURN:
                    try:
                        bet_amount = float(input_text)
                    except ValueError:
                        bet_amount = 0
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

        for i, (horse, odd) in enumerate(zip(horses, odds)):
            color = RED if i == selected_horse else BLACK
            draw_text(f"{horse} (Odds: {odd}/1)", font, color, 100, 100 + i * 40)

        pygame.draw.rect(screen, BLACK, (300, 400, 200, 40), 2)
        draw_text(input_text, font, BLACK, 310, 410)
        draw_text(f"Bet: ${bet_amount:.2f}", font, BLACK, 100, 420)

        pygame.draw.rect(screen, GREEN, (300, 500, 200, 40))
        draw_text("Place Bet", font, BLACK, 340, 510)

        pygame.display.flip()

def race_screen(selected_horse, bet_amount):
    horse_positions = {horse: 0 for horse in horses}
    race_results = []

    while True:
        screen.fill(WHITE)
        draw_text("Horse Race", large_font, BLACK, 300, 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        racing = True
        while racing:
            for horse in horses:
                if horse not in race_results:
                    horse_positions[horse] += random.randint(1, 10)
                    if horse_positions[horse] >= WIDTH - 100:
                        race_results.append((horse, odds[horses.index(horse)]))
                        if len(race_results) == len(horses):
                            racing = False
            draw_race(horse_positions)
            pygame.time.delay(50)

        return race_results, selected_horse, bet_amount

def draw_race(horse_positions):
    for horse, x in horse_positions.items():
        screen.blit(horse_images[horse], (x, 200))
    pygame.display.flip()

def results_screen(race_results, selected_horse, bet_amount):
    while True:
        screen.fill(WHITE)
        draw_text("Results", large_font, BLACK, 300, 50)

        # Draw podium
        pygame.draw.rect(screen, GOLD, (250, 400, 100, 100))
        pygame.draw.rect(screen, SILVER, (100, 450, 100, 50))
        pygame.draw.rect(screen, BRONZE, (400, 475, 100, 25))

        # Draw horses on podium
        for i, (horse, _) in enumerate(race_results[:3]):
            x = 110 if i == 1 else (260 if i == 0 else 410)
            y = 390 if i == 0 else (400 if i == 1 else 415)
            screen.blit(horse_images[horse], (x, y))

        # Draw horse names
        for i, (horse, _) in enumerate(race_results[:3]):
            text = font.render(horse, True, BLACK)
            x = 100 if i == 1 else (250 if i == 0 else 400)
            y = 510 if i == 1 else (510 if i == 0 else 510)
            screen.blit(text, (x + 50 - text.get_width()//2, y))

        # Draw result message
        if race_results[0][0] == horses[selected_horse]:
            result_text = large_font.render("You Won!", True, GOLD)
        else:
            result_text = large_font.render("You Lose.", True, BLACK)
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 50))

        # Draw user's horse placement if not in top 3
        user_horse = horses[selected_horse]
        user_place = next(i for i, (h, _) in enumerate(race_results) if h == user_horse) + 1
        if user_place > 3:
            place_text = font.render(f"Your horse placed {user_place}th", True, BLACK)
            screen.blit(place_text, (WIDTH - place_text.get_width() - 10, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

def main():
    while True:
        selected_horse, bet_amount = betting_screen()
        race_results, selected_horse, bet_amount = race_screen(selected_horse, bet_amount)
        results_screen(race_results, selected_horse, bet_amount)

if __name__ == "__main__":
    main()