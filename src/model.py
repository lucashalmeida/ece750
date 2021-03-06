from mesa import Model
from mesa.space import MultiGrid

from src.agents import Fish, Water


class SticklebackLeadership(Model):
    def __init__(self, height=20, width=20):
        super().__init__()
        self.height = height
        self.width = width
        
        self.grid = MultiGrid(self.height, self.width, torus=True)

        # x = self.random.randrange(self.width)
        # y = self.random.randrange(self.height)
        # energy = self.random.randrange(2 * self.sheep_gain_from_food)
        fish = Fish(self.next_id(), (1, 1), self)

        # Initialize the water
        for agent, x, y in self.grid.coord_iter():
            deep = self.random.choice([True, False])

            water = Water(self.next_id(), (x, y), self, deep)
            self.grid.place_agent(water, (x, y))            
      
    def step(self):
        self.schedule.step()
