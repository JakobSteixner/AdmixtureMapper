

import random, string, time
import matplotlib.pyplot as plt
import sys
import optparse # command line options
from math import log10
from numpy import array, average
from __main__ import bridges

def showstatus_rel(region, continent, generation, standalone=True, x_offset = 0, y_offset = 0, preferred_marker = ",", log_color_map = True, logbase=10):
    """Supposed to show the proportional contribution of ancestors in `continent` in `region`,
    instead of their absolute presence, in grayscale. Doesn't seem to work, maybe something
    gets lost on the road from specifying alpha to outputting as .eps via savefig?
    """
    coordinates_by_saturation = [[[],[]] for i in range(11)]
    from numpy import average
    def get_saturation(f):
        if f == 1.:
            return 0
        elif f == 0.0:
            return 10
        elif f > 0.98:
            return 1
        elif f > 0.9:
            return 2
        elif f > 0.5:
            return 3
        elif f > 0.1:
            return 4
        elif f > 0.02:
            return 5
        else:
            return min((9, 5 + int(abs(log10(f)))))
    for idx, village in enumerate(region):
        target = get_saturation(average([person.ancestry_matrix[continent.id] for person in village.adults]))
        #print target
        coordinates_by_saturation[target][0].append((idx%region.villagenumber_sqrt)+x_offset)
        coordinates_by_saturation[target][1].append((idx//region.villagenumber_sqrt)+y_offset)
    for i in range(10):
            saturation = 1.0-i/14. # let's not make the almost-zeros quite white
        #if any(coordinates_by_saturation[i]):
            x_positions, y_positions = coordinates_by_saturation[i]
            plt.plot(x_positions, y_positions, ",k", alpha=saturation)
    plt.plot(coordinates_by_saturation[10][0], coordinates_by_saturation[10][1], ",g", alpha=0.5) # the nones
    
    
    


def showstatus(region, continent, generation, standalone=True, x_offset=0, y_offset=0,preferred_marker=","):
    """
    Maps the presence of descendents from `continent` in `region` in a three-color coding:
    red: Everyone in this village has some ancestors from `continent`.
    yellow: Someone in this village has some ancestors from `continent`.
    green: Noone in this village has ancestors from `continent`
    black: This village currently has no inhabitants (should be none if done after immigrating)
    """
    emptyx, emptyy = [],[] # x/y coordinates of a temporarily abandoned village
    allafx, allafy = [], [] # (a village where) all (have) a(ncestors) f(rom), x-axis coorinates, y-axis coordinates
    someafx, someafy = [], [] # etc.
    noafx, noafy = [],[]
    region_sidelength = region.lon_size
    #contexponent = (len(worldmap) + 1 - continent.id)
    for idx, village in enumerate(region):
      if not village.adults:
        emptyx.append(idx%region_sidelength+x_offset)
        emptyy.append(idx // region_sidelength+y_offset)
      elif all([(person.ancestry_identifier >> continent.id) & 1 for person in village.adults]):
        #print type(x_offset)
        #for person in village.adults:
            #print person.ancestry_identifier, eval(('{0:0%db}' % len(worldmap)).format(person.ancestry_identifier)[continent.id])
        
        
        allafx. append(idx%region_sidelength+x_offset)
        allafy.append(idx // region_sidelength+y_offset)
      elif any([(person.ancestry_identifier >> continent.id) & 1   for person in village.adults]):
        someafx.append(idx % region_sidelength+x_offset)
        someafy.append(idx // region_sidelength+y_offset)
      else:
        noafx.append(idx % region_sidelength+x_offset)
        noafy.append(idx // region_sidelength+y_offset)
    if region_sidelength > 100:
        marker = ","
    elif region_sidelength > 40:
        marker = "."
    else:
        marker="x"
    if standalone == False:
        marker = preferred_marker
    
    plt.plot(allafx, allafy, marker+"r")
    plt.plot(someafx, someafy, marker+"y")
    plt.plot(noafx, noafy, marker+"g")
    plt.plot(emptyx, emptyy, marker+"k")
    if standalone:
        plt.axis("equal")
        plt.title("%d villages in region, generation %d" %(len(region), generation))
        #plt.show()
        plt.savefig(str(len(region))+"_"+str(generation)+".eps")
        plt.close()

def showstatus_multiregion(list_of_regions_with_offsets, continent, generation, villagesize=10, preferred_marker=",", rel_mode=False):
    """allows to plot several regions before outputting the map
    list_of_regions_with_offsets is a list of tuple(region, x_offset, y_offset)`s
    `continent` specifies which heritage will be mapped
    `generation` and `villagesize` are needed for titling the graph only
    """
    global bridges
    for regiondata in list_of_regions_with_offsets:
        #print regiondata[1:]
        region, currentx_offset, currenty_offset = regiondata
        #print currentx_offset, currenty_offset
        if rel_mode:
            showstatus_rel(region, continent, generation, standalone=False, x_offset=currentx_offset, y_offset = currenty_offset,preferred_marker=preferred_marker)
        else:
            showstatus(region, continent, generation, standalone=False, x_offset=currentx_offset, y_offset = currenty_offset,preferred_marker=preferred_marker)
        if region.name in ["Ireland", "North_Central_Siberia", "South_Central_Siberia", "Shangri_La", "Indonesia", "Patagonia", "Southeast_Asia", "Carribean", "Madagascar"]:
            plt.text(currentx_offset - region.lon_size, currenty_offset + 2 * region.lat_size/3, region.name, fontsize=float(region.lon_size) / len(region.name) * 4)
        else:
            plt.text(currentx_offset, currenty_offset + 2, region.name, fontsize=float(region.lon_size) / len(region.name) * 2)
    for landbridge in bridges:
        if sum(abs(sum([landbridge[0]-landbridge[1]]))) > 2:
            plt.plot(array(landbridge)[:,0], array(landbridge)[:,1], "k")
        else:
            plt.plot(average(array(landbridge)[:,0]), average(array(landbridge)[:,1]), ".k") 
    plt.title("Villages with descendents from %s, generation %d\n mean village size: %d" % (continent.name, generation, villagesize))
    plt.axis("equal")
    plt.savefig("allregions%d_%s_%d.eps" % (villagesize, continent.name, generation))
    plt.close()


 