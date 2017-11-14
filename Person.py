#!/usr/bin/python
# -*- coding: utf-8 -*-


import random, string, time

from math import log10

class Person():
    """Person()s have the a"""
    def __init__(self, homevillage, ancestry_as_int=0, mobility = 1,ancestry_computed=None, rel_mode=False):
        """
        homevillage parameter might become unnecessary
        ancestry_as_int: needed to derive ancestry variable, used as input to
            `self.ancestry_identifier = 2 ** ancestry_as_int`, used when a population
            is initialised. should be the index of its homeregion in a worldmap-list object
        ancestry_computed: derived identifier, computed from the identifier of the parents during spawn()ing
        mobility not currently used - meant to be a parameter for modifying the formula for searching partners
        """
        global worldmap
        if ancestry_computed:
            self.ancestry_identifier = ancestry_computed
        elif ancestry_as_int > -1:
            self.ancestry_identifier = 2 ** ancestry_as_int
        else:
            self.ancestry_identifier = 0
        self.rel_mode = rel_mode
        if rel_mode:
            self.ancestry_matrix = [0. for i in xrange(len(worldmap))]
        #self.distance_limit = distance_limit

        #print self.ancestry_identifier, type(self.ancestry_identifier)#self.ancestry_identifier = dict()
        #for continent in worldmap:
        #    self.ancestry_identifier[continent.name] = 1000000

        self.homevillage = homevillage
    def make_rel_mode(self):
            #from numpy import array
            self.ancestry_matrix=[0.0 for i in range(len(worldmap))]
    def assignancestry(self, continentid, value):
        self.ancestry_matrix[continentid] = value
    def __find_villages(self, distance_of_partner):
        """
        used by spawn() below, returns a list of villages given a distance
        and avoids IndexError's by quietly reducing the distance if needed
        """
        distance_limit = len(self.homevillage.distance_matrix)
        if distance_of_partner >= distance_limit:
            distance_of_partner = distance_limit-1
        while not self.homevillage.distance_matrix[distance_of_partner]:
                distance_of_partner -= 1
        return self.homevillage.distance_matrix[distance_of_partner]
    
    def spawn(self, number_to_replace=1, rel_mode=False):
        """
        Finds a partner in a log-normal distibuted distance, checks for exogamy taboos, and
        produces 0-2* `number_to_replace` offspring. For simulating more uneven reproductive
        success by only having a sample of the population spawn, provide a higher number for
        number_to_replace (i.e. 2 if half of the population spawns)
        if relative mode (rel_mode) is True, a matrix with proportional ancestry is created
        in addition to the integer ancestry identifier. Use this option with care, it's quite
        memory demanding!
        """
        if not isinstance(self, Person):
            print "I'm not a person, how did this happen???"
            print self, type(self)
            return 1
        distance_limit = len(self.homevillage.distance_matrix)
        distance_of_partner = distance_limit * 2 # set an implausibly high distance to initate loop
        
        while distance_of_partner >= distance_limit or (distance_of_partner > 0 and ((homevillage.exogamy_taboo or partner_homevillage.exogamy_taboo) and (random.random() > min(homevillage.endogamy_strength, partner_homevillage.endogamy_strength)))):
            try: # don't see any code that would be responsible so maybe it was a hardware fault (working at memory limits)
                # but I got the following error after 67 successful generations:
                """Traceback (most recent call last):
                File "vermischung.py", line 617, in <module>
                  person.spawn(1) #spawn(person)
                File "vermischung.py", line 338, in spawn
                  partner_homevillage = random.choice(self.__find_villages(distance_of_partner))
                File "vermischung.py", line 317, in __find_villages
                  while not self.homevillage.distance_matrix[distance_of_partner]:
              AttributeError: 'int' object has no attribute 'distance_matrix'
              """
              # here's me trying make the best of it by reassigning to the homevillage
              # parameter a random village where the person might
              # plausibly come from (ie that's in one of the continents where the Person()
              # has ancestors)
                try:
                    distance_of_partner =   int(2**abs(random.gauss(0.,1.5))-1)#
                                # should be parametrized too
                    homevillage=self.homevillage
                    partner_homevillage = random.choice(self.__find_villages(distance_of_partner))
                except AttributeError:
                    print """something crazy going on, it seems that something other than
                            a village has become a Person()'s homevillage
                            We'll try to make the best of it."""
                    homevillage = self.homevillage =  random.choice(random.choice([continent for idx,continent in enumerate(worldmap) if self.ancestry_identifier >> idx & 1]).mainregion) # picks a random village in which the Person() has ancestors
                    continue
            except TypeError:
                print "This is also very odd"
                homevillage = self.homevillage = random.choice(random.choice([continent for idx,continent in enumerate(worldmap) if self.ancestry_identifier >> idx & 1]).mainregion) # picks a random village in which the Person() has ancestors
                continue
        #trialcounter= 0
        for i in range(20):
            partner = random.choice(partner_homevillage.adults)
            if isinstance(partner, Person):
                break
            else:
                print partner_homevillage.adults
                print "partner homevillage populated by wrong type, attempt ", + i
        if not isinstance(partner, Person):
            partner = random.choice(homevillage)
        
            
            
        for i in range(random.randrange(2 * number_to_replace + 1)):
            offspring = Person(homevillage, ancestry_computed=self.ancestry_identifier | partner.ancestry_identifier)
            if rel_mode:
                offspring.ancestry_matrix = [(self.ancestry_matrix[i] + othercode) / 2.0 for (i, othercode) in enumerate(partner.ancestry_matrix)]

            
            homevillage.children.append(offspring)
            #offspring.homevillage = homevillage
 