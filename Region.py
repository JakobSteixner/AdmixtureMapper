#!/usr/bin/python
# -*- coding: utf-8 -*-


import random, string, time
from Village import *
from numpy import array


continentcounter = 0
bridges = []

class Region(list):
    """Region class, generates a list of villages and extracts their distance
        in a rectangular array, and writes those distances into each village's
        distance_matrix. Contains methods to join with other regions and set
        position relative to them for graphical display"""
    def __init__(self, lon_size, lat_size, distance_limit, villagesizerange=20, name="", ancestry_as_int=0, fill = False):
        global continentcounter
        #print continentcounter
        try: self.idnr = self.id = continentcounter
        except NameError:
            continentcounter = 0
            self.idnr = self.id = continentcounter
        self.makename(name)
        continentcounter += 1
        self.isfixed = False
        self.x_offset, self.y_offset = 0,0
        if type(villagesizerange) == int: # if int: fixed village size, otherwise expect tuple with lower and upper bound of size range
            villagesizerange = (villagesizerange,villagesizerange)
        else:
            try:
                tmp = villagesizerange[0]
                if type(tmp) == int:
                    pass
                else:
                    raise TypeError
            except TypeError:
                villagesizerange = eval(raw_input("village size must be integer or tuple (for range of stochastic values), please enter valid tuple: "))
        self.villagesizerange = villagesizerange
        self.distance_limit = distance_limit
        self.ancestry_as_int = ancestry_as_int
        self.lat_size, self.lon_size = lat_size, lon_size
        if fill:
            self.populate()
            self.calculate_distances(distance_limit)
    def makename(self, name):
            if name:
                rawname = string.join([char for char in name if char in string.letters+string.digits+"_ "],"")
                if rawname[0] in string.digits:
                    self.name = "_"+rawname
                else: self.name = rawname
            else:
                self.name = "continent" + str(self.id)
    def populate(self): #, lat_size=self.lat_size, lon_size=self.lon_size, villagesizerange=self.villagesizerange, ancestry_as_int=self.idnr, distance_limit=self.distance_limit):
        small_village, large_village = self.villagesizerange
        for i in xrange(self.lat_size*self.lon_size):
                if small_village != large_village: 
                    self.append(Village(random.randrange(small_village, large_village), ancestry_as_int = self.id,distance_limit=self.distance_limit))
                else:
                    self.append(Village(small_village, ancestry_as_int = self.id, distance_limit=self.distance_limit))
        self. villagenumber_sqrt = villagenumber_sqrt = int((self.lat_size*self.lon_size)**0.5)
        #print self.villagenumber_sqrt
        #exit()
    def calculate_distances(self,distance_limit=None):
            if distance_limit == None:
                distance_limit = self.distance_limit    
            for idx, village in enumerate(self):
                print "now calculating distances from village", idx
                potential_range_lower = max((0,idx-distance_limit*self.lon_size))
                potential_range_higher = min((self.lat_size*self.lon_size, idx + distance_limit*self.lon_size))
                print "calculating for range", potential_range_lower, potential_range_higher
                print "***"
                villagex = idx%self.villagenumber_sqrt
                for otherindex, othervillage in list(enumerate(self))[potential_range_lower:potential_range_higher]:
                    #otherx = otherindex % self.villagenumber_sqrt
                        #print "comparing", idx, otherindex
                        totaldistance = abs(idx%self.lon_size-otherindex % self.lon_size)\
                            + abs(idx//self.lon_size-otherindex//self.lon_size)
                        #print northsouthdistance
                        if totaldistance < distance_limit:
                            village.distance_matrix[totaldistance].append(othervillage)
    def make_anchor(self):
        self.isfixed = True
    def fixonmap(self, xpos_bonus, ypos_bonus):
        if self.isfixed == False:
            self.isfixed = True
            self.x_offset, self.y_offset = self.joint_x_offset + xpos_bonus, self.joint_y_offset + ypos_bonus
    def joint_corner_position(self, x_offset, y_offset):
        #if self.isfixed:
            self.joint_x_offset = x_offset
            self.joint_y_offset = y_offset
    def joinregions(self, region2, cornerof1, cornerof2=None,junctiondepth=8, gap=1):
        """region2 = the other region
            cornerof1, cornerof2 one of the 8 cardinal directions and their combinations,
                i. e. ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw'] or their English names
                if cornerof2 is not provided, the opposite corner is assumed
            junctiondepth: depth to which villages' distance matrixes are updated by use of
                this method. 
        """
        global bridges # not yet implemented
        landbridge_coordinates=[array([self.x_offset-1,self.y_offset-1]), array([0,0])]
        region2_was_fixed = region2.isfixed
        region1 = self
        def make_corner_ne(region, i):
            print landbridge_coordinates
            print landbridge_coordinates[i]
            landbridge_coordinates[i] += (self.lon_size, self.lat_size)
            return region[region.lat_size * region.lon_size - 1]
        def make_corner_se(region, i):
            landbridge_coordinates[i] += (self.lon_size, 0)
            return region[region.lon_size - 1]
        def make_corner_nw(region, i):
            landbridge_coordinates[i] += (0, self.lat_size)
            return region[region.lon_size * (region.lat_size - 1)]
        def make_corner_sw(region, i):
            return region[0]
        def make_corner_e(region, i):
            landbridge_coordinates[i] += (self.lon_size, self.lat_size // 2)
            return region[region.lon_size * (region.lat_size // 2) - 1]
        def make_corner_w(region, i):
            landbridge_coordinates[i] += (0, self.lat_size // 2)
            return region[region.lon_size * ((region.lat_size - 1) // 2) ]
        def make_corner_s(region, i):
            landbridge_coordinates[i] += (self.lon_size // 2, 0)
            return region[region.lon_size // 2]
        def make_corner_n(region, i):
            landbridge_coordinates[i] += (self.lon_size // 2, self.lat_size)
            return region[region.lon_size * region.lat_size - region.lon_size // 2]
        if string.lower(cornerof1) in ["ne", "northeast"]:
            region1_corner = make_corner_ne(self, 0)
            region2.joint_corner_position(self.x_offset + self.lon_size + gap, self.y_offset + self.lat_size + gap)
            if cornerof2 == None:
                cornerof2 = "sw"
        elif string.lower(cornerof1) in ["se", "southeast"]:
            region1_corner = make_corner_se(self, 0)
            region2.joint_corner_position(self.x_offset + self.lon_size + gap, self.y_offset - gap)
            if cornerof2 == None:
                cornerof2 = "nw"
        elif string.lower(cornerof1) in ["nw", "northwest"]:
            region1_corner  = make_corner_nw(self, 0)
            region2.joint_corner_position(self.x_offset-gap, self.y_offset + self.lat_size + gap)
            if cornerof2 == None:
                cornerof2 = "se"
        elif string.lower(cornerof1) in ["sw", "southwest"]:
            region2.joint_corner_position(self.x_offset - gap, self.y_offset - gap)
            region1_corner = make_corner_sw(self, 0)
            if cornerof2 == None:
                cornerof2 = "ne"
        elif string.lower(cornerof1) in ["e", "east"]:
            region2.joint_corner_position(self.x_offset + self.lon_size + gap, self.y_offset + self.lat_size // 2, )
            region1_corner = make_corner_e(self, 0)
            #print type(region1_corner)
            #print region1_corner in self
            if cornerof2 == None:
                cornerof2 = "w"
        elif string.lower(cornerof1) in ["w", "west"]:
            region2.joint_corner_position(self.x_offset - gap, self.y_offset + self.lat_size // 2)
            region1_corner = make_corner_w(self, 0)
            if cornerof2 == None:
                cornerof2 = "e"
        elif string.lower(cornerof1) in ["s", "south"]:
            region2.joint_corner_position(self.x_offset + self.lon_size // 2, self.y_offset - gap)
            region1_corner = make_corner_s(self, 0)
            if cornerof2 == None:
                cornerof2 = "n"
        elif string.lower(cornerof1) in ["n", "north"]:
            region2.joint_corner_position(self.x_offset + self.lon_size // 2, self.y_offset + self.lat_size + gap)
            region1_corner = make_corner_n(self, 0)
            if cornerof2 == None:
                cornerof2 = "s"
        else: print cornerof1, "not a valid direction"
        
        if string.lower(cornerof2) in ["ne", "northeast"]:
            region2_corner = make_corner_ne(region2, 1)
            region2.fixonmap(-region2.lon_size,-region2.lat_size)
            landbridge_coordinates[1] = array((region2.lon_size, region2.lat_size))
        elif string.lower(cornerof2) in ["se", "southeast"]:
            region2_corner = make_corner_se(region2, 1)
            region2.fixonmap(-region2.lon_size, 0)
            landbridge_coordinates[1] = array((region2.lon_size, 0))
        elif string.lower(cornerof2) in ["nw", "northwest"]:
            region2_corner  = make_corner_nw(region2, 1)
            region2.fixonmap(0, -region2.lat_size)
            landbridge_coordinates[1] = array((0, region2.lat_size ))
        elif string.lower(cornerof2) in ["sw", "southwest"]:
            region2_corner = make_corner_sw(region2, 1)
            region2.fixonmap(0, 0)
            landbridge_coordinates[1] = array((0,0))
        elif string.lower(cornerof2) in ["e", "east"]:
            region2_corner = make_corner_e(region2, 1)
            region2.fixonmap(-region2.lon_size,-region2.lat_size // 2)
            landbridge_coordinates[1] = array((region2.lon_size, region2.lat_size // 2))
        elif string.lower(cornerof2) in ["w", "west"]:
            region2_corner = make_corner_w(region2, 1)
            region2.fixonmap(0, -region2.lat_size // 2)
            landbridge_coordinates[1] = array((0, region2.lat_size//2))
        elif string.lower(cornerof2) in ["s", "south"]:
            region2_corner = make_corner_s(region2, 1)
            region2.fixonmap(region2.lon_size // 2, 0)
            landbridge_coordinates[1] = array((region2.lon_size // 2, 0))
        elif string.lower(cornerof2) in ["n", "north"]:
            region2_corner = make_corner_n(region2, 1)
            region2.fixonmap(-region2.lon_size // 2, -region2.lat_size)
            landbridge_coordinates[1] = array((region2.lon_size // 2, region2.lat_size))
        else: print cornerof2, "not a valid direction"
        
        landbridge_coordinates[1] +=  (region2.x_offset, region2.y_offset)
        #if region2_was_fixed == False:
        bridges.append(landbridge_coordinates)
        print "adjunction in progress, corners", cornerof1, cornerof2, "depth", junctiondepth
        print [len(distance) for distance in region1_corner.distance_matrix], [len(distance) for distance in region2_corner.distance_matrix]
        start = time.time()
        a, b = region1, region2
        region1_oldcornerarea = [[entry for entry in sublist] for sublist in region1_corner.distance_matrix]
        region2_oldcornerarea = [[entry for entry in sublist] for sublist in region2_corner.distance_matrix]
        for distancetocorner in range(junctiondepth+1):
            for village_on_side1 in region1_oldcornerarea[distancetocorner]:
                for farsidedistance in range(junctiondepth-distancetocorner):
                    village_on_side1.distance_matrix[distancetocorner + farsidedistance + 1].extend(region2_oldcornerarea[farsidedistance])
            for village_on_side2 in region2_oldcornerarea[distancetocorner]:
                for farsidedistance in range(junctiondepth-distancetocorner):
                    village_on_side2.distance_matrix[distancetocorner + farsidedistance + 1].extend(region1_oldcornerarea[farsidedistance])

        print "adjunction completed after seconds: ", time.time()-start
        print [len(distance) for distance in region1_corner.distance_matrix], [len(distance) for distance in region2_corner.distance_matrix]
    

Continent = Region

def testregion():  
    a = Region(30, 20, 16, fill=False)
    
    b = Region(30, 40, 16, fill=False)
    
    print a.idnr, b.idnr # tests incrementation of continentcounter
    print len(a), len(b) # should be 0
    
    a.populate()
    a.calculate_distances()
    b.populate()
    b.calculate_distances()
    #print a[0].distance_matrix
    assert all([len(row) == idx+1 for idx,row in enumerate(a[0].distance_matrix[:-1])]) # corner villages should have exactly n+1 neighbours in distance n
    print [len(row) for row in a[314].distance_matrix] # a village near the center, should have 4n neighbours at distance n for low distances
    print len(a)
    
    for i in range(len(a)):
        assert a[i].distance_matrix[0][0] == a[i] and len(a[i].distance_matrix[0]) == 1 # testing that the villages only have themselves as their 0-distance neighbours
    a.make_anchor()
    print a.isfixed, b.isfixed # expected: True, False
    a.joinregions(b, "ne", "nw", gap=2)
    print a.isfixed,b.isfixed # now True, True since joining b is supposed to fix it
    print b.x_offset, b.y_offset
    print b.y_offset == a.lat_size+2-b.lat_size #expect: True
    print a.x_offset, a.y_offset
    b.joinregions(a, "w", "se") # testing that Region().isfixed does what it should, i.e. blocks the assingment of new offsets
    print a.x_offset, a.y_offset
    
    print b.x_offset, b.y_offset
    print bridges # list of 
    print a.id, b.id # should b 0, 1
    print a[0].adults[0].ancestry_identifier # 1
    print b[0].adults[0].ancestry_identifier # 2
    c = Region(10, 20, 11, villagesizerange="test")
    c.populate()
    print c[0].adults[0].ancestry_identifier # 4
    b.joinregions(c,"sw", "e")
    print c.x_offset, c.y_offset 
    
    
#testregion()



def flattenonce(iterable):
    returnlist = []
    for member in iterable:
        returnlist.extend(member)
    return returnlist