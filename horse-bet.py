import random
import pygame
import sys
import os

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
GRAY = (128, 128, 128)

# Initial balance
INITIAL_BALANCE = 10000

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
        # Try to load image from file, use colored rectangle if file not found
        try:
            image_path = os.path.join("horses", f"{horse.lower()}.png")
            image = pygame.image.load(image_path).convert_alpha()
        except pygame.error:
            image = pygame.Surface((80, 60))
            image.fill(random.choice([RED, GREEN, BLUE, GOLD, SILVER]))
        images[horse] = pygame.transform.scale(image, (80, 60))
    return images

horse_images = load_horse_images()

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.topleft = (x, y)
    screen.blit(text_surface, text_rect)

def betting_screen():
    global INITIAL_BALANCE
    selected_horse = None
    bet_amount = 0
    bet_buttons = [5, 10, 25, 100, 1000, 10000]
    button_width = 100
    button_height = 40
    button_margin = 10
    total_height = len(bet_buttons) * (button_height + button_margin) - button_margin

    while True:
        screen.fill(WHITE)
        draw_text("Horse Betting", large_font, BLACK, 300, 50)
        draw_text(f"Balance: ${INITIAL_BALANCE}", font, BLACK, 550, 50)
        draw_text(f"Current bet: ${bet_amount}", font, BLACK, 50, 100)

        # Calculate the starting y-position for bet buttons
        start_y = 150
        if start_y + total_height > HEIGHT - 150:  # Check if buttons would overlap with bottom area
            start_y = HEIGHT - 150 - total_height

        # Draw horse selection
        for i, horse in enumerate(horses):
            color = RED if i == selected_horse else BLACK
            draw_text(f"{horse} (Odds: {odds[i]}/1)", font, color, 50, start_y + i * 40)

        # Draw bet increase buttons
        for i, amount in enumerate(bet_buttons):
            y = start_y + i * (button_height + button_margin)
            color = GREEN if bet_amount + amount <= INITIAL_BALANCE else GRAY
            pygame.draw.rect(screen, color, (WIDTH - 150, y, button_width, button_height))
            draw_text(f"+{amount}", font, BLACK, WIDTH - 140, y + 5)

        # Draw place bet and reset bet buttons
        pygame.draw.rect(screen, BLUE, (WIDTH - 200, HEIGHT - 100, 180, 40))
        draw_text("Place Bet", font, WHITE, WIDTH - 180, HEIGHT - 95)
        pygame.draw.rect(screen, RED, (WIDTH - 200, HEIGHT - 150, 180, 40))
        draw_text("Reset Bet", font, WHITE, WIDTH - 180, HEIGHT - 145)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Horse selection
                for i in range(len(horses)):
                    if 50 <= mouse_pos[0] <= 400 and start_y + i * 40 <= mouse_pos[1] <= start_y + (i + 1) * 40:
                        selected_horse = i
                # Bet increase buttons
                for i, amount in enumerate(bet_buttons):
                    y = start_y + i * (button_height + button_margin)
                    if WIDTH - 150 <= mouse_pos[0] <= WIDTH - 50 and y <= mouse_pos[1] <= y + button_height:
                        if bet_amount + amount <= INITIAL_BALANCE:
                            bet_amount += amount
                # Place bet button
                if WIDTH - 200 <= mouse_pos[0] <= WIDTH - 20 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 60:
                    if selected_horse is not None and bet_amount > 0:
                        return selected_horse, bet_amount
                # Reset bet button
                if WIDTH - 200 <= mouse_pos[0] <= WIDTH - 20 and HEIGHT - 150 <= mouse_pos[1] <= HEIGHT - 110:
                    bet_amount = 0

        # Ensure bet doesn't exceed balance
        bet_amount = min(bet_amount, INITIAL_BALANCE)

def race_screen(selected_horse, bet_amount):
    horse_positions = {horse: 0 for horse in horses}
    race_results = []
    finish_line_x = WIDTH - 100  # Position of the finish line
    
    # Create checkered pattern for finish line
    checker_size = 20
    checker_pattern = pygame.Surface((checker_size * 2, HEIGHT))
    checker_pattern.fill(WHITE)
    for y in range(0, HEIGHT, checker_size * 2):
        pygame.draw.rect(checker_pattern, BLACK, (0, y, checker_size, checker_size))
        pygame.draw.rect(checker_pattern, BLACK, (checker_size, y + checker_size, checker_size, checker_size))

    while True:
        screen.fill(WHITE)
        draw_text("Horse Race", large_font, BLACK, 300, 50)

        # Draw finish line
        screen.blit(checker_pattern, (finish_line_x, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        racing = True
        while racing:
            for horse in horses:
                if horse not in [h for h, _ in race_results]:
                    horse_positions[horse] += random.randint(1, 10)
                    if horse_positions[horse] >= finish_line_x:
                        race_results.append((horse, odds[horses.index(horse)]))
            draw_race(horse_positions, finish_line_x, race_results)
            pygame.time.delay(50)
            
            # Continue racing until all horses have finished
            if len(race_results) == len(horses):
                racing = False

        # Display "Race Finished!" message
        draw_text("Race Finished!", large_font, RED, WIDTH // 2 - 100, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(2000)  # Wait for 2 seconds before showing results

        return race_results, selected_horse, bet_amount

def draw_race(horse_positions, finish_line_x, race_results):
    for i, horse in enumerate(horses):
        if horse in [h for h, _ in race_results]:
            position = [h for h, _ in race_results].index(horse)
            y = 100 + position * 80  # Position based on finish order
        else:
            y = 100 + i * 80  # Original position if not finished
        screen.blit(horse_images[horse], (horse_positions[horse], y))
    
    # Draw finish line
    checker_size = 20
    for y in range(0, HEIGHT, checker_size * 2):
        pygame.draw.rect(screen, BLACK, (finish_line_x, y, checker_size, checker_size))
        pygame.draw.rect(screen, BLACK, (finish_line_x, y + checker_size, checker_size, checker_size))
    
    pygame.display.flip()

def results_screen(race_results, selected_horse, bet_amount):
    global INITIAL_BALANCE
    original_balance = INITIAL_BALANCE  # Store the original balance before the bet

    while True:
        screen.fill(WHITE)
        draw_text("Results", large_font, BLACK, WIDTH // 2 - 50, 50)

        # Draw podium (moved to bottom middle with podiums next to each other)
        podium_base_y = HEIGHT - 150
        podium_width = 100
        podium_spacing = 10  # Small space between podiums
        total_width = 3 * podium_width + 2 * podium_spacing
        start_x = WIDTH // 2 - total_width // 2

        pygame.draw.rect(screen, SILVER, (start_x, podium_base_y + 50, podium_width, 50))  # 2nd place (left)
        pygame.draw.rect(screen, GOLD, (start_x + podium_width + podium_spacing, podium_base_y, podium_width, 100))  # 1st place (middle)
        pygame.draw.rect(screen, BRONZE, (start_x + 2 * (podium_width + podium_spacing), podium_base_y + 75, podium_width, 25))  # 3rd place (right)

        # Draw horses on podium
        podium_positions = [
            (start_x + podium_width // 2 - 40, podium_base_y - 10),  # 2nd place
            (start_x + podium_width + podium_spacing + podium_width // 2 - 40, podium_base_y - 60),  # 1st place
            (start_x + 2 * (podium_width + podium_spacing) + podium_width // 2 - 40, podium_base_y + 15)  # 3rd place
        ]
        for i, (horse, _) in enumerate(race_results[:3]):
            x, y = podium_positions[i]
            screen.blit(horse_images[horse], (x, y))

        # Draw horse names
        for i, (horse, _) in enumerate(race_results[:3]):
            text = font.render(horse, True, BLACK)
            x = start_x + podium_width // 2 + i * (podium_width + podium_spacing)
            y = HEIGHT - 30
            screen.blit(text, (x - text.get_width()//2, y))

        # Draw result message and update balance
        selected_horse_name = horses[selected_horse]
        selected_horse_position = next((i for i, (h, _) in enumerate(race_results) if h == selected_horse_name), -1)
        
        if selected_horse_position == 0:  # First place
            winnings = bet_amount * odds[selected_horse]
            INITIAL_BALANCE = original_balance + winnings  # Add winnings to original balance
            result_text = large_font.render(f"You Won ${winnings}!", True, GOLD)
        else:
            INITIAL_BALANCE = original_balance - bet_amount  # Subtract the bet amount once
            result_text = large_font.render(f"You Lost ${bet_amount}.", True, BLACK)
            position_text = font.render(f"Your horse finished in {selected_horse_position + 1}{'st' if selected_horse_position == 0 else 'nd' if selected_horse_position == 1 else 'rd' if selected_horse_position == 2 else 'th'} place.", True, BLACK)
            screen.blit(position_text, (WIDTH//2 - position_text.get_width()//2, 200))
        
        screen.blit(result_text, (WIDTH//2 - result_text.get_width()//2, 100))

        # Display updated balance
        balance_text = font.render(f"New Balance: ${INITIAL_BALANCE}", True, BLACK)
        screen.blit(balance_text, (WIDTH//2 - balance_text.get_width()//2, 150))

        # Add larger button to return to main menu
        button_width = 250
        button_height = 50
        pygame.draw.rect(screen, GREEN, (WIDTH // 2 - button_width // 2, HEIGHT - 280, button_width, button_height))
        draw_text("Return to Main Menu", font, BLACK, WIDTH // 2 - button_width // 2 + 10, HEIGHT - 275)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if WIDTH // 2 - button_width // 2 <= event.pos[0] <= WIDTH // 2 + button_width // 2 and HEIGHT - 280 <= event.pos[1] <= HEIGHT - 280 + button_height:
                    return  # Return to main menu

def main():
    global INITIAL_BALANCE
    while True:
        selected_horse, bet_amount = betting_screen()
        race_results, selected_horse, bet_amount = race_screen(selected_horse, bet_amount)
        results_screen(race_results, selected_horse, bet_amount)
        # The game will return here after the results screen, ready for the next bet

if __name__ == "__main__":
    main()