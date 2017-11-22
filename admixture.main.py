#!/usr/bin/python

"""
This module 

"""

import random, string
import optparse # command line options
from Region import *
from admixturePlotter import *
default_scalefactor = 1.0
default_villagesize = 84
default_inputfile = None
rel_mode = False
default_distancelimit = 21

parser = optparse.OptionParser()

parser.add_option("-S", "--scale", dest="scalefactor", default = default_scalefactor,
                  help="Choose to scale the map up (not recommended due to performance) or down (for test runs). Default: 1")
parser.add_option("-v", "--village-size", dest="villagesize", default = default_villagesize,
                  help="Choose size of individual villages, default: " + str(default_villagesize))
parser.add_option("-f", "--input-file", dest="inputfile", default = default_inputfile,
                  help="path to a csv-file that specifies the coninents with their names, sizes and positions (parser not implemented yet)" )
parser.add_option("-o", "--output-folder", dest="outputfile", default = None,
                  help="path to output files" )
parser.add_option("-d", "--distance-limit", dest="distance_limit", default = default_distancelimit,
                  help="Default distance limit (unless otherwise stated for individual Continent/Region" )
(options, args) = parser.parse_args()
                  
vs = villagesize = int(options.villagesize)
scalefactor = float(options.scalefactor)
inputfile = options.inputfile
max_distance = distance_limit = int(options.distance_limit)



def flattenonce(iterable):
    returnlist = []
    for member in iterable:
        returnlist.extend(member)
    return returnlist


# input file reader urgently needed!

worldmap = [Region(37, 37, distance_limit, name="Europe"),
            Region(40, 40, distance_limit, name="Western_Africa"),
            Region(40, 40, distance_limit, name="Eastern_Africa"),
            Region(47, 47, distance_limit, name="Central_Asia"),
            Region(40, 40, distance_limit, name="Southern_Africa"),
            Region(44, 35, distance_limit, name="Middle_East"),
            Region(20, 20, distance_limit, name="France"),
           Region(15, 15, distance_limit, name="Spain"),
           Region(32, 32, distance_limit, name="India"),
           Region( 10,  20, distance_limit, name="Madagascar"),
           Region( 23,  23, distance_limit, name="South_Central_Siberia"),
           Region( 23,  23, distance_limit, name="North_Central_Siberia"),
           Region( 35,  35, distance_limit, name="Krasnoyarsk"),
           Region(50, 50, distance_limit, name="North_America"),
           Region(42, 42, distance_limit, name="East_Siberia"),
           Region(54, 54, distance_limit, name="Far_East"),
           Region(40, 40, distance_limit, name="South_America"),
           Region(20, 20, distance_limit, name="Carribean"),
           Region(18, 18, distance_limit, name="Alaska"),
           Region(25, 25, distance_limit, name="Greenland"),
           Region(27, 27, distance_limit, name="Southeast_Asia"),
           Region( 15,  15, distance_limit, name="Papua"),
           Region(40, 40, distance_limit, name="Australia"),
           Region(20, 20, distance_limit, name="Chukchi"),
           Region(14, 11, distance_limit, name="Shangri_La"),
           Region( 20,  20, distance_limit, name="Indonesia"),
           Region(17, 17, distance_limit, name="Britain"),
           Region(8, 8, distance_limit, name="Ireland"),
           Region(20, 35, distance_limit, name="Patagonia"), 
            ]

for continent in worldmap:
    continent.lat_size, continent.lon_size =  int(continent.lat_size * scalefactor), int(continent.lon_size * scalefactor)
    continent.villagesizerange = (vs, vs)


print "total villages to create", sum([(continent.lat_size * continent.lon_size) for continent in worldmap])
print " total people to create", sum([(continent.lat_size* continent.lon_size) for continent in worldmap]) * villagesize
   # assumes village size is equal across regions, which it is because of the previous block but theoretically doesn't have to be
for continent in worldmap:
    continent.populate()
    continent.calculate_distances()
    print len(continent)
    exec(string.lower(continent.name).replace(" ","_") + " = continent")
    # this is safe because Region().make_name already does sanity checking, thus only adequate names
    # consisting of nothing but digits, letters and _, and no digits in position 0, survive to this point
    if rel_mode:
        for village in continent:
            for person in village.adults:
                person.make_rel_mode()
                person.assignancestry(idx, 1.0)
        print continent[0].adults[0].ancestry_matrix
        #print [person.ancestry_matrix for person in continent.mainregion[0].adults]
for village in shangri_la+papua[:2 * len(papua) // 3]+random.sample(alaska,2 * len(alaska) // 3):
    village.set_exogamy_taboo(True)

for village in alaska+carribean+east_siberia+southern_africa:
    village.set_exogamy_taboo(True, 0.3)


for village in random.sample(western_africa, len(western_africa)//4):
    village.set_exogamy_taboo(True, 0.005)

for village in random.sample(india[:len(india) // 2], len(india) // 4):
    village.set_exogamy_taboo(True, 0.01)



for continent in worldmap:
    print continent.name
    print "ancestry_identifier", continent[0].adults[0].ancestry_identifier
    print "exogamy taboo is observed here: ", any([village.exogamy_taboo == True for village in continent])


allcontinents = flattenonce([continent for continent in worldmap])
# this should also be handled through specifications in the input file
eastern_africa.make_anchor()
eastern_africa.joinregions(southern_africa,"se", "ne", junctiondepth= distance_limit//2, gap=0)
eastern_africa.joinregions(southern_africa, "s")
#southern_africa.joinregions(eastern_africa, "n", junctiondepth= distance_limit // 4)
southern_africa.joinregions(western_africa, "nw", junctiondepth=distance_limit//2, gap=0)
southern_africa.joinregions(eastern_africa, "nw", "sw", junctiondepth=distance_limit//2)
eastern_africa.joinregions(middle_east, "ne", junctiondepth=distance_limit//2)
eastern_africa.joinregions(western_africa, "nw", "ne", junctiondepth=distance_limit//2)
eastern_africa.joinregions(western_africa, "sw", "se", junctiondepth=distance_limit//2)
middle_east.joinregions(europe, "nw", junctiondepth=distance_limit//2)
middle_east.joinregions(shangri_la, "e","nw")
shangri_la.joinregions(india, "se", "n", gap=1)
middle_east.joinregions(india, "se", junctiondepth=2 * distance_limit //3)
europe.joinregions(france, "sw", junctiondepth=distance_limit//2, gap=0)
france.joinregions(spain, "sw", junctiondepth=distance_limit//3, gap=0)
europe.joinregions(britain, "w", "ne", junctiondepth=distance_limit//2, gap=3)
france.joinregions(britain, "n", junctiondepth=distance_limit//3)
britain.joinregions(ireland, "w", junctiondepth=distance_limit//3, gap=2)
spain.joinregions(western_africa, "s", junctiondepth=distance_limit//2)
eastern_africa.joinregions(madagascar, "se", "nw", junctiondepth= distance_limit // 5, gap=3)
india.joinregions(far_east, "ne", junctiondepth=distance_limit//2)
india.joinregions(southeast_asia, "e", junctiondepth=distance_limit//3)
southeast_asia.joinregions(indonesia, "se", "w", junctiondepth = distance_limit//4, gap=5)
indonesia.joinregions(papua, "e", junctiondepth=4, gap=3)
#bridges = bridges[:-1]
#papua.y_offset *= 3
#indonesia.joinregions(papua, "e", junctiondepth=4)
papua.joinregions(australia,"s", "ne",junctiondepth=3, gap=4)
far_east.joinregions(north_central_siberia, "nw", junctiondepth = distance_limit//2, gap=1)
north_central_siberia.joinregions(south_central_siberia, "s")
south_central_siberia.joinregions(east_siberia, "ne", gap=2)
south_central_siberia.joinregions(central_asia, "nw", "e")
south_central_siberia.joinregions(far_east, "ne", "nw")
south_central_siberia.joinregions(far_east, "se", "w")
central_asia.joinregions(europe, "w", "ne")
central_asia.joinregions(europe,"w", "ne")
central_asia.joinregions(middle_east, "s", "ne")
east_siberia.joinregions(krasnoyarsk, "nw", "e")
east_siberia.joinregions(chukchi, "ne", "nw")
chukchi.joinregions(alaska, "e", "nw")
alaska.joinregions(north_america, "ne", "nw")
north_america.joinregions(greenland, "ne", "nw", junctiondepth=4, gap=3)
north_america.joinregions(south_america, "se")
north_america.joinregions(carribean, "e", "nw")
carribean.joinregions(south_america, "se", "n")
krasnoyarsk.joinregions(central_asia, "sw", "n")
south_america.joinregions(patagonia, "sw", "nw", gap=0)
south_america.joinregions(patagonia, "s", "ne")
india.joinregions(southeast_asia, "ne", "nw")
north_central_siberia.joinregions(east_siberia, "ne", "w")
north_central_siberia.joinregions(krasnoyarsk, "ne", "se")
north_central_siberia.joinregions(krasnoyarsk, "nw", "s")
north_central_siberia.joinregions(central_asia, "nw", "ne", junctiondepth=distance_limit//3 )
southeast_asia.joinregions(far_east, "ne", "s")
india.joinregions(southeast_asia, "ne", "nw")



#allcontinents = flattenonce([continent.mainregion for continent in worldmap])
print "combined length of distance_matrixs created", distance_limit * len(allcontinents)
print "combined transitive length of distance_matrixs created", sum(len(flattenonce(village.distance_matrix)) for village in allcontinents)

print "number of persons created", len(allcontinents) * vs



# shadow africa and siberia region because I'm too lazy to replace everything in the positioning matrix:
#africa = Region((southern_africa.villagenumber_sqrt + eastern_africa.villagenumber_sqrt) * (southern_africa.villagenumber_sqrt + western_africa.villagenumber_sqrt), 0, villagesizerange=(0,0), fill=False)
#siberia = Region((dummy_siberia_size) ** 2, 0, villagesizerange=(0,0), fill=False)

allcontinents = flattenonce([continent for continent in worldmap])

for generation in range(181):
    i = generation
    print "***"
    print "generation", i
    world_pop_size = 0
    for village in allcontinents:
        world_pop_size += len(village.adults)
    print "current total population", world_pop_size
    print "***"
    
    random.shuffle(allcontinents)
    for village in allcontinents: 
        for person in village.adults:
                person.spawn(1) 
    for village in allcontinents:
        village.adults = village.children
        village.children = []
    for village in allcontinents:
        if len(village.adults) <= vs // 4:
            village.immigrate()
    
    
    if generation % 5 == 0:
        for origin_continent in worldmap:
            print "mapping ", origin_continent.name
            showstatus_multiregion(
                [(continent_drawn, continent_drawn.x_offset, continent_drawn.y_offset) for continent_drawn in worldmap],
                    origin_continent , i, vs, preferred_marker=",")
    #exit()


#showstatus(a, "Europe", i)
#showstatus(b, "Africa", i)


len([village for village in europe+africa if any([(person.ancestry_identifier >> 1) & 1 for person in village.adults])])
len([village for village in europe+africa if all([(person.ancestry_identifier >> 1) & 1 for person in village.adults])])
len([village for village in europe+africa if any([(person.ancestry_identifier >> 1) & 1 == 0 for person in village.adults])])
    

"""
example for the distribution the formula produces (with distance_limit = 15), percentages
>>> examplepopulation = [int(2**abs(random.gauss(0.,2))-1) for i in range(100000)]
>>> for i in range(16):...    if i == 15:...      print i, sum(map(lambda x: x > i, examplepopulation)) / 1000....      break...    print i, sum(map(lambda x: x == i, examplepopulation)) / 1000.           ... 
0 38.211
1 19.123
2 11.048
3 7.108
4 4.957
5 3.501
6 2.623
7 2.042
8 1.601
9 1.291
10 1.045
11 0.909
12 0.705
13 0.648
14 0.524
15 4.205

# same with distancelimit 25:
0 38.211
1 19.123
2 11.048
3 7.108
4 4.957
5 3.501
6 2.623
7 2.042
8 1.601
9 1.291
10 1.045
11 0.909
12 0.705
13 0.648
14 0.524
15 0.459
16 0.427
17 0.359
18 0.318
19 0.26
20 0.219
21 0.205
22 0.174
23 0.181
24 0.147
25 1.797

"""
