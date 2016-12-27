"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import logging
import os
import uuid

from cards.deck import Deck
from cards.hand import Hand
from players.player import Player


class Blackjack:

    def __init__(self, player_names):
        """ Initialize """
        self._deck = Deck()
        self._dealer = Player('Mora', 'Dealer')
        self._players = [Player(name, 'Player') for name in player_names]
        self._discard_pile = Player('Pile', 'Discard')
        self._log_directory = "./logs"
        self._init_logger()
        self._logger = logging.getLogger('bj')

    @property
    def dealer(self):
        return self._dealer

    @property
    def deck(self):
        return self._deck

    @property
    def discard_pile(self):
        return self._discard_pile

    @property
    def players(self):
        return self._players

    def burn_a_card(self):
        card = self.deck.deal_card()
        self._logger.info(f"Burn the {card}")
        self.discard_pile.receives(card)

    def check_for_blackjack(self):
        got_blackjack = False
        self._logger.info("Check for blackjack")
        if self.dealer.total == 21:
            self._logger.info("***** TWENTY-ONE! *****")
            got_blackjack = True
        return got_blackjack

    def deal_round(self):
        """ Deal a round of blackjack """
        self._logger.info("No more bets. Good luck.")
        for i in range(2):
            for player in self.players:
                player.receives(self.deck.deal_card())

            self.dealer.receives(self.deck.deal_card())

    def dealers_turn(self):
        result = self.dealer.move(self.deck)
        if result == 'bust':
            self.discard_hand(self.dealer)

    def discard_hand(self, player):
        for card in player.hand:
            self.discard_pile.receives(card)
        player.init_hand()

    def _init_logger(self):
        """ Initialize the log file and logger. """
        # Create log directory if it doesn't already exist.
        if not os.path.exists(self._log_directory):
            os.makedirs(self._log_directory)

        log_filename = f"{self._log_directory}/bj_{uuid.uuid1()}.log"

        # Add the date to the log file names
        logging.basicConfig(
            filename=log_filename,
            filemode='w',
            level=logging.DEBUG,
            format='%(asctime)s|%(levelname)-5s| %(message)s',
            datefmt='%Y-%m-%d %I:%M:%S %p')
        # define a Handler which writes WARNING messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(levelname)-5s| %(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)

    def play(self):
        deck = self.deck
        deck.shuffle()
        self.burn_a_card()
        while len(deck) > 3 * (len(self.players) + 1):
            self.play_round()
        for player in self.players:
            self._logger.info("\n\n***** Deck summary *****")
            self._logger.info(f"{player.label} won {player.wins} hands!")
            self._logger.info(f"{player.label} lost {player.losses} hands!")

    def play_round(self):
        self.deal_round()
        if not self.check_for_blackjack():
            self.players_turn()
            self.dealers_turn()
            self.settle()
        else:
            for player in self.players:
                if player.total != 21:
                    player.losses += 1
        self.discard_hand(self.dealer)
        for player in self.players:
            self.discard_hand(player)

    def players_turn(self):
        deck = self.deck
        for player in self.players:
            result = player.move(deck)
            if result == 'bust':
                self.discard_hand(player)

    def settle(self):
        dealer = self.dealer
        for player in reversed(self.players):
            if player.total > dealer.total:
                self._logger.info(f"*** Player {player.name} wins! ***")
                player.wins += 1
            elif player.total == dealer.total:
                self._logger.info(f"*** Player {player.name} pushes! ***")
            else:
                self._logger.info(f"*** Player {player.name} loses")
                player.losses += 1
