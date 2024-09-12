import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Blackjack")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
NEON_GREEN = (57, 255, 20)

# Card setup
CARD_WIDTH, CARD_HEIGHT = 71, 96
CARD_BACK = pygame.image.load(os.path.join('cards', 'back.png'))
cards = {}
for suit in ['hearts', 'diamonds', 'clubs', 'spades']:
    for value in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']:
        cards[f"{value}_of_{suit}"] = pygame.image.load(os.path.join('cards', f"{value}_of_{suit}.png"))

# Card values
card_values = {
    'ace': 11, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'jack': 10, 'queen': 10, 'king': 10
}

# Chip values and colors
chips = {
    5: (WHITE, "5"),
    10: (RED, "10"),
    25: (NEON_GREEN, "25"),
    100: (BLACK, "100")
}

def deal_card():
    return random.choice(list(cards.keys()))

def calculate_score(hand):
    score = sum(card_values[card.split('_')[0]] for card in hand)
    if 'ace' in [card.split('_')[0] for card in hand] and score > 21:
        score -= 10
    return score

def display_hand(hand, x, y, show_all=True):
    for i, card in enumerate(hand):
        if i == 0 or show_all:
            SCREEN.blit(cards[card], (x + i * 30, y))
        else:
            SCREEN.blit(CARD_BACK, (x + i * 30, y))

def display_text(text, x, y, font_size=32, color=BLACK):
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    SCREEN.blit(text_surface, (x, y))

def ai_play(hand):
    while calculate_score(hand) < 17 or (calculate_score(hand) < 21 and random.random() < 0.3):
        hand.append(deal_card())
    return hand

def draw_button(text, x, y, width, height, color, text_color):
    pygame.draw.rect(SCREEN, color, (x, y, width, height))
    font = pygame.font.Font(None, 32)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width/2, y + height/2))
    SCREEN.blit(text_surface, text_rect)

def draw_chip(value, x, y):
    color, text = chips[value]
    pygame.draw.circle(SCREEN, color, (x, y), 20)
    display_text(text, x-10, y-10, 20, WHITE if color == BLACK else BLACK)

def betting_phase(balance):
    bet = 0
    betting = True
    while betting:
        SCREEN.fill(GREEN)
        display_text(f"Your balance: ${balance}", 50, 50)
        display_text(f"Current bet: ${bet}", 50, 100)
        display_text("Click on chips to add to your bet. Press SPACE to confirm.", 50, HEIGHT - 50)

        for i, (value, (color, _)) in enumerate(chips.items()):
            draw_chip(value, 100 + i * 100, HEIGHT - 100)

        draw_button("Reset Bet", WIDTH - 200, HEIGHT - 100, 150, 40, YELLOW, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, value in enumerate(chips.keys()):
                    if ((mouse_pos[0] - (100 + i * 100))**2 + (mouse_pos[1] - (HEIGHT - 100))**2) <= 400:
                        if bet + value <= balance:
                            bet += value
                if WIDTH - 200 <= mouse_pos[0] <= WIDTH - 50 and HEIGHT - 100 <= mouse_pos[1] <= HEIGHT - 60:
                    bet = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and bet > 0:
                betting = False

    return bet

def play_game(balance):
    bet = betting_phase(balance)
    if bet is None:
        return None

    player_hand = []
    dealer_hand = []
    ai1_hand = []
    ai2_hand = []
    game_over = False
    player_stand = False
    can_double = True

    for _ in range(2):
        player_hand.append(deal_card())
        dealer_hand.append(deal_card())
        ai1_hand.append(deal_card())
        ai2_hand.append(deal_card())

    while not game_over:
        SCREEN.fill(GREEN)
        
        # Display all hands
        display_hand(dealer_hand, WIDTH//2 - CARD_WIDTH, 50, show_all=True)
        display_hand(player_hand, WIDTH//2 - CARD_WIDTH, HEIGHT - CARD_HEIGHT - 130)
        display_hand(ai1_hand, 50, HEIGHT//2 - CARD_HEIGHT//2)
        display_hand(ai2_hand, WIDTH - 2*CARD_WIDTH - 50, HEIGHT//2 - CARD_HEIGHT//2)
        
        # Display scores and bet
        dealer_score = calculate_score(dealer_hand)
        player_score = calculate_score(player_hand)
        ai1_score = calculate_score(ai1_hand)
        ai2_score = calculate_score(ai2_hand)
        
        display_text("Dealer's Hand", WIDTH//2 - 70, 20)
        display_text(f"Score: {dealer_score}", WIDTH//2 - 40, 160)
        
        display_text("Your Hand", WIDTH//2 - 50, HEIGHT - CARD_HEIGHT - 160)
        display_text(f"Score: {player_score}", WIDTH//2 - 40, HEIGHT - 30)
        display_text(f"Bet: ${bet}", WIDTH//2 - 40, HEIGHT - 60)
        
        display_text("AI Player 1", 50, HEIGHT//2 - CARD_HEIGHT//2 - 30)
        display_text(f"Score: {ai1_score}", 50, HEIGHT//2 + CARD_HEIGHT//2 + 10)
        
        display_text("AI Player 2", WIDTH - 2*CARD_WIDTH - 50, HEIGHT//2 - CARD_HEIGHT//2 - 30)
        display_text(f"Score: {ai2_score}", WIDTH - 2*CARD_WIDTH - 50, HEIGHT//2 + CARD_HEIGHT//2 + 10)
        
        # Draw buttons
        draw_button("Hit", WIDTH//2 - 130, HEIGHT - CARD_HEIGHT - 200, 80, 40, RED, WHITE)
        draw_button("Stand", WIDTH//2 - 40, HEIGHT - CARD_HEIGHT - 200, 80, 40, BLUE, WHITE)
        if can_double and len(player_hand) == 2 and balance >= bet * 2:
            draw_button("Double", WIDTH//2 + 50, HEIGHT - CARD_HEIGHT - 200, 80, 40, YELLOW, BLACK)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.MOUSEBUTTONDOWN and not player_stand:
                mouse_pos = pygame.mouse.get_pos()
                if WIDTH//2 - 130 <= mouse_pos[0] <= WIDTH//2 - 50 and HEIGHT - CARD_HEIGHT - 200 <= mouse_pos[1] <= HEIGHT - CARD_HEIGHT - 160:
                    player_hand.append(deal_card())
                    can_double = False
                    if calculate_score(player_hand) > 21:
                        player_stand = True
                elif WIDTH//2 - 40 <= mouse_pos[0] <= WIDTH//2 + 40 and HEIGHT - CARD_HEIGHT - 200 <= mouse_pos[1] <= HEIGHT - CARD_HEIGHT - 160:
                    player_stand = True
                elif can_double and WIDTH//2 + 50 <= mouse_pos[0] <= WIDTH//2 + 130 and HEIGHT - CARD_HEIGHT - 200 <= mouse_pos[1] <= HEIGHT - CARD_HEIGHT - 160:
                    bet *= 2
                    player_hand.append(deal_card())
                    player_stand = True
        
        if player_stand:
            # AI players take their turns
            ai1_hand = ai_play(ai1_hand)
            ai2_hand = ai_play(ai2_hand)
            
            # Dealer's turn
            while calculate_score(dealer_hand) < 17:
                dealer_hand.append(deal_card())
            
            # Determine winners
            scores = [("You", player_score), ("Dealer", dealer_score), 
                      ("AI Player 1", ai1_score), ("AI Player 2", ai2_score)]
            non_busted = [(name, score) for name, score in scores if score <= 21]
            
            if non_busted:
                winner = max(non_busted, key=lambda x: x[1])
                if winner[0] == "You":
                    balance += bet
                    display_text(f"You win ${bet}!", WIDTH // 2 - 100, HEIGHT // 2)
                elif winner[0] == "Dealer":
                    balance -= bet
                    display_text(f"Dealer wins. You lose ${bet}.", WIDTH // 2 - 100, HEIGHT // 2)
                else:
                    display_text(f"{winner[0]} wins.", WIDTH // 2 - 100, HEIGHT // 2)
            else:
                display_text("Everyone busted!", WIDTH // 2 - 70, HEIGHT // 2)
            
            pygame.display.flip()
            pygame.time.wait(3000)
            game_over = True

    return balance

# Main game loop
balance = 1000
while balance > 0:
    new_balance = play_game(balance)
    if new_balance is None:
        break
    balance = new_balance
    display_text(f"Your new balance: ${balance}", WIDTH // 2 - 100, HEIGHT // 2 + 50)
    pygame.display.flip()
    pygame.time.wait(2000)

if balance <= 0:
    display_text("Game Over! You're out of money.", WIDTH // 2 - 150, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(3000)

pygame.quit()