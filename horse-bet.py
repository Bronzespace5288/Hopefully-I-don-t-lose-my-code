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

# Add this at the top of your file
net_result = 0  # Global variable to track net result

def betting_screen():
    global INITIAL_BALANCE, net_result
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
        draw_text(f"Net Result: ${net_result}", font, BLACK, 550, 90)  # Display net result
        draw_text(f"Current bet: ${bet_amount}", font, BLACK, 50, 100)

        # Calculate the starting y-position for bet buttons
        start_y = 150
        if start_y + total_height > HEIGHT - 150:
            start_y = HEIGHT - 150 - total_height

        # Draw horse selection with images
        for i, horse in enumerate(horses):
            color = RED if i == selected_horse else BLACK
            y = start_y + i * 70  # Increased spacing between horses
            screen.blit(horse_images[horse], (50, y))
            draw_text(f"{horse} (Odds: {odds[i]}/1)", font, color, 140, y + 20)

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
                    if 50 <= mouse_pos[0] <= 400 and start_y + i * 70 <= mouse_pos[1] <= start_y + (i + 1) * 70:
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
                        return selected_horse, bet_amount  # Return selected horse and bet amount
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

    # Player's bet info box
    info_box_width = 280  # Increased from 250 to 280
    info_box_height = 120
    info_box_x = 10
    info_box_y = HEIGHT - info_box_height - 10
    text_bg_color = (200, 200, 200)  # Light grey

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
            
            # Draw player's bet info box
            pygame.draw.rect(screen, GRAY, (info_box_x, info_box_y, info_box_width, info_box_height))
            selected_horse_name = horses[selected_horse]
            screen.blit(horse_images[selected_horse_name], (info_box_x + 10, info_box_y + 10))
            
            # Draw text backgrounds
            pygame.draw.rect(screen, text_bg_color, (info_box_x + 100, info_box_y + 20, 170, 30))  # Increased width from 140 to 170
            pygame.draw.rect(screen, text_bg_color, (info_box_x + 100, info_box_y + 60, 170, 30))  # Increased width from 140 to 170
            
            # Draw text
            draw_text(f"Bet: {selected_horse_name}", font, BLACK, info_box_x + 105, info_box_y + 25)
            draw_text(f"Amount: ${bet_amount}", font, BLACK, info_box_x + 105, info_box_y + 65)
            
            pygame.display.flip()
            pygame.time.delay(50)
            
            # Continue racing until all horses have finished
            if len(race_results) == len(horses):
                racing = False

        # Define winning_horse after the race is finished
        winning_horse = race_results[0][0] if race_results else None  # Get the first horse in race_results

        # Display final positions for a moment
        for _ in range(40):  # Show final positions for about 2 seconds
            draw_race(horse_positions, finish_line_x, race_results)
            pygame.display.flip()
            pygame.time.delay(50)

        # Display "Race Finished!" message
        draw_text("Race Finished!", large_font, RED, WIDTH // 2 - 100, HEIGHT // 2)
        pygame.display.flip()
        pygame.time.delay(2000)  # Wait for 2 seconds before showing results

        return race_results, selected_horse, bet_amount, winning_horse  # Return winning_horse

def draw_race(horse_positions, finish_line_x, race_results):
    # Define colors for positions
    position_colors = {
        0: GOLD,    # 1st place
        1: SILVER,  # 2nd place
        2: BRONZE   # 3rd place
    }

    # Sort horses based on their finish order or current position
    sorted_horses = sorted(horses, key=lambda h: (
        [r[0] for r in race_results].index(h) if h in [r[0] for r in race_results]
        else -horse_positions[h]
    ))

    for i, horse in enumerate(sorted_horses):
        y = 100 + i * 80  # Position based on current rank
        x = min(horse_positions[horse], finish_line_x)  # Ensure horse doesn't go past finish line
        screen.blit(horse_images[horse], (x, y))

        # Draw position circle
        if horse in [r[0] for r in race_results]:  # Only draw for finished horses
            position_index = [r[0] for r in race_results].index(horse)
            color = position_colors.get(position_index, GRAY)  # Default to gray if not in top 3
            pygame.draw.circle(screen, color, (x - 20, y + 30), 10)  # Draw circle to the left of the horse
            # Draw position number
            position_text = font.render(str(position_index + 1), True, BLACK)
            screen.blit(position_text, (x - 25, y + 25))  # Center the number in the circle

    # Draw finish line
    checker_size = 20
    for y in range(0, HEIGHT, checker_size * 2):
        pygame.draw.rect(screen, BLACK, (finish_line_x, y, checker_size, checker_size))
        pygame.draw.rect(screen, BLACK, (finish_line_x, y + checker_size, checker_size, checker_size))
    
    pygame.display.flip()

def results_screen(race_results, selected_horse, bet_amount, winning_horse):
    global INITIAL_BALANCE, net_result
    original_balance = INITIAL_BALANCE  # Store the original balance before the bet

    while True:
        screen.fill(WHITE)
        draw_text("Results", large_font, BLACK, WIDTH // 2 - 50, 50)

        # Draw podium
        podium_base_y = HEIGHT - 150
        podium_width = 100
        podium_spacing = 10  # Small space between podiums
        start_x = WIDTH // 2 - (3 * podium_width + 2 * podium_spacing) // 2

        # Draw podiums
        pygame.draw.rect(screen, SILVER, (start_x, podium_base_y + 50, podium_width, 50))  # 2nd place (left)
        pygame.draw.rect(screen, GOLD, (start_x + podium_width + podium_spacing, podium_base_y, podium_width, 100))  # 1st place (middle)
        pygame.draw.rect(screen, BRONZE, (start_x + 2 * (podium_width + podium_spacing), podium_base_y + 75, podium_width, 25))  # 3rd place (right)

        # Draw horses on podium based on their finishing positions
        podium_positions = [
            (start_x + podium_width // 2 - 40, podium_base_y - 10),  # 2nd place (left)
            (start_x + podium_width + podium_spacing + podium_width // 2 - 40, podium_base_y - 60),  # 1st place (middle)
            (start_x + 2 * (podium_width + podium_spacing) + podium_width // 2 - 40, podium_base_y + 15)  # 3rd place (right)
        ]
        
        # Draw the horses on the podium based on their finishing order
        for i in range(len(race_results)):
            horse, _ = race_results[i]  # Get the horse that finished in position i
            
            # Assign podium positions based on finishing order
            if i == 0:  # 1st place horse
                x, y = podium_positions[1]  # Draw on the gold podium
            elif i == 1:  # 2nd place horse
                x, y = podium_positions[0]  # Draw on the silver podium
            elif i == 2:  # 3rd place horse
                x, y = podium_positions[2]  # Draw on the bronze podium
            else:
                continue  # Skip any horses beyond the top 3

            screen.blit(horse_images[horse], (x, y))

            # Draw medals in the top right of the horse images
            medal_position = (x + 70, y + 10)  # Adjust these values as needed for positioning
            
            # Set medal colors based on finishing positions
            medal_color = GOLD if i == 0 else SILVER if i == 1 else BRONZE  # Gold for 1st, Silver for 2nd, Bronze for 3rd
            pygame.draw.circle(screen, medal_color, medal_position, 15)  # Draw the medal circle
            
            # Draw position number inside the medal
            position_text = font.render(str(i + 1), True, BLACK)
            text_rect = position_text.get_rect(center=medal_position)  # Center the text in the circle
            screen.blit(position_text, text_rect)

        # Draw horse names for only the top 3 horses
        for i in range(min(3, len(race_results))):
            horse, _ = race_results[i]
            text = font.render(horse, True, BLACK)
            x = start_x + podium_width // 2 + i * (podium_width + podium_spacing)
            y = HEIGHT - 30
            screen.blit(text, (x - text.get_width() // 2, y))

        # Draw result message and update balance
        selected_horse_name = horses[selected_horse]
        
        if selected_horse_name == winning_horse:  # Player's horse won
            winnings = bet_amount * odds[selected_horse]
            INITIAL_BALANCE = original_balance + winnings  # Add winnings to original balance
            net_result += winnings  # Update net result by adding winnings
            result_text = large_font.render(f"You Won ${winnings}!", True, GOLD)
        else:
            INITIAL_BALANCE = original_balance - bet_amount  # Subtract the bet amount once
            net_result -= bet_amount  # Update net result by subtracting the bet amount
            result_text = large_font.render(f"You Lost ${bet_amount}.", True, BLACK)
            selected_horse_position = next((i for i, (h, _) in enumerate(race_results) if h == selected_horse_name), -1)
            position_text = font.render(f"Your horse finished in {selected_horse_position + 1}{'st' if selected_horse_position == 0 else 'nd' if selected_horse_position == 1 else 'rd' if selected_horse_position == 2 else 'th'} place.", True, BLACK)
            screen.blit(position_text, (WIDTH // 2 - position_text.get_width() // 2, 200))
        
        screen.blit(result_text, (WIDTH // 2 - result_text.get_width() // 2, 100))

        # Display net result
        net_result_text = f"Net Result: ${net_result}"  # Format net result text
        balance_text = font.render(net_result_text, True, BLACK)
        screen.blit(balance_text, (WIDTH // 2 - balance_text.get_width() // 2, 150))

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

        # Break the loop after displaying results
        pygame.display.flip()
        pygame.time.delay(2000)  # Pause to show results
        break  # Exit the results screen loop

def main():
    global INITIAL_BALANCE, net_result
    while True:
        selected_horse, bet_amount = betting_screen()
        race_results, selected_horse, bet_amount, winning_horse = race_screen(selected_horse, bet_amount)  # Capture winning_horse
        results_screen(race_results, selected_horse, bet_amount, winning_horse)  # Pass winning_horse to results_screen

if __name__ == "__main__":
    main()