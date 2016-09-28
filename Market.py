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

def get_possible_addition(street, other_streets):
    """Gets the possible locations to add merchants to the market street. This 
    must account for other streets as merchatns can only be played in a location
    where they would only have one other merchant adjacent to them; no loops 
    allowed. This includes other streets. These locations branch from the head 
    and tail of a market street."""
    pass

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

