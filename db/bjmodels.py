"""
Created on Feb 18, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from sqlalchemy import Column, ForeignKey, Boolean, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship
from db.models import DeclarativeBase
from db import Card
from db import Shoe


class Player(DeclarativeBase):
    """A Player is an object with bets and hands"""
    __tablename__ = 'player'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    bankroll = Column(Float)


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


class DealerOutcome(DeclarativeBase):
    """A Dealer Outcome is a the dealer's outcome of a hand"""
    __tablename__ = 'dealer_outcome'
    id = Column(Integer, primary_key=True)
    hand_total = Column(Integer)
    soft_hand = Column(Boolean)
    result_id = Column(Integer, ForeignKey('result.id'))
    result = relationship(Result)


class Game(DeclarativeBase):
    """A Game is the game of blackjack played for a single shoe"""
    __tablename__ = 'game'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    number_of_players = Column(Integer)
    shoe_id = Column(Integer, ForeignKey('shoe.id'))
    shoe = relationship(Shoe)


class Participant(DeclarativeBase):
    """A Participant is a player of a specific game"""
    __tablename__ = 'participant'
    id = Column(Integer, primary_key=True)
    spot = Column(Integer)
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship(Game)
    player_id = Column(Integer, ForeignKey('player.id'))
    player = relationship(Player)


class Round(DeclarativeBase):
    """A Round is a single round of Blackjack"""
    __tablename__ = 'round'
    id = Column(Integer, primary_key=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    number_of_players = Column(Integer)
    dealer_outcome_id = Column(Integer, ForeignKey('dealer_outcome.id'))
    dealer_outcome = relationship(DealerOutcome)
    game_id = Column(Integer, ForeignKey('game.id'))
    game = relationship(Game)


class RoundOrder(DeclarativeBase):
    """A Round Order is the players of single round of Blackjack"""
    __tablename__ = 'round_order'
    id = Column(Integer, primary_key=True)
    spot = Column(Integer)
    participant_id = Column(Integer, ForeignKey('participant.id'))
    participant = relationship(Participant)
    round_id = Column(Integer, ForeignKey('round.id'))
    round = relationship(Round)


class Hand(DeclarativeBase):
    """A Hand is a collection of cards"""
    __tablename__ = 'hand'
    id = Column(Integer, primary_key=True)
    bet = Column(Integer)
    is_blackjack = Column(Boolean)
    total = Column(Integer)
    participant_id = Column(Integer, ForeignKey('participant.id'))
    participant = relationship(Participant)
    result_id = Column(Integer, ForeignKey('result.id'))
    result = relationship(Result)
    round_id = Column(Integer, ForeignKey('round.id'))
    round = relationship(Round)


class HandElement(DeclarativeBase):
    """A Hand element is a card in a hand"""
    __tablename__ = 'hand_element'
    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    hand_id = Column(Integer, ForeignKey('hand.id'))
    hand = relationship(Hand)
    card_id = Column(Integer, ForeignKey('card.id'))
    card = relationship(Card)
    action_id = Column(Integer, ForeignKey('action.id'))
    action = relationship(Action)
