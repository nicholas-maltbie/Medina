"""A Market is all the market streets that have been added to the board.

A Market Street is a line of merchants that strech across the board giving 
adjacency bonuses to nearby buildings.

Each merchant has a location so a market street is saved as a set of locations. 
Not two merchants can occupy the same location and merchants can only be added 
to the ends of the market street. 

When adding merchants, a merchant can only be played in a way in which it is 
only adjacent to at most one other merchant. In other words, A merchant can 
be played at the tail or head of the merchant street and can be played in 
a location that does not make a loop with the market street.

It is possible for a market street to terminate due to a loop or dead ends. If 
this happens, a new market street is started as an extension of this street. 
The rules for placement still apply to the new market street and the new 
market street is also restricted by the old market street(s).
"""

from Location import *

def make_market(start):
    """This function will make a market which is the list of all the market 
    streets of merchants there are in the game."""
    market = [];
    market.append(make_market_street(start));
    return market;

def contains_location(market, loc):
    """Checks if a market contains a specific location in any of its streets."""
    for street in market:
        if loc in street:
            return True
    return False

def get_num_streets(market):
    """Gets the number of streets in a market."""
    return len(market)
    
def add_market_street(market, start):
    """Adds a new market street to a market and sets it as the active street."""
    market.append(make_market_street(start))

def get_active_market_street(market):
    """Gets the active street in a market."""
    return  market[-1]

def make_market_street(start):
    """This function will make a market street which is a saved list of 
    locations that represents merchants placed on the board."""
    return [start]

def get_street_length(street):
    """Gets the length of a market street."""
    return len(street)

def add_merchant(street, merchant):
    """Adds a merchant to a market street."""
    street.append(merchant)

def get_adjacent_to_street(street):
    """Gets all locations orthogonally adjacent to a street."""
    adj = set()
    for loc in street:
        adj.update(get_orthogonal(loc))
    return adj.difference_update(street)

def is_valid_location(loc, market):
    """This checks if a location is a valid place to add a merchant for a given 
    market. A place is considered valid if it is attached to a spot adjacent to 
    the head or tail of the market street and only has 1 neighbor upon being 
    placed."""
    return loc in get_possible_addition(market)

def get_possible_addition(market):
    """Gets the possible locations to add merchants to the market street. This 
    must account for other streets as merchatns can only be played in a location
    where they would only have one other merchant adjacent to them; no loops 
    allowed. This includes other streets. These locations branch from the head 
    and tail of a market street."""
    possible = set()
    addition = set()
    for end in get_head_and_tail(get_active_market_street(market)):
        possible.update(get_orthogonal(end))
        addition.update(get_orthogonal(end))
    possible.difference_update(get_active_market_street(market))
    possible.difference_update(get_adjacent_to_market(market))
    return possible

def get_head_and_tail(street):
    """Gets the head and tail of a street. The head and tail are locations on 
    the street that can have merchants added to them. The head and the tail can 
    be identified because the merchant at the head or tail of the street will 
    only ever have one other merchant adjacent to them. This will return a list 
    of only one location if the street is only one merchant long."""
    def is_end(location):
        num_adj = 0
        adj = get_adjacent(location)
        for merchant in street:
            if merchant in adj:
                num_adj += 1
        return num_adj <= 1
    return [loc for loc in street if is_end(loc)]

