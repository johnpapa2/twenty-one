"""
Created on Jan 15, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""


class Bet:

    def __init__(self, value=0):
        self._amount = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    def increase(self, additional_bet):
        self._amount += additional_bet
