#!/usr/bin/env python3
"""
Created on Feb 20, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
import click

from replay import Replay


@click.command()
@click.option('--start', type=click.IntRange(4, 21), help='Value of starting hand.')
@click.option('--final', type=click.IntRange(4, 40), help='Final value of hand.')
def analyze(start, final):
    replay = Replay()
    if start:
        replay.win_loss(start_total=start)
    if final:
        replay.win_loss(final_total=final)

if __name__ == '__main__':
    analyze()
