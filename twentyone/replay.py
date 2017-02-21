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

    @property
    def session(self):
        return self._session

    def replay_all(self):
        matches = self._session.query(db.Match).all()
        for match in matches:
            self.replay_match(match)
            print("\n\n")

    def replay_match(self, match):
        match_header = f"Match {match.id} - start time: {match.start_time}"
        print_break = "-" * len(match_header)
        print(print_break)
        print(match_header)
        print(print_break)
        print(f"Number of players: {match.number_of_players}")
        print(f"Shoe ID: {match.shoe.id}")

        rounds = self._session.query(db.Round).filter_by(match_id=match.id).all()
        for round in rounds:
            self.replay_round(round)
            print("\n")

        print(f"end time: {match.end_time}")

    def replay_round(self, round):
        print(f"  Round {round.id} - start time: {round.start_time}")
        print(f"  Number of players: {round.number_of_players}")
        print(f"  -- Dealer shows a {round.dealer_up_card.name}")

        hands = self.session.query(db.Hand).filter_by(round_id=round.id).all()
        for hand in hands:
            self.replay_hand(hand)
            print("")

        print(f"    Dealer {round.dealer_outcome.result.name}")
        print(f"  end time: {round.start_time}")

    def replay_hand(self, hand):
        player = hand.participant.player
        print(f"    {player.role} {player.name} bets {hand.bet} on hand {hand.id}")
        if hand.is_blackjack:
            print(f"      Hand is a Blackjack!")
        print(f"      -- Hand starting value: {hand.start_value}")

        hand_elements = self.session.query(db.HandElement).filter_by(hand_id=hand.id).all()
        for element in hand_elements:
            self.replay_hand_element(element)

        print(f"      -- Hand final value: {hand.final_value}")
        print(f"      -- Hand result is {hand.result.name}")

    def replay_hand_element(self, element):
        print(f"        Action {element.action.name} - Card is {element.card.name}")

    def replay_starting_hand(self, total, upcard=None):
        hands = self.session.query(db.Hand).filter_by(start_value=total, is_player=True).all()
        for hand in hands:
            round = self.session.query(db.Round).filter_by(id=hand.round.id).one()
            self.replay_round(round)
            print("\n")

    def win_loss(self, final_total=None, start_total=None, upcard=None):
        strategies = self.session.query(db.Strategy).all()
        for strategy in strategies[1:]:
            if start_total:
                print(f"Results for strategy {strategy.name}, starting totals of {start_total}:")
                hands = self.session.query(db.Hand).filter_by(start_value=start_total, is_player=True).all()
            if final_total:
                print(f"Results for strategy {strategy.name}, final totals of {final_total}:")
                hands = self.session.query(db.Hand).filter_by(final_value=final_total, is_player=True).all()

            results = {result.name: 0 for result in self.session.query(db.Result).all()}
            for hand in hands:
                if strategy.id == hand.participant.strategy.id:
                    results[hand.result.name] += 1

            number_of_hands = sum([number for result, number in results.items()])
            if number_of_hands:
                print(f"  Wins:   {results['win']} - {(results['win'] / number_of_hands):.2%}")
                print(f"  Losses: {results['lose']} - {(results['lose'] / number_of_hands):.2%}")
                print(f"  Pushes: {results['push']} - {(results['push'] / number_of_hands):.2%}")
            else:
                print("  No hands found for this strategy")

if __name__ == '__main__':
    replay = Replay()
    replay.replay_all()
