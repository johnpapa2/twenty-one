"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import datetime
import db
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
        engine = models.db_connect()
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()
        self._shoe = Shoe(self._session, 1)
        self._dealer = Player(self._session, 'Mora', 'Dealer')
        self._players = [Player(self._session, name, 'Player') for name in player_names]
        self._discard_pile = DiscardPile()
        self._log_directory = "./logs"
        self._losses = dict()
        self._round = None
        self._wins = dict()
        self._results = {result.name: result.id for result in self._session.query(db.Result).all()}
        self._match = db.Match(start_time=datetime.datetime.now(),
                             number_of_players=len(self._players),
                             shoe_id=self.shoe.db_info.id)
        self._session.add(self._match)
        self._session.commit()
        spot = 0
        participant = db.Participant(spot=spot, match_id=self._match.id, player_id=self._dealer.db_info.id)
        self._session.add(participant)
        self._session.commit()
        self._dealer.participant_id = participant.id
        for player in self.players:
            spot += 1
            self._wins[player] = 0
            self._losses[player] = 0
            participant = db.Participant(spot=spot, match_id=self._match.id, player_id=player.db_info.id)
            self._session.add(participant)
            self._session.commit()
            player.participant_id = participant.id
        self._init_logger(console_log_level, file_log_level)
        self._logger = logging.getLogger('bj')
        self._deck_of_cards = {card.name: card.id for card in self._session.query(db.Card).all()}

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
                player.receives('dealt', self.shoe.deal_card())
            self.dealer.receives('dealt', self.shoe.deal_card())
            if i == 0:
                self._round.dealer_up_card_id = self._deck_of_cards[str(self.dealer.hand[0])]
        self.dealer.hand.db_info.start_value = self.dealer.hand.value
        for player in self.players:
            player.hand.db_info.start_value = player.hand.value
        self._session.commit()

    def dealers_turn(self):
        """ Dealers turn """
        self._logger.info(self.dealer.display_hand())
        self._logger.info(f"{self.dealer}'s turn:")
        self.dealer.hand.db_info.round_id = self._round.id
        self.dealer.hand.db_info.participant_id = self.dealer.participant_id
        self._session.commit()
        while self.dealer.hand.value < 17:
            self.dealer.move('hit', self.shoe)
        self.dealer.hand.db_info.final_value = self.dealer.hand.value
        if self.dealer.hand.value > 21:
            self.dealer.hand.db_info.result_id = self._results['bust']
            dealer_outcome = db.DealerOutcome(hand_total=self.dealer.hand.value,
                                              soft_hand=False,
                                              result_id=self._results['bust'])
            self.discard_hand(self.dealer)
            self.dealer.busted = False
        else:
            self.dealer.hand.db_info.result_id = self._results['pat']
            dealer_outcome = db.DealerOutcome(hand_total=self.dealer.hand.value, result_id=self._results['pat'])
        self._session.add(dealer_outcome)
        self._session.commit()
        self._round.dealer_outcome_id = dealer_outcome.id
        self._session.commit()

    def discard_hand(self, player):
        """ Move the players hand to the discard pile """
        for card in player.discard_hand():
            self.discard_pile.receives(card)

    def end_match(self):
        """ Log the end time of the match """
        self._match.end_time = datetime.datetime.now()
        self._session.commit()
        self._session.close()

    def play_round(self):
        """ Play a round of blackjack, from Players placing bets until bets are settled """
        self._round = db.Round(start_time=datetime.datetime.now(),
                         number_of_players=len(self.players),
                         match_id=self._match.id)
        self._session.add(self._round)
        self._session.commit()

        self.take_bets()
        self.deal_round()
        if not self.dealer.hand.is_blackjack:
            self.players_turn()
            self.dealers_turn()
            self.settle()
        else:
            dealer_outcome = db.DealerOutcome(hand_total=21, soft_hand=True, result_id=self._results['blackjack'])
            self._session.add(dealer_outcome)
            self._session.commit()
            self._round.dealer_outcome_id = dealer_outcome.id
            self._session.commit()
            self._logger.info(f"Dealer shows a [{self.dealer.hand[0].rank}]")
            for player in self.players:
                self._logger.info(player.display_hand())
                player.hand.db_info.round_id = self._round.id
                player.hand.db_info.participant_id = player.participant_id
                player.hand.db_info.final_value = player.hand.value
                if not player.hand.is_blackjack:
                    self.losses[player] += 1
                    player.hand.db_info.result_id = self._results['lose']
                else:
                    player.hand.db_info.result_id = self._results['push']
                self._session.commit()
            self._logger.info(f"Dealer has a Blackjack!")
            self._logger.info(self.dealer.display_hand())
            self.dealer.hand.db_info.result_id = self._results['blackjack']
            self.dealer.hand.db_info.round_id = self._round.id
            self.dealer.hand.db_info.participant_id = self.dealer.participant_id
            self.dealer.hand.db_info.final_value = self.dealer.hand.value
            self._session.commit()
        if self.dealer.hand is not None:
            self.discard_hand(self.dealer)
        for player in self.players:
            if player.hand:
                self.discard_hand(player)
            db_player = self._session.query(db.Player).filter_by(name=player.name).one()
            db_player.bankroll = player.bankroll.amount
            self._session.commit()
        self._round.end_time = datetime.datetime.now()
        self._session.commit()

    def players_turn(self):
        """ Players turn """
        shoe = self.shoe
        for player in self.players:
            player.hand.db_info.round_id = self._round.id
            player.hand.db_info.participant_id = player.participant_id
            self._session.commit()
            self._logger.info(f"Dealer shows a [{self.dealer.hand[0].rank}]")
            self._logger.info(player.display_hand())
            if player.hand.is_blackjack:
                player.hand.db_info.is_blackjack = True
                self._session.commit()
            else:
                action = 'hit'
                while action == 'hit' and player.hand:
                    #action = click.prompt(f'{player}, your turn', default='stand')
                    action = 'stand'
                    player.move(action, shoe)
                    if player.hand.value > 21:
                        player.hand.db_info.result_id = self._results['bust']
                        player.hand.db_info.final_value = player.hand.value
                        self._session.commit()
                        self._logger.info(f"{player} busts!")
                        self.discard_hand(player)

    def settle(self):
        """ Settle the bets at the end of the round. Pay winners, take loser's bets and push equal hands """
        dealer = self.dealer
        for player in reversed(self.players):
            if player.hand is None:
                self.losses[player] += 1
            elif player.hand.is_blackjack:
                player.hand.db_info.result_id = self._results['blackjack']
                player.hand.db_info.final_value = player.hand.value
                self._logger.info(f"*** {player} wins ${player.hand.bet.amount} with a Natural! ***")
                player.bankroll.invest(player.hand.bet.amount * 2.5)
                self.wins[player] += 1
            elif player.hand is not None and dealer.hand is None:
                player.hand.db_info.result_id = self._results['win']
                player.hand.db_info.final_value = player.hand.value
                self._logger.info(f"*** {player} wins ${player.hand.bet.amount}! ***")
                player.bankroll.invest(player.hand.bet.amount * 2)
                self.wins[player] += 1
            elif player.hand.value > dealer.hand.value:
                player.hand.db_info.result_id = self._results['win']
                player.hand.db_info.final_value = player.hand.value
                self._logger.info(f"*** {player} wins ${player.hand.bet.amount}! ***")
                player.bankroll.invest(player.hand.bet.amount * 2)
                self.wins[player] += 1
            elif player.hand.value == dealer.hand.value:
                player.hand.db_info.result_id = self._results['push']
                player.hand.db_info.final_value = player.hand.value
                self._logger.info(f"*** {player} pushes! ***")
                player.bankroll.invest(player.hand.bet.amount)
            else:
                player.hand.db_info.result_id = self._results['lose']
                player.hand.db_info.final_value = player.hand.value
                self._logger.info(f"*** {player} loses ${player.hand.bet.amount}! ***")
                self.losses[player] += 1
            self._session.commit()
            self._logger.info("\n")

    def take_bets(self):
        """ Give each player a chance to place a bet before dealing a round """
        for player in self.players:
            self._logger.info(f"{player}'s bankroll is ${player.bankroll.amount}")
            #bet_amount = click.prompt(f'{player}, please place bet', default=25)
            bet_amount = 100
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
