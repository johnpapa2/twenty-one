"""
Created on Jan 16, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""


class Bankroll:

    def __init__(self, value=0):
        self._amount = value

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = value

    def invest(self, investment):
        self._amount += investment

    def withdraw(self, withdrawl):
        self._amount -= withdrawl
