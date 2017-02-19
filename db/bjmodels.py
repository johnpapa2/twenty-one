"""
Created on Feb 18, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.models import DeclarativeBase
from db.cardmodels import Card


class Player(DeclarativeBase):
    """A Player is an object with bets and hands"""
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)


class Action(DeclarativeBase):
    """An Action is how the card got into the hand"""
    __tablename__ = 'action'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Result(DeclarativeBase):
    """A Result is an outcome of a hand"""
    __tablename__ = 'result'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Hand(DeclarativeBase):
    """A Hand is a collection of cards"""
    __tablename__ = 'hand'
    id = Column(Integer, primary_key=True)
    is_blackjack = Column(Boolean)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship(Player)
    bet = Column(Integer)
    result_id = Column(Integer, ForeignKey('result.id'))
    result = relationship(Result)


class HandElement(DeclarativeBase):
    """A Hand element is a card in a hand"""
    __tablename__ = 'hand_element'
    id = Column(Integer, primary_key=True)
    hand_id = Column(Integer, ForeignKey('hand.id'))
    hand = relationship(Hand)
    card_id = Column(Integer, ForeignKey('card.id'))
    card = relationship(Card)
    action_id = Column(Integer, ForeignKey('action.id'))
    action = relationship(Action)
    order = Column(Integer)
