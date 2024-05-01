# wumpus_kb.py
# ------------
# Licensing Information:
# Please DO NOT DISTRIBUTE OR PUBLISH solutions to this project.
# You are free to use and extend these projects for EDUCATIONAL PURPOSES ONLY.
# The Hunt The Wumpus AI project was developed at University of Arizona
# by Clay Morrison (clayton@sista.arizona.edu), spring 2013.
# This project extends the python code provided by Peter Norvig as part of
# the Artificial Intelligence: A Modern Approach (AIMA) book example code;
# see http://aima.cs.berkeley.edu/code.html
# In particular, the following files come directly from the AIMA python
# code: ['agents.py', 'logic.py', 'search.py', 'utils.py']
# ('logic.py' has been modified by Clay Morrison in locations with the
# comment 'CTM')
# The file ['minisat.py'] implements a slim system call wrapper to the minisat
# (see http://minisat.se) SAT solver, and is directly based on the satispy
# python project, see https://github.com/netom/satispy .

import utils

#-------------------------------------------------------------------------------
# Wumpus Propositions
#-------------------------------------------------------------------------------

### atemporal variables

proposition_bases_atemporal_location = ['P', 'W', 'S', 'B']

def pit_str(x, y):
    "There is a Pit at <x>,<y>"
    return 'P{0}_{1}'.format(x, y)
def wumpus_str(x, y):
    "There is a Wumpus at <x>,<y>"
    return 'W{0}_{1}'.format(x, y)
def stench_str(x, y):
    "There is a Stench at <x>,<y>"
    return 'S{0}_{1}'.format(x, y)
def breeze_str(x, y):
    "There is a Breeze at <x>,<y>"
    return 'B{0}_{1}'.format(x, y)

### fluents (every proposition who's truth depends on time)

proposition_bases_perceptual_fluents = ['Stench', 'Breeze', 'Glitter', 'Bump', 'Scream']

def percept_stench_str(t):
    "A Stench is perceived at time <t>"
    return 'Stench{0}'.format(t)
def percept_breeze_str(t):
    "A Breeze is perceived at time <t>"
    return 'Breeze{0}'.format(t)
def percept_glitter_str(t):
    "A Glitter is perceived at time <t>"
    return 'Glitter{0}'.format(t)
def percept_bump_str(t):
    "A Bump is perceived at time <t>"
    return 'Bump{0}'.format(t)
def percept_scream_str(t):
    "A Scream is perceived at time <t>"
    return 'Scream{0}'.format(t)

proposition_bases_location_fluents = ['OK', 'L']

def state_OK_str(x, y, t):
    "Location <x>,<y> is OK at time <t>"
    return 'OK{0}_{1}_{2}'.format(x, y, t)
def state_loc_str(x, y, t):
    "At Location <x>,<y> at time <t>"
    return 'L{0}_{1}_{2}'.format(x, y, t)

def loc_proposition_to_tuple(loc_prop):
    """
    Utility to convert location propositions to location (x,y) tuples
    Used by HybridWumpusAgent for internal bookkeeping.
    """
    parts = loc_prop.split('_')
    return (int(parts[0][1:]), int(parts[1]))

proposition_bases_state_fluents = ['HeadingNorth', 'HeadingEast',
                                   'HeadingSouth', 'HeadingWest',
                                   'HaveArrow', 'WumpusAlive']

def state_heading_north_str(t):
    "Heading North at time <t>"
    return 'HeadingNorth{0}'.format(t)
def state_heading_east_str(t):
    "Heading East at time <t>"
    return 'HeadingEast{0}'.format(t)
def state_heading_south_str(t):
    "Heading South at time <t>"
    return 'HeadingSouth{0}'.format(t)
def state_heading_west_str(t):
    "Heading West at time <t>"
    return 'HeadingWest{0}'.format(t)
def state_have_arrow_str(t):
    "Have Arrow at time <t>"
    return 'HaveArrow{0}'.format(t)
def state_wumpus_alive_str(t):
    "Wumpus is Alive at time <t>"
    return 'WumpusAlive{0}'.format(t)

proposition_bases_actions = ['Forward', 'Grab', 'Shoot', 'Climb',
                             'TurnLeft', 'TurnRight', 'Wait']

def action_forward_str(t=None):
    "Action Forward executed at time <t>"
    return ('Forward{0}'.format(t) if t != None else 'Forward')
def action_grab_str(t=None):
    "Action Grab executed at time <t>"
    return ('Grab{0}'.format(t) if t != None else 'Grab')
def action_shoot_str(t=None):
    "Action Shoot executed at time <t>"
    return ('Shoot{0}'.format(t) if t != None else 'Shoot')
def action_climb_str(t=None):
    "Action Climb executed at time <t>"
    return ('Climb{0}'.format(t) if t != None else 'Climb')
def action_turn_left_str(t=None):
    "Action Turn Left executed at time <t>"
    return ('TurnLeft{0}'.format(t) if t != None else 'TurnLeft')
def action_turn_right_str(t=None):
    "Action Turn Right executed at time <t>"
    return ('TurnRight{0}'.format(t) if t != None else 'TurnRight')
def action_wait_str(t=None):
    "Action Wait executed at time <t>"
    return ('Wait{0}'.format(t) if t != None else 'Wait')


def add_time_stamp(prop, t): return '{0}{1}'.format(prop, t)

proposition_bases_all = [proposition_bases_atemporal_location,
                         proposition_bases_perceptual_fluents,
                         proposition_bases_location_fluents,
                         proposition_bases_state_fluents,
                         proposition_bases_actions]


#-------------------------------------------------------------------------------
# Axiom Generator: Current Percept Sentence
#-------------------------------------------------------------------------------

#def make_percept_sentence(t, tvec):
def axiom_generator_percept_sentence(t, tvec):
    """
    Asserts that each percept proposition is True or False at time t.

    t := time
    tvec := a boolean (True/False) vector with entries corresponding to
            percept propositions, in this order:
                (<stench>,<breeze>,<glitter>,<bump>,<scream>)

    Example:
        Input:  [False, True, False, False, True]
        Output: '~Stench0 & Breeze0 & ~Glitter0 & ~Bump0 & Scream0'
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    percept_inputs = (percept_stench_str(t), percept_breeze_str(t), 
                    percept_glitter_str(t), percept_bump_str(t), percept_scream_str(t))
    # Initialize axiom_str with empty string
    axiom_str = ''
    # Iterate over each index in the range of the length of tvec
    for i in range(len(tvec)):
        # If tvec value at index i is False, prepend '~' to the percept input
        if not tvec[i]:
            axiom_str += '~' + percept_inputs[i]
        # Otherwise, append the percept input as it is
        else:
            axiom_str += percept_inputs[i]
        # If it's not the last element, add ' & ' to separate the percepts
        if i < len(tvec) - 1:
            axiom_str += ' & '

    return axiom_str



#-------------------------------------------------------------------------------
# Axiom Generators: Initial Axioms
#-------------------------------------------------------------------------------

def axiom_generator_initial_location_assertions(x, y):
    """
    Assert that there is no Pit and no Wumpus in the location

    x,y := the location
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    gen_init_loc = []
    #append negated pit and wumpus locations to gen_init_loc
    gen_init_loc.append('~' + pit_str(x, y))
    gen_init_loc.append('~' + wumpus_str(x, y))
    #add the negated pit and wumpus locations to gen_init_loc again
    gen_init_loc.extend(['~' + pit_str(x, y), '~' + wumpus_str(x, y)])
    #initialize an empty list to store the string representations of elements in gen_init_loc
    temp_list = []
    #convert each element in gen_init_loc to a string and append to temp_list
    for i in gen_init_loc:
        temp_list.append(str(i))
    #join the elements of temp_list with ' & ' to form a single string
    joined_str = ' & '.join(temp_list)
    #append the joined string to axiom_str
    axiom_str += joined_str
    
    return axiom_str


def axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Breezes (atemporal) are only found in locations where
    there are one or more Pits in a neighboring location (or the same location!)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Pits).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
 
    #initialize breeze_location list
    breeze_location = []
    #add breeze location and '<=>' to breeze_location
    breeze_location.extend([breeze_str(x, y), ' <=> ('])
    #join elements of breeze_location to form a string
    axiom_str = ''.join(map(str, breeze_location))
    #clear breeze_location for new entries
    breeze_location = []
    #define adjacent squares
    neighbour_squares = [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    #iterating over adjacent squares and filter squares within bounds
    valid_squares = [square for square in neighbour_squares if xmin <= square[0] <= xmax and ymin <= square[1] <= ymax]
    #adding pit location to breeze_location for valid squares
    breeze_location.extend([pit_str(square[0], square[1]) for square in valid_squares])
    #joining elements of breeze_location with ' | ' and add ')' to axiom_str
    axiom_str += ' | '.join(str(square) for square in breeze_location) + ')'

    return axiom_str


def generate_pit_and_breeze_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_pits_and_breezes(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_pits_and_breezes')
    return axioms

def axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax):
    """
    Assert that Stenches (atemporal) are only found in locations where
    there are one or more Wumpi in a neighboring location (or the same location!)

    (Don't try to assert here that there is only one Wumpus;
    we'll handle that separately)

    x,y := the location
    xmin, xmax, ymin, ymax := the bounds of the environment; you use these
           variables to 'prune' any neighboring locations that are outside
           of the environment (and therefore are walls, so can't have Wumpi).
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #initialize wumpus_stench_loc list
    wumpus_stench_loc = []
    #add stench location and '<=>' to wumpus_stench_loc
    wumpus_stench_loc.extend([stench_str(x, y), ' <=> ('])
    #initialize an empty string to store the joined elements of wumpus_stench_loc
    joined_str = ''
    for element in wumpus_stench_loc:
        #convert each element to a string and concatenate it to joined_str
        joined_str += str(element)
    axiom_str = joined_str
    #clear wumpus_stench_loc for new entries
    wumpus_stench_loc = []
    #define adjacent squares
    neighbour_squares = [(x, y), (x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    #iterating over adjacent squares and filter squares within bounds
    valid_squares = [square for square in neighbour_squares if xmin <= square[0] <= xmax and ymin <= square[1] <= ymax]
    #adding wumpus location to wumpus_stench_loc for valid squares
    wumpus_stench_loc.extend([wumpus_str(square[0], square[1]) for square in valid_squares])
    #joining elements of wumpus_stench_loc with ' | ' and add ')' to axiom_str
    axiom_str += ' | '.join(map(str, wumpus_stench_loc)) + ')'

    return axiom_str


def generate_wumpus_and_stench_axioms(xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_wumpus_and_stench(x, y, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_wumpus_and_stench')
    return axioms

def axiom_generator_at_least_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at least one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
    wumpus1_location=[]

    #iterate over the range of x and y coordinates within bounds
    wumpus1_location = [wumpus_str(i, j) for i in range(xmin, xmax+1) for j in range(ymin, ymax+1)]
    #joining elements of wumpus1_location with ' | ' and add it to axiom_str
    axiom_str += ' | '.join(map(str, wumpus1_location))

    return axiom_str

def axiom_generator_at_most_one_wumpus(xmin, xmax, ymin, ymax):
    """
    Assert that there is at at most one Wumpus.

    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
    
    max_wumpus_location = []
 
    #generate implications for each location (i, j)
    for i in range(xmin, xmax + 1):
        for j in range(ymin, ymax + 1):
            #initialize the implication string for the current location
            wumpus_implication = '(' + wumpus_str(i, j) + ' >> ('

            #initialize an empty list to store the clauses for wumpus absence
            wumpus_absent_clauses = []

            #iterate over each coordinate in the grid
            for k in range(xmin, xmax + 1):
                for l in range(ymin, ymax + 1):
                    #check if the coordinate is not the same as the current location (i, j)
                    if (k, l) != (i, j):
                        #append the negation of the wumpus presence at the current coordinate to the list
                        wumpus_absent_clauses.append('~' + wumpus_str(k, l))

            #joining the clauses with ' & ' and add them to the wumpus_implication string
            wumpus_implication += ' & '.join(wumpus_absent_clauses)

            #adding the closing parentheses to complete the implication
            wumpus_implication += '))'

            #appending the implication for the current location to max_wumpus_location
            max_wumpus_location.append(wumpus_implication)

    #joining the implications with ' & ' and add them to axiom_str
    axiom_str += ' & '.join(max_wumpus_location)
    return axiom_str

def axiom_generator_only_in_one_location(xi, yi, xmin, xmax, ymin, ymax, t = 0):
    """
    Assert that the Agent can only be in one (the current xi,yi) location at time t.

    xi,yi := the current location.
    xmin, xmax, ymin, ymax := the bounds of the environment.
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    #holding spots where our agent might be wanderin'
    agent_location = []  
    #adding agent location at (xi, yi)
    agent_location.extend([state_loc_str(i, j, t) for i in range(xmin, xmax+1) for j in range(ymin, ymax+1) if i == xi and j == yi])
    
    #adding negation of agent location for all other spots
    agent_location.extend(['~' + state_loc_str(i, j, t) for i in range(xmin, xmax+1) for j in range(ymin, ymax+1) if i != xi or j != yi])
    #making a list to hold string versions of agent_location elements
    temp_list = []  
    
    #turning each element of agent_location into a string and addin' it to temp_list
    for i in agent_location:
        temp_list.append(str(i))
    #joining all elements of temp_list into a single string usin' ' & ' separator
    joined_string = ' & '.join(temp_list)
    #adding the joined string to axiom_str
    axiom_str += joined_string

    return axiom_str



def axiom_generator_only_one_heading(heading = 'north', t = 0):
    """
    Assert that Agent can only head in one direction at a time.

    heading := string indicating heading; default='north';
               will be one of: 'north', 'east', 'south', 'west'
    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
    state_directions = [ state_heading_east_str(t), state_heading_south_str(t), state_heading_west_str(t), state_heading_north_str(t)]
    state_directions_val = [ 'east', 'south', 'west', 'north']

    #initialize dum list
    dum = []

    #constructing the dum list with appropriate state fluents
    dum = [state_directions[i] if state_directions_val[i] == heading else '~' + state_directions[i] for i in range(len(state_directions_val))] + ['~' + state_directions[i] for i in range(len(state_directions_val)) if state_directions_val[i] != heading]

    #concatenating dum list elements with '&', and add them to axiom_str
    axiom_str += ' & '.join(str(i) for i in dum)


    return axiom_str

def axiom_generator_have_arrow_and_wumpus_alive(t = 0):
    """
    Assert that Agent has the arrow and the Wumpus is alive at time t.

    t := time; default=0
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
    wumpus_stat=[]
    #append the arrow state
    wumpus_stat.append(state_have_arrow_str(t))
    #append the wumpus status
    wumpus_stat.append(state_wumpus_alive_str(t))
    #define an empty list to store string representations of elements in wumpus_stat
    elements_as_strings = []

    #iterating over each element in wumpus_stat
    for element in wumpus_stat:
        #converting the current element to a string and append it to the list
        elements_as_strings.append(str(element))

    #joining all elements in the list with ' & ' to form a single string
    joined_elements = ' & '.join(elements_as_strings)

    #appending the joined string to axiom_str
    axiom_str += joined_elements

    return axiom_str


def initial_wumpus_axioms(xi, yi, width, height, heading='east'):
    """
    Generate all of the initial wumpus axioms
    
    xi,yi = initial location
    width,height = dimensions of world
    heading = str representation of the initial agent heading
    """
    axioms = [axiom_generator_initial_location_assertions(xi, yi)]
    axioms.extend(generate_pit_and_breeze_axioms(1, width, 1, height))
    axioms.extend(generate_wumpus_and_stench_axioms(1, width, 1, height))
    
    axioms.append(axiom_generator_at_least_one_wumpus(1, width, 1, height))
    axioms.append(axiom_generator_at_most_one_wumpus(1, width, 1, height))

    axioms.append(axiom_generator_only_in_one_location(xi, yi, 1, width, 1, height))
    axioms.append(axiom_generator_only_one_heading(heading))

    axioms.append(axiom_generator_have_arrow_and_wumpus_alive())
    
    return axioms


#-------------------------------------------------------------------------------
# Axiom Generators: Temporal Axioms (added at each time step)
#-------------------------------------------------------------------------------

def axiom_generator_location_OK(x, y, t):
    """
    Assert the conditions under which a location is safe for the Agent.
    (Hint: Are Wumpi always dangerous?)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    parts = []

    #appending state_OK_str(x, y, t) to the parts list
    parts.append(state_OK_str(x, y, t))
    #append ' <=> (' to the parts list
    parts.append(' <=> (')
    #create a list to store safe location conditions
    safe_location = []
    #append conditions for safe location to safe_location list
    safe_location.append('~' + pit_str(x, y) + ' & (~' + wumpus_str(x, y) + ' | (' + wumpus_str(x, y) + ' & ~' + state_wumpus_alive_str(t) + '))')
    #create an empty string to store the joined safe location conditions
    safe_loc_str = ''
    #iterate over each item in safe_loc list
    for item in safe_location:
        #convert item to string and concatenate it to safe_loc_str
        safe_loc_str += str(item)
    #append safe_loc_str to parts list
    parts.append(safe_loc_str)
    #append ')' to parts list
    parts.append(')')
    #joining all parts together into a single string
    axiom_str = ''.join(parts)

    return axiom_str

    

def generate_square_OK_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_location_OK(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_location_OK')
    return list(filter(lambda s: s != '', axioms))


#-------------------------------------------------------------------------------
# Connection between breeze / stench percepts and atemporal location properties

def axiom_generator_breeze_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a breeze
    at that time (a percept) means that the location is breezy (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    #initialize lists to store location status and breeze status
    loc_status = []
    status_breeze = []
    #appending location status and breeze status to respective lists
    loc_status.append(state_loc_str(x, y, t) + ' >> ')  #add location status
    status_breeze.append('({} <=> {})'.format(percept_breeze_str(t), breeze_str(x, y)))  #add breeze status
    #combine location and breeze status lists
    status = loc_status + status_breeze
    #converting each element in the status list to a string
    status_strings = []
    for i in status:
        status_strings.append(str(i))
    #concatenating all the strings together and add them to axiom_str
    axiom_str += ''.join(status_strings)
    return axiom_str


def generate_breeze_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_breeze_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_breeze_percept_and_location_property')
    return list(filter(lambda s: s != '', axioms))

def axiom_generator_stench_percept_and_location_property(x, y, t):
    """
    Assert that when in a location at time t, then perceiving a stench
    at that time (a percept) means that the location has a stench (atemporal)

    x,y := location
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    #initialize lists to store state status and stench status
    loc_status = []
    status_stench = []
    #appending state status and stench status to respective lists
    loc_status.append(state_loc_str(x, y, t) + ' >> ')  #add state status
    status_stench.append('({} <=> {})'.format(percept_stench_str(t), stench_str(x, y)))  #add stench status
    #combine state and stench status lists
    status = loc_status + status_stench
    #convert each element in the status list to a string and concatenate them
    axiom_str += ''.join(str(i) for i in status)

    return axiom_str

def generate_stench_percept_and_location_axioms(t, xmin, xmax, ymin, ymax):
    axioms = []
    for x in range(xmin, xmax + 1):
        for y in range(ymin, ymax + 1):
            axioms.append(axiom_generator_stench_percept_and_location_property(x, y, t))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_stench_percept_and_location_property')
    return list(filter(lambda s: s != '', axioms))


#-------------------------------------------------------------------------------
# Transition model: Successor-State Axioms (SSA's)
# Avoid the frame problem(s): don't write axioms about actions, write axioms about
# fluents!  That is, write successor-state axioms as opposed to effect and frame
# axioms
#
# The general successor-state axioms pattern (where F is a fluent):
#   F^{t+1} <=> (Action(s)ThatCause_F^t) | (F^t & ~Action(s)ThatCauseNot_F^t)

# NOTE: this is very expensive in terms of generating many (~170 per axiom) CNF clauses!
def axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax):
    """
    Assert the condidtions at time t under which the agent is in
    a particular location (state_loc_str: L) at time t+1, following
    the successor-state axiom pattern.

    See Section 7. of AIMA.  However...
    NOTE: the book's version of this class of axioms is not complete
          for the version in Project 3.
    
    x,y := location
    t := time
    xmin, xmax, ymin, ymax := the bounds of the environment.
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"

    # Prepare for the next time step: t+1
    stat_t1 = []
    # Add logic for the state location at the next time step (t+1)
    stat_t1.append(state_loc_str(x, y, t+1) + ' <=> (')
    # Current state at time t
    stat_t = []
    # State logic for the current location and no forward action
    stat_t.append(f'({state_loc_str(x, y, t)} & ~{action_forward_str(t)})')
    # Explore neighboring squares and their orientations
    neighbour_squares = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
    state_orient = [state_heading_west_str(t), state_heading_east_str(t), state_heading_south_str(t), state_heading_north_str(t)]
    # Extend the state logic for each neighboring squar
    stat_t.extend([
        # Check if the square is within the boundary
        ' | (' + state_loc_str(square[0], square[1], t) + ' & ' + state_orient[idx] + ' & ' + action_forward_str(t) + ')'
        for idx, square in enumerate(neighbour_squares)
        if xmin <= square[0] <= xmax and ymin <= square[1] <= ymax
    ])

    stat_tot=stat_t1+stat_t
    temp_list = [] 

    #iterate through each element in stat_tot
    for i in stat_tot:
        #convert the element to a string and append it to temp_list
        temp_list.append(str(i))

    #join all elements of temp_list into a single string
    joined_string = ''.join(temp_list)

    #append the joined string to axiom_str
    axiom_str += joined_string

    axiom_str+=')'

    return axiom_str

def generate_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax, heading):
    """
    The full at_location SSA converts to a fairly large CNF, which in
    turn causes the KB to grow very fast, slowing overall inference.
    We therefore need to restric generating these axioms as much as possible.
    This fn generates the at_location SSA only for the current location and
    the location the agent is currently facing (in case the agent moves
    forward on the next turn).
    This is sufficient for tracking the current location, which will be the
    single L location that evaluates to True; however, the other locations
    may be False or Unknown.
    """
    axioms = [axiom_generator_at_location_ssa(t, x, y, xmin, xmax, ymin, ymax)]
    if heading == 'west' and x - 1 >= xmin:
        axioms.append(axiom_generator_at_location_ssa(t, x-1, y, xmin, xmax, ymin, ymax))
    if heading == 'east' and x + 1 <= xmax:
        axioms.append(axiom_generator_at_location_ssa(t, x+1, y, xmin, xmax, ymin, ymax))
    if heading == 'south' and y - 1 >= ymin:
        axioms.append(axiom_generator_at_location_ssa(t, x, y-1, xmin, xmax, ymin, ymax))
    if heading == 'north' and y + 1 <= ymax:
        axioms.append(axiom_generator_at_location_ssa(t, x, y+1, xmin, xmax, ymin, ymax))
    if utils.all_empty_strings(axioms):
        utils.print_not_implemented('axiom_generator_at_location_ssa')
    return list(filter(lambda s: s != '', axioms))

#----------------------------------

def axiom_generator_have_arrow_ssa(t):
    """
    Assert the conditions at time t under which the Agent
    has the arrow at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    loc_new_status_t = []
    #create conditions for the state of having an arrow at time t+1
    loc_new_status_t.append(state_have_arrow_str(t+1) + ' <=> (')
    #create conditions for the current state of having an arrow and not shooting at time t
    loc_current_status_t = []
    loc_current_status_t.append(state_have_arrow_str(t) + ' & ~' + action_shoot_str(t))
    #combine conditions for both time steps
    status = loc_new_status_t + loc_current_status_t
    #convert each condition to a string
    status_strings = []
    for condition in status:
        status_strings.append(str(condition))
    #concatenate all condition strings together
    axiom_str += ''.join(status_strings)
    #add closing parenthesis to complete the axiom string
    axiom_str += ')'

    return axiom_str


def axiom_generator_wumpus_alive_ssa(t):
    """
    Assert the conditions at time t under which the Wumpus
    is known to be alive at time t+1

    (NOTE: If this axiom is implemented in the standard way, it is expected
    that it will take one time step after the Wumpus dies before the Agent
    can infer that the Wumpus is actually dead.)

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    #create conditions for the state of wumpus being alive at time t+1
    loc_new_status_t = []
    loc_new_status_t.append(state_wumpus_alive_str(t+1) + ' <=> (')
    #create conditions for the current state of wumpus being alive and no scream being perceived at time t+1
    loc_current_status_t = []
    loc_current_status_t.append(state_wumpus_alive_str(t) + ' & ~' + percept_scream_str(t+1))
    #combine conditions for both time steps
    status = loc_new_status_t + loc_current_status_t
    #convert each condition to a string
    status_strings = []
    for condition in status:
        status_strings.append(str(condition))
    #concatenate all condition strings together
    axiom_str += ''.join(status_strings)
    #add closing parenthesis to complete the axiom string
    axiom_str += ')'

    return axiom_str

#----------------------------------


def axiom_generator_heading_north_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be North at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    # create conditions for the state of heading north at time t+1
    loc_new_status_t = []
    loc_new_status_t.append(state_heading_north_str(t+1) + ' <=> (')
    # create conditions for the current state of heading north and possible actions at time t
    loc_current_status_t = []
    loc_current_status_t.append(
        '(' + state_heading_north_str(t) + ' & ~' + action_turn_left_str(t) + ' & ~' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_west_str(t) + ' & ' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_east_str(t) + ' & ' + action_turn_left_str(t) + ')'
    )

    # combine conditions for both time steps
    status = loc_new_status_t + loc_current_status_t
    # convert each condition to a string
    status_strings = []
    for condition in status:
        status_strings.append(str(condition))
    # concatenate all condition strings together
    axiom_str += ''.join(status_strings)
    # add closing parenthesis to complete the axiom string
    axiom_str += ')'

    return axiom_str

def axiom_generator_heading_east_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be East at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
        
    # create conditions for the state of heading north at time t+1
    loc_new_status_t = []
    loc_new_status_t.append(state_heading_east_str(t+1) + ' <=> (')
    # create conditions for the current state of heading north and possible actions at time t
    loc_current_status_t = []
    loc_current_status_t.append(
        '(' + state_heading_east_str(t) + ' & ~' + action_turn_left_str(t) + ' & ~' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_north_str(t) + ' & ' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_south_str(t) + ' & ' + action_turn_left_str(t) + ')'
    )

    # combine conditions for both time steps
    status = loc_new_status_t + loc_current_status_t
    # convert each condition to a string
    status_strings = []
    for condition in status:
        status_strings.append(str(condition))
    # concatenate all condition strings together
    axiom_str += ''.join(status_strings)
    # add closing parenthesis to complete the axiom string
    axiom_str += ')'

    return axiom_str

def axiom_generator_heading_south_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be South at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
            
    # create conditions for the state of heading north at time t+1
    loc_new_status_t = []
    loc_new_status_t.append(state_heading_south_str(t+1) + ' <=> (')
    # create conditions for the current state of heading north and possible actions at time t
    loc_current_status_t = []
    loc_current_status_t.append(
        '(' + state_heading_south_str(t) + ' & ~' + action_turn_left_str(t) + ' & ~' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_east_str(t) + ' & ' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_west_str(t) + ' & ' + action_turn_left_str(t) + ')'
    )

    # combine conditions for both time steps
    status = loc_new_status_t + loc_current_status_t
    # convert each condition to a string
    status_strings = []
    for condition in status:
        status_strings.append(str(condition))
    # concatenate all condition strings together
    axiom_str += ''.join(status_strings)
    # add closing parenthesis to complete the axiom string
    axiom_str += ')'

    return axiom_str

def axiom_generator_heading_west_ssa(t):
    """
    Assert the conditions at time t under which the
    Agent heading will be West at time t+1

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
                
    # create conditions for the state of heading north at time t+1
    loc_new_status_t = []
    loc_new_status_t.append(state_heading_west_str(t+1) + ' <=> (')
    # create conditions for the current state of heading north and possible actions at time t
    loc_current_status_t = []
    loc_current_status_t.append(
        '(' + state_heading_west_str(t) + ' & ~' + action_turn_left_str(t) + ' & ~' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_south_str(t) + ' & ' + action_turn_right_str(t) + ') | ' +
        '(' + state_heading_north_str(t) + ' & ' + action_turn_left_str(t) + ')'
    )

    # combine conditions for both time steps
    status = loc_new_status_t + loc_current_status_t
    # convert each condition to a string
    status_strings = []
    for condition in status:
        status_strings.append(str(condition))
    # concatenate all condition strings together
    axiom_str += ''.join(status_strings)
    # add closing parenthesis to complete the axiom string
    axiom_str += ')'

    return axiom_str

def generate_heading_ssa(t):
    """
    Generates all of the heading SSAs.
    """
    return [axiom_generator_heading_north_ssa(t),
            axiom_generator_heading_east_ssa(t),
            axiom_generator_heading_south_ssa(t),
            axiom_generator_heading_west_ssa(t)]

def generate_non_location_ssa(t):
    """
    Generate all non-location-based SSAs
    """
    axioms = [] # all_state_loc_ssa(t, xmin, xmax, ymin, ymax)
    axioms.append(axiom_generator_have_arrow_ssa(t))
    axioms.append(axiom_generator_wumpus_alive_ssa(t))
    axioms.extend(generate_heading_ssa(t))
    return list(filter(lambda s: s != '', axioms))

#----------------------------------

def axiom_generator_heading_only_north(t):
    """
    Assert that when heading is North, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    #initialize variables
    heading_status = []
    heading_status_dir = []
    #append the initial part of heading_status_dir
    heading_status_dir.append(state_heading_north_str(t) + ' <=> (')
    #convert the list to a string
    heading_status_dir = ''.join(heading_status_dir)

    not_heading_status = []
    #generating conditions for not heading west, east, and south
    directional_states = [state_heading_west_str(t), state_heading_east_str(t), state_heading_south_str(t)]
    for k in range(len(directional_states)):
        not_heading_status.append('~' + directional_states[k])

    #construct condition for heading north
    for _ in range(len(not_heading_status)):
        heading_status_dir += str(not_heading_status[_])
        if _ < len(not_heading_status) - 1:
            heading_status_dir += ' & '

    heading_status_dir += ')'
    #adingd condition for heading north to status
    heading_status.append(heading_status_dir)
    #constructing axiom_str by iterating through heading_status and appending each element
    axiom_str += '' 
    for element in heading_status:
        axiom_str += str(element)

    return axiom_str

def axiom_generator_heading_only_east(t):
    """
    Assert that when heading is East, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    #initialize variables
    heading_status = []
    heading_status_dir = []
    #append the initial part of heading_status_dir
    heading_status_dir.append(state_heading_east_str(t) + ' <=> (')
    #convert the list to a string
    heading_status_dir = ''.join(heading_status_dir)

    not_heading_status = []
    #generating conditions for not heading west, east, and south
    directional_states = [state_heading_north_str(t), state_heading_west_str(t), state_heading_south_str(t)]
    for k in range(len(directional_states)):
        not_heading_status.append('~' + directional_states[k])

    #construct condition for heading north
    for _ in range(len(not_heading_status)):
        heading_status_dir += str(not_heading_status[_])
        if _ < len(not_heading_status) - 1:
            heading_status_dir += ' & '

    heading_status_dir += ')'
    #adingd condition for heading north to status
    heading_status.append(heading_status_dir)
    #constructing axiom_str by iterating through heading_status and appending each element
    axiom_str += '' 
    for element in heading_status:
        axiom_str += str(element)

    return axiom_str

def axiom_generator_heading_only_south(t):
    """
    Assert that when heading is South, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    #initialize variables
    heading_status = []
    heading_status_dir = []
    #append the initial part of heading_status_dir
    heading_status_dir.append(state_heading_south_str(t) + ' <=> (')
    #convert the list to a string
    heading_status_dir = ''.join(heading_status_dir)

    not_heading_status = []
    #generating conditions for not heading west, east, and south
    directional_states = [state_heading_north_str(t), state_heading_west_str(t), state_heading_east_str(t)]
    for k in range(len(directional_states)):
        not_heading_status.append('~' + directional_states[k])

    #construct condition for heading north
    for _ in range(len(not_heading_status)):
        heading_status_dir += str(not_heading_status[_])
        if _ < len(not_heading_status) - 1:
            heading_status_dir += ' & '

    heading_status_dir += ')'
    #adingd condition for heading north to status
    heading_status.append(heading_status_dir)
    #constructing axiom_str by iterating through heading_status and appending each element
    axiom_str += '' 
    for element in heading_status:
        axiom_str += str(element)

    return axiom_str

    return axiom_str

def axiom_generator_heading_only_west(t):
    """
    Assert that when heading is West, the agent is
    not heading any other direction.

    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()

    #initialize variables
    heading_status = []
    heading_status_dir = []
    #append the initial part of heading_status_dir
    heading_status_dir.append(state_heading_west_str(t) + ' <=> (')
    #convert the list to a string
    heading_status_dir = ''.join(heading_status_dir)

    not_heading_status = []
    #generating conditions for not heading west, east, and south
    directional_states = [state_heading_north_str(t), state_heading_east_str(t), state_heading_south_str(t)]
    for k in range(len(directional_states)):
        not_heading_status.append('~' + directional_states[k])

    #construct condition for heading north
    for _ in range(len(not_heading_status)):
        heading_status_dir += str(not_heading_status[_])
        if _ < len(not_heading_status) - 1:
            heading_status_dir += ' & '

    heading_status_dir += ')'
    #adingd condition for heading north to status
    heading_status.append(heading_status_dir)
    #constructing axiom_str by iterating through heading_status and appending each element
    axiom_str += '' 
    for element in heading_status:
        axiom_str += str(element)

    return axiom_str

    return axiom_str

def generate_heading_only_one_direction_axioms(t):
    return [axiom_generator_heading_only_north(t),
            axiom_generator_heading_only_east(t),
            axiom_generator_heading_only_south(t),
            axiom_generator_heading_only_west(t)]


def axiom_generator_only_one_action_axioms(t):
    """
    Assert that only one axion can be executed at a time.
    
    t := time
    """
    axiom_str = ''
    "*** YOUR CODE HERE ***"
    # Comment or delete the next line once this function has been implemented.
    #utils.print_not_implemented()
    #actions that can be obtained from orignal actions
    orig_actions = [action_forward_str(t), action_grab_str(t), action_shoot_str(t), action_climb_str(t), action_turn_left_str(t), action_turn_right_str(t), action_wait_str(t)]
    #empty list to store the logic
    act=[]
    #temp str to store the logic
    select_action=''
    #terating through eacha action in orig_actions
    for i in range(len(orig_actions)):
        select_action=''
        #constructing the logic
        select_action+='('+orig_actions[i]+ ' <=> ('
        #ist to store the negated actions
        neg_action=[]
        #iterating here through orig actions to get he neg list
        for j in range(len(orig_actions)):
            if (j!=i):
                neg_action.append('~'+orig_actions[j])
        #convert neg_action elements to strings and join them with ' & ' separator
        temp_list = []
        for x in neg_action:
            temp_list.append(str(x))
        neg_action_string = ' & '.join(temp_list)
        select_action += neg_action_string
        #compelting the logic
        select_action+='))'
        act.append(select_action)
    #convert actions in act list to strings and join them with ' & ' separator
    temp_list1 = []
    for x in act:
        temp_list1.append(str(x))
    actions_string = ' & '.join(temp_list1)
    #concatenating with itself
    axiom_str += actions_string

    return axiom_str



def generate_mutually_exclusive_axioms(t):
    """
    Generate all time-based mutually exclusive axioms.
    """
    axioms = []
    
    # must be t+1 to constrain which direction could be heading _next_
    axioms.extend(generate_heading_only_one_direction_axioms(t + 1))

    # actions occur in current time, after percept
    axioms.append(axiom_generator_only_one_action_axioms(t))

    return list(filter(lambda s: s != '', axioms))

#-------------------------------------------------------------------------------
