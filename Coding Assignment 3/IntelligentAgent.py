from BaseAI import BaseAI
import random
import time


# 0 stands for "Up", 1 stands for "Down", 2 stands for "Left", and 3 stands for "Right".
class IntelligentAgent(BaseAI):

    def getMove(self, grid):

        self.time_limit = time.process_time() + 0.199  # set time limit for each recursion
        action = self.minimax(grid)

        if not action:
            random.choice(grid.getAvailableMoves())[1]

        return action

    def minimax(self, grid):
        return (self.maximize(grid, alpha=-float('inf'), beta=float('inf'), depth=0))[0]

    def maximize(self, grid, alpha, beta, depth):

        if depth >= 9 or time.process_time() > self.time_limit:
            return None, self.get_mark_heuristic(grid)

        maxUtility = -float('inf')
        maxChild = None

        for child in grid.getAvailableMoves():
            utility = self.get_node_chance_utility(child[1], alpha, beta, (depth + 1))

            if utility > maxUtility:
                maxUtility = utility
                maxChild = child[0]

            if maxUtility >= beta:
                break

            if maxUtility > alpha:
                alpha = maxUtility

        return maxChild, maxUtility

    def minimize(self, grid, cell_value, alpha, beta, depth):

        if depth >= 9 or time.process_time() > self.time_limit:
            return self.get_mark_heuristic(grid)

        minUtility = float('inf')
        minChild = None

        for child in grid.getAvailableCells():

            board_temp = grid.clone()
            board_temp.insertTile(child, cell_value)

            utility = self.maximize(board_temp, alpha, beta, (depth + 1))
            if utility[1] < minUtility:
                minUtility = utility[1]

            if minUtility <= beta:
                break

            if minUtility < beta:
                beta = minUtility

        return minUtility

    def get_node_chance_utility(self, grid, alpha, beta, depth):
        if depth >= 9 or time.process_time() > self.time_limit:
            return None, self.get_mark_heuristic(grid)

        # here, (0.9, 0.1) or (0.8, 0.2)?
        # it feels like the previous one gets 4096 easier, while the latter one gets 2048 easier
        left = 0.8 * self.minimize(grid, 2, alpha, beta, depth + 1)
        right = 0.2 * self.minimize(grid, 4, alpha, beta, depth + 1)
        return (left + right) / 2

    def get_mark_heuristic(self, grid):

        mark = 0
        temp_mark = 0

        # step 1
        # r represents row, c represents column
        for r in range(len(grid.map)):
            for c in range(len(grid.map[r])):

                if c == 3:
                    if r == 0:
                        mark += 1 * grid.map[r][c]
                        temp_mark += 0
                    elif r == 1:
                        mark += 1 * grid.map[r][c]
                        temp_mark += 1
                    elif r == 2:
                        mark += .5 * grid.map[r][c]
                        temp_mark += 2
                    elif r == 3:
                        mark += .2 * grid.map[r][c]
                        temp_mark += 3

                elif c == 2:
                    if r == 0:
                        mark += 5 * grid.map[r][c]
                        temp_mark += 0
                    elif r == 1:
                        mark += 2 * grid.map[r][c]
                        temp_mark += 2
                    elif r == 2:
                        mark += 1 * grid.map[r][c]
                        temp_mark += 4
                    elif r == 3:
                        mark += .5 * grid.map[r][c]
                        temp_mark += 6

                elif c == 1:
                    if r == 0:
                        mark += 7 * grid.map[r][c]
                        temp_mark += 0
                    elif r == 1:
                        mark += 5 * grid.map[r][c]
                        temp_mark += 3
                    elif r == 2:
                        mark += 2 * grid.map[r][c]
                        temp_mark += 6
                    elif r == 3:
                        mark += 1 * grid.map[r][c]
                        temp_mark += 9

                elif c == 0:
                    if r == 0:
                        mark += 20 * grid.map[r][c]
                        temp_mark += 0
                    elif r == 1:
                        mark += 10 * grid.map[r][c]
                        temp_mark += 4
                    elif r == 2:
                        mark += 5 * grid.map[r][c]
                        temp_mark += 8
                    elif r == 3:
                        mark += 2 * grid.map[r][c]
                        temp_mark += 12

        # step 2
        for r in range(0, 3):  # 0, 1, 2
            for c in range(0, 3):
                if grid.map[r][c] >= grid.map[r][c + 1]:
                    mark += 1
                    if grid.map[c][r] >= grid.map[c][r + 1]:
                        mark += 1
        # step 3
        for c in grid.map:
            for cell in c:
                if (cell == 0):
                    mark += 1

        return mark
