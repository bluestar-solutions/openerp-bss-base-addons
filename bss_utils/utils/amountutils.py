# -*- coding: utf-8 -*-
# Part of Python Utilities.
# See LICENSE file for full copyright and licensing details.


class Direction():
    FLOOR = -1
    NEAR = 0
    CEIL = 1


def round_to(n, precision, direction=Direction.NEAR):
    correction = 0.0
    if direction == Direction.NEAR:
        correction = 0.5 if n >= 0 else -0.5
    elif direction == Direction.CEIL:
        if int(n / precision) * precision == n:
            return n
        correction = 1.0 if n >= 0 else -1.0
    return int(n / precision + correction) * precision


def round_to_05(n, direction=Direction.NEAR):
    return round_to(n, 0.05, direction)
