"""
war-time-simulator.py
author: cary xiao
version: 1 June 2022
---------------------------------
This file runs simulations of the card game War and some of its variations,
keeping track of the number of card flips per player until the game ended.
The sample for each game type is then written into separate .csv files defined by
the file name inputted by the user, depositing each file into the same folder as 
this script. 
"""
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
import pathlib


# class that either represents a 52-card deck of playing 
# cards or the stack that a player has in a game of war. 
class Deck:
    def __init__(self):
        self.cards = [] # value of card followed by suit, separated by a dash. value goes from 2 - 10, then j, q, k, a. suit is represented by s, c, d, h.
        self.spoils = [] # represents set of cards that the given player has won
        
        values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'j', 'q', 'k', 'a']
        for value in values:
            suits = ['s', 'c', 'd', 'h']
            for suit in suits:
                self.cards.append(value + '-' + suit)

    # shuffle all the cards. If there are cards in the spoils pile, incorporate them into the main deck before shuffling.
    def shuffle(self):
        if len(self.spoils) > 0:
            self.cards += self.spoils
            self.spoils = []
        shuffled = []
        for i in range(len(self.cards)):
            # pick random card and remove it
            card = np.random.choice(self.cards)
            shuffled.append(card)
            self.cards.remove(card)
        self.cards = shuffled
    
    # used to split deck of 52 into 2 decks fo 26, one being self and the other being the returned object. 
    # Shuffles the deck, puts the 1st half in self.cards, and returns the other half.
    def split(self):
        new_deck = Deck()
        self.shuffle()
        new_deck.cards = self.cards[len(self.cards)//2:]
        self.cards = self.cards[:len(self.cards)//2]
        return new_deck
    
    # function to play card. Returns string value for the card that was played. Cards at end of list are defined to be at the top of the deck.
    def play_card(self):
        return self.cards.pop()
    
    # function designed to add cards won from a round into the pile of spoils for the card
    def add_to_spoils(self, cards: str): # cards is a list of card strings
        self.spoils += cards

    # print command
    def __str__(self):
        return "Deck(): " + str(self.cards)


# helper function for each round of game. Takes in the string 
# representation of a card and returns the int value of the card. 
def value(card: str):
    str_value = card[:card.index('-')]
    if (str_value == 'j'):
        return 11
    elif (str_value == 'q'):
        return 12
    elif (str_value == 'k'):
        return 13
    elif (str_value == 'a'):
        return 14
    else:
        return int(str_value)


# class that simulates one game of War.
class Game:
    def __init__(self, war_deposit=1, reduction=False):
        self.player1 = Deck()
        self.player2 = self.player1.split()
        self.num_plays = 0
        self.war_deposit = war_deposit
        self.reduction = reduction

    # helper function for simulate_game. Reshuffles each player's cards if needed and returns True if 
    # game can still continue and false if the game has ended. 
    def check_reshuffle_end(self):
        if (len(self.player1.cards) == 0):
            self.player1.shuffle()
            if (len(self.player1.cards) == 0):
                return False
        if (len(self.player2.cards) == 0):
            self.player2.shuffle()
            if (len(self.player2.cards) == 0):
                return False
        return True
    
    def siumulate_game(self):
        # variable below used if reduction is set to true
        cards_remain = [2, 2, 2, 2, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14]
        while (self.check_reshuffle_end()):
            self.num_plays += 1
            # simulate one round
            p1_card = self.player1.play_card()
            p2_card = self.player2.play_card()
            cards = [p1_card, p2_card] # represents the pile of cards the winner of the round will gain
            
            # simulate WAR! (when both players play the same value card)
            while (value(p1_card) == value(p2_card) and self.check_reshuffle_end()):
                # Have each player contribute 1 card to the spoils pile
                for x in range(self.war_deposit):
                    self.num_plays += 1
                    if (not self.check_reshuffle_end()):
                        return self.num_plays
                    cards.append(self.player1.play_card())
                    cards.append(self.player2.play_card())
                if (not self.check_reshuffle_end()):
                    break
                # play new face-up cards
                self.num_plays += 1
                p1_card = self.player1.play_card()
                p2_card = self.player2.play_card()
                cards += [p1_card, p2_card]
            # winner gets cards in their spoils pile
            if (self.check_reshuffle_end()):
                # remove requisite cards if reduction is true
                if (self.reduction):
                    lowest_value = cards_remain[0]
                    reduced_cards = []
                    for i in range(len(cards)):
                        if not value(cards[i]) == lowest_value:
                            reduced_cards.append(cards[i]) # remove the lowest value card
                        else:
                            cards_remain.pop(0)
                    cards = reduced_cards
                if (value(p1_card) > value(p2_card)):
                    self.player1.add_to_spoils(cards)
                elif (value(p1_card) < value(p2_card)):
                    self.player2.add_to_spoils(cards)
        return self.num_plays


# gets a valid file name or path for a csv file. used by the program
# to create / write into a file 
def get_valid_file_name(display_name: str, default: str):
    file_name = input('input file name for the csv of ' + display_name + ' (or press ENTER to have name ' + default + '): ')
    if file_name == '':
        file_name = default
    # check for ending .csv
    end_name = ''
    if (len(file_name) > 4):
        end_name = file_name[len(file_name) - 4:]
    # if there is no .csv, add it
    if not (end_name == '.csv'):
        file_name += '.csv'
    # return full directory of current directory + file name
    return str(pathlib.Path(__file__).parent.resolve()) + '\\' + file_name


# writes data from dist into a csv defined by file_name.
# used to write the results from simulating games of War.
def write_data(file_name: str, dist: list):
    with open(file_name, 'w', newline='') as csvfile:
        fieldnames = ['number of cards flipped']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(dist)):
            writer.writerow({'number of cards flipped': str(dist[i])})


# simulates NUM_TRIALS games of War based on the 
def simulate_games(game_type: str, NUM_TRIALS, war_deposit=1, reduction=False):
    dist = []
    progress = 0.0
    print("simulating games for " + game_type + "...")    
    print()
    for i in range(NUM_TRIALS):
        game = Game(war_deposit, reduction)
        num_plays = game.siumulate_game()
        # update progress of calculation to the user
        if (int(round(i / NUM_TRIALS * 100, 2)) > progress):
            progress = int(round(i / NUM_TRIALS * 100, 2))
            sys.stdout.write("\033[F") # Cursor up one line
            print(progress, "%")
        dist.append(num_plays)
    sys.stdout.write("\033[F") # Cursor up one line
    print(100, '%')
    return dist

    


#############################################################################
# Main code
#############################################################################

NUM_TRIALS = 250

# create each sample distribution
dist_default = simulate_games('default_war', NUM_TRIALS)
dist_three_card_war = simulate_games('3-card war', NUM_TRIALS, war_deposit=2)
dist_five_card_war = simulate_games('5-card war', NUM_TRIALS, war_deposit=4)
dist_reduction = simulate_games('5-card war', NUM_TRIALS, reduction=True)
dist_reduction_five_card = simulate_games('5-card reduction war', NUM_TRIALS, war_deposit=4, reduction=True)

print()
print('--------------------------------------------------------')
file_path = get_valid_file_name('stock war', 'default_times.csv')
write_data(file_path, dist_default)
print('write finished.')
print()

file_path = get_valid_file_name('3-card war', '3card_times.csv')
write_data(file_path, dist_three_card_war)
print('write finished.')
print()

file_path = get_valid_file_name('5-card war', '5card_times.csv')
write_data(file_path, dist_five_card_war)
print('write finished.')
print()

file_path = get_valid_file_name('reduction war', 'reduction_times.csv')
write_data(file_path, dist_reduction)
print('write finished.')
print()

file_path = get_valid_file_name('5-card reduction war', 'reduction_5card_times.csv')
write_data(file_path, dist_reduction_five_card)
print('write finished.')