#!/usr/bin/env python3
"""
Created on Dec 25, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import click
import logging

from blackjack import Blackjack

bj = None


@click.command()
@click.option('--players', default=1, type=click.IntRange(1, 7), help='Number of players.')
@click.option('--console', default='info', help='Console logging level.')
@click.option('--file', default='debug', help='File logging level.')
def play_game(players, console, file):
    global bj
    player_names = list()
    for player in range(players):
        player_names.append(click.prompt('Player name', default='John'))
    bj = Blackjack(player_names, console, file)
    logger = logging.getLogger('bj')
    shoe = bj.shoe
    shoe.shuffle()
    bj.burn_a_card()
    while len(shoe) > 3 * (len(bj.players) + 1):
        bj.play_round()
    for player in bj.players:
        logger.info("\n\n***** shoe summary *****")
        logger.info(f"{player} won {bj.wins[player]} hands!")
        logger.info(f"{player} lost {bj.losses[player]} hands!")
        logger.info(f"{player} bankroll is ${player.bankroll.amount}")

if __name__ == '__main__':
    play_game()
