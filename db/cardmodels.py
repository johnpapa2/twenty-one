"""
Created on Feb 18, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.models import DeclarativeBase


class Rank(DeclarativeBase):
    """A Rank is a card value designator"""
    __tablename__ = 'rank'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class SuitType(DeclarativeBase):
    """A Suit Type is a card origin designator"""
    __tablename__ = 'suit_type'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Suit(DeclarativeBase):
    """A Suit is a card group designator"""
    __tablename__ = 'suit'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    suit_type_id = Column(Integer, ForeignKey('suit_type.id'))
    suit_type = relationship(SuitType)


class Card(DeclarativeBase):
    """A Card is an object with a rank and a suit"""
    __tablename__ = 'card'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    is_joker_card = Column(Boolean)
    rank_id = Column(Integer, ForeignKey('rank.id'))
    rank = relationship(Rank)
    suit_id = Column(Integer, ForeignKey('suit.id'))
    suit = relationship(Suit)


class Shoe(DeclarativeBase):
    """A Shoe is a collection of cards"""
    __tablename__ = 'shoe'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    number_of_decks = Column(Integer)


class ShoeElement(DeclarativeBase):
    """A Shoe element is a card in a hand"""
    __tablename__ = 'shoe_element'
    id = Column(Integer, primary_key=True)
    shoe_id = Column(Integer, ForeignKey('shoe.id'))
    shoe = relationship(Shoe)
    card_id = Column(Integer, ForeignKey('card.id'))
    card = relationship(Card)
    order = Column(Integer)
