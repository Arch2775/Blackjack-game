## BlackJack game in Python
import random
import time

try:
    import pygame
except ImportError:
    pygame = None


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        suits = ["Hearts", "Spades", "Clubs", "Diamonds"]
        ranks = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J", "value": 10},
            {"rank": "Q", "value": 10},
            {"rank": "K", "value": 10},
        ]
        for rank in ranks:
            for suit in suits:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
        cards_dealt = []
        for _ in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False
        for card in self.cards:
            card_value = int(card.rank["value"])
            self.value += card_value
            if card.rank["rank"] == "A":
                has_ace = True
        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        print(f"""{"Dealer's" if self.dealer else "Your"} hand:""")
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                print("Hidden")
            else:
                print(card)
        if not self.dealer:
            print("Value:", self.get_value())
        print()


class Game:
    def __init__(self):
        self.balance = 1000

    def animate_text(self, message, delay=0.03):
        for char in message:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()

    def simulate_deal(self, label):
        self.animate_text(f"{label} dealing", delay=0.02)
        for _ in range(3):
            print(".", end="", flush=True)
            time.sleep(0.25)
        print("\n")

    def place_bet(self):
        print(f"Current balance: {self.balance}")
        while True:
            try:
                bet = int(input("Enter your bet amount for this round: "))
                if bet <= 0:
                    print("Bet must be greater than 0.")
                elif bet > self.balance:
                    print("Bet cannot be more than your current balance.")
                else:
                    return bet
            except ValueError:
                print("Please enter a valid number.")

    def play(self):
        game_number = 0
        games_to_play = 0
        while games_to_play <= 0:
            try:
                games_to_play = int(input("How many games do you want to play? "))
            except ValueError:
                print("you must enter a number.")

        while game_number < games_to_play:
            if self.balance <= 0:
                print("You are out of balance. Game over.")
                break

            game_number += 1
            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for _ in range(2):
                self.simulate_deal("Cards")
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            bet = self.place_bet()
            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print(f"Round bet: {bet}")
            print(f"Available balance: {self.balance}")
            print("*" * 30)
            player_hand.display()
            dealer_hand.display()

            outcome = self.check_winner(player_hand, dealer_hand)
            if outcome:
                self.update_balance(outcome, bet)
                continue

            choice = ""
            while player_hand.get_value() < 21 and choice not in ["s", "stand"]:
                choice = input("please choose 'Hit' or 'Stand': ").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please enter 'Hit' or 'Stand' (or H/S): ").lower()
                    print()
                if choice in ["hit", "h"]:
                    self.simulate_deal("Player")
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            outcome = self.check_winner(player_hand, dealer_hand)
            if outcome:
                self.update_balance(outcome, bet)
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()

            while dealer_hand_value < 17:
                self.simulate_deal("Dealer")
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_cards=True)
            outcome = self.check_winner(player_hand, dealer_hand)
            if outcome:
                self.update_balance(outcome, bet)
                continue

            print("Final results")
            print("Your hand:", player_hand_value)
            print("Dealer's hand:", dealer_hand_value)
            outcome = self.check_winner(player_hand, dealer_hand, True)
            self.update_balance(outcome, bet)
            print(f"Updated balance: {self.balance}")

        print("\n Thanks for playing!!")
        print(f"Final balance: {self.balance}")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:
            if player_hand.get_value() > 21:
                print("You busted. Dealer wins!! :P")
                return "dealer_win"
            if dealer_hand.get_value() > 21:
                print("Dealer busted. you win!!! :)")
                return "player_win"
            if dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both dealer and player have blackjack! Tie -_-")
                return "tie"
            if player_hand.is_blackjack():
                print("You have a blackjack!! You win! :)")
                return "player_win"
            if dealer_hand.is_blackjack():
                print("Dealer has a blackjack. Dealer wins! :(")
                return "dealer_win"
            return None

        if player_hand.get_value() > dealer_hand.get_value():
            print("You Win! :)")
            return "player_win"
        if player_hand.get_value() == dealer_hand.get_value():
            print("Tie! -_-")
            return "tie"
        print("Dealer wins! :(")
        return "dealer_win"

    def update_balance(self, outcome, bet):
        if outcome == "player_win":
            self.balance += bet
            print(f"You won {bet}! New balance: {self.balance}")
        elif outcome == "dealer_win":
            self.balance -= bet
            print(f"You lost {bet}. New balance: {self.balance}")
        elif outcome == "tie":
            print(f"Bet returned. Balance remains: {self.balance}")


class PygameBlackjackApp:
    def __init__(self):
        if pygame is None:
            raise RuntimeError("Pygame is not installed.")

        pygame.init()
        pygame.display.set_caption("Blackjack - Pygame")
        self.screen = pygame.display.set_mode((1000, 650))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 28)
        self.small_font = pygame.font.SysFont("arial", 22)
        self.card_rank_font = pygame.font.SysFont("arial", 26, bold=True)
        self.card_suit_font = pygame.font.SysFont("segoeuisymbol", 24)
        self.card_center_font = pygame.font.SysFont("arial", 34, bold=True)
        self.chip_font = pygame.font.SysFont("arial", 18, bold=True)

        self.balance = 1000
        self.bet = 50
        self.min_bet = 10

        self.deck = None
        self.player_hand = Hand()
        self.dealer_hand = Hand(dealer=True)
        self.state = "idle"
        self.message = "Set your bet and press DEAL."
        self.outcome = None
        self.reveal_dealer = False

        self.pending_deals = []
        self.active_animation = None

        self.deck_pos = (70, 250)
        self.card_w = 90
        self.card_h = 130
        self.card_gap = 28
        self.dealer_y = 90
        self.player_y = 360

        self.buttons = {
            "bet_minus": pygame.Rect(660, 120, 55, 42),
            "bet_plus": pygame.Rect(885, 120, 55, 42),
            "all_in": pygame.Rect(730, 120, 140, 42),
            "deal": pygame.Rect(660, 190, 280, 50),
            "hit": pygame.Rect(660, 270, 130, 50),
            "stand": pygame.Rect(810, 270, 130, 50),
        }

    def suit_symbol(self, suit):
        symbols = {
            "Hearts": "♥",
            "Diamonds": "♦",
            "Spades": "♠",
            "Clubs": "♣",
        }
        return symbols.get(suit, "?")

    def suit_color(self, suit):
        return (190, 30, 30) if suit in ("Hearts", "Diamonds") else (20, 20, 20)

    def card_pip_layout(self, rank):
        layouts = {
            "A": [(0.5, 0.5)],
            "2": [(0.5, 0.28), (0.5, 0.72)],
            "3": [(0.5, 0.25), (0.5, 0.5), (0.5, 0.75)],
            "4": [(0.3, 0.28), (0.7, 0.28), (0.3, 0.72), (0.7, 0.72)],
            "5": [(0.3, 0.28), (0.7, 0.28), (0.5, 0.5), (0.3, 0.72), (0.7, 0.72)],
            "6": [
                (0.3, 0.25),
                (0.7, 0.25),
                (0.3, 0.5),
                (0.7, 0.5),
                (0.3, 0.75),
                (0.7, 0.75),
            ],
            "7": [
                (0.3, 0.22),
                (0.7, 0.22),
                (0.5, 0.38),
                (0.3, 0.5),
                (0.7, 0.5),
                (0.3, 0.75),
                (0.7, 0.75),
            ],
            "8": [
                (0.3, 0.22),
                (0.7, 0.22),
                (0.3, 0.4),
                (0.7, 0.4),
                (0.3, 0.6),
                (0.7, 0.6),
                (0.3, 0.78),
                (0.7, 0.78),
            ],
            "9": [
                (0.3, 0.2),
                (0.7, 0.2),
                (0.3, 0.35),
                (0.7, 0.35),
                (0.5, 0.5),
                (0.3, 0.65),
                (0.7, 0.65),
                (0.3, 0.8),
                (0.7, 0.8),
            ],
            "10": [
                (0.3, 0.18),
                (0.7, 0.18),
                (0.3, 0.33),
                (0.7, 0.33),
                (0.3, 0.48),
                (0.7, 0.48),
                (0.3, 0.63),
                (0.7, 0.63),
                (0.3, 0.78),
                (0.7, 0.78),
            ],
        }
        return layouts.get(rank, [])

    def pip_count_for_rank(self, rank):
        if rank == "A":
            return 1
        if rank in ("J", "Q", "K"):
            return 0
        return int(rank)

    def draw_chip(self, center, radius, value, color):
        x, y = center
        pygame.draw.circle(self.screen, (235, 235, 235), (x + 2, y + 2), radius + 1)
        pygame.draw.circle(self.screen, color, center, radius)
        pygame.draw.circle(self.screen, (245, 245, 245), center, radius - 6, 3)
        pygame.draw.circle(self.screen, (250, 250, 250), center, radius - 13)

        for angle in range(0, 360, 30):
            tick_x = x + int((radius - 3) * pygame.math.Vector2(1, 0).rotate(angle).x)
            tick_y = y + int((radius - 3) * pygame.math.Vector2(1, 0).rotate(angle).y)
            pygame.draw.circle(self.screen, (250, 250, 250), (tick_x, tick_y), 3)

        label = self.chip_font.render(str(value), True, (25, 25, 25))
        label_rect = label.get_rect(center=center)
        self.screen.blit(label, label_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)

            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def handle_click(self, mouse_pos):
        if self.buttons["bet_minus"].collidepoint(mouse_pos):
            if self.state in ("idle", "round_over"):
                self.bet = max(self.min_bet, self.bet - 10)

        elif self.buttons["bet_plus"].collidepoint(mouse_pos):
            if self.state in ("idle", "round_over") and self.bet + 10 <= self.balance:
                self.bet += 10

        elif self.buttons["all_in"].collidepoint(mouse_pos):
            if self.state in ("idle", "round_over") and self.balance > 0:
                self.bet = self.balance
                self.message = f"All in placed: {self.bet}"

        elif self.buttons["deal"].collidepoint(mouse_pos):
            if self.state in ("idle", "round_over"):
                self.start_round()

        elif self.buttons["hit"].collidepoint(mouse_pos):
            if self.state == "player_turn" and self.active_animation is None:
                self.state = "player_hit"
                self.start_card_animation("player")

        elif self.buttons["stand"].collidepoint(mouse_pos):
            if self.state == "player_turn" and self.active_animation is None:
                self.reveal_dealer = True
                self.state = "dealer_turn"
                self.message = "Dealer is playing..."

    def start_round(self):
        if self.balance <= 0:
            self.message = "No balance left. Restart the game."
            return

        if self.bet > self.balance:
            self.bet = self.balance

        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand(dealer=True)
        self.reveal_dealer = False
        self.outcome = None
        self.pending_deals = ["player", "dealer", "player", "dealer"]
        self.active_animation = None
        self.state = "dealing"
        self.message = "Dealing cards..."

    def get_hand_card_pos(self, hand_name, card_index):
        x = 220 + card_index * (self.card_w + self.card_gap)
        y = self.player_y if hand_name == "player" else self.dealer_y
        return x, y

    def start_card_animation(self, hand_name):
        card_list = self.deck.deal(1)
        if not card_list:
            return

        card = card_list[0]
        hand = self.player_hand if hand_name == "player" else self.dealer_hand
        end_x, end_y = self.get_hand_card_pos(hand_name, len(hand.cards))
        self.active_animation = {
            "hand": hand_name,
            "card": card,
            "start_x": self.deck_pos[0],
            "start_y": self.deck_pos[1],
            "end_x": end_x,
            "end_y": end_y,
            "start_time": pygame.time.get_ticks(),
            "duration": 260,
        }

    def finish_round(self, outcome):
        self.outcome = outcome
        self.reveal_dealer = True
        self.state = "round_over"

        if outcome == "player_win":
            self.balance += self.bet
            self.message = f"You win! +{self.bet}   Balance: {self.balance}"
        elif outcome == "dealer_win":
            self.balance -= self.bet
            self.message = f"Dealer wins! -{self.bet}   Balance: {self.balance}"
        else:
            self.message = f"Push (tie). Balance: {self.balance}"

        if self.balance <= 0:
            self.message = "You are out of balance. Close window to exit."

    def check_round_outcome(self, game_over=False):
        if not game_over:
            if self.player_hand.get_value() > 21:
                return "dealer_win"
            if self.dealer_hand.get_value() > 21:
                return "player_win"
            if self.dealer_hand.is_blackjack() and self.player_hand.is_blackjack():
                return "tie"
            if self.player_hand.is_blackjack():
                return "player_win"
            if self.dealer_hand.is_blackjack():
                return "dealer_win"
            return None

        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()
        if player_value > 21:
            return "dealer_win"
        if dealer_value > 21:
            return "player_win"
        if player_value > dealer_value:
            return "player_win"
        if player_value < dealer_value:
            return "dealer_win"
        return "tie"

    def update(self):
        now = pygame.time.get_ticks()

        if self.active_animation is not None:
            elapsed = now - self.active_animation["start_time"]
            if elapsed >= self.active_animation["duration"]:
                hand_name = self.active_animation["hand"]
                card = self.active_animation["card"]
                if hand_name == "player":
                    self.player_hand.add_card([card])
                else:
                    self.dealer_hand.add_card([card])
                self.active_animation = None

                if self.state == "player_hit":
                    outcome = self.check_round_outcome()
                    if outcome:
                        self.finish_round(outcome)
                    else:
                        self.state = "player_turn"
                        self.message = "Your turn: Hit or Stand."
            return

        if self.state == "dealing":
            if self.pending_deals:
                self.start_card_animation(self.pending_deals.pop(0))
            else:
                outcome = self.check_round_outcome()
                if outcome:
                    self.finish_round(outcome)
                else:
                    self.state = "player_turn"
                    self.message = "Your turn: Hit or Stand."

        elif self.state == "dealer_turn":
            if self.dealer_hand.get_value() < 17:
                self.start_card_animation("dealer")
            else:
                self.finish_round(self.check_round_outcome(game_over=True))

    def draw_card(self, card, x, y, hidden=False):
        card_rect = pygame.Rect(x, y, self.card_w, self.card_h)
        shadow = pygame.Rect(x + 4, y + 4, self.card_w, self.card_h)
        pygame.draw.rect(self.screen, (10, 60, 20), shadow, border_radius=8)

        if hidden:
            pygame.draw.rect(self.screen, (30, 80, 150), card_rect, border_radius=8)
            pygame.draw.rect(self.screen, (220, 220, 220), card_rect, 2, border_radius=8)
            for row in range(4):
                for col in range(3):
                    dot_x = x + 18 + col * 24
                    dot_y = y + 16 + row * 26
                    pygame.draw.circle(self.screen, (225, 235, 255), (dot_x, dot_y), 3)
            back_text = self.small_font.render("BJ", True, (240, 240, 240))
            self.screen.blit(back_text, (x + 33, y + 52))
            return

        pygame.draw.rect(self.screen, (250, 250, 250), card_rect, border_radius=8)
        pygame.draw.rect(self.screen, (30, 30, 30), card_rect, 2, border_radius=8)

        rank = card.rank["rank"]
        suit = self.suit_symbol(card.suit)
        color = self.suit_color(card.suit)

        rank_text = self.card_rank_font.render(rank, True, color)
        suit_text = self.card_suit_font.render(suit, True, color)
        rank_pos = rank_text.get_rect(topleft=(x + 8, y + 6))
        suit_pos = suit_text.get_rect(topleft=(x + 12, y + 32))
        self.screen.blit(rank_text, rank_pos)
        self.screen.blit(suit_text, suit_pos)

        rank_br = pygame.transform.rotate(self.card_rank_font.render(rank, True, color), 180)
        suit_br = pygame.transform.rotate(self.card_suit_font.render(suit, True, color), 180)
        rank_br_pos = rank_br.get_rect(bottomright=(x + self.card_w - 8, y + self.card_h - 8))
        suit_br_pos = suit_br.get_rect(bottomright=(x + self.card_w - 10, y + self.card_h - 36))
        self.screen.blit(rank_br, rank_br_pos)
        self.screen.blit(suit_br, suit_br_pos)

        # Keep card face minimal: rank + suit only, no center pips/face art.

    def draw_button(self, key, label, enabled=True):
        rect = self.buttons[key]
        color = (230, 200, 90) if enabled else (140, 140, 140)
        pygame.draw.rect(self.screen, color, rect, border_radius=8)
        pygame.draw.rect(self.screen, (30, 30, 30), rect, 2, border_radius=8)
        txt = self.small_font.render(label, True, (20, 20, 20))
        txt_rect = txt.get_rect(center=rect.center)
        self.screen.blit(txt, txt_rect)

    def draw(self):
        self.screen.fill((16, 102, 56))
        pygame.draw.ellipse(self.screen, (26, 122, 70), (150, 15, 500, 620), 0)
        pygame.draw.ellipse(self.screen, (12, 74, 40), (130, 0, 540, 650), 5)
        title = self.font.render("Blackjack", True, (245, 245, 245))
        self.screen.blit(title, (30, 20))

        balance_text = self.small_font.render(f"Balance: {self.balance}", True, (255, 255, 255))
        bet_text = self.small_font.render(f"Bet: {self.bet}", True, (255, 255, 255))
        msg_text = self.small_font.render(self.message, True, (255, 255, 230))
        self.screen.blit(balance_text, (30, 65))
        self.screen.blit(bet_text, (30, 95))
        self.screen.blit(msg_text, (30, 600))

        pygame.draw.rect(self.screen, (35, 70, 35), (40, 235, 110, 150), border_radius=8)
        pygame.draw.rect(self.screen, (230, 230, 230), (40, 235, 110, 150), 2, border_radius=8)
        deck_text = self.small_font.render("DECK", True, (240, 240, 240))
        self.screen.blit(deck_text, (66, 300))

        # chip graphics for the active bet and total balance
        self.draw_chip((770, 84), 28, self.bet, (210, 45, 45))
        self.draw_chip((840, 84), 28, self.balance, (35, 95, 200))
        self.draw_chip((540, 305), 30, self.bet, (35, 145, 45))

        dealer_label = "Dealer"
        if self.reveal_dealer:
            dealer_label += f" ({self.dealer_hand.get_value()})"
        player_label = f"Player ({self.player_hand.get_value()})"
        self.screen.blit(self.small_font.render(dealer_label, True, (255, 255, 255)), (220, 58))
        self.screen.blit(self.small_font.render(player_label, True, (255, 255, 255)), (220, 328))

        for idx, card in enumerate(self.dealer_hand.cards):
            x, y = self.get_hand_card_pos("dealer", idx)
            hidden = idx == 0 and not self.reveal_dealer and self.state in ("dealing", "player_turn", "player_hit")
            self.draw_card(card, x, y, hidden=hidden)

        for idx, card in enumerate(self.player_hand.cards):
            x, y = self.get_hand_card_pos("player", idx)
            self.draw_card(card, x, y)

        if self.active_animation is not None:
            elapsed = pygame.time.get_ticks() - self.active_animation["start_time"]
            t = min(1, elapsed / self.active_animation["duration"])
            cur_x = int(self.active_animation["start_x"] + (self.active_animation["end_x"] - self.active_animation["start_x"]) * t)
            cur_y = int(self.active_animation["start_y"] + (self.active_animation["end_y"] - self.active_animation["start_y"]) * t)
            hidden = self.active_animation["hand"] == "dealer" and len(self.dealer_hand.cards) == 0 and not self.reveal_dealer
            self.draw_card(self.active_animation["card"], cur_x, cur_y, hidden=hidden)

        can_adjust = self.state in ("idle", "round_over")
        self.draw_button("bet_minus", "-", enabled=can_adjust)
        self.draw_button("all_in", "ALL IN", enabled=can_adjust and self.balance > 0)
        self.draw_button("bet_plus", "+", enabled=can_adjust)
        self.draw_button("deal", "DEAL", enabled=can_adjust and self.balance > 0)
        self.draw_button("hit", "HIT", enabled=self.state == "player_turn")
        self.draw_button("stand", "STAND", enabled=self.state == "player_turn")


if __name__ == "__main__":
    if pygame is None:
        print("Pygame is not installed. Running CLI mode.")
        Game().play()
    else:
        mode = input("Choose mode: [P]ygame or [C]LI (default P): ").strip().lower()
        if mode == "c":
            Game().play()
        else:
            PygameBlackjackApp().run()