from __future__ import division
from __future__ import print_function

import queue
import sys
import math
import time
import queue as Q
import random

import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        self.depth = 1
        self.priority = None

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def __lt__(self, other):
        return self.priority < other.priority

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])
        print('')

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        new_config = []
        for i in range(len(self.config)):
            new_config.append(self.config[i])

        for i in range(len(new_config)):
            if (new_config[i] == 0):
                if (i == 0 or i == 1 or i == 2):
                    return None
                else:
                    new_config[i] = new_config[i - 3]
                    new_config[i - 3] = 0
                    new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Up')
                    new_state.depth = new_state.parent.depth + 1
                    return new_state

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        new_config = []
        for i in range(len(self.config)):
            new_config.append(self.config[i])

        for i in range(len(new_config)):
            if (new_config[i] == 0):
                if (i == 6 or i == 7 or i == 8):
                    return None
                else:
                    new_config[i] = new_config[i + 3]
                    new_config[i + 3] = 0
                    new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Down')
                    new_state.depth = new_state.parent.depth + 1
                    return new_state

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        new_config = []
        for i in range(len(self.config)):
            new_config.append(self.config[i])

        for i in range(len(new_config)):
            if (new_config[i] == 0):
                if (i == 0 or i == 3 or i == 6):
                    return None
                else:
                    new_config[i] = new_config[i - 1]
                    new_config[i - 1] = 0
                    new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Left')
                    new_state.depth = new_state.parent.depth + 1
                    return new_state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        new_config = []
        for i in range(len(self.config)):
            new_config.append(self.config[i])

        for i in range(len(new_config)):
            if (new_config[i] == 0):
                if (i == 2 or i == 5 or i == 8):
                    return None
                else:
                    new_config[i] = new_config[i + 1]
                    new_config[i + 1] = 0
                    new_state = PuzzleState(new_config, int(math.sqrt(len(new_config))), parent=self, action='Right')
                    new_state.depth = new_state.parent.depth + 1
                    return new_state

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        for child in self.children:
            child.depth = self.depth + 1
        return self.children

    def get_path(self):
        path = []
        state = self
        while (state.parent != None):
            path.insert(0, state.action)
            state = state.parent
        return path


# Function that Writes to output.txt
### Students need to change the method to have the corresponding parameters
def writeOutput(state, nodes_expanded, max_search_depth):
    ### Student Code Goes here
    path_to_goal = state.get_path()
    print('path_to_goal:', path_to_goal)
    print('cost_of_path:', len(path_to_goal))
    print('nodes_expanded:', nodes_expanded)
    print('search_depth:', len(path_to_goal))
    print('max_search_depth:', max_search_depth)

    file = open('output.txt', 'w')
    file.write('path_to_goal: ' + str(path_to_goal) + '\n')
    file.write('cost_of_path: ' + str(len(path_to_goal)) + '\n')
    file.write('nodes_expanded: ' + str(nodes_expanded) + '\n')
    file.write('search_depth: ' + str(len(path_to_goal)) + '\n')
    file.write('max_search_depth: ' + str(max_search_depth) + '\n')
    return


def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    nodes_expanded = 0
    max_search_depth = 0

    print("Initial State is:")
    initial_state.display()

    frontier = []
    frontier.append(initial_state)

    fList = {}  # fringe state config list
    eList = {}  # explored state config list

    while frontier:  # while frontier is not empty
        state = frontier.pop(0)
        fList[tuple(state.config)] = False
        eList[tuple(state.config)] = True

        max_search_depth = max(max_search_depth, state.depth)

        if test_goal(state):
            print('GOAL REACHED!')
            writeOutput(state, nodes_expanded, max_search_depth)
            return True

        state.expand()
        nodes_expanded += 1
        print(nodes_expanded)

        for children in state.children:  # if there is no children for the state, program pass this automatically
            try:
                if fList[tuple(children.config)] == True:
                    continue
                if eList[tuple(children.config)] == True:
                    continue
            except:
                pass

            frontier.append(children)
            fList[tuple(children.config)] = True
    return False


def dfs_search(initial_state):  # Change dfs first and change the other two
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    nodes_expanded = 0
    max_search_depth = 0

    print("Initial State is:")
    initial_state.display()

    frontier = []
    frontier.append(initial_state)

    fList = {}  # fringe state config list
    eList = {}  # explored state config list

    while frontier:  # while frontier is not empty
        state = frontier.pop(-1)
        fList[tuple(state.config)] = False
        eList[tuple(state.config)] = True

        max_search_depth = max(max_search_depth, state.depth)

        if test_goal(state):
            print('GOAL REACHED!')
            writeOutput(state, nodes_expanded, max_search_depth - 1)
            return True

        state.expand()
        state.children.reverse()
        nodes_expanded += 1
        print(nodes_expanded)

        for children in state.children:  # if there is no children for the state, program pass this automatically
            try:
                if fList[tuple(children.config)] == True:
                    continue
                if eList[tuple(children.config)] == True:
                    continue
            except:
                pass

            frontier.append(children)
            fList[tuple(children.config)] = True
    return False


def A_star_search(initial_state):
    """A * search"""
    nodes_expanded = 0
    max_search_depth = 0

    print("Initial State is:")
    initial_state.display()
    initial_state.priority = calculate_total_cost(initial_state)

    frontier = queue.PriorityQueue()
    frontier.put(initial_state)
    explored = []

    while frontier:  # while frontier is not empty
        state = frontier.get()
        explored.append(state)

        max_search_depth = max(max_search_depth, state.depth)

        if test_goal(state):
            print('GOAL REACHED!')
            writeOutput(state, nodes_expanded, max_search_depth - 1)
            return True

        state.expand()
        nodes_expanded += 1
        print(nodes_expanded)

        if (nodes_expanded % 5000 == 0): random.shuffle(explored)  # shuffle explored states to speed up the program

        for children in state.children:  # if there is no children for the state, program pass this automatically
            children.cost = children.parent.cost + 1
            if (check_exist_A_star(children, frontier, explored) == False):
                children.priority = calculate_total_cost(children)
                frontier.put(children)
    return False


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    man_dist = 0
    for tile in state.config:
        if tile == 0: continue
        man_dist += calculate_manhattan_dist(state.config.index(tile), tile)
    return (state.cost + man_dist)


def calculate_manhattan_dist(idx, value, n=None):  # always n = 3 for this assignment
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    col = {0: 0, 3: 0, 6: 0, 1: 1, 4: 1, 7: 1, 2: 2, 5: 2, 8: 2}
    row = {0: 0, 1: 0, 2: 0, 3: 1, 4: 1, 5: 1, 6: 2, 7: 2, 8: 2}
    current = [col[idx], row[idx]]
    target = [col[value], row[value]]
    return (abs(current[0] - target[0]) + abs(current[1] - target[1]))


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    for i in range(len(puzzle_state.config)):
        if (puzzle_state.config[i] != i):
            return False
    return True


def check_exist_A_star(child_state, frontier, explored):
    # here, frontier should be a priority queue, and explored should be a list
    for i in range(frontier.qsize()):
        if (child_state.cost == frontier.queue[i].cost and child_state.config == frontier.queue[i].config):
            return True
    for i in range(len(explored)):
        if (child_state.cost == explored[i].cost and child_state.config == explored[i].config):
            return True
    return False


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

    if search_mode == "bfs":
        bfs_search(hard_state)
    elif search_mode == "dfs":
        dfs_search(hard_state)
    elif search_mode == "ast":
        A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    ram_usage = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (2 ** 20)

    print('running_time: %.8f' % (end_time - start_time))
    print('max_ram_usage: %.8f' % ram_usage)
    print('max_ram_usage:')

    file = open('output.txt', 'a')
    file.write(str('running_time: %.8f' % (end_time - start_time)) + '\n')

    file.write(str('max_ram_usage: %.8f' % ram_usage) + '\n')
    # file.write(str('max_ram_usage: %.8f' % (end_time - start_time)) + '\n')


if __name__ == '__main__':
    main()
