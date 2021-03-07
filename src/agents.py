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
    def __init__(self, unique_id, pos, model, bold, transitionWhenAlone, moore=True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.bold = bold
        self.transitionWhenAlone = TransitionIntensity(
            ["safe", "exposed"], 
            [
                ["SS", "SE"], 
                ["ES", "EE"]
            ], 
            transitionWhenAlone
        )
        self.transitionWhenPaired = TransitionIntensity(
            ["both_safe", "bold_exposed_shy_safe", "bold_safe_shy_exposed", "both_exposed"], 
            [
                ["BS_BS", "BS_BESS", "BS_BSSE", "BS_BE"],
                ["BESS_BS", "BESS_BESS", "BESS_BSSE", "BESS_BE"],
                ["BSSE_BS", "BSSE_BESS", "BSSE_BSSE", "BSSE_BE"],
                ["BE_BS", "BE_BESS", "BE_BSSE", "BE_BE"],
            ], 
            [
                [0.864, 0.035, 0.101, 0],
                [0.053, 0.918, 0, 0.029],
                [0.101, 0, 0.812, 0.087],
                [0, 0.03, 0.015, 0.955],
            ]
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

        self.random.shuffle(fishes)
        self.random.shuffle(waters)

        # For every fish around the current fish, in random order, try to move synced with that fish
        if len(fishes) > 0:
            for fish in fishes:
                other_fish_in_deep_water = self.is_water_deep(fish.pos)
                
                # Select where to go randomly, in case we decide to go to a shallow or deep neighbour
                shallow_neighbours = [w for w in waters if not w.deep]
                shallow_neighbour = shallow_neighbours[0] if len(shallow_neighbours) > 0 else None
                deep_neighbours = [w for w in waters if w.deep]
                deep_neighbour = deep_neighbours[0] if len(deep_neighbours) > 0 else None
                
                if in_deep_water and other_fish_in_deep_water:

                    change = np.random.choice(self.transitionWhenPaired.transitionName[0],replace=True,p=self.transitionWhenPaired.transitionMatrix[0])
                    if change == "BS_BESS":
                        if self.bold and not fish.bold:
                            self.model.grid.move_agent(self, shallow_neighbour.pos)
                            return

                        elif not self.bold and fish.bold:
                            self.model.grid.move_agent(fish, shallow_neighbour.pos)
                            return

                    elif change == "BS_BSSE":
                        if self.bold and not fish.bold:
                            self.model.grid.move_agent(fish, shallow_neighbour.pos)
                            return
                            
                        elif not self.bold and fish.bold:
                            self.model.grid.move_agent(self, shallow_neighbour.pos)     
                            return
                            
                elif not in_deep_water and not other_fish_in_deep_water:
                    
                    change = np.random.choice(self.transitionWhenPaired.transitionName[3],replace=True,p=self.transitionWhenPaired.transitionMatrix[3])

                    if change == "BE_BESS":
                        if self.bold and not fish.bold:
                            self.model.grid.move_agent(fish, deep_neighbour.pos)
                            return
                            
                        elif not self.bold and fish.bold:
                            self.model.grid.move_agent(self, deep_neighbour.pos)
                            return
                            
                    elif change == "BE_BSSE":
                        if self.bold and not fish.bold:
                            self.model.grid.move_agent(self, deep_neighbour.pos)
                            return
                            
                        elif not self.bold and fish.bold:
                            self.model.grid.move_agent(fish, deep_neighbour.pos)
                            return
                            
                else:
                    if self.bold and not fish.bold:

                        if in_deep_water and not other_fish_in_deep_water:

                            change = np.random.choice(self.transitionWhenPaired.transitionName[2],replace=True,p=self.transitionWhenPaired.transitionMatrix[2])
                            if change == "BSSE_BS":
                                self.model.grid.move_agent(fish, deep_neighbour.pos)
                                return
                            
                            elif change == "BSSE_BE":
                                self.model.grid.move_agent(self, shallow_neighbour.pos)
                                return
                            

                        elif not in_deep_water and other_fish_in_deep_water:

                            change = np.random.choice(self.transitionWhenPaired.transitionName[1],replace=True,p=self.transitionWhenPaired.transitionMatrix[1])
                            if change == "BESS_BS":
                                self.model.grid.move_agent(self, deep_neighbour.pos)
                                return

                            elif change == "BESS_BE":
                                self.model.grid.move_agent(fish, shallow_neighbour.pos)
                                return
                    
                    elif not self.bold and fish.bold:

                        if in_deep_water and not other_fish_in_deep_water:

                            change = np.random.choice(self.transitionWhenPaired.transitionName[2],replace=True,p=self.transitionWhenPaired.transitionMatrix[1])
                            if change == "BESS_BS":
                                self.model.grid.move_agent(fish, deep_neighbour.pos)
                                return

                            elif change == "BESS_BE":
                                self.model.grid.move_agent(self, shallow_neighbour.pos)
                                return
                        
                        elif not in_deep_water and other_fish_in_deep_water:

                            change = np.random.choice(self.transitionWhenPaired.transitionName[1],replace=True,p=self.transitionWhenPaired.transitionMatrix[2])
                            if change == "BSSE_BS":
                                self.model.grid.move_agent(self, deep_neighbour.pos)
                                return

                            elif change == "BSSE_BE":
                                self.model.grid.move_agent(fish, shallow_neighbour.pos)
                                return

        # If we didn't move towards any fish, try to move somewhere else, in random order
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
        transitionWhenAlone = [
            [0.977,0.023],
            [0.031,0.969]
        ]
        bold = True
        super().__init__(unique_id, pos, model, bold, transitionWhenAlone)
        self.pos = pos

    def step(self):
        self.move()


class ShyFish(Fish):
    def __init__(self, unique_id, pos, model):
        transitionWhenAlone = [
            [0.995,0.005],
            [0.038,0.962]
        ]
        bold = False
        super().__init__(unique_id, pos, model, bold, transitionWhenAlone)
    
    def step(self):
        self.move()

class Water(Agent):
    def __init__(self, unique_id, pos, model, deep):
        super().__init__(unique_id, model)
        self.deep = deep

