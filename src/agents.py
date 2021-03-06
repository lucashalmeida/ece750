from mesa import Agent


class Fish(Agent):
    def __init__(self, unique_id, pos, model):
        super().__init__(unique_id, model)
        self.pos = pos

    def step(self):
        pass

class Water(Agent):
    def __init__(self, unique_id, pos, model, deep):
        super().__init__(unique_id, model)
        self.deep = deep
    
    def step(self):
        pass
