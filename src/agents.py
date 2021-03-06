import numpy as np
import random as rm

from mesa import Agent
from numpy.random import choice


class TransitionIntensity:
    def __init__(self, states, transitionName, transitionMatrix):
        super().__init__()
        self.states = states
        self.transitionName = transitionName
        self.transitionMatrix = transitionMatrix
        

class Fish(Agent):
    def __init__(self, unique_id, pos, model, transitionMatrix, moore=True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.transitionWhenAlone = TransitionIntensity(
            ["safe", "exposed"], 
            [["SS", "SE"], ["ES", "EE"]], 
            transitionMatrix
        )

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)

    def is_water_deep(self, pos):
        water = [item for item in self.model.grid.get_cell_list_contents(pos) if type(item) is Water]
        return water[0].deep

    def move(self):
        # Check our current location
        in_deep_water = self.is_water_deep(self.pos)

        # Get all neighbours
        neighbours = self.model.grid.get_neighbors(self.pos, self.moore, True)

        # Make a list of all fish
        fishes = []
        waters = []
        for neighbour in neighbours:
            neighbour_type= type(neighbour)
            if neighbour_type is BoldFish or neighbour_type is ShyFish:
                fishes.append(neighbour)
            elif neighbour_type is Water:
                waters.append(neighbour)

        # For every fish around the current fish, in random order, try to move towards that fish
        # if len(fishes) > 0:
        #     self.random.shuffle(fishes)
        #     for fish in fishes:
        #         # Build the transition matrix
        #         water = self.is_water_deep(fish.pos)
        #         print(water)

        # If we didn't move towards any fish, try to move somewhere else, in random order
        self.random.shuffle(waters)
        for water in waters:
            if water.deep != in_deep_water:
                # If I'm looking at a water region with a different depth, use the transion matrix   
                initialState = "safe" if in_deep_water else "exposed"
                if initialState == "safe":
                    change = np.random.choice(self.transitionWhenAlone.transitionName[0],replace=True,p=self.transitionWhenAlone.transitionMatrix[0])
                    if change == "SE":
                        self.model.grid.move_agent(self, water.pos)
                elif initialState == "exposed":
                    change = np.random.choice(self.transitionWhenAlone.transitionName[1],replace=True,p=self.transitionWhenAlone.transitionMatrix[1])
                    if change == "ES":
                        self.model.grid.move_agent(self, water.pos)
            else:
                # If I'm looking at a water region in the same depth, move with a simple decision
                if self.random.choice([True, False]):
                    self.model.grid.move_agent(self, water.pos)


class BoldFish(Fish):
    def __init__(self, unique_id, pos, model):
        transitionMatrix = [
            [0.977,0.023],
            [0.031,0.969]
        ]
        super().__init__(unique_id, pos, model, transitionMatrix)
        self.pos = pos

    def step(self):
        self.move()


class ShyFish(Fish):
    def __init__(self, unique_id, pos, model):
        transitionMatrix = [
            [0.995,0.005],
            [0.038,0.962]
        ]
        super().__init__(unique_id, pos, model, transitionMatrix)
    
    def step(self):
        self.move()

class Water(Agent):
    def __init__(self, unique_id, pos, model, deep):
        super().__init__(unique_id, model)
        self.deep = deep

