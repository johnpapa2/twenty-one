"""
Created on Feb 18, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import db

from sqlalchemy.orm import sessionmaker


class InitDbTables():
    """

    """
    def __init__(self):
        """ Initialize the database session

        Arguments:
            None
        """
        self._engine = db.models.db_connect()

        Session = sessionmaker(bind=self._engine)
        self._session = Session()

    def init_all(self):
        self.init_ranks()
        self.init_suit_types()
        self.init_suits()
        self.init_cards()
        self.init_action()
        self.init_result()
        self.init_player()

    def init_action(self):
        session = self._session
        action_dealt = db.Action(name='dealt')
        action_hit = db.Action(name='hit')
        action_stand = db.Action(name='stand')
        action_double = db.Action(name='double')
        action_split = db.Action(name='split')
        action_surrender = db.Action(name='surrender')
        session.add(action_dealt)
        session.add(action_hit)
        session.add(action_stand)
        session.add(action_double)
        session.add(action_split)
        session.add(action_surrender)
        session.commit()

    def init_cards(self, suit='French'):
        """ This will create a single deck of cards """
        session = self._session
        suit_type = session.query(db.SuitType).filter_by(name=suit).one()
        suits = session.query(db.Suit).filter_by(suit_type_id=suit_type.id).all()
        for suit in suits:
            ranks = session.query(db.Rank).all()
            if suit.id < 3:
                for rank in ranks:
                    card = db.Card(name=f"{rank.name} of {suit.name}", is_joker_card=False, rank_id=rank.id,
                                           suit_id=suit.id)
                    session.add(card)
            else:
                for rank in reversed(ranks):
                    card = db.Card(name=f"{rank.name} of {suit.name}", is_joker_card=False, rank_id=rank.id,
                                           suit_id=suit.id)
                    session.add(card)
        session.commit()

    def init_player(self):
        session = self._session
        player = db.Player(name='John', role='Player', bankroll=1000)
        dealer = db.Player(name='Mora', role='Dealer', bankroll=0)
        session.add(player)
        session.add(dealer)
        session.commit()

    def init_ranks(self):
        session = self._session
        rank_ace = db.Rank(name='Ace')
        session.add(rank_ace)

        for rank in range(2, 11):
            number_rank = db.Rank(name=rank)
            session.add(number_rank)

        rank_jack = db.Rank(name='Jack')
        rank_queen = db.Rank(name='Queen')
        rank_king = db.Rank(name='King')
        session.add(rank_jack)
        session.add(rank_queen)
        session.add(rank_king)
        session.commit()

    def init_result(self):
        session = self._session
        result_win = db.Result(name='win')
        result_lose = db.Result(name='lose')
        result_push = db.Result(name='push')
        result_bust = db.Result(name='bust')
        session.add(result_win)
        session.add(result_lose)
        session.add(result_push)
        session.add(result_bust)
        session.commit()

    def init_suit_types(self):
        session = self._session
        suit_type_french = db.SuitType(name='French')
        suit_type_german = db.SuitType(name='German')
        suit_type_italian = db.SuitType(name='Italian')
        suit_type_spanish = db.SuitType(name='Spanish')
        suit_type_swiss = db.SuitType(name='Swiss')
        session.add(suit_type_french)
        session.add(suit_type_german)
        session.add(suit_type_italian)
        session.add(suit_type_spanish)
        session.add(suit_type_swiss)
        session.commit()

    def init_suits(self):
        session = self._session
        # French deck suits
        suit_type = session.query(db.SuitType).filter_by(name='French').one()
        suit_spades = db.Suit(name='spades', suit_type_id=suit_type.id)
        suit_diamonds = db.Suit(name='diamonds', suit_type_id=suit_type.id)
        suit_clubs = db.Suit(name='clubs', suit_type_id=suit_type.id)
        suit_hearts = db.Suit(name='hearts', suit_type_id=suit_type.id)
        session.add(suit_spades)
        session.add(suit_diamonds)
        session.add(suit_clubs)
        session.add(suit_hearts)

        # German deck suits
        suit_type = session.query(db.SuitType).filter_by(name='German').one()
        suit_leaves = db.Suit(name='leaves', suit_type_id=suit_type.id)
        suit_bells = db.Suit(name='bells', suit_type_id=suit_type.id)
        suit_acorns = db.Suit(name='acorns', suit_type_id=suit_type.id)
        suit_german_hearts = db.Suit(name='hearts', suit_type_id=suit_type.id)
        session.add(suit_leaves)
        session.add(suit_bells)
        session.add(suit_acorns)
        session.add(suit_german_hearts)

        # Italian deck suits
        suit_type = session.query(db.SuitType).filter_by(name='Italian').one()
        suit_swords = db.Suit(name='swords', suit_type_id=suit_type.id)
        suit_coins = db.Suit(name='coins', suit_type_id=suit_type.id)
        suit_italian_clubs = db.Suit(name='clubs', suit_type_id=suit_type.id)
        suit_cups = db.Suit(name='cups', suit_type_id=suit_type.id)
        session.add(suit_swords)
        session.add(suit_coins)
        session.add(suit_italian_clubs)
        session.add(suit_cups)

        # Spanish deck suits
        suit_type = session.query(db.SuitType).filter_by(name='Spanish').one()
        suit_spanish_swords = db.Suit(name='swords', suit_type_id=suit_type.id)
        suit_spanish_coins = db.Suit(name='coins', suit_type_id=suit_type.id)
        suit_spanish_clubs = db.Suit(name='clubs', suit_type_id=suit_type.id)
        suit_spanish_cups = db.Suit(name='cups', suit_type_id=suit_type.id)
        session.add(suit_spanish_swords)
        session.add(suit_spanish_coins)
        session.add(suit_spanish_clubs)
        session.add(suit_spanish_cups)

        # Swiss deck suits
        suit_type = session.query(db.SuitType).filter_by(name='Swiss').one()
        suit_shields = db.Suit(name='shields', suit_type_id=suit_type.id)
        suit_swiss_bells = db.Suit(name='bells', suit_type_id=suit_type.id)
        suit_swiss_acorns = db.Suit(name='acorns', suit_type_id=suit_type.id)
        suit_roses = db.Suit(name='roses', suit_type_id=suit_type.id)
        session.add(suit_shields)
        session.add(suit_swiss_bells)
        session.add(suit_swiss_acorns)
        session.add(suit_roses)

        session.commit()
