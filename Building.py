"""A building is a saved set of locations on a board and has a color and
possibly an owner.  A building also includes the locations of attached
stables.

A building can only have building pieces added to it if it does not have an
owner. A stable can be added to a building at any time. When adding to a
building, a gap must be left between buildings and the well."""

from Player import *
from Location import *
import random

NEUTRAL_OWNER = ()

def make_building(color, start):
    """Makes a building of a given color starting at a location."""
    return {'color':color,
            'locations':[start],
            'stables':[],
            'owner':None,
            'owner_color':None,
            'rooftop':None}

def clone_building(building):
    """Clones a building"""
    return {'color': get_building_color(building),
            'locations': get_building_locations(building)[:],
            'stables': get_stable_locations(building)[:],
            'owner': get_owner(building),
            'owner_color': get_owner_color(building),
            'rooftop': get_rooftop_location(building)}

def get_building_color(building):
    """Gets the color of a building"""
    return building['color']

def get_building_locations(building):
    """Gets all the locations a building pieces occupies."""
    return building['locations'][:]

def attach_building_locations(building, location):
    """Attaches a building piece to the buliding. The building must no be
    claimed in order to attach building segments."""
    assert not has_owner(building)
    building['locations'].append(location)

def get_stable_locations(building):
    """Gets all the stables attached to a building."""
    return building['stables'][:]

def buidling_contains_location(building, location):
    """Checks if a location is part of the building."""
    return location in get_building_locations(building)

def get_building_and_stables(building):
    """Gets all the building and stable locations of a building in a single list."""
    locs = set(get_stable_locations(building))
    locs = locs.union(get_building_locations(building))
    return locs

def buliding_contans_location_stables(building, location):
    """Checks if a building or it's attached stables contains a location."""
    return locaiton in get_building_locations(building) or location in get_stable_locations(building)

def get_building_peice_attach(building):
    """Gets all the locations that building peices can be attached, this is the
    list of orthogonal location excluding those occupied by stables."""
    return get_building_orthogonal(building).difference(set(get_stable_locations(building)));

def get_building_orthogonal(building):
    """Gets a set of all locations orthogonally adjacent to the building. This
    only includes locations that are next to the building pieces. This will
    include the location of stables adjacent to the building if any are
    attached."""
    included = get_building_locations(building)
    stables = get_stable_locations(building)
    building_orth = set()
    for loc in included:
        if loc not in stables:
            building_orth.update([orth for orth in get_orthogonal(loc) if orth not in included])
    return building_orth

def get_building_stable_orthogonal(building):
    """Gets a set of all locations orthogonally adjacent to the building and
    attached stables. This excludes the locations of stables."""
    included = get_building_locations(building)[:]
    included.extend(get_stable_locations(building))
    building_orth = set()
    for loc in included:
        building_orth.update([orth for orth in get_orthogonal(loc) if orth not in included])
    return building_orth

def get_building_adjacent(building):
    """Gets a set of all the locations adjacent to the building, excluding
    those that are part of the building. This is adjacency to building pieces,
    this does not locations adjacent to attached stables but will include the
    location of attached stables if they exist."""
    included = get_building_locations(building)
    building_adj = set()
    for loc in included:
        building_adj.update([adj for adj in get_adjacent(loc) if adj not in included])
    return building_adj

def get_building_stable_adjacent(building):
    """Gets a set of all the locations adjacent to the building and attached
    stables. This adjacency is to any attached part of the building. It does
    include locations adjacent to stables and excludes stables."""
    included = get_building_locations(building)
    included.extend(get_stable_locations(building))
    building_adj = set()
    for loc in included:
        building_adj.update([adj for adj in get_adjacent(loc) if adj not in included])
    return building_adj

def attach_stable_location(building, location):
    """Attaches a building piece to a building."""
    building['stables'].append(location)

def get_owner_color(building):
    """Gets the color of the owner"""
    return building['owner_color']

def get_rooftop_location(building):
    """Gets the location of a rooftop in a building"""
    return building['rooftop']

def get_owner(building):
    """Gets the owner of a building."""
    return building['owner']

def has_owner(building):
    """Checks if a building has an owner."""
    return get_owner(building) != None

def assign_owner(building, player, color, rooftop=None):
    """Sets the owner of a building. The building must not have an owner to be
    claimed."""
    assert not has_owner(building)
    building['owner'] = player
    building['owner_color'] = color
    if rooftop == None or rooftop not in get_building_locations(building):
        rooftop = random.choice(get_building_locations(building))
    building['rooftop'] = rooftop
