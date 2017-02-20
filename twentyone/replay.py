#!/usr/bin/env python3
"""
Created on Feb 18, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import db

from db import models
from sqlalchemy.orm import sessionmaker


class Replay():
    """ This is a class for the command line interface used for the game of Blackjack.

    This class should work for any standard game of blackjack or twenty-one.

    """
    def __init__(self):
        engine = models.db_connect()
        DBSession = sessionmaker(bind=engine)
        self._session = DBSession()

    def replay_all(self):
        games = self._session.query(db.Game).all()
        for game in games:
            self.replay_game(game)
            print("\n\n")

    def replay_game(self, game):
        game_header = f"Game {game.id} - start time: {game.start_time}"
        print_break = "-" * len(game_header)
        print(print_break)
        print(game_header)
        print(print_break)
        print(f"Number of players: {game.number_of_players}")
        print(f"Shoe ID: {game.shoe.id}")

        rounds = self._session.query(db.Round).filter_by(game_id=game.id).all()
        for round in rounds:
            self.replay_round(round)
            print("\n")

        print(f"end time: {game.end_time}")

    def replay_round(self, round):
        print(f"  Round {round.id} - start time: {round.start_time}")
        print(f"  Number of players: {round.number_of_players}")

        hands = self._session.query(db.Hand).filter_by(round_id=round.id).order_by(db.Hand.participant.spot).all()
        for hand in hands:
            self.replay_hand(hand)
            print("")

        print(f"    Dealer {round.dealer_outcome.result.name}")
        print(f"  end time: {round.start_time}")

    def replay_hand(self, hand):
        player = hand.participant.player
        print(f"    {player.role} {player.name} bets {hand.bet} on hand {hand.id}")
        if hand.is_blackjack:
            print(f"    Hand is a Blackjack!")

        hand_elements = self._session.query(db.HandElement).filter_by(hand_id=hand.id).all()
        for element in hand_elements:
            self.replay_hand_element(element)

        print(f"    -- Hand total: {hand.total}")
        print(f"    -- Hand result is {hand.result.name}")

    def replay_hand_element(self, element):
        print(f"    Action {element.action.name} - Card is {element.card.name}")

if __name__ == '__main__':
    replay = Replay()
    replay.replay_all()
