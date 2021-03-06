from mesa import Model
from mesa.space import MultiGrid

from src.agents import ShyFish, BoldFish, Water
from src.schedule import RandomActivation


class SticklebackLeadership(Model):
    def __init__(self, height=20, width=20):
        super().__init__()
        self.height = height
        self.width = width
        
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)

        boldFish = BoldFish(self.next_id(), (1, 1), self)
        self.grid.place_agent(boldFish, (1, 1))     
        self.schedule.add(boldFish)

        shyFish = ShyFish(self.next_id(), (10, 10), self)
        self.grid.place_agent(shyFish, (10, 10))     
        self.schedule.add(shyFish)

        # Initialize the water
        for agent, x, y in self.grid.coord_iter():
            deep = self.random.choice([True, False])

            water = Water(self.next_id(), (x, y), self, deep)
            self.grid.place_agent(water, (x, y))            
        
    def step(self):
        self.schedule.step()
