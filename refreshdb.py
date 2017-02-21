#!/usr/bin/env python3
"""
Created on Feb 19, 2017

@author: john papa

Copyright 2017 John Papa.  All rights reserved.
This work is licensed under the MIT License.
"""
from db import models
from twentyone import InitDbTables


def refresh():
    engine = models.db_connect()
    models.recreate_db(engine)
    setup = InitDbTables()
    setup.init_all()

if __name__ == '__main__':
    refresh()
