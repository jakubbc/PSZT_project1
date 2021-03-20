#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" individual
Authors: Jakub Ciemięga, Krzysztof Piątek
"""

import numpy as np
import cv2


def generate_individual(img_size: int) -> np.ndarray:
    """ generate an individual for the pop

    :param img_size: size of the square input image
    :type img_size: int

    :return: individual
    :rtype: np.ndarray with shape (k, 8) where k is number of rectangles of a given individual. Each row contains
    information about one rectangle: top-left corner (x1,y1), bottom-right corner (x2,y2) and image canals (BGRA) which
    are Integer values in range 0-255
    """

    # draw number of rectangles k
    k = np.random.randint(5, 11)
    # print(k)
    # create individual consisting of k rectangles
    individual = np.zeros((k, 8), int)

    # fill rectangles
    # x1, y1
    individual[:, :2] = np.random.randint(0, img_size - 1, (k, 2))
    # x2, y2
    for i in range(k):
        individual[i, 2] = np.random.randint(individual[i, 0] + 1, img_size)
        individual[i, 3] = np.random.randint(individual[i, 1] + 1, img_size)
    # BGRA canals
    individual[:, 4:] = np.random.randint(0, 256, (k, 4))

    # print(individual.shape)

    return individual


def create_image(img_size: int, individual: np.ndarray) -> np.ndarray:
    """ generate image based on an individual
    
    :param img_size: size of the square input image
    :type img_size: int
    
    :param individual: individual base the generated image on
    :type individual: np.ndarray with shape (k, 8) where k is number of rectangles of a given individual. Each row 
    contains information about one rectangle: top-left corner (x1,y1), bottom-right corner (x2,y2) and image canals
    (BGRA) which are Integer values in range 0-255
    
    :return: img: image generated by putting together all rectangles of a given individual
    :rtype: img: np.ndarray with shape (img_size, img_size)
    """

    B = np.zeros((img_size, img_size), int)
    G = np.zeros((img_size, img_size), int)
    R = np.zeros((img_size, img_size), int)
    # print(individual.shape[0])

    for i in range(individual.shape[0]):
        # print(individual)
        x1, y1, x2, y2, b, g, r, alpha = individual[i]
        # alpha should be in range 0-1
        alpha /= 255.
        B[y1:y2 + 1, x1:x2 + 1] = (1 - alpha) * B[y1:y2 + 1, x1:x2 + 1] + alpha * b
        G[y1:y2 + 1, x1:x2 + 1] = (1 - alpha) * G[y1:y2 + 1, x1:x2 + 1] + alpha * g
        R[y1:y2 + 1, x1:x2 + 1] = (1 - alpha) * R[y1:y2 + 1, x1:x2 + 1] + alpha * r

    # print(individual.shape[0])

    return cv2.merge((B, G, R))
