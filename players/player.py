"""
Created on Dec 24, 2016

@author: john papa

Copyright 2016 - 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import logging

from .bankroll import Bankroll
from .bjhand import BjHand


class Player():
    """ This is a class for Players used in the game of Blackjack.

    Players from this class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self, name, role='Player'):
        """ Initialize the player with a role and name.

        Arguments:
            name - The name of the Player.
            role - The players role. This can be 'Player' or 'Dealer'.
        """
        self._bankroll = Bankroll(1000)
        self._hand = None
        self._name = name
        self._role = role
        self._logger = logging.getLogger('bj')
        if role == 'Dealer':
            self._logger.info(f"{self} taps into table")
        elif role == 'Player':
            self._logger.info(f"{self} sits at table")

    def __str__(self):
        """ Returns a description of the player """
        return f"{self.role} {self.name}"

    @property
    def bankroll(self):
        """ Returns the player's bankroll """
        return self._bankroll

    @property
    def hand(self):
        """ Returns the player's hand """
        return self._hand

    @hand.setter
    def hand(self, new_hand):
        """ Set the player's hand to a new hand

        Arguments:
            new_hand - The new hand to set the player's hand to.
        """
        self._hand = new_hand

    @property
    def name(self):
        """ Returns the player's name """
        return self._name

    @property
    def role(self):
        """ Returns the player's role """
        return self._role

    def discard_hand(self):
        """ Returns all the cards from the player's hand so they can be added to the discard pile """
        discards = self.hand.cards
        self.hand = None
        return discards

    def display_hand(self):
        """ Returns a description of the player's hand """
        hand_display = f"{self} has {self.hand}"
        return hand_display

    def double(self, shoe):
        """ Double down on the player's hand

        Arguments:
            shoe - The shoe that the next card will be dealt from.
        """
        if self.role == 'Player':
            self._logger.info(f"{self} doubles")
            self.bankroll.withdraw(self.hand.bet.amount)
            self.hand.bet.increase(self.hand.bet.amount)
            self.receives(shoe.deal_card())
            self._logger.info(self.display_hand())
            if self.hand.value > 21:
                self.busted = True
                self._logger.info(f"{self} Busted!")
            self._logger.info(f"*** {self} loses ${self.hand.bet.amount}! ***")
        else:
            return
        self._logger.info(f"{self}'s hand value is {self.hand.value}")

    def hit(self, shoe):
        """ Take a card

        Arguments:
            shoe - The shoe that the next card will be dealt from.
        """
        self._logger.info(f"{self} hits")
        self.receives(shoe.deal_card())
        self._logger.info(self.display_hand())
        if self.hand.value > 21:
            self.busted = True
            self._logger.info(f"{self} Busted!")
            self._logger.info(f"*** {self} loses ${self.hand.bet.amount}! ***")
        self._logger.info(f"{self}'s hand value is {self.hand.value}")

    def move(self, action, shoe):
        """ Make a move

        Arguments:
            action - The action to be taken.
            shoe - The shoe to deal a card from if needed.
        """
        if action == 'hit':
            self.hit(shoe)
        elif action == 'double':
            self.double(shoe)
        elif action == 'stand':
            self.stand()
        elif action == 'split':
            pass

    def stand(self):
        """ Stand """
        self._logger.info(f"{self} stands!")
        self._logger.info(f"{self}'s hand value is {self.hand.value}")

    def place_bet(self, bet):
        """ Place's a bet before receiving a new hand

        Arguments:
            bet - The amount to bet on the new hand.
        """
        self._logger.info(f"{self}'s bankroll is ${self.bankroll.amount}")
        self.bankroll.amount -= bet
        self._hand = BjHand(bet)
        self._logger.info(f"{self} bets ${bet} dollars.")

    def receives(self, card):
        """ Adds a card to the player's hand

        Arguments:
            card - The card to add to the player's hand.
        """
        self.hand.add_card(card)
        self._logger.debug(f"{self} gets {card}")
