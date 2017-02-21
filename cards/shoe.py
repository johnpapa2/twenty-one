"""
Created on Jan 15, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import db
import logging
import random

from .bjcard import BjCard


class Shoe():
    """ This is a class for a Shoe composed of cards from one or more french decks.

    A shoe from this class should work for any standard card game.

    """
    def __init__(self, session, num_decks=1):
        """ Initialize shoe with n number of decks, with each deck in standard 52 card new deck order

        Arguments:
            num_decks - The number of decks in the shoe.
        """
        self._session = session
        self._cards = list()
        deck_of_cards = self._session.query(db.Card).all()
        for deck in range(num_decks):
            for card in deck_of_cards:
                self._cards.append(BjCard(session, card.suit.name, card.rank.name))

            self._logger = logging.getLogger('bj')
            self._logger.info("New deck of cards opened and spread")
        self._db_info = db.Shoe(number_of_decks=num_decks)
        session.add(self._db_info)
        session.commit()

    def __getitem__(self, position):
        """ Return the card at a given position

        Arguments:
            position - The position of the card to return
        """
        return self._cards[position]

    def __len__(self):
        """ Return the number of cards in the shoe """
        return len(self._cards)

    @property
    def db_info(self):
        """ Returns the db object associated with this shoe """
        return self._db_info

    def deal_card(self):
        """ Remove the top card from the shoe and return it """
        card = self._cards.pop(0)
        self._logger.debug(f"  Dealing a {card}")
        return card

    def shuffle(self):
        """ Shuffle the shoe """
        # TODO: Implement real shuffling algorithms to simulate how people actually shuffle
        #       This will be useful for shuffle tracking simulations
        random.shuffle(self._cards)
        self._logger.info("Now's a good time to take a break while I shuffle")
        self._add_shoe_to_db()

    def _add_shoe_to_db(self):
        for index, card in enumerate(self._cards):
            db_card = self._session.query(db.Card).filter_by(name=str(card)).one()
            shoe_element = db.ShoeElement(order=index + 1, shoe_id=self._db_info.id, card_id=db_card.id)
            self._session.add(shoe_element)
            self._session.commit()
