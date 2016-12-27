"""
Created on Dec 25, 2016

@author: john papa

Copyright 2016 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import click

from blackjack import Blackjack

bj = None


@click.command()
@click.option('--players', default=1, type=click.IntRange(1, 7), help='Number of players.')
def play_game(players):
    global bj
    player_names = list()
    for player in range(players):
        player_names.append(click.prompt('Player name', default='John'))
    bj = Blackjack(player_names)
    if click.confirm('Do you want to start game?', abort=True):
        click.echo('Lets do it!')
    bj.play()

if __name__ == '__main__':
    play_game()
