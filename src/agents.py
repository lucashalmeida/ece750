import numpy as np
import random as rm

from mesa import Agent
from numpy.random import choice

class Fish(Agent):
    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)

    def is_water_deep(self, pos):
        water = [item for item in self.model.grid.get_cell_list_contents(pos) if type(item) is Water]
        return water[0].deep

    def transition_matrix(self):
        states = ["safe", "exposed"]
        transitionName = [["SS", "SE", "ES", "EE"]]
        transitionMatrix = [[0.995,0.005],[0.038,0.062]]


    def move(self):
        # Check our current location
        in_deep_water = self.is_water_deep(self.pos)

        # Get all neighbours
        neighbours = self.model.grid.get_neighbors(self.pos, self.moore, True)

        # Make a list of all fish
        fishes = []
        waters = []
        for neighbour in neighbours:
            if type(neighbour) is BoldFish:
                fishes.append(neighbour)
            elif type (neighbour) is Water:
                waters.append(neighbour)

        # For every fish around the current fish, in random order, try to move towards that fish
        # if len(fishes) > 0:
        #     self.random.shuffle(fishes)
        #     for fish in fishes:
        #         # Build the transition matrix
        #         water = self.is_water_deep(fish.pos)
        #         print(water)
        states = ["safe", "exposed"]
        transitionName = [["SS", "SE"], ["ES", "EE"]]
        transitionMatrix = [[0.995,0.005],[0.038,0.962]]

        # If we didn't move towards any fish, try to move somewhere else, in random order
        self.random.shuffle(waters)
        for water in waters:
            if water.deep != in_deep_water:
                # If I'm looking at a water region with a different depth, build the transion matrix   
                initialState = "safe" if in_deep_water else "exposed"

                if initialState == "safe":
                    change = np.random.choice(transitionName[0],replace=True,p=transitionMatrix[0])
                    if change == "SE":
                        self.model.grid.move_agent(self, water.pos)
                elif initialState == "exposed":
                    change = np.random.choice(transitionName[1],replace=True,p=transitionMatrix[1])
                    if change == "ES":
                        self.model.grid.move_agent(self, water.pos)

            else:
                # If I'm looking at a water region in the same depth, move with a simple decision
                if self.random.choice([True, False]):
                    self.model.grid.move_agent(self, water.pos)


        # Make a list of all 

        # next_moves = {}
        # for neighbour in neighbours:
        #     if neighbour.pos not in next_moves:
        #         next_moves[neighbour.pos] = []
        #     next_moves[neighbour.pos].append(neighbour)

        # list_of_candidates = [0] * len(neighbours)
        # probability_distribution = [0] * len(neighbours)

        # index = 0
        # for k, v in next_moves.items():

        #     list_of_candidates[index] = k
            
        #     for agents in v:
        #         # try:
        #         current = probability_distribution[index]
        #         # except IndexError:
        #         #     current = 0

        #         if type(v) is Fish:
        #             probability_distribution[index] = current + 0.1
        #         else:
        #             probability_distribution[index] = current + 0
        #     index += 1

        # print(list_of_candidates)
        # print(probability_distribution)
        # next_move_index = choice(len(list_of_candidates), 1, p=probability_distribution)       
        # next_move = list_of_candidates[next_move_index]
        # self.model.grid.move_agent(self, next_move)

class BoldFish(Fish):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.pos = pos

    def step(self):
        self.random_move()


class ShyFish(Fish):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, pos, model)
        self.pos = pos
    
    def step(self):
        self.move()

class Water(Agent):
    def __init__(self, unique_id, pos, model, deep):
        super().__init__(unique_id, model)
        self.deep = deep

