#!/usr/bin/env python

# Uno Card Game v.0.0.2
# Official Rules straight from Wiki: https://en.wikipedia.org/wiki/Uno_(card_game)
# The aim of the game is to be the first player to score 500 points.
# This is achieved (usually over several rounds of play) by a player
# discarding all of their cards and earning points corresponding to the
# value of the remaining cards still held by the other players.

# """
# Skip - Next player in sequence misses a turn
# Draw Two - Next player in sequence draws two cards and misses a turn
# Reverse - Order of play switches directions (clockwise to counterclockwise, or vice versa)
# Wild - Player declares next color to be matched (may be used on any turn even if the player has matching color)
# Wild Draw Four - Player declares next color to be matched; next player in sequence draws four cards and loses a turn. May be legally played only if the player has no cards of the current color; cards of other colors in the current rank and Wild cards do not count in this respect.
# """

# The start of the game, 7 cards are dealth to each player with the top card of the deck flipped over to set aside discard pile

# TODOs:
# - After a wild card is played
# - Command input menu and handling inputs
# - When someone is on their last card
# - When an action card is played
# - When somebody plays their last card
#     - Calculating score
# - Starting game over after somebody wins
'''
    File name: uno.py
    Author: Noel Colon
    Date created: 10/20/2016
    Date last modified: 10/24/2016
    Python Version: 2.7
'''

import random
import time
from itertools import cycle, islice, dropwhile


class Game(object):
    direction = 'clockwise'
    dealer = {}
    turn = {}
    table = {}
    deck = {}
    pile = {}

    def __init__(self, player_name):
        self.create_players(player_name)
        self.assign_dealer()
        self.setup_table()

    def setup_table(self):
        self.table = Table(self.player_one, self.player_two,
                           self.player_three, self.player_four)
        self.create_deck()
        self.deal_hands(self.deck)
        self.set_turn()
        self.create_pile()
        self.start_game()

    def create_players(self, player_name):
        player_one = Player(player_name)
        computer_one = Bot()
        computer_two = Bot()
        computer_three = Bot()

        self.player_one = player_one
        self.player_two = computer_one
        self.player_three = computer_two
        self.player_four = computer_three

    def assign_dealer(self):
        self.dealer = random.choice(
            [self.player_one, self.player_two, self.player_three, self.player_four])
        self.dealer.is_dealer = True

    def create_deck(self):
        self.deck = Deck()

    def create_pile(self):
        card = self.deck.cards[0]

        print 'Pile card: ', card.type
        print 'Turn name: ', self.turn.name

        if self.turn.name == self.table.seat_one.name and (card.color == 'Wild' or card.color == 'Wild Draw Four'):
            card.color = self.prompt_user()
        elif card.color == 'Wild' or card.color == 'Wild Draw Four':
            card.color = random.choice(['Red', 'Green', 'Yellow', 'Blue'])
            print 'The first pile card was wild and was set to {}'.format(card.color)
        self.pile = card
        self.deck.cards.pop(0)

    def change_direction(self):
        if self.direction == 'clockwise':
            self.direction = 'counterclockwise'
        elif self.direction == 'counterclockwise':
            self.direction = 'clockwise'

    def check_players_hands(self):
        pass

    def calculate_score(self):
        pass

    def command_input_handler(self):
        pass

    def set_turn(self):
        players = [self.table.seat_one, self.table.seat_two,
                   self.table.seat_three, self.table.seat_four]
        index = 0
        for player in players:
            if player.is_dealer:
                index = players.index(player)
                try:
                    self.turn = players[index + 1]
                except Exception, e:
                    self.turn = players[0]

    def deal_hands(self, deck):
        dealer = self.dealer
        players = [self.table.seat_one, self.table.seat_two,
                   self.table.seat_three, self.table.seat_four]
        starting_index = players.index(dealer)

        after_dealer = players[starting_index + 1:] + \
            players[:starting_index + 1]

        counter = 0
        while counter < 7:
            for p in after_dealer:
                p.draw_card(deck)
            counter += 1

    def start_game(self):
        self.check_player()

    def next_turn(self):
        # test directions
        players = [
            self.table.seat_one,
            self.table.seat_two,
            self.table.seat_three,
            self.table.seat_four
        ]
        index = players.index(self.turn)
        if index == 3 and self.direction == 'clockwise':
            next_player = players[0]
        elif index == 3 and self.direction == 'counterclockwise':
            next_player = players[index - 1]
        elif self.direction == 'clockwise':
            next_player = players[index + 1]
        elif index == 0 and self.direction == 'counterclockwise':
            next_player = players[4]
        elif self.direction == 'counterclockwise':
            next_player = players[index - 1]

        self.turn = next_player
        self.check_player()

    def check_player(self):
        if self.turn.computer:
            pile = self.pile
            print 'It\'s {}\'s turn.'.format(self.turn.name)
            # time.sleep(3)
            new_pile_card = self.turn.start(
                self.direction, self.table, self.deck, self.pile)
            print '{} plays the {} card'.format(self.turn.name, new_pile_card.type)
            self.pile = new_pile_card
            self.next_turn()
        else:
            print 'It\'s your turn.'
            print 'Pile card: {} (Color: {}, Rank: {})'.format(self.pile.type, self.pile.color, self.pile.rank)
            self.user_command_prompt()

    def prompt_user(self):
        print 'Select a color:\n1. Red  2. Blue  3. Green  4. Yellow'

        choice = raw_input(': ')

        if choice == '1':
            print 'Wild card was set to Red'
            choice = 'Red'
        elif choice == '2':
            print 'Wild card was set to Blue'
            choice = 'Blue'
        elif choice == '3':
            print 'Wild card was set to Green'
            choice = 'Green'
        elif choice == '4':
            print 'Wild card was set to Yellow'
            choice = 'Yellow'

        return choice

    def user_command_prompt(self):
        print 'What would you like to do?'
        first_msg = '|1. See Hand  2. Draw Card  3. Check Table|'
        after_draw_msg = '|1. See Hand  2. Draw Card  3. Check Table  4. Skip|'
        drew = False

        while True:
            print first_msg
            choice = raw_input(': ')

            if choice == '1':
                self.see_hand()
            elif choice == '2':
                self.turn.draw_card(self.deck)
                drew = True
                break
            elif choice == '3':
                print 'Table:\n Players:'
                print '  {}: {} card(s)'.format(self.table.seat_one.name, len(self.table.seat_one.hand))
                print '  {}: {} card(s)'.format(self.table.seat_two.name, len(self.table.seat_two.hand))
                print '  {}: {} card(s)'.format(self.table.seat_three.name, len(self.table.seat_three.hand))
                print '  {}: {} card(s)'.format(self.table.seat_four.name, len(self.table.seat_four.hand))
                print ' Pile card: {}'.format(self.pile.type)
                print ' Deck: {} card(s) left'.format(len(self.deck.cards))
            elif choice == '':
                continue

        while drew:
            print after_draw_msg
            choice = raw_input(': ')

            if choice == '1':
                self.see_hand()
            elif choice == '2':
                self.turn.draw_card(self.deck)
            elif choice == '3':
                print 'Table:\n Players:'
                print '  Seat 1: {}: {} card(s)'.format(self.table.seat_one.name, len(self.table.seat_one.hand))
                print '  Seat 2: {}: {} card(s)'.format(self.table.seat_two.name, len(self.table.seat_two.hand))
                print '  Sear 3: {}: {} card(s)'.format(self.table.seat_three.name, len(self.table.seat_three.hand))
                print '  Seat 4: {}: {} card(s)'.format(self.table.seat_four.name, len(self.table.seat_four.hand))
                print ' Pile card: {}'.format(self.pile.type)
                print ' Deck: {} card(s) left'.format(len(self.deck.cards))
            elif choice == '4':
                break
            elif choice == '':
                continue

        self.next_turn()

    def see_hand(self):
        print '---------------------'
        for val, card in enumerate(self.turn.hand):
            print '{}. {}'.format(val + 1, card.type)
        print 'Enter. Back'
        print '---------------------'

        playable = self.turn.analyze_cards(self.pile)

        choice = raw_input(': ')
        if choice:
            choice = int(choice)

        if choice in range(1, len(self.turn.hand) + 1) and (self.turn.hand[choice - 1] in playable):
            # proceed to play card
            card = self.turn.hand[choice - 1]

            if card.color == 'Wild' or card.color == 'Wild Draw Four':
                index = self.turn.hand.index(card)
                card.color = self.prompt_user()
                self.turn.hand.pop(index)
                self.pile = card
                # prompt for wild card color selection
            else:
                index = self.turn.hand.index(card)
                self.turn.hand.pop(index)
                self.pile = card

            self.next_turn()
            # print 'Card is playable!'
            # print 'Card choice: {} (Color: {}, Rank: {})'.format(self.turn.hand[choice-1].type, self.turn.hand[choice-1].color, self.turn.hand[choice-1].rank)
        else:
            print 'Can\'t play that card!'

        print 'Choice: ', choice
        print 'Pile card: {} (Color: {}, Rank: {})'.format(self.pile.type, self.pile.color, self.pile.rank)
        print 'Playable: '
        for i in playable:
            print i.type


class Player(object):
    is_dealer = False
    points = 0

    def __init__(self, name):
        self.name = name
        self.hand = []
        self.computer = False

    def set_time_limit(self):
        pass

    def set_turn(self):
        pass

    def get_hand(self):
        pass

    def draw_card(self, deck):
        card = deck.cards[0]
        if not self.computer:
            print 'You drew the {}'.format(card.type)
        self.hand.append(card)
        deck.cards.pop(0)

    def analyze_cards(self, pile):
        playable = []

        for card in self.hand:
            if card.color == pile.color:
                playable.append(card)

            elif card.color == 'Wild' or card.color == 'Wild Draw Four':
                # Prompt color selection
                # Set card color to prompted selection
                playable.append(card)

            elif card.rank == pile.rank:
                playable.append(card)

            else:
                continue

        return playable

    def get_number_of_cards(self):
        pass

    def challenge_player(self):
        pass

    def call_uno(self):
        pass


class Bot(Player):
    bot_names = [
        'AI Ralph',
        'AI Randy',
        'AI Charlotte',
        'AI Johnny',
        'AI Lexa',
        'AI Boulder',
        'AI Frank',
        'AI Sisco'
    ]

    def __init__(self):
        self.name = random.choice(self.bot_names)
        name_index = self.bot_names.index(self.name)
        self.bot_names.pop(name_index)  # To avoid duplicates
        self.hand = []
        self.computer = True

    def start(self, direction, table, deck, pile):
        print '{} is looking at their hand..'.format(self.name)
        # time.sleep(3)
        playable = self.analyze_play(direction, table, deck, pile)
        selected_card = self.pick_a_card(playable)
        if selected_card.color == 'Wild' or selected_card.color == 'Wild Draw Four':
            selected_card.color = random.choice(
                ['Red', 'Yellow', 'Blue', 'Green'])
            print '{} selected {} and set the color to {}'.format(self.name, selected_card.type, selected_card.color)
        return selected_card

    def analyze_play(self, direction, table, deck, pile):
        playable = self.analyze_cards(pile)

        while not playable:
            self.draw_card(deck)
            playable = self.analyze_cards(pile)

        return playable

    def pick_a_card(self, playable):
        choice = random.choice(playable)
        index = self.hand.index(choice)
        return choice


class Table(object):

    def __init__(self, player1, player2, player3, player4):
        self.seat_one = player1
        self.seat_two = player2
        self.seat_three = player3
        self.seat_four = player4

    def print_seats(self):
        return 'Seat 1: %s\nSeat 2: %s\nSeat 3: %s\nSeat 4: %s' % (self.seat_one.name, self.seat_two.name, self.seat_three.name, self.seat_four.name)

    def get_seats(self):
        return [self.seat_one, self.seat_two, self.seat_three, self.seat_four]


class Deck(object):
    total = 108
    colors = ['Red', 'Green', 'Yellow', 'Blue']
    ranks = ['Zero', 'One', 'Two', 'Three', 'Four',
             'Five', 'Six', 'Seven', 'Eight', 'Nine']
    actions = ['Reverse', 'Skip', 'Draw Two']
    wildcards = ['Wild', 'Wild Draw Four']
    cards = []

    # 25 of each color, each color having two of each rank except zero

    def __init__(self):
        self.create_deck(self.colors, self.ranks, self.actions, self.wildcards)
        self.shuffle_cards()

    def create_deck(self, colors, ranks, actions, wildcards):
        # Create one of each rank and action card for each color
        for color in colors:
            for rank in ranks:
                card = Card(color, rank)
                self.cards.append(card)
            for act in actions:
                card = Card(color, act)
                self.cards.append(card)

        # Get rid of the Zero card
        ranks.pop(0)

        # Create one of each for each again minus the Zero card
        for color in colors:
            for rank in ranks:
                card = Card(color, rank)
                self.cards.append(card)
            for act in actions:
                card = Card(color, act)
                self.cards.append(card)

        # Create four of each wildcard (not the best implementation but whatever)
        times = 0
        while times < 8:
            for name in wildcards:
                wc = Card(name, '')
                self.cards.append(wc)
                times += 1

    def get_cards(self):
        pass

    def shuffle_cards(self):
        random.shuffle(self.cards)
        random.shuffle(self.cards)

    def get_card(self):
        pass

    def get_card_count(self):
        pass


class Card(object):
    def __init__(self, color, rank):
        self.color = color
        self.rank = rank
        self.set_card_type()

    def set_card_type(self):
        if self.color == 'Wild' or self.color == 'Wild Draw Four':
            self.type = '[' + self.color + ']'
        else:
            self.type = '[' + self.color + ' ' + self.rank + ']'
        self.set_points()

    def set_points(self):
        if self.rank == 'Zero':
            self.points = 0
        elif self.rank == 'One':
            self.points = 1
        elif self.rank == 'Two':
            self.points = 2
        elif self.rank == 'Three':
            self.points = 3
        elif self.rank == 'Four':
            self.points = 4
        elif self.rank == 'Five':
            self.points = 5
        elif self.rank == 'Six':
            self.points = 6
        elif self.rank == 'Seven':
            self.points = 7
        elif self.rank == 'Eight':
            self.points = 8
        elif self.rank == 'Nine':
            self.points = 9
        elif self.rank == 'Skip':
            self.points = 20
        elif self.rank == 'Draw Two':
            self.points = 20
        elif self.rank == 'Reverse':
            self.points = 20
        elif self.rank == '':
            self.points = 503

    def get_points(self):
        pass


# Startup Prompt
name = raw_input('Uno Card Game v.0.0.2\nName? ')
game = Game(name)
