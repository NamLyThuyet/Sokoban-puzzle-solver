
'''

    2020 CAB320 Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.
No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.


You are NOT allowed to change the defined interfaces.
That is, changing the formal parameters of a function will break the 
interface and results in a fail for the test of your code.
This is not negotiable! 


'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import search 
import sokoban
import itertools

taboo_cell = 'X'
wall_cell = "#"
target = "."
emptySpace = " "
box = "$"
player = "@"
playerOnTarget = "!"
boxOnTarget = "*"


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
    return [ (9998616, 'John', 'Pase'), (10182403, 'Lasni', 'Hakmanage'), (10098097, 'Nam', 'Ly') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell inside a warehouse is 
    called 'taboo'  if whenever a box get pushed on such a cell then the puzzle 
    becomes unsolvable. Cells outside the warehouse should not be tagged as taboo.
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with a worker inside the warehouse

    @return
       A string representing the puzzle with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE"
    array_x = []
    array_y = []
    array_wall = []
    count = -1;
    tabooCount = 0;

    # Getting the x,y values for the wall locations
    X,Y = zip(*warehouse.walls)
    x_size, y_size = 1+max(X), 1+max(Y)

    # Create an empty space inside the walls
    vis = [[" "] * x_size for y in range(y_size)]

    # Search through each wall location and add # for wall into vis
    for (x,y) in warehouse.walls:
        vis[y][x] = wall_cell
        array_x.append(x)
        array_y.append(y)

    # Search through each target location and add . for target into vis
    for (x,y) in warehouse.targets:
        vis[y][x] = target

    # Find each row and append it to a 2d array
    for i in range(len(array_x)):
        if array_x[i] < array_x[i - 1]: # If the value of array_x[i] is less than the previous value move to next row
            count += 1
            array_wall.append([])
        array_wall[count].append(array_x[i])

    # Search Through each row and add an X for a taboo cell
    for x in range(x_size):
        tabooCount = 0
        for y in range(y_size):
            # Search inbetween the walls
            if x > min(array_wall[tabooCount]) and x < max(array_wall[tabooCount]): 
                if y > min(array_y) and y < max(array_y):
                    if vis[y][x] == emptySpace: # Only adds a taboo cell if space is empty
                        # Top left corner wall cell 
                        if vis[y - 1][x] == wall_cell and vis[y][x - 1] == wall_cell:
                            vis[y][x] = taboo_cell
                        # Top right corner wall cell
                        if vis[y - 1][x] == wall_cell and vis[y][x + 1] == wall_cell:
                            vis[y][x] = taboo_cell
                        # Bottom left corner wall cell
                        if vis[y + 1][x] == wall_cell and vis[y][x - 1] == wall_cell:
                            vis[y][x] = taboo_cell
                        # Bottom right corner wall cell
                        if vis[y + 1][x] == wall_cell and vis[y][x + 1] == wall_cell:
                            vis[y][x] = taboo_cell
            # Increase tabooCount when y increases and reset to 0 when x increases 
            if tabooCount >= len(array_wall) - 1:
                tabooCount = 0
            else:
                tabooCount += 1

    # Search through each row and add an X for taboo cell if empty space between 2 taboo cells
    for x in range(x_size):
        tabooCount = 0
        for y in range(y_size):
            if x > min(array_wall[tabooCount]) and x < max(array_wall[tabooCount]):
                if y > min(array_y) and y < max(array_y):
                    if vis[y][x] == emptySpace:
                        # Top and bottom taboo cell
                        if vis[y - 1][x] == taboo_cell and vis[y + 1][x] == taboo_cell and (vis[y][x - 1] == wall_cell or vis[y][x + 1] == wall_cell):
                            vis[y][x] = taboo_cell
                        # Left and right taboo cell
                        if vis[y][x - 1] == taboo_cell and vis[y][x + 1] == taboo_cell and (vis[y - 1][x] == wall_cell or vis[y + 1][x] == wall_cell):
                            vis[y][x] = taboo_cell
                                
            if tabooCount >= len(array_wall) - 1:
                tabooCount = 0
            else:
                tabooCount += 1

    # Delete the target cells
    for (x,y) in warehouse.targets:
        vis[y][x] = emptySpace

    # Join the rows together 
    return "\n".join(["".join(line) for line in vis])

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    Each SokobanPuzzle instance should have at least the following attributes
    - self.allow_taboo_push
    - self.macro
    
    When self.allow_taboo_push is set to True, the 'actions' function should 
    return all possible legal moves including those that move a box on a taboo 
    cell. If self.allow_taboo_push is set to False, those moves should not be
    included in the returned list of actions.
    
    If self.macro is set True, the 'actions' function should return 
    macro actions. If self.macro is set False, the 'actions' function should 
    return elementary actions.        
    '''
    
    def __init__(self, warehouse, push_costs = None):

        self.initial = (warehouse.worker,) + tuple(warehouse.boxes,)

        self.walls = warehouse.walls

        self.goal = warehouse.targets
        self.taboo_cells = list(sokoban.find_2D_iterator(taboo_cells(warehouse).split('\n'), "X"))
        self.macro = False
        self.allow_taboo = True
        self.push_costs = push_costs

    def setMacro(self, macroState):
        """
        Change self.macro to True or False
        """
        self.macro = macroState

    def setAllowTaboo(self, tabooState):
        """
        Change self.allow_taboo to True or False
        """
        self.allow_taboo = tabooState
    
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        As specified in the header comment of this class, the attributes
        'self.allow_taboo_push' and 'self.macro' should be tested to determine
        what type of list of actions is to be returned.
        """
        
        legal_actions = []

        worker_pos_x, worker_pos_y = state[0]
        boxes = state[1:]

        if self.macro == False:
            if (worker_pos_x, worker_pos_y - 1) not in self.walls:
                if (worker_pos_x, worker_pos_y - 1) in boxes:
                    if (worker_pos_x, worker_pos_y - 2) not in self.walls:
                        if self.allow_taboo == False:
                            if (worker_pos_x, worker_pos_y - 2) not in self.taboo_cells:
                                legal_actions.append('Up')
                        else:
                            legal_actions.append('Up')
                else:
                    legal_actions.append('Up') # Add Up into legal_action array

            if (worker_pos_x, worker_pos_y + 1) not in self.walls:
                if (worker_pos_x, worker_pos_y + 1) in boxes:
                    if (worker_pos_x, worker_pos_y + 2) not in self.walls:
                        if self.allow_taboo == False:
                            if (worker_pos_x, worker_pos_y + 2) not in self.taboo_cells:
                                legal_actions.append('Down')
                        else:
                            legal_actions.append('Down')
                else:
                    legal_actions.append('Down')
                    
            if (worker_pos_x - 1, worker_pos_y) not in self.walls:
                if (worker_pos_x - 1, worker_pos_y) in boxes:
                    if (worker_pos_x - 2, worker_pos_y) not in self.walls:
                        if self.allow_taboo == False:
                            if (worker_pos_x - 2, worker_pos_y) not in self.taboo_cells:
                                legal_actions.append('Left')
                        else:
                            legal_actions.append('Left')
                else:
                    legal_actions.append('Left')

            if (worker_pos_x + 1, worker_pos_y) not in self.walls:
                if (worker_pos_x + 1, worker_pos_y) in boxes:
                    if (worker_pos_x + 2, worker_pos_y) not in self.walls:
                        if self.allow_taboo == False:
                            if (worker_pos_x + 2, worker_pos_y) not in self.taboo_cells:
                                legal_actions.append('Right')
                        else:
                            legal_actions.append('Right')
                else:
                    legal_actions.append('Right')
        else:
            for box in boxes:
                if (box[0], box[1] - 1) not in self.walls and (box[0], box[1] - 1) not in boxes and can_go_there(state, (box[1] + 1, box[0]), self.walls, self.macro):
                    if self.allow_taboo == False:
                        if (box[0], box[1] - 1) not in self.taboo_cells:
                            legal_actions.append(((box[1], box[0]), 'Up'))
                    else:
                        legal_actions.append(((box[1], box[0]), 'Up'))

                if (box[0], box[1] + 1) not in self.walls and (box[0], box[1] + 1) not in boxes and can_go_there(state, (box[1] - 1, box[0]), self.walls, self.macro):
                    if self.allow_taboo == False:
                        if (box[0], box[1] + 1) not in self.taboo_cells:
                            legal_actions.append(((box[1], box[0]), 'Down'))
                    else:
                        legal_actions.append(((box[1], box[0]), 'Down'))

                if (box[0] - 1, box[1]) not in self.walls and (box[0] - 1, box[1]) not in boxes and can_go_there(state, (box[1], box[0] + 1), self.walls, self.macro):
                    if self.allow_taboo == False:
                        if (box[0] - 1, box[1]) not in self.taboo_cells:
                            legal_actions.append(((box[1], box[0]), 'Left'))
                    else:
                        legal_actions.append(((box[1], box[0]), 'Left'))

                if (box[0] + 1, box[1]) not in self.walls and (box[0] + 1, box[1]) not in boxes and can_go_there(state, (box[1], box[0] - 1), self.walls, self.macro):
                    if self.allow_taboo == False:
                        if (box[0] + 1, box[1]) not in self.taboo_cells:
                            legal_actions.append(((box[1], box[0]), 'Right'))
                    else:
                        legal_actions.append(((box[1], box[0]), 'Right'))
                 
        return legal_actions

    def result(self, state, action):
        """
        Return the state that results from exexuting the given
        action in the given state. The action must be one of
        self.actions(state).
        """

        next_state = state
        worker_pos_x, worker_pos_y = state[0]
        boxes = state[1:]
        next_boxes = []

        if self.macro == False:
            
            if action == 'Up':
                if (worker_pos_x, worker_pos_y - 1) in boxes:
                    for box in boxes:
                        if  (worker_pos_x, worker_pos_y - 1) == box:
                            next_boxes += ((worker_pos_x, worker_pos_y - 2),)
                        else:
                            next_boxes += (box,)
                    next_state = ((worker_pos_x, worker_pos_y - 1),) + tuple(next_boxes)
                else:    
                    next_state = ((worker_pos_x, worker_pos_y - 1),) + tuple(boxes)
            if action == 'Down':
                if (worker_pos_x, worker_pos_y + 1) in boxes:
                    for box in boxes:
                        if  (worker_pos_x, worker_pos_y + 1) == box:
                            next_boxes += ((worker_pos_x, worker_pos_y + 2),)
                        else:
                            next_boxes += (box,)
                    next_state = ((worker_pos_x, worker_pos_y + 1),) + tuple(next_boxes)
                else:    
                    next_state = ((worker_pos_x, worker_pos_y + 1),) + tuple(boxes)

            if action == 'Left':
                if (worker_pos_x - 1, worker_pos_y) in boxes:
                    for box in boxes:
                        if  (worker_pos_x - 1, worker_pos_y) == box:
                            next_boxes += ((worker_pos_x - 2, worker_pos_y),)
                        else:
                            next_boxes += (box,)
                    next_state = ((worker_pos_x - 1, worker_pos_y),) + tuple(next_boxes)
                else:   
                    next_state = ((worker_pos_x - 1, worker_pos_y),) + tuple(boxes)

            if action == 'Right':
                if (worker_pos_x + 1, worker_pos_y) in boxes:
                    for box in boxes:
                        if (worker_pos_x + 1, worker_pos_y) == box:
                            next_boxes += ((worker_pos_x + 2, worker_pos_y),)
                        else:
                            next_boxes += (box,)
                    next_state = ((worker_pos_x + 1, worker_pos_y),) + tuple(next_boxes)
                else:    
                    next_state = ((worker_pos_x + 1, worker_pos_y),) + tuple(boxes)

        else:
            box_pos = action[0]

            if action[1] == 'Up':
                for box in boxes:
                    if box == (box_pos[1], box_pos[0]):
                        next_boxes += ((box_pos[1], box_pos[0] - 1),)
                    else:
                        next_boxes += (box,)
                next_state = ((box_pos[1], box_pos[0]),) + tuple(next_boxes)

            elif action[1] == 'Down':
                for box in boxes:
                    if box == (box_pos[1], box_pos[0]):
                        next_boxes += ((box_pos[1], box_pos[0] + 1),)
                    else:
                        next_boxes += (box,)
                next_state = ((box_pos[1], box_pos[0]),) + tuple(next_boxes)

            elif action[1] == 'Left':
                for box in boxes:
                    if box == (box_pos[1], box_pos[0]):
                        next_boxes += ((box_pos[1] - 1, box_pos[0]),)
                    else:
                        next_boxes += (box,)
                next_state = ((box_pos[1], box_pos[0]),) + tuple(next_boxes)

            elif action[1] == 'Right':
                for box in boxes:
                    if box == (box_pos[1], box_pos[0]):
                        next_boxes += ((box_pos[1] + 1, box_pos[0]),)
                    else:
                        next_boxes += (box,)
                next_state = ((box_pos[1], box_pos[0]),) + tuple(next_boxes)      

        return next_state

    def goal_test(self, state):
        """
        Return true if boxes have reached the goal or false if they havent
        """

        boxes = list(state[1:])
        goal = list(self.goal)
        goal.sort()
        boxes.sort()

        if boxes == self.goal:
            return True
        else:
            return False

    def path_cost(self, c, state1, action, state2):
        """
        Return the path cost of each move taken
        """
        next_state1 = state1
        next_state2 = state2
        
        if self.push_costs == None:
            return c + 1
        else:
            if next_state1[0] != next_state2[1]:
                return c + sum(self.push_costs)
            else:
                return c + 1

    def h(self, node):
        """
        Return the heuristics value of the distance to box and worker to box
        """

        boxes = node.state[1:]
        worker = node.state[0]
        goal = self.goal
        
        if self.macro == False:
            
            heuristics_box = []
            
            dist = 0
            total_dist = 0
            for box in boxes:
                for target in goal:
                    dist = (abs(box[0] - target[0]) + abs(box[1] - target[1]))
                    total_dist += dist
                heuristics_box.append(total_dist)
            box_to_target = min(heuristics_box)

            heuristics_worker = []
            
            for box in boxes:
                dist = (abs(worker[0] - box[0]) + abs(worker[1] - box[1]))
                heuristics_worker.append(dist)
            worker_to_box = min(heuristics_worker)

            return (box_to_target + worker_to_box)
        else:
            
            heuristics_box = []
            
            dist = 0
            total_dist = 0
            for target in goal:
                for box in boxes:
                    dist = (abs(box[0] - target[0]) + abs(box[1] - target[1]))
                    total_dist += dist
                heuristics_box.append(total_dist)
            box_to_target = min(heuristics_box)

            return box_to_target
            
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''

    puzzle = SokobanPuzzle(warehouse)
    puzzle.setMacro(False)
    puzzle.setAllowTaboo(True)
    

    # Check each action in action_seq to see if the action is legal or impossible
    for action in action_seq:
        state = (warehouse.worker,) + tuple(warehouse.boxes,)
        
        results = puzzle.result(state, action) # Get the legal action results

        warehouse.worker = results[0]
        warehouse.boxes = results[1:]
            
        # Check if a worker has gone into a wall
        if warehouse.worker in warehouse.walls:
            return 'Impossible'

        addBox = []
        
        # Check if a box has gone into a wall
        for box in warehouse.boxes:
            if box in warehouse.walls:
                return 'Impossible'
                
            if box in addBox:
                return 'Impossible'
            else:
                addBox.append(box)
        
    return warehouse.__str__()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using A* algorithm and elementary actions
    the puzzle defined in the parameter 'warehouse'.
    
    In this scenario, the cost of all (elementary) actions is one unit.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return the string 'Impossible'
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''

    puzzle = SokobanPuzzle(warehouse)
    puzzle.setMacro(False)
    puzzle.setAllowTaboo(False)

    result = search.astar_graph_search(puzzle)

    if result == None:
        return 'Impossible'
    else:
        return result.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst, walls = None, macro = None):
    '''    
    Determine whether the worker can walk to the cell dst=(row,column) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,column) without pushing any box
      False otherwise
    '''

    if macro == True:
        result = search.astar_graph_search(CanGoThere(warehouse, (dst[1], dst[0]), walls, macro))
        return result is not None
    else:
        result = search.astar_graph_search(CanGoThere(warehouse, (dst[1], dst[0])))
        return result is not None
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class CanGoThere(search.Problem):

    def __init__(self, state, goal, walls = None, macro = None):

        if macro == True:
            self.initial = state[0]
            self.boxes = state[1:]
            self.walls = walls
            
        else:
            # Set initial
            self.initial = state.worker
            self.boxes = state.boxes
            self.walls = state.walls

        # Set the goal as the target locations
        self.goal = goal

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        """
        
        legal_actions = []
        worker = state

        # Check to see if worker is going into a wall when going up
        if (worker[0], worker[1] - 1) not in self.walls and (worker[0], worker[1] - 1) not in self.boxes:
            legal_actions.append('Up') # Add Up into legal_action array

        #Down
        if (worker[0], worker[1] + 1) not in self.walls and (worker[0], worker[1] + 1) not in self.boxes:
            legal_actions.append('Down')
                
        #Left
        if (worker[0] - 1, worker[1]) not in self.walls and (worker[0] - 1, worker[1]) not in self.boxes:
            legal_actions.append('Left')

        #Right
        if (worker[0] + 1, worker[1]) not in self.walls and (worker[0] + 1, worker[1]) not in self.boxes:
            legal_actions.append('Right')

        return legal_actions

    def result(self, state, action):
        """
        Return the state that results from exexuting the given
        action in the given state. The action must be one of
        self.actions(state).
        """

        worker = state
        
        next_state = worker

        # If action is up move player and boxes pos to new location
        if action == 'Up':   
            next_state = (worker[0], worker[1] - 1)
            
        # Do the same for down
        elif action == 'Down':   
            next_state = (worker[0], worker[1] + 1)

        # Do the same for left
        elif action == 'Left':  
            next_state = (worker[0] - 1, worker[1])

        # Do the same for right
        elif action == 'Right': 
            next_state = (worker[0] + 1, worker[1])

        return next_state

    def goal_test(self, state):
        """
        Return true if boxes have reached the goal or false if they havent
        """

        return state == self.goal

    def h(self, node):
        """
        Return the heuristics value of the distance of the worker to goal
        """
        
        return (abs(node.state[0] - self.goal[0]) + abs(node.state[1] - self.goal[1]))
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using using A* algorithm and macro actions the puzzle defined in 
    the parameter 'warehouse'. 
    
    A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes to the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    In this scenario, the cost of all (macro) actions is one unit. 

    @param warehouse: a valid Warehouse object

    @return
        If the puzzle cannot be solved return the string 'Impossible'
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''

    puzzle = SokobanPuzzle(warehouse)
    puzzle.setMacro(True)
    puzzle.setAllowTaboo(False)
    
    result = search.astar_graph_search(puzzle)

    if result == None:
        return 'Impossible'
    else:
        return result.solution()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban_elem(warehouse, push_costs):
    '''
    In this scenario, we assign a pushing cost to each box, whereas for the
    functions 'solve_sokoban_elem' and 'solve_sokoban_macro', we were 
    simply counting the number of actions (either elementary or macro) executed.
    
    When the worker is moving without pushing a box, we incur a
    cost of one unit per step. Pushing the ith box to an adjacent cell 
    now costs 'push_costs[i]'.
    
    The ith box is initially at position 'warehouse.boxes[i]'.
        
    This function should solve using A* algorithm and elementary actions
    the puzzle 'warehouse' while minimizing the total cost described above.
    
    @param 
     warehouse: a valid Warehouse object
     push_costs: list of the weights of the boxes (pushing cost)

    @return
        If puzzle cannot be solved return 'Impossible'
        If a solution exists, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    puzzle = SokobanPuzzle(warehouse,push_costs)
    puzzle.setMacro(False)
    puzzle.setAllowTaboo(False)
    
    puzzleGoalState = warehouse.copy() 
    if (puzzleGoalState.boxes == puzzleGoalState.targets):
        return []

    result = search.astar_graph_search(puzzle)
    step_move = []   
    if (result is None):
        return 'Impossible'
    else:
        for node in result.path():
            step_move.append(node.action.__str__())
        action_seq = step_move[1:]
        if check_elem_action_seq(warehouse,action_seq) == 'Impossible':
            return 'Impossible'
        else:
            return action_seq


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

