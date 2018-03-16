#!/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np


def cos(vect_1, vect_2):
    dot = np.dot(vect_1, vect_2)
    Lx = np.sqrt(np.dot(vect_1, vect_1))
    Ly = np.sqrt(np.dot(vect_2, vect_2))
    cos = dot / (Lx * Ly)
    return cos
