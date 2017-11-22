#!/usr/bin/python
# -*- coding: utf-8 -*-


import random, string, time
from Person import *

class Village ():
    """generates a list of Person()s and contains a method to immigrate from another village. If
    called from Region(), a distancematrix is also created that allows the inhabitants to select their potential mates"""
    def __init__(self, popnumber, exogamy_taboo=False, ancestry_as_int=0, distance_limit=10):
        #global villagecounter
        #self.villageid = self.id = villagecounter
        #villagecounter += 1
        self.exogamy_taboo = exogamy_taboo
        self.endogamy_strength = 1 # high: no taboo, lower=stronger taboo
        self.distance_matrix = [[] for i in xrange(distance_limit + 1)]
        #self.distance_matrix[0] = [self] # probably not necessary
        self.adults = [Person(self,ancestry_as_int = ancestry_as_int) for j in xrange(popnumber)]
        self.children = []
    def set_exogamy_taboo(self, boolean, endogamy_strength=0.02):
        self.exogamy_taboo = boolean
        self.endogamy_strength = endogamy_strength
    def generation_change(self):
        self.adults = self.children
        self.children = []
    def immigrate(self):
        """If random fluctuations see a village's population drop to zero (or whatever threshold), the largest
            village in the vicinity is selected and half its population migrates into
            the abandoned village. Should be called at the end of every generation -- there's a call
            to it in Person.spawn() just in case but calling it from there while a new generation is being
            processed can have weird effects, such as some people spawning more than once
        """
        #neighbourhood = flattenonce(self.distance_matrix[:5]) # creates a list of villages in distance < 5
        maxvillagesize = 0 # initialize at 0
        biggest_village = None # If None: throws an error when all villages nearby are also abandoned.
                                # alternative: initialise as self, or as distance_matrix[1][0]
        for distancedata in self.distance_matrix[:5]:
            for village in distancedata:
                size = len(village.adults)
                if size > maxvillagesize:
                    maxvillagesize = size
                    biggest_village = village
        print "village population has dropped to %d, migrating from a nearby village, number of migrants: %d" % (len(self.adults), maxvillagesize//2)
        for i in range(maxvillagesize//2):
            immigrant = biggest_village.adults.pop()
            immigrant.homevillage = self 
            self.adults.append(immigrant)
        del maxvillagesize, biggest_village
      