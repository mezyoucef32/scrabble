
from copy import deepcopy
from random import choice, seed

from itertools import cycle
from collections import defaultdict

# ----------- Persistence ------------
# Don't want to use a database. 
# Currently relying on Python's 
# thread-safe built-in data-types 

# For all socketio rooms, aliased
# as game IDs
rooms = dict()

# For all players associated with rooms
# identified by their roomID and ordered 
# by turn
players = defaultdict(list)
# -------------------------------------

# The weight each scrabble piece carries
pieces_weight = {
    ' ': 0,
    'A': 1,
    'E': 1,
    'I': 1,
    'O': 1,
    'U': 1,
    'N': 1,
    'R': 1,
    'T': 1,
    'L': 1,
    'S': 1,
    'D': 2,
    'G': 2,
    'B': 3,
    'C': 3,
    'M': 3,
    'P': 3,
    'F': 4,
    'H': 4,
    'V': 4,
    'W': 4,
    'Y': 4,
    'K': 5,
    'J': 8,
    'X': 8,
    'Z': 10,
    'Q': 10
}

# The number of pieces each scrabble piece has
pieces_number = {
    ' ': 2,
    'A': 9,
    'E': 12,
    'I': 9,
    'O': 8,
    'U': 4,
    'N': 6,
    'R': 6,
    'T': 6,
    'L': 4,
    'S': 4,
    'D': 4,
    'G': 3,
    'B': 2,
    'C': 2,
    'M': 2,
    'P': 2,
    'F': 2,
    'H': 2,
    'V': 2,
    'W': 2,
    'Y': 2,
    'K': 1,
    'J': 1,
    'X': 1,
    'Z': 1,
    'Q': 1
}


pieces = list(pieces_number.keys())


def make_bag():
    """Creates a scrabble bag for a game session"""
    return deepcopy(pieces_number)

def get_remaining_pieces(room_id): 
    """
    Returns the number of pieces left 
    in the bag
    """
    return sum(rooms[room_id].values()) 

def get_all_pieces(room_id): 
    """
    Returns all the pieces left in the 
    bag, sorted.
    """
    return sorted(rooms[room_id].items(), key=lambda x: x[0])

def get_pieces(amount, room_id):
    """
    Gets pieces from the bag 
    and updates the bag, of course
    """

    # Storage for the requested new pieces
    new_pieces = [] 

    # Get the number of the remaining tiles
    bag_length = get_remaining_pieces(room_id)

    # If the requested amount is less than the number of
    # pieces in the bag, re-assign the amount to the remainder
    amount = bag_length if bag_length < amount else amount

    # Fill up the requested new pieces
    while len(new_pieces) != amount:
        # Get a random piece
        seed()
        piece = choice(pieces)
        
        # Get items from the bag
        session_bag = rooms[room_id]

        # If the piece hasn't been exhausted
        if session_bag.get(piece) > 0:

            # Add it to the result array
            new_pieces.append(dict(letter=piece, value=pieces_weight[piece]))
            
            # Decrease the number of said piece
            session_bag[piece] -= 1   

    return new_pieces

def get_player_to_play(room_id):
    """Returns the player to play next in a given room"""
   
    player_to_play = ''
    room = players.get(room_id)

    try:         
        # If the first item is still None i.e
        # it's still a mere list
        if room[0] == None:
            # Pop out the None
            room.pop(0)
            # Change the room to a round-robin list
            players[room_id] = cycle(room)
            next(players[room_id]) # Client knows already, initially.
            player_to_play = next(players[room_id]) # Who's next to play?

    # It's already a round-robin. 
    # Get the next player
    except TypeError:
        player_to_play = next(room)
    
    return player_to_play

    