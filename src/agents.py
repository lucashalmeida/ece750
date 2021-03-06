from mesa import Agent


class Fish(Agent):
    def __init__(self, unique_id, pos, model, moore=True):
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore

    def random_move(self):
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        self.model.grid.move_agent(self, next_move)

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
        self.random_move()

class Water(Agent):
    def __init__(self, unique_id, pos, model, deep):
        super().__init__(unique_id, model)
        self.deep = deep
    
    def step(self):
        pass
