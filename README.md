# AdmixtureMapper
Stochastic model for admixture in a geographically structured population
Default mode is all-or nothing: The only thing that is recorded is whether a person has *any* ancestors from a given region, or none (for display purposes: whether all, some, or no persons in a village have ancestors from region x). The alternative rel_mode is meant to store the fractions of ancestry from different regions, but its currently not fully implemented.

Region() class defined in Region.py, constructs a two-dimensional (rectangular) arrangement of villages as a list, calculates their distances up to a given limit and stores the resulting distance matrices in the village objects. Can be joined at the four corners and four cardinal directions with another region, with parametrized degree of permeability
properties:
width and height (lon_size, lat_size) in villages, integer
village size (integer or range of two integers)
name (sanitized string)
distance_limit
x_offset, y_offset determine position on map, relevant for displaying results

Village() class, defined in Village.py, usually called from Region
distance matrices are stored here
taboos against exogamy, if used, are stored here
contains two lists of Person()s: adults and children. At the end of each generation, the caller needs to call the .generation_change method

Person() class, usually called from Village
Contains a method for spawning offspring with a partner selected from the homevillage´s distance matrix, with a biased random distribution favouring the closest villages (current implementation: about 50% from the same village, and less than 5% from more than 6 steps away)
attribute: ancestry_identifier identifies all the regions where this person´s ancestors lived at the beginning of the simulation through an integer, where every position in the integer´s binary representation corresponds to a region. The order is determined counting backward from the ones in the order the regions were created (e. g. the first region created and thus with identifier 0 will be represented as a 0 or 1 in a person´s ancestry_identifier)

admixturePlotter maps the results


See blog post demonstrating and discussing an exemplary run: https://panloquens.wordpress.com/2017/11/14/were-all-siberians/

