from mesa import Model
from mesa.space import MultiGrid

from src.agents import ShyFish, BoldFish, Water
from src.schedule import RandomActivation


class SticklebackLeadership(Model):
    def __init__(
        self, 
        height=20, 
        width=20,
        initial_bold=1,
        initial_shy=5,
    ):
        super().__init__()
        self.height = height
        self.width = width
        self.initial_bold = initial_bold
        self.initial_shy = initial_shy    
        
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        deep_waters = []

        # Initialize the water
        for agent, x, y in self.grid.coord_iter():
            deep = self.random.choice([True, False])

            water = Water(self.next_id(), (x, y), self, deep)
            self.grid.place_agent(water, (x, y))            
            if deep:
                deep_waters.append(water)

        for i in range(self.initial_bold):
            water = self.random.choice(deep_waters)
            pos = water.pos
            boldFish = BoldFish(self.next_id(), pos, self)
            self.grid.place_agent(boldFish, pos)
            self.schedule.add(boldFish)

        for i in range(self.initial_shy):
            water = self.random.choice(deep_waters)
            pos = water.pos
            shyFish = ShyFish(self.next_id(), pos, self)
            self.grid.place_agent(shyFish, pos)     
            self.schedule.add(shyFish)
        
    def step(self):
        self.schedule.step()
