#!/usr/bin/env python
# -*- coding: utf-8 -*-

from us_rep.processors import *


def run():
    senate.run()
    house_of_reps.run()


if __name__ == '__main__':
    run()
