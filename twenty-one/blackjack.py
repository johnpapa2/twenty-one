"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import click
import logging
import os
import uuid

from cards import Shoe
from cards import DiscardPile
from players import Player
from sqlalchemy.orm import sessionmaker
from db import models, cardmodels, bjmodels


class Blackjack():
    """ This is a class for the command line interface used for the game of Blackjack.

    This class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self, player_names, console_log_level=None, file_log_level=None):
        """ Initialize the blackjack game

        Arguments:
            player_names - A list of player names
            console_log_level - The log level for stdout
            file_log_level - The log level used for writing to the log file.
        """
        self._shoe = Shoe()
        self._dealer = Player('Mora', 'Dealer')
        self._players = [Player(name, 'Player') for name in player_names]
        self._discard_pile = DiscardPile()
        self._log_directory = "./logs"
        self._losses = dict()
        self._wins = dict()
        for player in self.players:
            self._wins[player] = 0
            self._losses[player] = 0
        self._init_logger(console_log_level, file_log_level)
        self._logger = logging.getLogger('bj')
        engine = models.db_connect()
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()

    @property
    def dealer(self):
        """ Returns the deal of the current game """
        return self._dealer

    @property
    def shoe(self):
        """ Returns the shoe from the current game """
        return self._shoe

    @property
    def discard_pile(self):
        """ Returns the discard pile of the current game """
        return self._discard_pile

    @property
    def losses(self):
        """ Returns a dictionary with the number of losses"""
        return self._losses

    @property
    def players(self):
        """ Returns the players currently sitting at the table """
        return self._players

    @property
    def wins(self):
        """ Returns a dictionary with the number of wins"""
        return self._wins

    def burn_a_card(self):
        """ Burn the top card in the shoe """
        card = self.shoe.deal_card()
        self._logger.info(f"Burn the {card}")
        self.discard_pile.receives(card)

    def deal_round(self):
        """ Deal a round of blackjack """
        self._logger.info("No more bets. Good luck.")
        self.dealer.place_bet(0)
        for i in range(2):
            for player in self.players:
                player.receives(self.shoe.deal_card())
            self.dealer.receives(self.shoe.deal_card())

    def dealers_turn(self):
        """ Dealers turn """
        self._logger.info(self.dealer.display_hand())
        self._logger.info(f"{self.dealer}'s turn:")
        while self.dealer.hand.value < 17:
            self.dealer.move('hit', self.shoe)
        if self.dealer.hand.value > 21:
            self.discard_hand(self.dealer)
            self.dealer.busted = False

    def discard_hand(self, player):
        """ Move the players hand to the discard pile """
        for card in player.discard_hand():
            self.discard_pile.receives(card)

    def play_round(self):
        """ Play a round of blackjack, from Players placing bets until bets are settled """
        self.take_bets()
        self.deal_round()
        if not self.dealer.hand.is_blackjack:
            self.players_turn()
            self.dealers_turn()
            self.settle()
        else:
            for player in self.players:
                if player.hand.value != 21:
                    self.losses[player] += 1
        if self.dealer.hand is not None:
            self.discard_hand(self.dealer)
        for player in self.players:
            if player.hand:
                self.discard_hand(player)

    def players_turn(self):
        """ Players turn """
        shoe = self.shoe
        for player in self.players:
            self._logger.info(f"Dealer shows a [{self.dealer.hand[0].rank}]")
            self._logger.info(player.display_hand())
            action = 'hit'
            while action == 'hit' and player.hand:
                action = click.prompt(f'{player}, your turn', default='stand')
                player.move(action, shoe)
                if player.hand.value > 21:
                    self._logger.info(f"{player} busts!")
                    self.discard_hand(player)

    def settle(self):
        """ Settle the bets at the end of the round. Pay winners, take loser's bets and push equal hands """
        dealer = self.dealer
        for player in reversed(self.players):
            if player.hand is None:
                self.losses[player] += 1
            elif player.hand.value == 21 and len(player.hand) == 2:
                self._logger.info(f"*** {player} wins ${player.hand.bet.amount} with a Natural! ***")
                player.bankroll.invest(player.hand.bet.amount * 2.5)
                self.wins[player] += 1
            elif player.hand is not None and dealer.hand is None:
                self._logger.info(f"*** {player} wins ${player.hand.bet.amount}! ***")
                player.bankroll.invest(player.hand.bet.amount * 2)
                self.wins[player] += 1
            elif player.hand.value > dealer.hand.value:
                self._logger.info(f"*** {player} wins ${player.hand.bet.amount}! ***")
                player.bankroll.invest(player.hand.bet.amount * 2)
                self.wins[player] += 1
            elif player.hand.value == dealer.hand.value:
                self._logger.info(f"*** {player} pushes! ***")
                player.bankroll.invest(player.hand.bet.amount)

            else:
                self._logger.info(f"*** {player} loses ${player.hand.bet.amount}! ***")
                self.losses[player] += 1
            self._logger.info("\n")

    def take_bets(self):
        """ Give each player a chance to place a bet before dealing a round """
        for player in self.players:
            self._logger.info(f"{player}'s bankroll is ${player.bankroll.amount}")
            bet_amount = click.prompt(f'{player}, please place bet', default=25)
            player.place_bet(bet_amount)

    def _init_logger(self, console_log_level=None, file_log_level=None):
        """ Initialize the log file and logger.

        Arguments:
            console_log_level - The log level used for displaying output to standard out.
            file_log_level - The logging level to use for the log files.
        """
        # Create log directory if it doesn't already exist.
        if not os.path.exists(self._log_directory):
            os.makedirs(self._log_directory)

        log_filename = f"{self._log_directory}/bj_{uuid.uuid1()}.log"

        file_logging = logging.DEBUG
        if file_log_level == 'info':
            file_logging = logging.INFO
        elif file_log_level == 'warning':
            file_logging = logging.WARNING
        elif file_log_level == 'error':
            file_logging = logging.ERROR

        # Add the date to the log file names
        logging.basicConfig(
            filename=log_filename,
            filemode='w',
            level=file_logging,
            format='%(asctime)s|%(levelname)-5s| %(message)s',
            datefmt='%Y-%m-%d %I:%M:%S %p')

        console_logging = logging.DEBUG
        if console_log_level == 'info':
            console_logging = logging.INFO
        elif console_log_level == 'warning':
            console_logging = logging.WARNING
        elif console_log_level == 'error':
            console_logging = logging.ERROR

        console = logging.StreamHandler()
        console.setLevel(console_logging)
        # set a format which is simpler for console use
        #formatter = logging.Formatter('%(levelname)-5s| %(message)s')
        formatter = logging.Formatter('%(message)s')
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
